# Otimização de Carteiras Em Ações Utilizando Simulated Annealing

Este script Python demonstra a otimização de carteiras usando um algoritmo Simulated Annealing. Ele permite encontrar uma alocação ótima de ativos (por exemplo, ações) em uma carteira para maximizar os retornos, ao mesmo tempo que gerencia o risco.

O Simulated Annealing (SA) é um algoritmo de otimização inspirado na técnica de recozimento metalúrgico. Ele é usado para encontrar a solução ótima (ou uma boa aproximação) em problemas complexos onde muitas combinações de parâmetros podem ser exploradas. O SA começa com uma solução inicial e realiza perturbações controladas, aceitando mudanças com base em uma função de probabilidade que depende da diferença de aptidão das soluções e de uma temperatura atual. 

Uma explicação mais aprofundada sobre o SA e seu funcionamento pode ser [encontrada aqui.](https://pt.wikipedia.org/wiki/Simulated_annealing)



## Configuração do Código

O código lê as configurações necessárias a partir de um arquivo YAML chamado "config.yml". Este arquivo contém os parametros necessarios para o funcionamento do codigo: 

- `acoes`: É a lista dos tickers das ações que a carteira deve possuir.
- `inicio` e `fim` : O período de análise define o intervalo de tempo durante o qual os dados de mercado serão considerados para a otimização. Os dados devem ser fornecidos no formato AAAA-MM-DD (Ano-Mês-Dia).
- `max_risk`: O nível de risco máximo (max_risk) é um valor entre 0 e 1 que representa o risco máximo que a carteira pode assumir.
- `qtd_iteracoes`: É o número de iterações (ou gerações) que o algoritmo executará durante a otimização da carteira. 
- `temperatura_min`: Representa a temperatura mínima do sistema durante a execução do algoritmo.
- `temperatura_max`: Representa a temperatura máxima do sistema no início da execução do algoritmo. 
- `alpha`:  Um valor que controla o tamanho das perturbações aplicadas à alocação de ativos durante o processo de otimização. Valores menores resultam em perturbações menores.

`IMPORTANTE : `Os tickers das ações devem estar no formato que aparece no Yahoo Finance para que a biblioteca possa obter os dados delas.

Certifique-se de que o seu arquivo `config.yml` siga a estrutura necessária conforme especificada. Se alguma dessas chaves estiver ausente, o código levantara um erro.

## Coleta e Ingestão do Código

Uma vez que as configurações são lidas, o código inicia a coleta de dados financeiros usando a biblioteca `yfinance` (Yahoo Finance). Ele baixa os preços de fechamento das ações especificadas no intervalo de datas fornecido no arquivo de configuração. Esses preços são usados para calcular os retornos diários das ações, a média dos retornos, a matriz de covariância entre outros insumos.

## Funcionamento do Código

### Classe `Config`

A classe `Config` é usada para armazenar as configurações iniciais do programa. Ela define várias variáveis, como a lista de ações (`acoes`), o período de análise (`inicio` e `fim`), o nível de risco máximo (`max_risk`), a quantidade máxima de iterações (`qtd_iteracoes`), e parâmetros do algoritmo de Simulated Annealing, como as temperaturas máxima e mínima (`temperatura_max` e `temperatura_min`) e o valor de `alpha`.

### Classe `Calculator`

A classe `Calculator` é usada para calcular métricas relacionadas à carteira, como retornos, risco e outras estatísticas. Ela inicializa os preços das ações, calcula os retornos, a média dos retornos e a matriz de covariância dos retornos. Também armazena o nível de risco máximo da carteira.

### Classe `Portfolio`

A classe `Portfolio` representa uma alocação de ativos na carteira. Ela armazena os pesos dos ativos e calcula o valor de retorno, risco e a "aptidão" (fitness) da carteira com base nos pesos.

### Classe `SA` (Simulated Annealing)

A classe `SA` implementa o algoritmo Simulated Annealing. Ela usa parâmetros definidos na classe `Config` para controlar o comportamento do algoritmo, como a temperatura inicial e final, o número máximo de iterações e o valor `alpha`. O método `perturb` é usado para perturbar a alocação atual dos ativos, gerando uma nova alocação. O método `update_temp` atualiza a temperatura à medida que o algoritmo avança nas iterações. O método `simulate` executa o algoritmo Simulated Annealing. Ele começa com uma alocação inicial, faz perturbações, calcula a aptidão das alocações e decide se aceita ou rejeita as novas alocações com base nas probabilidades calculadas. O resultado final é a melhor alocação encontrada pelo algoritmo.

### Função `main`

A função `main` é o ponto de entrada do programa. Ela lê as configurações de um arquivo YAML chamado `config.yml`. Em seguida, ela instancia a classe `Calculator` para preparar os dados de mercado e a classe `SA` para executar a otimização. Finalmente, ela chama o método `simulate` da classe `SA` para encontrar a melhor alocação de ativos e gera um arquivo de resultados.

No final, o código imprime a alocação de ativos otimizada, os resultados (retorno, risco e aptidão) e os armazena em um arquivo de resultados chamado `resultados.txt`.

### Executando o Código

1. Certifique-se de ter as bibliotecas necessárias instaladas. Você pode instalá-las usando o pip, se necessário:

```bash
pip install pandas numpy yfinance pyyaml python-dateutils
```

2. Baixe o arquivo `config.yml` ou crie um com os parâmetros de configuração apropriados.

3. Execute o script no seu terminal de preferencia:

```bash
python sa_class.py
```

O script realizará a otimização da carteira e exibirá os resultados no console. Além disso, salvará os resultados em um arquivo `resultados.txt` no mesmo diretório.

Observe que este script fornece um exemplo básico de otimização de carteiras utilizando Simulated Annealing. Dependendo dos requisitos financeiros específicos, você pode precisar adaptar e estender o código para atender às suas necessidades.


## Glossário

Aqui explicamos conceitos financeiros relevantes no contexto do código:

- **Carteira de Ativos**: Refere-se a um conjunto de ativos financeiros, como ações, títulos, moedas, etc., mantidos por um investidor.

- **Retorno**: O ganho ou perda financeira obtido com um investimento ao longo do tempo.

- **Risco**: A possibilidade de perder parte ou a totalidade do investimento devido a flutuações no valor dos ativos. É muitas vezes medido pela volatilidade.

- **Média dos Retornos**: A média dos retornos passados de um ativo ou carteira, geralmente usada como indicador de desempenho.

- **Tickers**: Símbolos únicos que representam ativos financeiros em um sistema de negociação. No código, os tickers são usados para identificar ações específicas.