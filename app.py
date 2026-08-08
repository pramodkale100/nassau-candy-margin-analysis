"""
Nassau Candy Distributor - Product Line Profitability & Margin Performance Analysis
Day 4: Streamlit Dashboard

Author: Pramod Kale

Run locally with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# CONFIG - CSV paths (all outputs from Day 1-3 scripts)
# ---------------------------------------------------------------------------
CLEANED_CSV_PATH = "outputs/cleaned_transactions.csv"
PRODUCT_SUMMARY_PATH = "outputs/product_kpi_summary_with_quadrants.csv"
DIVISION_SUMMARY_PATH = "outputs/division_summary.csv"
PARETO_PATH = "outputs/pareto_analysis.csv"
DIAGNOSTICS_PATH = "outputs/cost_structure_diagnostics.csv"

st.set_page_config(
    page_title="Nassau Candy - Product Profitability Dashboard",
    page_icon="🍬",
    layout="wide",
)

# ---------------------------------------------------------------------------
# LOAD DATA (cached so filters don't re-read CSVs every interaction)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(CLEANED_CSV_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    product_summary = pd.read_csv(PRODUCT_SUMMARY_PATH)
    division_summary = pd.read_csv(DIVISION_SUMMARY_PATH)
    pareto = pd.read_csv(PARETO_PATH)
    diagnostics = pd.read_csv(DIAGNOSTICS_PATH)
    return df, product_summary, division_summary, pareto, diagnostics


df, product_summary, division_summary, pareto, diagnostics = load_data()

# ---------------------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------------------
st.sidebar.title("🍬 Filters")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

divisions = sorted(df["Division"].unique().tolist())
selected_divisions = st.sidebar.multiselect("Division", divisions, default=divisions)

margin_threshold = st.sidebar.slider(
    "Minimum Gross Margin % (product-level)", 0, 100, 0, step=5
)

product_search = st.sidebar.text_input("Search Product Name", "")

st.sidebar.markdown("---")
st.sidebar.caption("Data source: Nassau Candy Distributor order-level dataset")

# ---------------------------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------------------------
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df_filtered = df[
    (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
    & (df["Division"].isin(selected_divisions))
]

product_filtered = product_summary[product_summary["Division"].isin(selected_divisions)]
product_filtered = product_filtered[product_filtered["Gross Margin %"] >= margin_threshold]
if product_search:
    product_filtered = product_filtered[
        product_filtered["Product Name"].str.contains(product_search, case=False, na=False)
    ]

diagnostics_filtered = diagnostics[diagnostics["Division"].isin(selected_divisions)]
diagnostics_filtered = diagnostics_filtered[diagnostics_filtered["Gross Margin %"] >= margin_threshold]

# ---------------------------------------------------------------------------
# HEADER + TOP-LINE METRICS
# ---------------------------------------------------------------------------
st.title("Product Line Profitability & Margin Performance")
st.caption("Nassau Candy Distributor")

total_sales = df_filtered["Sales"].sum()
total_profit = df_filtered["Gross Profit"].sum()
overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
n_products = product_filtered["Product Name"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Gross Profit", f"${total_profit:,.0f}")
col3.metric("Overall Gross Margin", f"{overall_margin:.2f}%")
col4.metric("Products (filtered)", n_products)

st.markdown("---")

# ---------------------------------------------------------------------------
# TABS = DASHBOARD MODULES
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Product Profitability", "🏭 Division Performance", "⚠️ Cost vs Margin Diagnostics", "📈 Profit Concentration"]
)

# --- TAB 1: PRODUCT PROFITABILITY OVERVIEW ---
with tab1:
    st.subheader("Product-Level Margin Leaderboard")

    if product_filtered.empty:
        st.warning("No products match the current filters.")
    else:
        leaderboard = product_filtered.sort_values("Gross Margin %", ascending=False)
        fig = px.bar(
            leaderboard,
            x="Gross Margin %",
            y="Product Name",
            color="Quadrant",
            orientation="h",
            title="Gross Margin % by Product",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Profit Contribution Breakdown")
        fig2 = px.bar(
            leaderboard.sort_values("Profit Contribution %", ascending=False),
            x="Product Name",
            y="Profit Contribution %",
            color="Division",
            title="Profit Contribution % by Product",
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Quadrant Classification")
        fig3 = px.scatter(
            leaderboard,
            x="Total_Sales",
            y="Gross Margin %",
            color="Quadrant",
            size="Total_Gross_Profit",
            hover_name="Product Name",
            title="Sales vs Margin Quadrant Map",
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.dataframe(
            leaderboard[
                ["Product Name", "Division", "Total_Sales", "Total_Gross_Profit",
                 "Gross Margin %", "Profit per Unit", "Quadrant"]
            ].round(2),
            use_container_width=True,
        )

# --- TAB 2: DIVISION PERFORMANCE DASHBOARD ---
with tab2:
    st.subheader("Revenue vs Profit Share by Division")

    div_filtered = division_summary[division_summary["Division"].isin(selected_divisions)]

    fig4 = go.Figure()
    fig4.add_bar(name="Revenue Share %", x=div_filtered["Division"], y=div_filtered["Revenue Share %"])
    fig4.add_bar(name="Profit Share %", x=div_filtered["Division"], y=div_filtered["Profit Share %"])
    fig4.update_layout(barmode="group", title="Revenue Share vs Profit Share by Division")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Gross Margin % by Division")
    fig5 = px.bar(
        div_filtered, x="Division", y="Gross Margin %", color="Efficiency Flag",
        title="Average Gross Margin % by Division",
        text="Gross Margin %",
    )
    fig5.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Division Summary Table")
    st.dataframe(div_filtered.round(2), use_container_width=True)

# --- TAB 3: COST VS MARGIN DIAGNOSTICS ---
with tab3:
    st.subheader("Cost vs Sales Scatter — Identifying Pricing Inefficiencies")

    if diagnostics_filtered.empty:
        st.warning("No products match the current filters.")
    else:
        fig6 = px.scatter(
            diagnostics_filtered,
            x="Total_Sales",
            y="Total_Cost",
            color="Cost Structure Flag",
            hover_name="Product Name",
            size="Total_Gross_Profit",
            title="Cost vs Sales (color = cost structure flag)",
        )
        max_val = max(diagnostics_filtered["Total_Sales"].max(), diagnostics_filtered["Total_Cost"].max())
        fig6.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                        line=dict(color="gray", dash="dash"))
        st.plotly_chart(fig6, use_container_width=True)

        st.subheader("Margin Risk Flags")
        st.dataframe(
            diagnostics_filtered[
                ["Product Name", "Division", "Cost as % of Sales", "Gross Margin %",
                 "Cost Structure Flag", "Recommended Action"]
            ].sort_values("Cost as % of Sales", ascending=False).round(2),
            use_container_width=True,
        )

        action_counts = diagnostics_filtered["Recommended Action"].value_counts()
        st.subheader("Recommended Actions Summary")
        fig7 = px.pie(values=action_counts.values, names=action_counts.index,
                       title="Distribution of Recommended Actions")
        st.plotly_chart(fig7, use_container_width=True)

# --- TAB 4: PROFIT CONCENTRATION (PARETO) ANALYSIS ---
with tab4:
    st.subheader("Pareto Analysis: Profit Concentration")

    pareto_filtered = pareto[pareto["Division"].isin(selected_divisions)].sort_values(
        "Product Rank %"
    )

    if pareto_filtered.empty:
        st.warning("No products match the current filters.")
    else:
        fig8 = go.Figure()
        fig8.add_bar(
            x=pareto_filtered["Product Name"],
            y=pareto_filtered["Total_Gross_Profit"],
            name="Gross Profit ($)",
        )
        fig8.add_trace(
            go.Scatter(
                x=pareto_filtered["Product Name"],
                y=pareto_filtered["Cumulative Profit %"],
                name="Cumulative Profit %",
                yaxis="y2",
                mode="lines+markers",
                line=dict(color="red"),
            )
        )
        fig8.update_layout(
            title="Pareto Chart: Profit Concentration by Product",
            yaxis=dict(title="Gross Profit ($)"),
            yaxis2=dict(title="Cumulative Profit %", overlaying="y", side="right", range=[0, 110]),
        )
        fig8.add_hline(y=80, yref="y2", line_dash="dash", line_color="gray")
        st.plotly_chart(fig8, use_container_width=True)

        n_for_80 = (pareto_filtered["Cumulative Profit %"] >= 80).idxmax() + 1 if (
            pareto_filtered["Cumulative Profit %"] >= 80
        ).any() else len(pareto_filtered)
        pct_for_80 = n_for_80 / len(pareto_filtered) * 100

        st.info(
            f"**{n_for_80} of {len(pareto_filtered)} products ({pct_for_80:.1f}% of the lineup) "
            f"drive 80% of total profit** — indicating a concentrated, dependency-risk product mix."
        )

        st.dataframe(pareto_filtered.round(2), use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit · Nassau Candy Distributor Product Profitability Analysis")