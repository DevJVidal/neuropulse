import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ================================
# CAMINHO DO DATASET PROCESSADO
# ================================

BASE_DIR = Path(__file__).resolve().parent.parent  # pasta raiz do projeto
DATA_PROCESSED = BASE_DIR / "data" / "processed"


@st.cache_data
def load_data():
    path = DATA_PROCESSED / "neuropulse_pns_depressao.csv"
    df = pd.read_csv(path)

    # Mapeia nome do estado -> sigla ISO (para o mapa)
    mapa_uf = {
        "Rondonia": "BR-RO",
        "Acre": "BR-AC",
        "Amazonas": "BR-AM",
        "Roraima": "BR-RR",
        "Para": "BR-PA",
        "Amapa": "BR-AP",
        "Tocantins": "BR-TO",
        "Maranhao": "BR-MA",
        "Piaui": "BR-PI",
        "Ceara": "BR-CE",
        "Rio Grande do Norte": "BR-RN",
        "Paraiba": "BR-PB",
        "Pernambuco": "BR-PE",
        "Alagoas": "BR-AL",
        "Sergipe": "BR-SE",
        "Bahia": "BR-BA",
        "Minas Gerais": "BR-MG",
        "Espirito Santo": "BR-ES",
        "Rio de Janeiro": "BR-RJ",
        "Sao Paulo": "BR-SP",
        "Parana": "BR-PR",
        "Santa Catarina": "BR-SC",
        "Rio Grande do Sul": "BR-RS",
        "Mato Grosso do Sul": "BR-MS",
        "Mato Grosso": "BR-MT",
        "Goias": "BR-GO",
        "Distrito Federal": "BR-DF",
    }

    df["uf_iso"] = df["UF"].map(mapa_uf)

    # Garante que não tem linhas duplicadas
    df = df.drop_duplicates(
        subset=["year", "UF", "sexo", "faixa_idade", "domicilio", "indicador"]
    )

    return df


# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================

st.set_page_config(
    page_title="NeuroPulse - Saúde Mental no Brasil",
    layout="wide",
    page_icon="🧠",
)

df = load_data()

st.title("🧠 NeuroPulse – Painel de Saúde Mental (PNS/IBGE)")
st.markdown(
    """
Análise de **depressão diagnosticada por profissional de saúde mental**  
Fonte: Pesquisa Nacional de Saúde (PNS 2019 – IBGE).
"""
)

# ================================
# SIDEBAR – FILTROS
# ================================

st.sidebar.header("Filtros")

ufs = sorted(df["UF"].unique())
sexo_opts = sorted(df["sexo"].unique())
faixa_opts = sorted(df["faixa_idade"].unique())

ufs_sel = st.sidebar.multiselect("Estados (UF)", ufs, default=ufs)
sexo_sel = st.sidebar.selectbox("Sexo", sexo_opts, index=0)
faixa_sel = st.sidebar.selectbox("Faixa de idade", faixa_opts, index=0)

df_filt = df[
    (df["UF"].isin(ufs_sel))
    & (df["sexo"] == sexo_sel)
    & (df["faixa_idade"] == faixa_sel)
]

# ================================
# KPIs – INDICADORES RÁPIDOS
# ================================

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

# Média Brasil (nos UFs filtrados)
media_brasil = df_filt["valor"].mean()

# Maior e menor valor
uf_max = df_filt.loc[df_filt["valor"].idxmax()]
uf_min = df_filt.loc[df_filt["valor"].idxmin()]

col_kpi1.metric(
    "Média de depressão (%) nos estados selecionados",
    f"{media_brasil:.1f}%",
)

col_kpi2.metric(
    f"Maior percentual – {uf_max['UF']}",
    f"{uf_max['valor']:.1f}%",
)

col_kpi3.metric(
    f"Menor percentual – {uf_min['UF']}",
    f"{uf_min['valor']:.1f}%",
)

st.markdown("---")

# ================================
# GRÁFICO DE BARRAS POR UF
# ================================

st.subheader("📊 Percentual de depressão por UF")

fig_bar = px.bar(
    df_filt.sort_values("valor", ascending=False),
    x="UF",
    y="valor",
    labels={"valor": "% de depressão", "UF": "Unidade da Federação"},
    color="valor",
    color_continuous_scale="Reds",
    text="valor",
)

fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig_bar.update_layout(yaxis_title="% de pessoas com diagnóstico de depressão")

st.plotly_chart(fig_bar, use_container_width=True)

# ================================
# 📋 TABELA DETALHADA DOS DADOS
# ================================

st.subheader("📋 Tabela completa dos dados filtrados")

df_tabela = (
    df_filt[["UF", "sexo", "faixa_idade", "valor"]]
    .sort_values("valor", ascending=False)
    .rename(columns={"valor": "% de depressão"})
)

st.dataframe(df_tabela, use_container_width=True)

st.markdown("---")

# ================================
# MAPA DO BRASIL (SCATTER GEO)
# ================================

st.subheader("🗺️ Mapa da prevalência de depressão por estado")

# Coordenadas aproximadas das capitais (lat, lon)
coords_uf = {
    "Rondônia": (-8.76, -63.90),
    "Acre": (-9.97, -67.81),
    "Amazonas": (-3.13, -60.02),
    "Roraima": (2.82, -60.67),
    "Pará": (-1.46, -48.49),
    "Amapá": (0.03, -51.07),
    "Tocantins": (-10.25, -48.32),
    "Maranhão": (-2.53, -44.30),
    "Piauí": (-5.09, -42.80),
    "Ceará": (-3.72, -38.54),
    "Rio Grande do Norte": (-5.81, -35.21),
    "Paraíba": (-7.12, -34.86),
    "Pernambuco": (-8.05, -34.90),
    "Alagoas": (-9.66, -35.74),
    "Sergipe": (-10.91, -37.07),
    "Bahia": (-12.97, -38.50),
    "Minas Gerais": (-19.92, -43.94),
    "Espírito Santo": (-20.32, -40.34),
    "Rio de Janeiro": (-22.91, -43.17),
    "São Paulo": (-23.55, -46.63),
    "Paraná": (-25.43, -49.27),
    "Santa Catarina": (-27.59, -48.55),
    "Rio Grande do Sul": (-30.03, -51.23),
    "Mato Grosso do Sul": (-20.44, -54.65),
    "Mato Grosso": (-15.60, -56.10),
    "Goiás": (-16.68, -49.25),
    "Distrito Federal": (-15.78, -47.93),
}

df_mapa = df_filt.copy()
df_mapa["lat"] = df_mapa["UF"].map(lambda uf: coords_uf.get(uf, (None, None))[0])
df_mapa["lon"] = df_mapa["UF"].map(lambda uf: coords_uf.get(uf, (None, None))[1])

df_mapa = df_mapa.dropna(subset=["lat", "lon"])

fig_map = px.scatter_geo(
    df_mapa,
    lat="lat",
    lon="lon",
    color="valor",
    hover_name="UF",
    size="valor",
    color_continuous_scale="Reds",
    labels={"valor": "% de depressão"},
)

fig_map.update_geos(
    scope="south america",
    showcountries=True,
    countrycolor="rgba(255,255,255,0.3)",
    projection_type="mercator",
)

fig_map.update_layout(
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.info(
    "Este é o **painel inicial do NeuroPulse**. "
    "Depois vamos incluir outros indicadores (ansiedade, TDAH, autismo, uso de medicamentos, acesso a serviços etc.)."
)
