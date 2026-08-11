# Product Line Profitability & Margin Performance Analysis
### Nassau Candy Distributor

A data-driven analysis identifying which products in Nassau Candy Distributor's catalog actually drive profitability — versus which merely generate sales volume — using one year of order-level transaction data.

**Live Dashboard:** https://dvxgcx8cyqepynmf4rn6tn.streamlit.app

---

##  Project Overview

For distributors, sales volume alone is a misleading measure of business health. This project analyzes 10,194 order-line transactions across 15 products and 3 divisions (Chocolate, Sugar, Other) to answer:

- Which product lines deliver the highest gross margin?
- Are high-sales products actually profitable?
- How does profitability vary across divisions?
- Which products represent margin risk?

##  Key Findings

- **Overall company gross margin: 65.9%** ($141,784 total sales, $93,443 total gross profit)
- **Concentration risk:** 5 of 15 products (33%) drive 80% of both revenue and profit — all from the Chocolate division
- **Structural margin issue:** The "Other" division generates 6.8% of revenue but only 4.6% of profit (44.8% margin vs. 65.9% company average)
- **Weakest performer:** Kazookles converts only 7.7% of sales into profit (92.3% cost-to-sales ratio)
- All identified margin problems trace back to **cost structure**, not pricing strategy

## 🛠️ Methodology

1. **Data Cleaning & Validation** — verified cost/sales integrity, standardized labels
2. **Core KPI Calculation** — Gross Margin %, Profit per Unit, Revenue/Profit Contribution %
3. **Product Quadrant Classification** — High-Profit/High-Margin, High-Sales/Low-Margin (Margin Risk), Low-Sales/High-Margin (Niche), Low-Sales/Low-Profit
4. **Division-Level Performance Analysis** — revenue vs. profit balance by division
5. **Profit Concentration (Pareto) Analysis** — identifying dependency risk
6. **Cost Structure Diagnostics** — flagging products for cost renegotiation, repricing, or discontinuation review

##  Repository Structure

```
nassau-candy-margin-analysis/
├── app.py                          # Streamlit dashboard application
├── requirements.txt                # Python dependencies
├── outputs/                        # Cleaned data & analysis outputs
│   ├── cleaned_transactions.csv
│   ├── product_kpi_summary_with_quadrants.csv
│   ├── division_summary.csv
│   ├── pareto_analysis.csv
│   └── cost_structure_diagnostics.csv
├── Nassau_Candy_Profitability_Research_Paper.docx
├── Nassau_Candy_Executive_Summary.docx
└── Nassau_Candy_Margin_Analysis.pbix   # Power BI dashboard
```

##  Deliverables

| Deliverable | Description |
|---|---|
| **Streamlit Dashboard** | Live, interactive dashboard with 4 modules: Product Profitability, Division Performance, Cost vs Margin Diagnostics, Profit Concentration |
| **Power BI Dashboard** | Parallel BI dashboard mirroring the same KPIs, built with 10 custom DAX measures |
| **Research Paper** | Full EDA, methodology, findings, and prioritized recommendations |
| **Executive Summary** | One-page stakeholder brief leading with business impact |

##  Running the Dashboard Locally

```bash
git clone https://github.com/pramodkale100/nassau-candy-margin-analysis.git
cd nassau-candy-margin-analysis
pip install -r requirements.txt
streamlit run app.py
```

##  Recommendations

1. **Cost renegotiation (High priority)** — 7 products flagged, starting with Kazookles
2. **Discontinuation review (Medium priority)** — 4 low-sales/low-profit products contributing under $90 combined annual profit
3. **Diversify supply risk (Medium priority)** — reduce dependency on the concentrated Chocolate product line
4. **Protect the core line (Ongoing)** — prioritize inventory and supply chain reliability for top Chocolate products

---

**Author:** Pramod Kale
**Program:** Data Analyst Fellowship — Unified Mentor
**Tools:** Python (pandas, matplotlib), Streamlit, Power BI, DAX
