from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="LLMOps Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main{
    background:#0E1117;
}

.block-container{
    padding-top:2rem;
}

.metric-card{
    background:#1B1F2A;
    padding:20px;
    border-radius:18px;
    border:1px solid #2E3440;
    text-align:center;
    box-shadow:0px 4px 18px rgba(0,0,0,0.25);
}

.metric-title{
    color:#A0AEC0;
    font-size:14px;
}

.metric-value{
    font-size:34px;
    font-weight:bold;
    color:white;
}

.header{
    font-size:42px;
    font-weight:bold;
}

.sub{
    color:#9CA3AF;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

history_file = Path("reports/json/comparison_history.json")

if not history_file.exists():
    st.error("No evaluation history found.")
    st.stop()

with open(history_file, "r") as f:
    history = json.load(f)

df = pd.DataFrame(history)
df["accuracy"] = df["accuracy"] * 100

latest = df.iloc[-1]

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🤖 LLMOps")

st.sidebar.success("Model Regression Detection")

st.sidebar.markdown("---")

provider = latest["provider"]

prompt = latest["prompt"]

st.sidebar.metric("Provider", provider)

st.sidebar.metric("Prompt", prompt)

st.sidebar.metric(
    "Accuracy",
    f"{latest['accuracy']:.2f}%"
)

st.sidebar.markdown("---")

st.sidebar.info(
"""
Project Features

✅ Multi LLM

✅ Prompt Versioning

✅ Regression Detection

✅ Dashboard

✅ HTML Reports
"""
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
'<div class="header">🤖 LLM Evaluation Dashboard</div>',
unsafe_allow_html=True)

st.markdown(
'<div class="sub">Enterprise LLM Monitoring Platform</div>',
unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

cards = [
("Provider",latest["provider"]),
("Prompt",latest["prompt"]),
("Accuracy",f"{latest['accuracy']:.2f}%"),
("Evaluations",len(df))
]

cols=[c1,c2,c3,c4]

for col,(title,value) in zip(cols,cards):

    col.markdown(f"""
<div class="metric-card">

<div class="metric-title">

{title}

</div>

<div class="metric-value">

{value}

</div>

</div>
""",unsafe_allow_html=True)

st.write("")
st.divider()

# ---------------------------------------------------
# GAUGE + TREND
# ---------------------------------------------------

left,right = st.columns([1,2])

with left:

    gauge = go.Figure(go.Indicator(

        mode="gauge+number",

        value=latest["accuracy"],

        title={"text":"Model Health"},

        gauge={

            "axis":{"range":[0,100]},

            "bar":{"color":"royalblue"},

            "steps":[

                {"range":[0,60],"color":"#ef4444"},

                {"range":[60,90],"color":"#facc15"},

                {"range":[90,100],"color":"#22c55e"}

            ]
        }
    ))

    gauge.update_layout(height=420)

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

with right:

    fig = px.line(

        df,

        x="timestamp",

        y="accuracy",

        markers=True,

        title="Accuracy Trend"

    )

    fig.update_layout(

        height=420,

        paper_bgcolor="#0E1117",

        plot_bgcolor="#0E1117",

        font_color="white"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()
# ==========================================================
# PROMPT ANALYTICS
# ==========================================================

st.markdown("## 📊 Prompt Analytics")

left, right = st.columns(2)

with left:

    prompt_summary = (
        df.groupby("prompt")["accuracy"]
        .mean()
        .reset_index()
        .sort_values("accuracy", ascending=False)
    )

    fig = px.bar(
        prompt_summary,
        x="prompt",
        y="accuracy",
        color="accuracy",
        text="accuracy",
        title="Prompt Performance",
        color_continuous_scale="Viridis",
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white",
        coloraxis_showscale=False,
        xaxis_title="Prompt Version",
        yaxis_title="Accuracy (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    provider_summary = (
        df.groupby("provider")["accuracy"]
        .mean()
        .reset_index()
    )

    fig = px.pie(
        provider_summary,
        values="accuracy",
        names="provider",
        hole=0.65,
        title="Provider Comparison",
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    fig.update_layout(
        height=430,
        paper_bgcolor="#0E1117",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# ACCURACY DISTRIBUTION
# ==========================================================

left, right = st.columns([2, 1])

with left:

    fig = px.histogram(
        df,
        x="accuracy",
        nbins=10,
        color="provider",
        title="Accuracy Distribution"
    )

    fig.update_layout(
        height=400,
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.markdown("### 🏆 Best Prompt")

    best = prompt_summary.iloc[0]

    st.success(
        f"""
### {best['prompt']}

Accuracy

## {best['accuracy']:.2f}%
"""
    )

    worst = prompt_summary.iloc[-1]

    st.error(
        f"""
### Worst Prompt

{worst['prompt']}

Accuracy

## {worst['accuracy']:.2f}%
"""
    )

st.divider()

# ==========================================================
# REGRESSION TIMELINE
# ==========================================================

st.markdown("## 🚨 Regression Timeline")

timeline = df.copy()

timeline["Status"] = timeline["accuracy"].apply(
    lambda x: "Regression" if x < 95 else "Healthy"
)

colors = {
    "Healthy": "#22c55e",
    "Regression": "#ef4444",
}

fig = px.scatter(
    timeline,
    x="timestamp",
    y="accuracy",
    color="Status",
    size="accuracy",
    hover_data=["provider", "prompt"],
    color_discrete_map=colors,
    title="Evaluation Timeline",
)

fig.update_layout(
    height=450,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font_color="white",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

# ==========================================================
# SUMMARY
# ==========================================================

c1, c2, c3 = st.columns(3)

healthy = len(df[df["accuracy"] >= 95])
failed = len(df[df["accuracy"] < 95])

c1.metric(
    "Healthy Runs",
    healthy
)

c2.metric(
    "Regression Runs",
    failed
)

c3.metric(
    "Average Accuracy",
    f"{df['accuracy'].mean():.2f}%"
)

# ==========================================================
# FILTERS
# ==========================================================

st.divider()

st.markdown("## 🔍 Explore Evaluations")

f1, f2, f3 = st.columns(3)

provider_options = ["All"] + sorted(df["provider"].unique().tolist())
prompt_options = ["All"] + sorted(df["prompt"].unique().tolist())

selected_provider = f1.selectbox(
    "Provider",
    provider_options,
)

selected_prompt = f2.selectbox(
    "Prompt Version",
    prompt_options,
)

search_text = f3.text_input(
    "Search Prompt",
    placeholder="current, v1..."
)

filtered_df = df.copy()

if selected_provider != "All":
    filtered_df = filtered_df[
        filtered_df["provider"] == selected_provider
    ]

if selected_prompt != "All":
    filtered_df = filtered_df[
        filtered_df["prompt"] == selected_prompt
    ]

if search_text:

    filtered_df = filtered_df[
        filtered_df["prompt"]
        .str.contains(search_text, case=False)
    ]

# ==========================================================
# STATUS COLUMN
# ==========================================================

filtered_df = filtered_df.copy()

filtered_df["Status"] = filtered_df["accuracy"].apply(
    lambda x: "🟢 Healthy" if x >= 95 else "🔴 Regression"
)

st.markdown("### 📋 Evaluation History")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# LATEST RUN
# ==========================================================

st.markdown("## ⚡ Latest Evaluation")

latest_run = filtered_df.iloc[-1]

left, right = st.columns([2, 1])

with left:

    st.success(
f"""
### Provider

{latest_run['provider']}

### Prompt

{latest_run['prompt']}

### Accuracy

{latest_run['accuracy']:.2f}%

### Status

{latest_run['Status']}
"""
    )

with right:

    fig = go.Figure(
        go.Indicator(
            mode="number+delta",

            value=latest_run["accuracy"],

            delta={
                "reference":95
            },

            title={
                "text":"Accuracy Score"
            }
        )
    )

    fig.update_layout(
        height=300
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# DOWNLOAD CENTER
# ==========================================================

st.markdown("## 📥 Download Center")

c1, c2, c3 = st.columns(3)

with c1:

    with open(
        "reports/json/comparison_history.json",
        "rb",
    ) as f:

        st.download_button(

            "⬇ JSON",

            f,

            file_name="comparison_history.json",
        )

with c2:

    with open(
        "reports/html/comparison_report.html",
        "rb",
    ) as f:

        st.download_button(

            "⬇ HTML Report",

            f,

            file_name="comparison_report.html",
        )

with c3:

    csv = filtered_df.to_csv(index=False)

    st.download_button(

        "⬇ CSV",

        csv,

        file_name="evaluation_history.csv",

        mime="text/csv",
    )

st.divider()

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.markdown("## ⚙️ System Information")

i1, i2, i3, i4 = st.columns(4)

i1.metric(
    "Total Evaluations",
    len(df)
)

i2.metric(
    "Providers",
    df["provider"].nunique()
)

i3.metric(
    "Prompt Versions",
    df["prompt"].nunique()
)

i4.metric(
    "Average Accuracy",
    f"{df['accuracy'].mean():.2f}%"
)

st.divider()
# ==========================================================
# MODEL HEALTH PANEL
# ==========================================================

st.divider()

st.markdown("## 🧠 Model Health")

health = latest["accuracy"]

if health >= 95:
    color = "green"
    emoji = "🟢"
    message = "Excellent"

elif health >= 80:
    color = "orange"
    emoji = "🟡"
    message = "Stable"

else:
    color = "red"
    emoji = "🔴"
    message = "Regression"

left, right = st.columns([1,2])

with left:

    st.markdown(f"""
<div style="

background:#1B1F2A;

padding:25px;

border-radius:18px;

text-align:center;

border:2px solid {color};

">

<h1>{emoji}</h1>

<h2>{health:.2f}%</h2>

<h3>{message}</h3>

</div>

""",unsafe_allow_html=True)

with right:

    st.markdown("### Recent Runs")

    recent = df.tail(5)[
        [
            "timestamp",
            "provider",
            "prompt",
            "accuracy",
        ]
    ]

    st.table(recent)

# ==========================================================
# INSIGHTS
# ==========================================================

st.divider()

st.markdown("## 💡 AI Insights")

best_prompt = (
    df.groupby("prompt")["accuracy"]
    .mean()
    .idxmax()
)

best_accuracy = (
    df.groupby("prompt")["accuracy"]
    .mean()
    .max()
)

worst_prompt = (
    df.groupby("prompt")["accuracy"]
    .mean()
    .idxmin()
)

worst_accuracy = (
    df.groupby("prompt")["accuracy"]
    .mean()
    .min()
)

st.info(f"""
### Recommendation

✅ Best Prompt : **{best_prompt}**

Accuracy : **{best_accuracy:.2f}%**

---

⚠ Worst Prompt : **{worst_prompt}**

Accuracy : **{worst_accuracy:.2f}%**

---

Current Provider

**{latest["provider"]}**

Current Prompt

**{latest["prompt"]}**
""")

# ==========================================================
# PERFORMANCE SCORE
# ==========================================================

st.divider()

st.markdown("## 🏆 Overall Performance")

score = round(df["accuracy"].mean(),2)

progress = score/100

st.progress(progress)

st.metric(
    "Overall Evaluation Score",
    f"{score:.2f}%"
)

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.divider()

exp = st.expander(
    "📖 About this Project"
)

with exp:

    st.markdown("""

### Model Regression Detection System

Enterprise-grade LLM Evaluation Platform.

### Features

- Multi-LLM Support

- Prompt Versioning

- Regression Detection

- Prompt Comparison

- Evaluation Reports

- HTML Report Generation

- Streamlit Dashboard

- FastAPI Backend

- JSON Evaluation Storage

- Download Center

### Supported Providers

- Groq

- Gemini

### Tech Stack

Python

FastAPI

Streamlit

Plotly

Pandas

Scikit-learn

Groq API

Gemini API

""")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown("""
<center>

<h3>🚀 Enterprise LLMOps Platform</h3>

Built for Prompt Engineering • LLM Evaluation • Regression Detection

Made with ❤️ using

FastAPI • Streamlit • Plotly • Groq • Gemini

</center>
""",
unsafe_allow_html=True)

st.balloons()
