import os
import random
from math import exp
from datetime import date

import yaml
import pandas as pd
import numpy as np
import yfinance as yf
from dateutil.parser import parse

class Config:
    
    # Ações que compõem a carteira
    
    acoes:list = []

    # Periodo de analise     
    
    inicio:date = parse('2018-01-01').date()
    fim:date = parse('2023-03-31').date()

    # Nivel de risco

    max_risk:float = 0.3

    # Quantidade maxima de iterações (steps)

    qtd_iteracoes:int = 1000
    
    # Parametros do algoritmo

    temperatura_max: 2500
    temperatura_min: 1
    alpha: 0.1

class Calculator:
    _instance = None

    returns = pd.DataFrame()
    mean_returns = pd.DataFrame()
    prices = pd.DataFrame()
    covmatrix = pd.DataFrame()
    max_risk = 0
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        
        return cls._instance

    @classmethod
    def _init_calculator(cls) -> None:
        
        stocks = Config.acoes
        start = Config.inicio
        end = Config.fim

        cls.prices =  yf.download(stocks, start=start, end=end)['Adj Close']
        cls.returns = cls.prices.pct_change().dropna()
        cls.mean_returns = cls.returns.mean()
        cls.covmatrix = cls.returns.cov()
        cls.max_risk = Config.max_risk

    @staticmethod
    def annualised_performance(weights: np.array) -> tuple:
        mean_returns = Calculator.mean_returns
        covmatrix = Calculator.covmatrix

        returns = np.sum(mean_returns * weights) * 252
        std = np.sqrt(np.dot(weights.T, np.dot(covmatrix, weights))) * np.sqrt(252)

        return std, returns

    @staticmethod
    def random_portfolio():
        weights = [random.uniform(0, 1) for _ in range(len(Config.acoes))]
        return np.array([w/sum(weights) for w in weights])

    @staticmethod
    def safe_exp(delta:float, temp:float):
        try:
            return exp(-delta / temp)    
        except:
            return 0


class Portfolio:

    def __init__(self, weights) -> None:
        self.weights:np.array = np.array(weights)

    @property
    def weights(self) -> np.array:
        return self._weights

    @weights.setter
    def weights(self, weights:np.array) -> None:
        w = np.array(weights)

        self._weights = w
        self.var, self.returns = Calculator.annualised_performance(w)
        self.fitness = self.get_fitness()

    def get_fitness(self) -> float:
        if self.var > Calculator.max_risk:
            return 99999999
        
        return -1 * (self.returns - self.var - 0.01 * max(0, self.var - Calculator.max_risk))
        
class SA():
    def __init__(self) -> None:
        self.steps_max:int = Config.qtd_iteracoes
        self.tmin:float = Config.temperatura_min
        self.tmax:float = Config.temperatura_max
        self.alpha:float = Config.alpha 

        self.tfactor:float = -np.log(self.tmax / self.tmin)
        self.t:float = self.tmax
        self.steps = 0
        


    def perturb(self, current:list, c_alpha:float) -> Portfolio:
        nweights = current.copy()
        nstocks = len(nweights)

        while True:

            asset_idx = random.randint(0, nstocks-1)
            delta = random.uniform(-c_alpha, c_alpha)
            nweights[asset_idx] += delta

            asset_idx1, asset_idx2 = random.sample(range(nstocks), 2)
            nweights[asset_idx1], nweights[asset_idx2] = nweights[asset_idx2], nweights[asset_idx1]

            nweights = [max(min(w, 1.0), 0.01) for w in nweights]
            sum_weights = sum(nweights)
            nweights = [w/sum_weights for w in nweights]

            testing = Portfolio(nweights)

            if testing.var < Calculator.max_risk:
                return testing

    def update_temp(self):
        self.t =  self.tmax * np.exp(self.tfactor * self.steps/self.steps_max)

    def simulate(self):
        weights = Calculator.random_portfolio()
        current = Portfolio(weights)
        best = Portfolio(weights)

        c_alpha = self.alpha

        print('Calculando simulação ....','\n')

        while self.steps < self.steps_max and self.t >= self.tmin:
            
            print('Iteração:', self.steps, end='\r')

            accept = False
            new = self.perturb(current.weights, c_alpha)
            delta = new.fitness - current.fitness

            rand = random.random()
            check = Calculator.safe_exp(delta, self.t)

            accept = new.fitness < current.fitness or check > rand

            if accept:
                current = Portfolio(new.weights)
      
                if current.fitness < best.fitness:
                    best = Portfolio(current.weights)

            c_alpha *= 0.97
            self.steps += 1
    
            self.update_temp()

        
        dist = dict(zip(Config.acoes, np.round(best.weights * 100, 3)))
        sdist = '\n'.join([f'{key}: {value}' for key, value in dist.items()])
        fitness = best.fitness * -1

        print('Melhor distribuição dos pesos:','\n')
        print(sdist,'\n')
        print('Resultados:','\n')
        print('Melhor retorno:', best.returns)
        print('Melhor risco:', best.var)
        print('Melhor fitness:', fitness)

        filepath = os.path.join(os.path.abspath(''), 'resultados.txt')

        with open(filepath, 'w',encoding='utf-8') as txt:
            txt.write('Melhor distribuição dos pesos:\n')
            txt.write('\n')
            txt.write(f'{sdist}\n')
            txt.write('\n')
            txt.write('Resultados:\n')
            txt.write('\n')
            txt.write(f'Melhor retorno: {best.returns}\n')
            txt.write(f'Melhor risco: {best.var}\n')
            txt.write(f'Melhor fitness: {fitness}\n')

def main():

    yaml_file_path = os.path.join(os.path.abspath(''), 'config.yml')
    
    with open(yaml_file_path, 'r') as file:
        fconfig = yaml.safe_load(file)

    Config.acoes = fconfig['acoes']
    Config.inicio = fconfig['inicio']
    Config.fim = fconfig['fim']
    Config.max_risk = fconfig['max_risk']
    Config.qtd_iteracoes = fconfig['qtd_iteracoes']
    Config.temperatura_max = fconfig['temperatura_max']
    Config.temperatura_min = fconfig['temperatura_min']
    Config.alpha = fconfig['alpha']

    # Instacia as classes
    
    Calculator._init_calculator()
    sa = SA()

    # Roda simulação

    sa.simulate()

if __name__ == "__main__":
    main()