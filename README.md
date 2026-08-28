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
├── notebook.ipynb         # Notebook com a análise completa (EDA, modelagem, diagnóstico)
├── requirements.txt       # Dependências
├── Dockerfile              # Empacotamento para execução em container
├── README.md
├── dados/
│   └── base_tratada.csv   # Base tratada, gerada pelo notebook (Seção 5)
└── modelo/
    ├── modelo.pkl          # Modelo final + metadados, gerado pelo notebook (Seção 12)
    └── metricas.json
```

## Como reproduzir

### 1. Notebook

O notebook foi desenvolvido no Google Colab e lê a base bruta da ANAC a partir do Google Drive. Para rodar:

1. Baixe a base bruta da ANAC no link acima e faça upload no seu Google Drive (ajuste `CAMINHO_BASE` na
   Seção 4 se necessário).
2. Abra `notebook.ipynb` no Colab e execute todas as células, em ordem, do início ao fim.
3. O notebook salva `base_tratada.csv` e `modelo.pkl` em pastas `dados/` e `modelo/` **ao lado do arquivo
   bruto no seu Google Drive** (não neste repositório). Baixe os dois arquivos gerados e copie-os para as
   pastas `dados/` e `modelo/` deste repositório antes de rodar o app localmente ou publicar no Streamlit.

### 2. Aplicação Streamlit

Localmente:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Com Docker:

```bash
docker build -t consumo-combustivel .
docker run -p 8501:8501 consumo-combustivel
```

A aplicação abre em `http://localhost:8501`.

### 3. Publicação (Streamlit Community Cloud)

1. Suba este repositório para o GitHub (veja seção abaixo).
2. Em https://share.streamlit.io, conecte o repositório e aponte `app.py` como arquivo principal.
3. Garanta que `dados/base_tratada.csv` e `modelo/modelo.pkl` estejam versionados no repositório (ou gerados
   por um passo de build), já que o app depende deles no carregamento.

## Como subir para o GitHub

```bash
git init
git add .
git commit -m "Checkpoint 4: regressão linear e polinomial - consumo de combustível ANAC"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<nome-do-repo>.git
git push -u origin main
```

## Principais limitações conhecidas

- A base agrega múltiplas etapas de voo em uma média/soma mensal por rota e empresa, perdendo variação
  entre aeronaves individuais e condições específicas de cada voo.
- Não há informação sobre o modelo/tipo de aeronave, que provavelmente explica parte relevante do erro
  residual do modelo.
- O modelo é observacional: associação entre as variáveis e o consumo não implica causalidade.
- Previsões fora do intervalo de distância, decolagens e carga observado no treino (2020–2025, voos
  domésticos regulares) são extrapolações e devem ser tratadas com cautela — a aplicação exibe um aviso
  nesses casos.
