import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Power Trios — DNA Espectral",
    page_icon="🎸",
    layout="wide"
)

TRIOS_CORES = {
    "Hendrix Experience":   "#8B5CF6",
    "Cream":                "#EC4899",
    "The Police":           "#3B82F6",
    "ZZ Top":               "#F59E0B",
    "SRV & Double Trouble": "#10B981",
}

COLUNAS = ["sub_grave", "grave_baixo", "medio_guitarra", "medio_agudo", "agudo_pratos"]
LABELS  = ["Sub-grave", "Grave/Baixo", "Médio/Guitarra", "Médio-Agudo", "Agudo/Pratos"]

@st.cache_data
def carregar_dados():
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(base, "data", "spectral_features.csv"))
    df_pct = df.copy()
    df_pct[COLUNAS] = df[COLUNAS].div(df[COLUNAS].sum(axis=1), axis=0) * 100
    return df, df_pct

@st.cache_data
def calcular_medias(df_pct):
    medias = df_pct.groupby("trio")[COLUNAS].mean()
    medias.columns = LABELS
    return medias

df_raw, df_pct = carregar_dados()
df_medias = calcular_medias(df_pct)

st.title("🎸 Power Trios — A Ciência por Trás do Som")
st.markdown("### Como três músicos conseguem soar maiores do que bandas inteiras?")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🎯 DNA Espectral", "🔍 Explorar Trio", "📊 Comparação"])

with tab1:
    st.subheader("DNA Espectral dos 5 Power Trios")
    st.markdown("Cada trio tem uma assinatura sonora única. O radar mostra como cada um distribui a energia pelo espectro.")

    fig = go.Figure()
    for trio, cor in TRIOS_CORES.items():
        if trio in df_medias.index:
            vals = df_medias.loc[trio].tolist()
            fig.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=LABELS + [LABELS[0]],
                fill="toself",
                name=trio,
                line_color=cor,
                fillcolor=cor,
                opacity=0.2,
            ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 70])),
        showlegend=True,
        height=600,
        title="Radar Chart — DNA Espectral"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Heatmap Comparativo")
    fig2 = px.imshow(
        df_medias.round(1),
        text_auto=True,
        color_continuous_scale="magma",
        aspect="auto",
        height=320,
    )
    fig2.update_layout(
        title="% de Energia por Faixa de Frequência",
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        margin=dict(l=150, r=50, t=60, b=50),
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Explorar um Trio")
    trio_sel = st.selectbox("Escolha o trio:", list(TRIOS_CORES.keys()))

    df_trio = df_pct[df_pct["trio"] == trio_sel].copy()
    df_trio_plot = df_trio.set_index("faixa")[COLUNAS]
    df_trio_plot.columns = LABELS

    fig3 = px.bar(
        df_trio_plot.reset_index().melt(id_vars="faixa", var_name="Frequência", value_name="Energia %"),
        x="faixa", y="Energia %", color="Frequência",
        barmode="group",
        title=f"Distribuição Espectral — {trio_sel}",
        color_discrete_sequence=px.colors.sequential.Plasma,
        height=500,
    )
    fig3.update_layout(xaxis_tickangle=-15)
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(df_trio_plot.round(1), use_container_width=True)

with tab3:
    st.subheader("Comparar Trios")
    trios_sel = st.multiselect(
        "Escolha os trios para comparar:",
        list(TRIOS_CORES.keys()),
        default=["Hendrix Experience", "Cream"]
    )

    if len(trios_sel) >= 2:
        fig4 = go.Figure()
        for trio in trios_sel:
            if trio in df_medias.index:
                vals = df_medias.loc[trio].tolist()
                fig4.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=LABELS + [LABELS[0]],
                    fill="toself",
                    name=trio,
                    line_color=TRIOS_CORES[trio],
                    fillcolor=TRIOS_CORES[trio],
                    opacity=0.3,
                ))
        fig4.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 70])),
            showlegend=True,
            height=600,
            title="Comparação de DNA Espectral"
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.dataframe(df_medias.loc[trios_sel].round(1), use_container_width=True)
    else:
        st.info("Selecione pelo menos 2 trios para comparar.")