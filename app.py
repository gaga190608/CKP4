import os
import pickle

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Consumo de Combustível — Aviação Regular Doméstica",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Carregamento (cacheado)
# ---------------------------------------------------------------------------

@st.cache_resource
def carregar_modelo():
    with open(os.path.join("modelo", "modelo.pkl"), "rb") as f:
        return pickle.load(f)


@st.cache_data
def carregar_dados():
    return pd.read_csv(os.path.join("dados", "base_tratada.csv"))


artefato = carregar_modelo()
df = carregar_dados()

modelo = artefato["modelo"]
FEATURES = artefato["features"]
TARGET = artefato["target"]
RANGES = artefato["ranges_treino"]
METRICAS = artefato["metricas_teste"]
NOME_MODELO = artefato["nome_modelo"]

# ---------------------------------------------------------------------------
# Cabeçalho / descrição do projeto
# ---------------------------------------------------------------------------

st.title("✈️ Estimação do Consumo de Combustível de Aeronaves")

st.markdown(
    """
Aplicação do projeto de **regressão linear e polinomial** (Checkpoint 4 — Data Science & Statistical Computing, FIAP).

**Pergunta de pesquisa:** em que medida a distância voada, o número de decolagens e o volume de carga paga
transportada explicam o total de combustível consumido (em litros) por uma empresa aérea, em um par de
aeroportos, em voos regulares domésticos no Brasil?

**Fonte dos dados:** Agência Nacional de Aviação Civil (ANAC) — Dados Estatísticos do Transporte Aéreo
([portal de dados abertos](https://www.anac.gov.br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/dados-estatisticos-do-transporte-aereo)).
Escopo: voos domésticos, regulares, 2020–2025.
"""
)

st.markdown(
    f"""
**Variável resposta (y):** `COMBUSTIVEL_LITROS` — combustível consumido no mês, em litros, por par de
aeroportos/empresa.

**Variáveis explicativas (X) usadas na previsão:** `{"`, `".join(FEATURES)}`.

**Modelo final utilizado:** regressão {NOME_MODELO}.
"""
)

# ---------------------------------------------------------------------------
# Amostra da base e estatísticas descritivas
# ---------------------------------------------------------------------------

st.header("1. Amostra da base e estatísticas descritivas")

col_a, col_b = st.columns([2, 1])
with col_a:
    st.subheader("Amostra dos dados tratados")
    st.dataframe(df.sample(min(10, len(df)), random_state=42))

with col_b:
    st.subheader("Estatísticas descritivas")
    st.dataframe(df[[TARGET] + FEATURES].describe().round(2))

# ---------------------------------------------------------------------------
# Gráficos exploratórios
# ---------------------------------------------------------------------------

st.header("2. Gráficos exploratórios")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Distribuição de {TARGET}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df[TARGET], bins=50, color="#2b6cb0")
    ax.set_xlabel("Combustível consumido (litros)")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

with col2:
    st.subheader(f"{TARGET} vs. {FEATURES[0]}")
    fig, ax = plt.subplots(figsize=(6, 4))
    amostra = df.sample(min(3000, len(df)), random_state=42)
    ax.scatter(amostra[FEATURES[0]], amostra[TARGET], alpha=0.3, s=10, color="#2b6cb0")
    ax.set_xlabel(FEATURES[0])
    ax.set_ylabel("Combustível consumido (litros)")
    st.pyplot(fig)

# ---------------------------------------------------------------------------
# Métricas do modelo final
# ---------------------------------------------------------------------------

st.header("3. Desempenho do modelo final (conjunto de teste)")

m1, m2, m3 = st.columns(3)
m1.metric("MAE (L)", f"{METRICAS['MAE (L)']:,.0f}")
m2.metric("RMSE (L)", f"{METRICAS['RMSE (L)']:,.0f}")
m3.metric("R²", f"{METRICAS['R²']:.3f}")


def preparar_X(df_in: pd.DataFrame) -> pd.DataFrame:
    """O modelo final salvo no pickle já é um Pipeline completo (ou LinearRegression
    simples), então basta selecionar as colunas de entrada na ordem certa — sem
    pré-processamento manual aqui, evitando qualquer regra diferente da usada no notebook."""
    return df_in[FEATURES]


# Gráficos de valores reais x previstos e resíduos, calculados sobre uma amostra da base
amostra_diag = df.sample(min(3000, len(df)), random_state=42)
X_diag = preparar_X(amostra_diag)
pred_diag = modelo.predict(X_diag)
resid_diag = amostra_diag[TARGET].to_numpy() - pred_diag

g1, g2 = st.columns(2)

with g1:
    st.subheader("Valores reais x previstos")
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(amostra_diag[TARGET], pred_diag, alpha=0.3, s=10, color="#2b6cb0")
    lims = [
        min(amostra_diag[TARGET].min(), pred_diag.min()),
        max(amostra_diag[TARGET].max(), pred_diag.max()),
    ]
    ax.plot(lims, lims, "--", color="red", linewidth=1.2)
    ax.set_xlabel("Real (L)")
    ax.set_ylabel("Previsto (L)")
    st.pyplot(fig)

with g2:
    st.subheader("Resíduos vs. valores ajustados")
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(pred_diag, resid_diag, alpha=0.3, s=10, color="#2b6cb0")
    ax.axhline(0, color="red", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Previsto (L)")
    ax.set_ylabel("Resíduo (L)")
    st.pyplot(fig)

# ---------------------------------------------------------------------------
# Formulário de previsão
# ---------------------------------------------------------------------------

st.header("4. Faça uma previsão")

with st.form("form_previsao"):
    st.write("Informe os valores das variáveis explicativas:")

    entradas = {}
    for feat in FEATURES:
        r = RANGES[feat]
        entradas[feat] = st.number_input(
            f"{feat} (intervalo observado no treino: {r['min']:,.0f} a {r['max']:,.0f})",
            min_value=0.0,
            value=float(r["min"]),
            step=1.0,
        )

    enviado = st.form_submit_button("Calcular previsão")

if enviado:
    entrada_df = pd.DataFrame([entradas])[FEATURES]
    X_entrada = preparar_X(entrada_df)
    previsao = modelo.predict(X_entrada)[0]
    previsao = max(previsao, 0.0)

    st.success(f"**Combustível previsto: {previsao:,.0f} litros**")

    fora_do_intervalo = []
    for feat in FEATURES:
        r = RANGES[feat]
        if entradas[feat] < r["min"] or entradas[feat] > r["max"]:
            fora_do_intervalo.append(feat)

    if fora_do_intervalo:
        st.warning(
            "⚠️ As seguintes variáveis estão **fora do intervalo observado na base de treino**, "
            "o que torna a previsão uma extrapolação e reduz a confiabilidade do resultado: "
            f"{', '.join(fora_do_intervalo)}."
        )

st.caption(
    "Aplicação desenvolvida para o Checkpoint 4 — Regressão Linear e Polinomial "
    "(Data Science & Statistical Computing, FIAP 2026)."
)
