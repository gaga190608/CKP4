# Estimação do Consumo de Combustível de Aeronaves por Regressão Linear e Polinomial

Checkpoint 4 — Data Science & Statistical Computing — FIAP 2026

## Integrantes

| Nome | RM |
|---|---|
| Jéssica Domingues | 562973 |
| Kauã Carvalho de Oliveira | 566371 |
| João Vitor Piccolo | 565127 |
| Leonardo Pereira | 561349 |
| Gabrielle Calazans | 564460 |

## Objetivo

Estimar o consumo de combustível (litros) de empresas aéreas em voos regulares domésticos no Brasil, em
função da distância voada, do número de decolagens e do volume de carga paga transportada, por par de
aeroportos/empresa/mês.

## Fonte dos dados

Agência Nacional de Aviação Civil (ANAC) — *Dados Estatísticos do Transporte Aéreo*, portal de dados abertos:
https://www.anac.gov.br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/dados-estatisticos-do-transporte-aereo

Escopo utilizado: voos domésticos, regulares, 2020–2025.

## Condições de uso / licença dos dados

Os dados são publicados pela ANAC no **Portal de Dados Abertos**, com acesso livre para qualquer interessado, sem custo ou necessidade de cadastro. A agência disponibiliza a série histórica dos dados estatísticos do transporte aéreo do Brasil para consulta pública, com o objetivo declarado de ampliar o conhecimento da sociedade e subsidiar pesquisas, estudos e análises sobre o setor. O Portal de Dados Abertos da ANAC busca especificamente democratizar o uso dos dados e reduzir a assimetria de informação entre o setor regulado e o cidadão, promovendo pesquisa científica, desenvolvimento tecnológico e inovação — finalidade dentro da qual este projeto acadêmico se enquadra.

Fonte: https://www.anac.gov.br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/dados-estatisticos-do-transporte-aereo

## Estrutura do projeto

```
projeto/
├── app.py                 # Aplicação Streamlit
├── notebook.ipynb         # Análise completa, treinamento e exportação dos artefatos
├── requirements.txt       # Dependências da aplicação
├── README.md
├── dados/
│   └── base_tratada.csv   # Base tratada gerada pelo notebook
└── modelo/
    ├── modelo.pkl         # Modelo final e metadados
    └── metricas.json      # Métricas de avaliação
```

## Como reproduzir

### Treinamento no Google Colab

O notebook foi desenvolvido no Google Colab e lê a base bruta da ANAC a partir do Google Drive:

1. Baixe a base bruta da ANAC pelo link informado acima.
2. Envie o arquivo ao Google Drive como `Colab Notebooks/Dados_Estatisticos.csv`.
3. Abra `notebook.ipynb` no Colab e execute todas as células em ordem.
4. Copie os artefatos gerados para este repositório:
   - `dados/base_tratada.csv`
   - `modelo/modelo.pkl`
   - `modelo/metricas.json`

### Aplicação Streamlit

Para executar localmente:

```bash
pip install -r requirements.txt
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`.

A versão publicada é executada pelo **Streamlit Community Cloud**, diretamente a partir da branch `main` e do arquivo `app.py`.

> **Docker não é necessário neste projeto.** O treinamento é realizado no Google Colab e a aplicação é executada pelo Streamlit Community Cloud, que instala automaticamente as dependências declaradas em `requirements.txt`.

## Principais limitações conhecidas

- A base agrega múltiplas etapas de voo em uma média/soma mensal por rota e empresa, perdendo variação
  entre aeronaves individuais e condições específicas de cada voo.
- Não há informação sobre o modelo/tipo de aeronave, que provavelmente explica parte relevante do erro
  residual do modelo.
- O modelo é observacional: associação entre as variáveis e o consumo não implica causalidade.
- Previsões fora do intervalo de distância, decolagens e carga observado no treino (2020–2025, voos
  domésticos regulares) são extrapolações e devem ser tratadas com cautela — a aplicação exibe um aviso
  nesses casos.
