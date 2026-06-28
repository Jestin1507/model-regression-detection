from pathlib import Path
import json

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Model Regression Detection System",
    page_icon="🤖",
    layout="wide",
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background:#0E1117;
}

.metric-card{
    background:#161B22;
    border-radius:12px;
    padding:20px;
    text-align:center;
    border:1px solid #30363D;
}

.metric-title{
    color:#9CA3AF;
    font-size:15px;
    margin-bottom:10px;
}

.metric-value{
    font-size:34px;
    font-weight:bold;
    color:white;
}

.banner{
    padding:25px;
    border-radius:15px;
    background:linear-gradient(90deg,#2563EB,#7C3AED);
    color:white;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD HISTORY
# ==========================================================

history_file = Path(
    "reports/json/comparison_history.json"
)

if not history_file.exists():

    st.error("Run evaluation first.")

    st.stop()

with open(
    history_file,
    "r",
    encoding="utf-8",
) as f:

    history = json.load(f)

df = pd.DataFrame(history)

if df.empty:

    st.warning("No evaluation history available.")

    st.stop()

df["accuracy"] = df["accuracy"] * 100

# ==========================================================
# LOAD PROMPT COMPARISON
# ==========================================================

comparison_file = Path(
    "reports/json/prompt_comparison.json"
)

comparison_df = pd.DataFrame()

if comparison_file.exists():

    with open(
        comparison_file,
        "r",
        encoding="utf-8",
    ) as f:

        comparison_df = pd.DataFrame(json.load(f))

    if not comparison_df.empty:

        comparison_df["accuracy"] *= 100

        comparison_df["change"] *= 100

# ==========================================================
# LOAD EVALUATION RESULTS
# ==========================================================

results_file = Path(
    "reports/json/evaluation_results.json"
)

results_df = pd.DataFrame()

if results_file.exists():

    with open(
        results_file,
        "r",
        encoding="utf-8",
    ) as f:

        results_df = pd.DataFrame(json.load(f))

# ==========================================================
# CURRENT RUN
# ==========================================================

latest = df.iloc[-1]

provider = latest["provider"]

prompt = latest["prompt"]

current_accuracy = latest["accuracy"]

previous_accuracy = (
    df.iloc[-2]["accuracy"]
    if len(df) > 1
    else current_accuracy
)

accuracy_change = current_accuracy - previous_accuracy

threshold = 3.0

regression_pass = (
    "FAIL"
    if accuracy_change <= -threshold
    else "PASS"
)

regression_status = (
    "🔴 Regression"
    if regression_pass == "FAIL"
    else "🟢 Healthy"
)

healthy_runs = len(df[df["accuracy"] >= 95])

regression_runs = len(df[df["accuracy"] < 95])

average_accuracy = df["accuracy"].mean()

# ==========================================================
# PROMPT INSIGHTS
# ==========================================================

if not comparison_df.empty:

    leaderboard = comparison_df.sort_values(
        "accuracy",
        ascending=False,
    ).reset_index(drop=True)

    best_prompt = leaderboard.iloc[0]["prompt"]

    best_prompt_accuracy = leaderboard.iloc[0]["accuracy"]

    worst_prompt = leaderboard.iloc[-1]["prompt"]

    worst_prompt_accuracy = leaderboard.iloc[-1]["accuracy"]

else:

    best_prompt = prompt

    worst_prompt = prompt

    best_prompt_accuracy = current_accuracy

    worst_prompt_accuracy = current_accuracy

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🤖 LLMOps Dashboard")

st.sidebar.divider()

st.sidebar.metric(
    "Provider",
    provider.upper()
)

st.sidebar.metric(
    "Prompt",
    prompt
)

st.sidebar.metric(
    "Accuracy",
    f"{current_accuracy:.2f}%"
)

st.sidebar.metric(
    "Regression",
    regression_pass
)

st.sidebar.metric(
    "Evaluations",
    len(df)
)

st.sidebar.divider()

if regression_pass == "PASS":

    st.sidebar.success(
        "✅ Model Healthy"
    )

else:

    st.sidebar.error(
        "🚨 Regression Detected"
    )

# ==========================================================
# HEADER
# ==========================================================

st.markdown(f"""
<div class="banner">

<h1>🤖 Model Regression Detection System</h1>

<p>

<b>Provider:</b> {provider.upper()}

&nbsp;&nbsp;&nbsp;

<b>Prompt:</b> {prompt}

&nbsp;&nbsp;&nbsp;

<b>Accuracy:</b> {current_accuracy:.2f}%

&nbsp;&nbsp;&nbsp;

<b>Status:</b> {regression_pass}

</p>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# NAVIGATION
# ==========================================================

overview_tab, analytics_tab, regression_tab, history_tab, reports_tab, about_tab = st.tabs(
[
    "🏠 Overview",
    "📊 Analytics",
    "🚨 Regression",
    "📋 History",
    "📄 Reports",
    "ℹ️ About",
]
)

# ==========================================================
# OVERVIEW
# ==========================================================

with overview_tab:

    st.subheader("🏠 Overview")

    # ------------------------------------------------------
    # KPI CARDS
    # ------------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Current Accuracy",
        f"{current_accuracy:.2f}%"
    )

    c2.metric(
        "Previous Accuracy",
        f"{previous_accuracy:.2f}%"
    )

    c3.metric(
        "Change",
        f"{accuracy_change:+.2f}%"
    )

    c4.metric(
        "Regression",
        regression_pass
    )

    c5.metric(
        "Best Prompt",
        best_prompt
    )

    st.divider()

    # ------------------------------------------------------
    # HEALTH GAUGE + ACCURACY TREND
    # ------------------------------------------------------

    left, right = st.columns([1, 2])

    with left:

        gauge = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=current_accuracy,

                title={"text": "Model Health"},

                gauge={

                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": "#2563EB"
                    },

                    "steps": [

                        {
                            "range": [0, 60],
                            "color": "#DC2626"
                        },

                        {
                            "range": [60, 90],
                            "color": "#F59E0B"
                        },

                        {
                            "range": [90, 100],
                            "color": "#22C55E"
                        },

                    ]

                }

            )

        )

        gauge.update_layout(

            height=430,

            paper_bgcolor="#0E1117",

            plot_bgcolor="#0E1117",

            font_color="white",

        )

        st.plotly_chart(
            gauge,
            use_container_width=True,
        )

    with right:

        trend = px.line(

            df,

            x="timestamp",

            y="accuracy",

            markers=True,

            title="Accuracy Trend",

        )

        trend.update_traces(

            line=dict(width=4),

            marker=dict(size=9),

        )

        trend.update_layout(

            height=430,

            paper_bgcolor="#0E1117",

            plot_bgcolor="#0E1117",

            font_color="white",

            xaxis_title="",

            yaxis_title="Accuracy (%)",

        )

        st.plotly_chart(

            trend,

            use_container_width=True,

        )

    st.divider()

    # ------------------------------------------------------
    # QUICK SUMMARY
    # ------------------------------------------------------

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Healthy Runs",
        healthy_runs
    )

    s2.metric(
        "Regression Runs",
        regression_runs
    )

    s3.metric(
        "Average Accuracy",
        f"{average_accuracy:.2f}%"
    )

    st.divider()

    # ------------------------------------------------------
    # LATEST EVALUATION
    # ------------------------------------------------------

    st.subheader("📄 Latest Evaluation")

    info, table = st.columns([1, 2])

    with info:

        st.metric(
            "Provider",
            provider.upper()
        )

        st.metric(
            "Prompt Version",
            prompt
        )

        st.metric(
            "Current Accuracy",
            f"{current_accuracy:.2f}%"
        )

        st.metric(
            "Previous Accuracy",
            f"{previous_accuracy:.2f}%"
        )

        st.metric(
            "Accuracy Change",
            f"{accuracy_change:+.2f}%"
        )

        st.metric(
            "Regression Status",
            regression_pass
        )

    with table:

        recent = (
            df.sort_values(
                "timestamp",
                ascending=False,
            )
            .head(10)
            .copy()
        )

        recent["accuracy"] = recent["accuracy"].map(
            lambda x: f"{x:.2f}%"
        )

        recent["change"] = recent["change"].map(
            lambda x: f"{x:+.2f}%"
        )

        recent.rename(
            columns={
                "timestamp": "Timestamp",
                "provider": "Provider",
                "prompt": "Prompt",
                "accuracy": "Accuracy",
                "change": "Change",
                "status": "Status",
            },
            inplace=True,
        )

        st.dataframe(

            recent[
                [
                    "Timestamp",
                    "Provider",
                    "Prompt",
                    "Accuracy",
                    "Change",
                    "Status",
                ]
            ],

            hide_index=True,

            use_container_width=True,

        )

    st.divider()

    # ------------------------------------------------------
    # CURRENT CONFIGURATION
    # ------------------------------------------------------

    st.subheader("⚙️ Current Configuration")

    cfg1, cfg2, cfg3, cfg4 = st.columns(4)

    cfg1.metric(
        "Provider",
        provider.upper()
    )

    cfg2.metric(
        "Current Prompt",
        prompt
    )

    cfg3.metric(
        "Best Prompt",
        best_prompt
    )

    cfg4.metric(
        "Threshold",
        f"{threshold:.1f}%"
    )

    st.divider()

    # ------------------------------------------------------
    # PROMPT LEADERBOARD
    # ------------------------------------------------------

    st.subheader("🏆 Prompt Leaderboard")

    if not comparison_df.empty:

        leaderboard = comparison_df.sort_values(
            "accuracy",
            ascending=False,
        ).copy()

        leaderboard["accuracy"] = leaderboard["accuracy"].map(
            lambda x: f"{x:.2f}%"
        )

        leaderboard["change"] = leaderboard["change"].map(
            lambda x: f"{x:+.2f}%"
        )

        leaderboard.rename(
            columns={
                "prompt": "Prompt",
                "accuracy": "Accuracy",
                "change": "Change",
                "status": "Status",
            },
            inplace=True,
        )

        st.dataframe(

            leaderboard[
                [
                    "Prompt",
                    "Accuracy",
                    "Change",
                    "Status",
                ]
            ],

            hide_index=True,

            use_container_width=True,

        )

# ==========================================================
# ANALYTICS
# ==========================================================

with analytics_tab:

    st.subheader("📊 Analytics")

    # ------------------------------------------------------
    # PROMPT PERFORMANCE
    # ------------------------------------------------------

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        if not comparison_df.empty:

            fig = px.bar(

                comparison_df.sort_values(
                    "accuracy",
                    ascending=False,
                ),

                x="prompt",

                y="accuracy",

                color="accuracy",

                text="accuracy",

                title="Prompt Performance",

                color_continuous_scale="Viridis",

            )

            fig.update_traces(

                texttemplate="%{text:.2f}%",

                textposition="outside",

            )

            fig.update_layout(

                height=420,

                paper_bgcolor="#0E1117",

                plot_bgcolor="#0E1117",

                font_color="white",

                coloraxis_showscale=False,

                xaxis_title="Prompt",

                yaxis_title="Accuracy (%)",

            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    # ------------------------------------------------------
    # PROVIDER PERFORMANCE
    # ------------------------------------------------------

    with row1_col2:

        provider_summary = (

            df.groupby("provider")["accuracy"]

            .mean()

            .reset_index()

        )

        fig = px.pie(

            provider_summary,

            names="provider",

            values="accuracy",

            hole=0.65,

            title="Provider Distribution",

        )

        fig.update_layout(

            height=420,

            paper_bgcolor="#0E1117",

            font_color="white",

        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()

    # ------------------------------------------------------
    # PROMPT LEADERBOARD
    # ------------------------------------------------------

    left, right = st.columns([2, 1])

    with left:

        if not comparison_df.empty:

            leaderboard = comparison_df.sort_values(
                "accuracy",
                ascending=False,
            )

            fig = px.bar(

                leaderboard,

                x="prompt",

                y="accuracy",

                color="accuracy",

                text="accuracy",

                title="🏆 Prompt Leaderboard",

                color_continuous_scale="Turbo",

            )

            fig.update_traces(

                texttemplate="%{text:.2f}%",

                textposition="outside",

            )

            fig.update_layout(

                height=420,

                paper_bgcolor="#0E1117",

                plot_bgcolor="#0E1117",

                font_color="white",

                coloraxis_showscale=False,

            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    with right:

        st.success(f"""
### 🥇 Best Prompt

**{best_prompt}**

Accuracy

## {best_prompt_accuracy:.2f}%
""")

        st.warning(f"""
### 🥉 Lowest Prompt

**{worst_prompt}**

Accuracy

## {worst_prompt_accuracy:.2f}%
""")

        st.info(f"""
### 📈 Current Run

Provider

**{provider.upper()}**

Prompt

**{prompt}**

Status

**{regression_pass}**
""")

    st.divider()

    # ------------------------------------------------------
    # CATEGORY-WISE ANALYSIS
    # ------------------------------------------------------

    st.subheader("📊 Category-wise Accuracy")

    if not comparison_df.empty:

        selected = comparison_df.iloc[0]

        category_df = pd.DataFrame(
            selected["category_metrics"]
        )

        left, right = st.columns([2, 1])

        with left:

            fig = px.bar(

                category_df,

                x="category",

                y="accuracy",

                color="accuracy",

                text="accuracy",

                color_continuous_scale="Viridis",

                title=f"{selected['prompt']} Category Accuracy",

            )

            fig.update_traces(

                texttemplate="%{text:.1f}%",

                textposition="outside",

            )

            fig.update_layout(

                height=420,

                paper_bgcolor="#0E1117",

                plot_bgcolor="#0E1117",

                font_color="white",

                coloraxis_showscale=False,

            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with right:

            best = category_df.loc[
                category_df["accuracy"].idxmax()
            ]

            worst = category_df.loc[
                category_df["accuracy"].idxmin()
            ]

            st.success(f"""
### 🏆 Best Category

**{best['category']}**

## {best['accuracy']:.2f}%
""")

            st.error(f"""
### ⚠ Lowest Category

**{worst['category']}**

## {worst['accuracy']:.2f}%
""")

        st.dataframe(

            category_df,

            hide_index=True,

            use_container_width=True,

        )

    st.divider()

    # ------------------------------------------------------
    # PROMPT COMPARISON
    # ------------------------------------------------------

    st.subheader("📋 Prompt Comparison")

    if not comparison_df.empty:

        table = comparison_df[
            [
                "prompt",
                "accuracy",
                "change",
                "status",
            ]
        ].copy()

        table.rename(
            columns={
                "prompt": "Prompt",
                "accuracy": "Accuracy",
                "change": "Change",
                "status": "Status",
            },
            inplace=True,
        )

        table["Accuracy"] = table["Accuracy"].map(
            lambda x: f"{x:.2f}%"
        )

        table["Change"] = table["Change"].map(
            lambda x: f"{x:+.2f}%"
        )

        table["Status"] = table["Status"].replace({
            "PASS": "✅ PASS",
            "REGRESSION": "🚨 REGRESSION",
        })

        st.dataframe(

            table,

            hide_index=True,

            use_container_width=True,

        )

# ==========================================================
# REGRESSION
# ==========================================================

with regression_tab:

    st.subheader("🚨 Regression Monitor")

    # ------------------------------------------------------
    # KPI
    # ------------------------------------------------------

    r1, r2, r3, r4, r5 = st.columns(5)

    r1.metric(
        "Current Accuracy",
        f"{current_accuracy:.2f}%"
    )

    r2.metric(
        "Previous Accuracy",
        f"{previous_accuracy:.2f}%"
    )

    r3.metric(
        "Change",
        f"{accuracy_change:+.2f}%"
    )

    r4.metric(
        "Threshold",
        f"{threshold:.1f}%"
    )

    r5.metric(
        "Regression",
        regression_pass
    )

    st.divider()

    # ------------------------------------------------------
    # TIMELINE
    # ------------------------------------------------------

    left, right = st.columns([2.2, 1])

    timeline = df.copy()

    timeline["Status"] = timeline["accuracy"].apply(
        lambda x: "Healthy"
        if x >= 95
        else "Regression"
    )

    with left:

        fig = px.scatter(

            timeline,

            x="timestamp",

            y="accuracy",

            color="Status",

            size="accuracy",

            hover_data=[
                "provider",
                "prompt",
            ],

            color_discrete_map={
                "Healthy": "#22C55E",
                "Regression": "#EF4444",
            },

            title="Regression Timeline",

        )

        fig.update_layout(

            height=500,

            paper_bgcolor="#0E1117",

            plot_bgcolor="#0E1117",

            font_color="white",

        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:

        st.metric(
            "Healthy Runs",
            healthy_runs
        )

        st.metric(
            "Regression Runs",
            regression_runs
        )

        st.metric(
            "Average Accuracy",
            f"{average_accuracy:.2f}%"
        )

        st.progress(
            current_accuracy / 100
        )

        if regression_pass == "PASS":

            st.success(
                "✅ No Regression"
            )

        else:

            st.error(
                "🚨 Regression Found"
            )

    st.divider()

    # ------------------------------------------------------
    # LATEST SUMMARY
    # ------------------------------------------------------

    st.subheader("📄 Latest Regression Summary")

    c1, c2 = st.columns([1, 2])

    with c1:

        st.metric(
            "Provider",
            provider.upper()
        )

        st.metric(
            "Prompt",
            prompt
        )

        st.metric(
            "Status",
            regression_status
        )

        st.metric(
            "Accuracy",
            f"{current_accuracy:.2f}%"
        )

        st.metric(
            "Best Prompt",
            best_prompt
        )

    with c2:

        summary = pd.DataFrame({

            "Metric":[

                "Provider",

                "Prompt",

                "Previous Accuracy",

                "Current Accuracy",

                "Accuracy Change",

                "Threshold",

                "Regression",

                "Best Prompt",

            ],

            "Value":[

                provider.upper(),

                prompt,

                f"{previous_accuracy:.2f}%",

                f"{current_accuracy:.2f}%",

                f"{accuracy_change:+.2f}%",

                f"{threshold:.1f}%",

                regression_pass,

                best_prompt,

            ]

        })

        st.dataframe(
            summary,
            hide_index=True,
            use_container_width=True,
        )

    st.divider()

    # ------------------------------------------------------
    # FAILED PREDICTIONS
    # ------------------------------------------------------

    st.subheader("❌ Failed Prediction Analysis")

    if not results_df.empty:

        failed_df = results_df[
            results_df["correct"] == False
        ].copy()

        if failed_df.empty:

            st.success(
                "🎉 No failed predictions."
            )

        else:

            failed_df.rename(
                columns={
                    "question": "Question",
                    "expected": "Expected",
                    "predicted": "Predicted",
                    "category": "Category",
                    "difficulty": "Difficulty",
                    "prompt_version": "Prompt",
                },
                inplace=True,
            )

            st.metric(
                "Failed Samples",
                len(failed_df)
            )

            st.dataframe(

                failed_df[
                    [
                        "Question",
                        "Expected",
                        "Predicted",
                        "Category",
                        "Difficulty",
                        "Prompt",
                    ]
                ],

                hide_index=True,

                use_container_width=True,

            )

    else:

        st.info(
            "No evaluation results available."
        )
# ==========================================================
# HISTORY
# ==========================================================

with history_tab:

    st.subheader("📋 Evaluation History")

    # ------------------------------------------------------
    # FILTERS
    # ------------------------------------------------------

    f1, f2, f3 = st.columns(3)

    provider_options = ["All"] + sorted(df["provider"].unique())

    prompt_options = ["All"] + sorted(df["prompt"].unique())

    selected_provider = f1.selectbox(
        "Provider",
        provider_options,
    )

    selected_prompt = f2.selectbox(
        "Prompt",
        prompt_options,
    )

    search = f3.text_input(
        "Search Prompt",
        placeholder="current, v1..."
    )

    history_df = df.copy()

    if selected_provider != "All":

        history_df = history_df[
            history_df["provider"] == selected_provider
        ]

    if selected_prompt != "All":

        history_df = history_df[
            history_df["prompt"] == selected_prompt
        ]

    if search:

        history_df = history_df[
            history_df["prompt"].str.contains(
                search,
                case=False,
            )
        ]

    # ------------------------------------------------------
    # TABLE
    # ------------------------------------------------------

    display = history_df.copy()

    display["accuracy"] = display["accuracy"].map(
        lambda x: f"{x:.2f}%"
    )

    display["previous_accuracy"] = display[
        "previous_accuracy"
    ].map(
        lambda x: f"{x:.2f}%"
    )

    display["change"] = display["change"].map(
        lambda x: f"{x:+.2f}%"
    )

    display.rename(
        columns={
            "timestamp": "Timestamp",
            "provider": "Provider",
            "prompt": "Prompt",
            "accuracy": "Accuracy",
            "previous_accuracy": "Previous",
            "change": "Change",
            "status": "Status",
        },
        inplace=True,
    )

    st.dataframe(

        display[
            [
                "Timestamp",
                "Provider",
                "Prompt",
                "Previous",
                "Accuracy",
                "Change",
                "Status",
            ]
        ],

        hide_index=True,

        use_container_width=True,

    )

    st.divider()

    # ------------------------------------------------------
    # HISTORY SUMMARY
    # ------------------------------------------------------

    latest_history = history_df.iloc[-1]

    left, right = st.columns([1, 2])

    with left:

        st.metric(
            "Provider",
            latest_history["provider"].upper()
        )

        st.metric(
            "Prompt",
            latest_history["prompt"]
        )

        st.metric(
            "Accuracy",
            f"{latest_history['accuracy']:.2f}%"
        )

        st.metric(
            "Status",
            latest_history["status"]
        )

    with right:

        summary = pd.DataFrame({

            "Metric": [

                "Provider",

                "Prompt",

                "Previous Accuracy",

                "Current Accuracy",

                "Accuracy Change",

                "Threshold",

                "Regression",

            ],

            "Value": [

                provider.upper(),

                prompt,

                f"{previous_accuracy:.2f}%",

                f"{current_accuracy:.2f}%",

                f"{accuracy_change:+.2f}%",

                f"{threshold:.1f}%",

                regression_pass,

            ]

        })

        st.dataframe(

            summary,

            hide_index=True,

            use_container_width=True,

        )

    st.divider()

    # ------------------------------------------------------
    # HISTORY TIMELINE
    # ------------------------------------------------------

    st.subheader("📈 Evaluation Timeline")

    fig = px.line(

        df,

        x="timestamp",

        y="accuracy",

        color="provider",

        markers=True,

        title="Accuracy Across Evaluations",

    )

    fig.update_traces(

        line=dict(width=4),

        marker=dict(size=8),

    )

    fig.update_layout(

        height=420,

        paper_bgcolor="#0E1117",

        plot_bgcolor="#0E1117",

        font_color="white",

        xaxis_title="",

        yaxis_title="Accuracy (%)",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

# ==========================================================
# REPORTS
# ==========================================================

with reports_tab:

    st.subheader("📄 Reports & Downloads")

    # ------------------------------------------------------
    # REPORT SUMMARY
    # ------------------------------------------------------

    left, right = st.columns([1, 2])

    with left:

        st.metric(
            "Current Accuracy",
            f"{current_accuracy:.2f}%"
        )

        st.metric(
            "Previous Accuracy",
            f"{previous_accuracy:.2f}%"
        )

        st.metric(
            "Accuracy Change",
            f"{accuracy_change:+.2f}%"
        )

        st.metric(
            "Regression",
            regression_pass
        )

        st.metric(
            "Best Prompt",
            best_prompt
        )

    with right:

        summary = pd.DataFrame({

            "Metric":[

                "Provider",

                "Current Prompt",

                "Current Accuracy",

                "Previous Accuracy",

                "Accuracy Change",

                "Regression",

                "Best Prompt",

                "Threshold",

            ],

            "Value":[

                provider.upper(),

                prompt,

                f"{current_accuracy:.2f}%",

                f"{previous_accuracy:.2f}%",

                f"{accuracy_change:+.2f}%",

                regression_pass,

                best_prompt,

                f"{threshold:.1f}%",

            ]

        })

        st.dataframe(

            summary,

            hide_index=True,

            use_container_width=True,

        )

    st.divider()

    # ------------------------------------------------------
    # DOWNLOAD CENTER
    # ------------------------------------------------------

    st.subheader("📥 Download Center")

    d1, d2, d3 = st.columns(3)

    with d1:

        if Path("reports/json/comparison_history.json").exists():

            with open(
                "reports/json/comparison_history.json",
                "rb",
            ) as f:

                st.download_button(

                    "⬇ Regression History",

                    f,

                    file_name="comparison_history.json",

                    use_container_width=True,

                )

    with d2:

        if Path("reports/json/prompt_comparison.json").exists():

            with open(
                "reports/json/prompt_comparison.json",
                "rb",
            ) as f:

                st.download_button(

                    "⬇ Prompt Comparison",

                    f,

                    file_name="prompt_comparison.json",

                    use_container_width=True,

                )

    with d3:

        if Path("reports/html/comparison_report.html").exists():

            with open(
                "reports/html/comparison_report.html",
                "rb",
            ) as f:

                st.download_button(

                    "⬇ HTML Report",

                    f,

                    file_name="comparison_report.html",

                    use_container_width=True,

                )

    st.divider()

    # ------------------------------------------------------
    # SYSTEM OVERVIEW
    # ------------------------------------------------------

    st.subheader("⚙️ System Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Evaluations",
        len(df)
    )

    c2.metric(
        "Providers",
        df["provider"].nunique()
    )

    c3.metric(
        "Prompt Versions",
        comparison_df["prompt"].nunique()
        if not comparison_df.empty
        else 0
    )

    c4.metric(
        "Average Accuracy",
        f"{average_accuracy:.2f}%"
    )

    st.divider()

    # ------------------------------------------------------
    # PROMPT LEADERBOARD
    # ------------------------------------------------------

    st.subheader("🏆 Prompt Leaderboard")

    if not comparison_df.empty:

        leaderboard = comparison_df.copy()

        leaderboard = leaderboard.sort_values(
            "accuracy",
            ascending=False,
        )

        leaderboard["accuracy"] = leaderboard[
            "accuracy"
        ].map(
            lambda x: f"{x:.2f}%"
        )

        leaderboard["change"] = leaderboard[
            "change"
        ].map(
            lambda x: f"{x:+.2f}%"
        )

        leaderboard.rename(
            columns={
                "prompt": "Prompt",
                "accuracy": "Accuracy",
                "change": "Change",
                "status": "Status",
            },
            inplace=True,
        )

        st.dataframe(

            leaderboard[
                [
                    "Prompt",
                    "Accuracy",
                    "Change",
                    "Status",
                ]
            ],

            hide_index=True,

            use_container_width=True,

        )

    st.divider()

    # ------------------------------------------------------
    # RECENT EVALUATIONS
    # ------------------------------------------------------

    st.subheader("🕒 Recent Evaluation Runs")

    recent = (

        df.sort_values(

            "timestamp",

            ascending=False,

        )

        .head(10)

        .copy()

    )

    recent["accuracy"] = recent["accuracy"].map(
        lambda x: f"{x:.2f}%"
    )

    recent["change"] = recent["change"].map(
        lambda x: f"{x:+.2f}%"
    )

    recent.rename(

        columns={

            "timestamp": "Timestamp",

            "provider": "Provider",

            "prompt": "Prompt",

            "accuracy": "Accuracy",

            "change": "Change",

            "status": "Status",

        },

        inplace=True,

    )

    st.dataframe(

        recent[
            [
                "Timestamp",
                "Provider",
                "Prompt",
                "Accuracy",
                "Change",
                "Status",
            ]
        ],

        hide_index=True,

        use_container_width=True,

    )

# ==========================================================
# ABOUT
# ==========================================================

with about_tab:

    st.subheader("ℹ️ About Model Regression Detection System")

    left, right = st.columns([1, 2])

    # ------------------------------------------------------
    # PROJECT STATUS
    # ------------------------------------------------------

    with left:

        st.metric(
            "Current Accuracy",
            f"{current_accuracy:.2f}%"
        )

        st.metric(
            "Regression",
            regression_pass
        )

        st.metric(
            "Provider",
            provider.upper()
        )

        st.metric(
            "Current Prompt",
            prompt
        )

        st.metric(
            "Best Prompt",
            best_prompt
        )

        st.progress(current_accuracy / 100)

        if regression_pass == "PASS":

            st.success("🟢 Production Ready")

        else:

            st.error("🚨 Regression Detected")

    # ------------------------------------------------------
    # PROJECT DESCRIPTION
    # ------------------------------------------------------

    with right:

        st.markdown("""

# 🤖 Model Regression Detection System

An enterprise-grade **LLMOps platform** for evaluating Large Language Models and automatically detecting prompt regressions before deployment.

---

## 🎯 Objectives

- Evaluate prompt versions on a golden dataset.
- Compare multiple prompt versions.
- Detect prompt regressions.
- Monitor category-wise performance.
- Generate evaluation reports.
- Support CI/CD quality gates.

---

## 🚀 Key Features

- ✅ Multi-Provider Architecture
- ✅ Prompt Versioning
- ✅ Prompt Comparison
- ✅ Regression Detection
- ✅ Category-wise Accuracy
- ✅ Failed Prediction Analysis
- ✅ Prompt Leaderboard
- ✅ Evaluation History
- ✅ HTML & JSON Reports
- ✅ Interactive Dashboard
- ✅ Download Center
- ✅ CI/CD Ready

""")

    st.divider()

    # ------------------------------------------------------
    # ARCHITECTURE
    # ------------------------------------------------------

    st.subheader("🏗 Architecture")

    st.code("""

                  Golden Dataset
                         │
                         ▼
                Prompt Version (v1/v2/current)
                         │
                         ▼
                 Ticket Classifier
                         │
                  LLM Factory Pattern
             ┌───────────┴───────────┐
             │                       │
         Groq Client            Gemini Client
             │                       │
             └───────────┬───────────┘
                         ▼
                 Model Prediction
                         │
                         ▼
              Evaluation + Metrics
                         │
                         ▼
               Regression Detection
                         │
                         ▼
      JSON Reports • HTML Reports • Dashboard

""")

    st.divider()

    # ------------------------------------------------------
    # TECHNOLOGY STACK
    # ------------------------------------------------------

    st.subheader("🛠 Technology Stack")

    t1, t2, t3, t4 = st.columns(4)

    with t1:

        st.info("""
### Backend

- Python
- FastAPI
- Pandas
- NumPy
""")

    with t2:

        st.info("""
### LLM

- Groq API
- Gemini API
- Factory Pattern
""")

    with t3:

        st.info("""
### Dashboard

- Streamlit
- Plotly
- HTML Reports
- JSON Reports
""")

    with t4:

        st.info("""
### Evaluation

- Scikit-learn
- Regression Engine
- Prompt Comparison
- Category Metrics
""")

    st.divider()

    # ------------------------------------------------------
    # PLATFORM STATISTICS
    # ------------------------------------------------------

    st.subheader("📊 Platform Statistics")

    s1, s2, s3, s4 = st.columns(4)

    s1.metric(
        "Evaluations",
        len(df)
    )

    s2.metric(
        "Providers",
        df["provider"].nunique()
    )

    s3.metric(
        "Prompt Versions",
        comparison_df["prompt"].nunique()
        if not comparison_df.empty
        else 0
    )

    s4.metric(
        "Average Accuracy",
        f"{average_accuracy:.2f}%"
    )

    st.divider()

    # ------------------------------------------------------
    # ENTERPRISE FEATURES
    # ------------------------------------------------------

    st.success("""

## ✅ Enterprise Features

✔ Prompt Regression Testing

✔ Prompt Version Comparison

✔ Category-wise Accuracy

✔ Failed Prediction Analysis

✔ Multi-Provider LLM Support

✔ Golden Dataset Evaluation

✔ Interactive Dashboard

✔ JSON & HTML Report Generation

✔ Download Center

✔ CI/CD Ready

✔ Scalable LLMOps Architecture

""")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown("""

<div style="text-align:center;padding:20px;">

<h3>🤖 Model Regression Detection System</h3>

<p>
Evaluate • Compare • Detect • Monitor • Deploy
</p>

<hr>

<small>

Built with Python • FastAPI • Streamlit • Plotly • Groq • Gemini

</small>

</div>

""", unsafe_allow_html=True)                       