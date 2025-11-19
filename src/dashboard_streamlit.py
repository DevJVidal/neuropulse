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

    # Mapeia o nome do estado -> sigla ISO (para o mapa)
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

# ================================
# ESTILO CUSTOMIZADO (SIDEBAR + APP)
# ================================

st.markdown(
    """
    <style>

    /* ===== SIDEBAR GERAL ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #151822, #0b0d17);
        border-right: 1px solid rgba(255,255,255,0.12);
    }

    /* Espaçamento interno da sidebar */
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem;
        padding-bottom: 1.8rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Título "Filtros" */
    [data-testid="stSidebar"] h2 {
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #f7931e;
        margin-bottom: 1rem;
    }

    /* Labels (Estados, Sexo, Faixa de idade) */
    [data-testid="stSidebar"] label {
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #c9d1f5 !important;
        margin-bottom: 0.25rem;
    }

    /* Blocos dos inputs (multiselect e selects) */
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSelectbox {
        background-color: #0f111a;
        border-radius: 12px;
        padding: 0.25rem 0.4rem;
        box-shadow: 0 10px 24px rgba(0,0,0,0.45);
        margin-bottom: 1rem;
    }

    /* Borda interna do componente */
    [data-testid="stSidebar"] .stMultiSelect > div,
    [data-testid="stSidebar"] .stSelectbox > div {
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
        background-color: #111320 !important;
    }

    /* Texto dentro dos widgets */
    [data-testid="stSidebar"] .stMultiSelect span,
    [data-testid="stSidebar"] .stSelectbox span {
        color: #f5f7ff !important;
        font-size: 0.9rem;
    }

    /* Tags do multiselect (UFs selecionadas) */
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #f7931e !important;
        color: #ffffff !important;
        border-radius: 999px !important;
        padding: 0.15rem 0.55rem !important;
        font-size: 0.8rem !important;
        font-weight: 600;
        border: none !important;
    }

    /* Ícone de “x” da tag */
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {
        width: 12px;
        height: 12px;
    }

    /* Pequeno separador entre grupos de filtros */
    [data-testid="stSidebar"] hr {
        margin: 0.8rem 0 1rem 0;
        border-color: rgba(255,255,255,0.08);
    }

    /* ===== FUNDO GERAL DO APP ===== */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #1c2340 0, #050712 55%);
        color: #f5f7ff;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Título principal */
    [data-testid="stAppViewContainer"] h1 {
        font-size: 2.4rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        font-weight: 800;
    }

    /* Subtítulos das seções (st.subheader) */
    [data-testid="stAppViewContainer"] h3 {
        font-size: 1.1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #f7931e;
        margin-top: 1.8rem;
        margin-bottom: 0.6rem;
    }

    /* Texto normal */
    [data-testid="stAppViewContainer"] p {
        font-size: 0.95rem;
        color: #d4ddff;
    }

    /* ===== CARDS DOS KPIs (st.metric) ===== */
    [data-testid="stMetric"] {
        background: #111320;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 26px rgba(0,0,0,0.55);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #b4c0ff;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }

    /* ===== TABELA (st.dataframe) ===== */
    .stDataFrame {
        background: #111320 !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        box-shadow: 0 10px 26px rgba(0,0,0,0.55) !important;
        padding: 0.4rem !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ================================
# FUNÇÃO PARA ESTILO DOS GRÁFICOS
# ================================

def aplica_estilo_fig(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, sans-serif",
            color="#f5f7ff",
        ),
        margin=dict(l=20, r=20, t=40, b=40),
    )
    return fig


# ================================
# CARREGA OS DADOS
# ================================

df = load_data()

st.title("🧠 NeuroPulse – Painel de Saúde Mental (PNS/IBGE)")

# Badge / descrição inicial
st.markdown(
    """
    <div style="
        display:flex;
        flex-direction:column;
        gap:4px;
        margin-bottom: 1.4rem;
    ">
      <span style="
        display:inline-flex;
        align-items:center;
        gap:6px;
        font-size:0.8rem;
        letter-spacing:0.14em;
        text-transform:uppercase;
        color:#b4c0ff;
      ">
        <span>●</span> Painel PNS 2019 · IBGE
      </span>
      <span style="font-size:0.95rem; color:#d4ddff;">
        Análise da <strong>prevalência de depressão diagnosticada</strong> por profissional de saúde mental,
        por estado, sexo e faixa etária.
      </span>
    </div>
    """,
    unsafe_allow_html=True,
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

# ===== Caso sem estados selecionados / sem dados =====
if df_filt.empty:
    st.info(
        "🚫 **NENHUM ESTADO SELECIONADO**\n\n"
        "Use o painel de filtros à esquerda e selecione pelo menos um estado (UF) "
        "para visualizar os indicadores."
    )
    st.stop()

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
fig_bar = aplica_estilo_fig(fig_bar)

st.plotly_chart(fig_bar, use_container_width=True)

# ================================
# 👥 COMPARAÇÃO POR SEXO (MÉDIA)
# ================================

df_sexo_comp = df[
    (df["UF"].isin(ufs_sel))
    & (df["faixa_idade"] == faixa_sel)
]

df_sexo_comp = df_sexo_comp[df_sexo_comp["sexo"].isin(["Masculino", "Feminino"])]

if not df_sexo_comp.empty and df_sexo_comp["sexo"].nunique() > 1:
    df_sexo_media = (
        df_sexo_comp.groupby("sexo", as_index=False)["valor"].mean()
    )

    st.subheader("👥 Comparação da prevalência por sexo\n(média nos estados selecionados)")
    fig_sexo = px.bar(
        df_sexo_media,
        x="sexo",
        y="valor",
        labels={"sexo": "Sexo", "valor": "% com diagnóstico de depressão"},
        text="valor",
    )
    fig_sexo.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_sexo.update_layout(yaxis_title="% de pessoas com diagnóstico de depressão")
    fig_sexo = aplica_estilo_fig(fig_sexo)

    st.plotly_chart(fig_sexo, use_container_width=True)

st.markdown("---")

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
    projection_type="mercator",
    showcountries=True,
    countrycolor="rgba(255,255,255,0.3)",
    lataxis_range=[-35, 6],
    lonaxis_range=[-75, -34],
)

fig_map.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    height=550,
)

fig_map = aplica_estilo_fig(fig_map)

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.info(
    "Este é o **painel inicial do NeuroPulse**. "
    "Sobre indicadores de depressão, temos informações sobre a prevalência, tendência e evolução nos estados brasileiros."
)
