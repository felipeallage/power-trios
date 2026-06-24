import librosa
import numpy as np
import pandas as pd

BASE = "C:/Users/felip/OneDrive/Documentos/power_trios/data/audio/"

TRIOS = {
    "Hendrix Experience": {
        "path": BASE + "hendrix/",
        "faixas": {
            "Purple Haze":          "purple_haze.mp3",
            "Voodoo Child":         "voodoo_child.mp3",
            "Little Wing":          "littlewing.mp3",
            "All Along Watchtower": "all_allong_the_watchtower.mp3",
        }
    },
    "Cream": {
        "path": BASE + "cream/",
        "faixas": {
            "Sunshine of Your Love": "sunshine_of_your_love.mp3",
            "White Room":            "white_room.mp3",
            "Crossroads":            "crossroads.mp3",
            "Badge":                 "badge.mp3",
        }
    },
    "The Police": {
        "path": BASE + "the_police/",
        "faixas": {
            "Roxanne":               "roxanne.mp3",
            "Every Breath You Take": "every_breath_you_take.mp3",
            "Message in a Bottle":   "message_in_a_bottle.mp3",
            "Synchronicity II":      "synchronicity_ii.mp3",
        }
    },
    "ZZ Top": {
        "path": BASE + "zz_top/",
        "faixas": {
            "Sharp Dressed Man":     "sharp_dressed_man.mp3",
            "La Grange":             "la_grange.mp3",
            "Legs":                  "legs.mp3",
            "Gimme All Your Lovin'": "gimme_all_your_lovin.mp3",
        }
    },
    "SRV & Double Trouble": {
        "path": BASE + "srv/",
        "faixas": {
            "Pride and Joy":              "pride_and_joy.mp3",
            "Texas Flood":                "texas_flood.mp3",
            "Couldn't Stand the Weather": "couldnt_stand_the_weather.mp3",
            "The Sky is Crying":          "the_sky_is_crying.mp3",
        }
    },
}

rows = []
for trio, info in TRIOS.items():
    print(f"Processando {trio}...")
    for faixa, arquivo in info["faixas"].items():
        y, sr = librosa.load(info["path"] + arquivo, duration=60)
        D = librosa.stft(y)
        mag = np.abs(D)
        freqs = librosa.fft_frequencies(sr=sr)
        rows.append({
            "trio":           trio,
            "faixa":          faixa,
            "sub_grave":      mag[(freqs >= 20)  & (freqs < 80)].mean(),
            "grave_baixo":    mag[(freqs >= 80)  & (freqs < 300)].mean(),
            "medio_guitarra": mag[(freqs >= 300) & (freqs < 2000)].mean(),
            "medio_agudo":    mag[(freqs >= 2000)& (freqs < 6000)].mean(),
            "agudo_pratos":   mag[(freqs >= 6000)& (freqs < 20000)].mean(),
        })

df = pd.DataFrame(rows)
df.to_csv("data/spectral_features.csv", index=False)
print(f"\nConcluído! {len(df)} faixas salvas em data/spectral_features.csv")
print(df)