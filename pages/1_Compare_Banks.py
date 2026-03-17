# ─────────────────────────────────────────────────────────────────
# Compare Two Banks — Page 2
# ─────────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Compare Banks — SA Bank Trust Score",
    page_icon="⚖️",
    layout="wide"
)

BANK_COLORS = {
    "Standard Bank": "#1565C0",
    "FNB":           "#E65100",
    "Absa":          "#C62828",
    "Nedbank":       "#2E7D32",
    "Capitec":       "#6A1B9A",
    "TymeBank":      "#00838F"
}

def trust_label(score):
    if score >= 7:   return "🟢 HIGH TRUST"
    elif score >= 4: return "🟡 MEDIUM TRUST"
    else:            return "🔴 LOW TRUST"

def trust_color(score):
    if score >= 7:   return "#2E7D32"
    elif score >= 4: return "#F9A825"
    else:            return "#C62828"

def comparison_bar(banks, values, title, xlabel, invert_note=""):
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    colors = [BANK_COLORS[b] for b in banks]
    bars   = ax.bar(banks, values, color=colors, edgecolor="#dddddd", width=0.45)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.02,
                f"{val:.1f}", ha="center", fontsize=12,
                fontweight="bold", color="#333333")

    ax.set_title(f"{title}{invert_note}", fontsize=11, pad=10, color="#333333")
    ax.set_xlabel(xlabel, fontsize=9, color="#333333")
    ax.set_ylim(0, max(values) * 1.25)
    ax.grid(axis="y", alpha=0.3, color="#dddddd")
    ax.tick_params(colors="#333333")
    ax.spines["bottom"].set_color("#dddddd")
    ax.spines["left"].set_color("#dddddd")
    ax.spines["top"].set_color("#dddddd")
    ax.spines["right"].set_color("#dddddd")

    return fig

@st.cache_data
def load_data():
    complaints = pd.read_csv("data/complaints.csv")
    sanctions  = pd.read_csv("data/sanctions.csv")
    sentiment  = pd.read_csv("data/sentiment.csv")
    return complaints, sanctions, sentiment

@st.cache_data
def build_scores(complaints, sanctions, sentiment):
    def normalise(series, invert=False):
        mn, mx = series.min(), series.max()
        if mx == mn:
            return pd.Series([5.0] * len(series), index=series.index)
        n = (series - mn) / (mx - mn) * 10
        return (10 - n) if invert else n

    df = complaints[[
        "bank", "referral_conversion_rate_pct",
        "cases_decided_consumer_favour_pct",
        "formal_cases_2021", "formal_cases_2022", "formal_cases_2023"
    ]].copy()
    df = df.merge(
        sentiment[["bank", "dataeq_net_sentiment_pct", "sagaci_satisfaction_2025"]],
        on="bank"
    )
    sanctions_total = (
        sanctions.groupby("bank")["penalty_zar"]
        .sum().reset_index()
        .rename(columns={"penalty_zar": "total_penalty_zar"})
    )
    df = df.merge(sanctions_total, on="bank", how="left").fillna(0)
    df["score_resolution"] = normalise(df["referral_conversion_rate_pct"], invert=True)
    df["score_favour"]     = normalise(df["cases_decided_consumer_favour_pct"])
    df["score_sanctions"]  = normalise(df["total_penalty_zar"], invert=True)
    df["score_sentiment"]  = normalise(
        (df["dataeq_net_sentiment_pct"] + df["sagaci_satisfaction_2025"]) / 2
    )
    df["trust_score"] = (
        df["score_resolution"] * 0.30 +
        df["score_favour"]     * 0.25 +
        df["score_sanctions"]  * 0.25 +
        df["score_sentiment"]  * 0.20
    )
    return df.sort_values("trust_score", ascending=False).reset_index(drop=True)

complaints, sanctions, sentiment = load_data()
df = build_scores(complaints, sanctions, sentiment)

# ─────────────────────────────────────────────────────────────────
# PAGE CONTENT
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#333333;'>⚖️ Compare Two Banks</h1>
<p style='text-align:center; color:#666666; font-size:16px;'>
    Select any two banks to compare their performance across every dimension.
</p>
<hr style='border-color:#e0e0e0;'>
""", unsafe_allow_html=True)

bank_list = df["bank"].tolist()
c1, c2 = st.columns(2)
bank_a = c1.selectbox("Bank A:", options=bank_list, index=0, key="compare_a")
bank_b = c2.selectbox("Bank B:", options=bank_list, index=1, key="compare_b")

if bank_a == bank_b:
    st.warning("Please select two different banks to compare.")
else:
    row_a = df[df["bank"] == bank_a].iloc[0]
    row_b = df[df["bank"] == bank_b].iloc[0]

    h1, mid, h2 = st.columns([2, 1, 2])
    with h1:
        st.markdown(f"""
        <div style='text-align:center; background:#f8f9fa; border:1px solid {BANK_COLORS[bank_a]};
             border-radius:10px; padding:16px;'>
            <div style='font-size:20px; font-weight:bold; color:{BANK_COLORS[bank_a]};'>{bank_a}</div>
            <div style='font-size:36px; font-weight:bold; color:#333;'>{row_a["trust_score"]:.1f}/10</div>
            <div style='color:{trust_color(row_a["trust_score"])};'>{trust_label(row_a["trust_score"])}</div>
        </div>
        """, unsafe_allow_html=True)
    with mid:
        st.markdown("<div style='text-align:center; padding-top:40px; font-size:24px; color:#aaaaaa;'>vs</div>",
                    unsafe_allow_html=True)
    with h2:
        st.markdown(f"""
        <div style='text-align:center; background:#f8f9fa; border:1px solid {BANK_COLORS[bank_b]};
             border-radius:10px; padding:16px;'>
            <div style='font-size:20px; font-weight:bold; color:{BANK_COLORS[bank_b]};'>{bank_b}</div>
            <div style='font-size:36px; font-weight:bold; color:#333;'>{row_b["trust_score"]:.1f}/10</div>
            <div style='color:{trust_color(row_b["trust_score"])};'>{trust_label(row_b["trust_score"])}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Dimension by Dimension")

    dim_comparisons = [
        ("Complaint Resolution Score",  "Score (0–10)", "score_resolution", "\n(higher = fewer escalations)"),
        ("Consumer Favour Score",       "Score (0–10)", "score_favour",     ""),
        ("Regulatory Record Score",     "Score (0–10)", "score_sanctions",  "\n(higher = fewer penalties)"),
        ("Consumer Sentiment Score",    "Score (0–10)", "score_sentiment",  ""),
    ]

    dim_cols = st.columns(2)
    for i, (title, xlabel, field, note) in enumerate(dim_comparisons):
        with dim_cols[i % 2]:
            fig = comparison_bar(
                [bank_a, bank_b],
                [row_a[field], row_b[field]],
                title, xlabel, note
            )
            st.pyplot(fig)

    st.markdown("#### Verdict")
    winner = bank_a if row_a["trust_score"] > row_b["trust_score"] else bank_b
    winner_row = row_a if winner == bank_a else row_b
    loser  = bank_b if winner == bank_a else bank_a
    margin = abs(row_a["trust_score"] - row_b["trust_score"])

    if margin < 0.5:
        verdict = f"**{bank_a}** and **{bank_b}** are very closely matched. Either is a reasonable choice — review the dimension breakdown above to decide based on what matters most to you."
    else:
        verdict = (
            f"Based on verified data, **{winner}** scores higher than **{loser}** "
            f"by {margin:.1f} points. "
            f"{winner} performs particularly well on "
        )
        best_dim = max(
            [("complaint resolution", winner_row["score_resolution"]),
             ("consumer favour rate", winner_row["score_favour"]),
             ("regulatory record",    winner_row["score_sanctions"]),
             ("consumer sentiment",   winner_row["score_sentiment"])],
            key=lambda x: x[1]
        )
        verdict += f"**{best_dim[0]}** ({best_dim[1]:.1f}/10)."

    st.info(verdict)