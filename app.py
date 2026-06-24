import streamlit as st
import librosa
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Power Trios — DNA Espectral",
    page_icon="🎸",
    layout="wide"
)

BASE = "C:/Users/felip/OneDrive/Documentos/power_trios/data/audio/"

TRIOS = {
    "Hendrix Experience": {
        "path": BASE + "hendrix/",
        "cor": "#8B5CF6",
        "faixas": {
            "Purple Haze":          "purple_haze.mp3",
            "Voodoo Child":         "voodoo_child.mp3",
            "Little Wing":          "littlewing.mp3",
            "All Along Watchtower": "all_allong_the_watchtower.mp3",
        }
    },
    "Cream": {
        "path": BASE + "cream/",
        "cor": "#EC4899",
        "faixas": {
            "Sunshine of Your Love": "sunshine_of_your_love.mp3",
            "White Room":            "white_room.mp3",
            "Crossroads":            "crossroads.mp3",
            "Badge":                 "badge.mp3",
        }
    },
    "The Police": {
        "path": BASE + "the_police/",
        "cor": "#3B82F6",
        "faixas": {
            "Roxanne":               "roxanne.mp3",
            "Every Breath You Take": "every_breath_you_take.mp3",
            "Message in a Bottle":   "message_in_a_bottle.mp3",
            "Synchronicity II":      "synchronicity_ii.mp3",
        }
    },
    "ZZ Top": {
        "path": BASE + "zz_top/",
        "cor": "#F59E0B",
        "faixas": {
            "Sharp Dressed Man":     "sharp_dressed_man.mp3",
            "La Grange":             "la_grange.mp3",
            "Legs":                  "legs.mp3",
            "Gimme All Your Lovin'": "gimme_all_your_lovin.mp3",
        }
    },
    "SRV & Double Trouble": {
        "path": BASE + "srv/",
        "cor": "#10B981",
        "faixas": {
            "Pride and Joy":              "pride_and_joy.mp3",
            "Texas Flood":                "texas_flood.mp3",
            "Couldn't Stand the Weather": "couldnt_stand_the_weather.mp3",
            "The Sky is Crying":          "the_sky_is_crying.mp3",
        }
    },
}

FAIXAS_FREQ = ["Sub-grave", "Grave/Baixo", "Médio/Guitarra", "Médio-Agudo", "Agudo/Pratos"]

@st.cache_data
def extrair_features(path, arquivo):
    y, sr = librosa.load(path + arquivo, duration=60)
    D = librosa.stft(y)
    mag = np.abs(D)
    freqs = librosa.fft_frequencies(sr=sr)
    return {
        "Sub-grave":      mag[(freqs >= 20)  & (freqs < 80)].mean(),
        "Grave/Baixo":    mag[(freqs >= 80)  & (freqs < 300)].mean(),
        "Médio/Guitarra": mag[(freqs >= 300) & (freqs < 2000)].mean(),
        "Médio-Agudo":    mag[(freqs >= 2000)& (freqs < 6000)].mean(),
        "Agudo/Pratos":   mag[(freqs >= 6000)& (freqs < 20000)].mean(),
    }

@st.cache_data
def carregar_todos():
    medias = {}
    for trio, info in TRIOS.items():
        features = []
        for faixa, arquivo in info["faixas"].items():
            feat = extrair_features(info["path"], arquivo)
            feat["Faixa"] = faixa
            features.append(feat)
        df = pd.DataFrame(features).set_index("Faixa")
        medias[trio] = df.mean()
    df_trios = pd.DataFrame(medias).T
    df_trios_pct = df_trios.div(df_trios.sum(axis=1), axis=0) * 100
    return df_trios_pct

st.title("🎸 Power Trios — A Ciência por Trás do Som")
st.markdown("### Como três músicos conseguem soar maiores do que bandas inteiras?")
st.markdown("---")

with st.spinner("Analisando espectro sonoro..."):
    df_trios_pct = carregar_todos()

tab1, tab2, tab3 = st.tabs(["🎯 DNA Espectral", "🔍 Explorar Trio", "📊 Comparação"])

with tab1:
    st.subheader("DNA Espectral dos 5 Power Trios")
    st.markdown("Cada trio tem uma assinatura sonora única. O radar mostra como cada um distribui a energia pelo espectro.")

    fig = go.Figure()
    for trio, info in TRIOS.items():
        vals = df_trios_pct.loc[trio].tolist()
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=FAIXAS_FREQ + [FAIXAS_FREQ[0]],
            fill="toself",
            name=trio,
            line_color=info["cor"],
            fillcolor=info["cor"],
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
        df_trios_pct.round(1),
        text_auto=True,
        color_continuous_scale="magma",
        aspect="auto",
        height=320,
    )
    fig2.update_layout(
        title="% de Energia por Faixa de Frequência",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(df_trios_pct.columns))),
            ticktext=df_trios_pct.columns.tolist(),
            tickfont=dict(size=12),
        ),
        yaxis=dict(tickfont=dict(size=12)),
        margin=dict(l=150, r=50, t=60, b=50),
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Explorar um Trio")
    trio_sel = st.selectbox("Escolha o trio:", list(TRIOS.keys()))

    info = TRIOS[trio_sel]
    rows = []
    for faixa, arquivo in info["faixas"].items():
        feat = extrair_features(info["path"], arquivo)
        feat["Faixa"] = faixa
        rows.append(feat)

    df_trio = pd.DataFrame(rows).set_index("Faixa")
    df_trio_pct = df_trio.div(df_trio.sum(axis=1), axis=0) * 100

    fig3 = px.bar(
        df_trio_pct.reset_index().melt(id_vars="Faixa", var_name="Frequência", value_name="Energia %"),
        x="Faixa", y="Energia %", color="Frequência",
        barmode="group",
        title=f"Distribuição Espectral — {trio_sel}",
        color_discrete_sequence=px.colors.sequential.Plasma,
        height=500,
    )
    fig3.update_layout(xaxis_tickangle=-15)
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(df_trio_pct.round(1), use_container_width=True)

with tab3:
    st.subheader("Comparar Trios")
    trios_sel = st.multiselect(
        "Escolha os trios para comparar:",
        list(TRIOS.keys()),
        default=["Hendrix Experience", "Cream"]
    )

    if len(trios_sel) >= 2:
        fig4 = go.Figure()
        for trio in trios_sel:
            vals = df_trios_pct.loc[trio].tolist()
            fig4.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=FAIXAS_FREQ + [FAIXAS_FREQ[0]],
                fill="toself",
                name=trio,
                line_color=TRIOS[trio]["cor"],
                fillcolor=TRIOS[trio]["cor"],
                opacity=0.3,
            ))
        fig4.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 70])),
            showlegend=True,
            height=600,
            title="Comparação de DNA Espectral"
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.dataframe(df_trios_pct.loc[trios_sel].round(1), use_container_width=True)
    else:
        st.info("Selecione pelo menos 2 trios para comparar.")