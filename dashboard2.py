import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Elis Danmark - Customer Review & NLP Dashboard",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            background-color: #fafbfc;
        }

        .kpi-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            text-align: center;
        }

        .risk-card {
            padding: 16px;
            border-radius: 10px;
            margin-bottom: 12px;
            color: white;
            font-family: sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        .risk-high {
            background: linear-gradient(135deg, #ef4444 0%, #991b1b 100%);
            border-left: 6px solid #7f1d1d;
        }

        .risk-medium {
            background: linear-gradient(135deg, #eab308 0%, #854d0e 100%);
            border-left: 6px solid #713f12;
        }

        .risk-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 4px;
        }

        .risk-meta {
            font-size: 13px;
            opacity: 0.95;
            line-height: 1.4;
        }

        .executive-note {
            background-color: #f0fdf4;
            border: 1px solid #bbf7d0;
            padding: 15px;
            border-radius: 8px;
            color: #166534;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONSTANTS
# ============================================================

PRIMARY_DATASET = "trustpilot_elis_analyzed.csv"
FALLBACK_DATASET = "trustpilot_elis_reviews_all.csv"

STOPWORDS = {
    "og", "i", "jeg", "det", "at", "en", "den", "til", "er", "som",
    "på", "de", "med", "han", "af", "for", "ikke", "der", "var",
    "mig", "seg", "men", "et", "har", "om", "vi", "min", "hadde",
    "fra", "ud", "da", "særdeles", "kan", "så", "være", "dem",
    "os", "blive", "eller", "and", "the", "to", "a", "of", "in",
    "is", "that", "it", "you", "was", "with", "on", "as", "have",
    "but", "be", "they", "we", "elis", "dk", "com",
    "star", "stjerne", "stjerner",
}


# ============================================================
# CATEGORY DETECTION
# ============================================================

def calculate_dynamic_category(text):
    """Classify a customer review into an operational category."""

    if not isinstance(text, str) or not text.strip():
        return "General Operations"

    text_lower = text.lower()

    if any(
        keyword in text_lower
        for keyword in [
            "binding",
            "opsigelse",
            "kontrakt",
            "cancellation",
            "bindingstid",
            "aftale",
        ]
    ):
        return "Binding / Contract Issues"

    if any(
        keyword in text_lower
        for keyword in [
            "fatura",
            "regning",
            "priser",
            "invoice",
            "finance",
            "penge",
            "gebyr",
            "pris",
        ]
    ):
        return "Finance / Price & Billing"

    if any(
        keyword in text_lower
        for keyword in [
            "iletişim",
            "telefon",
            "svar",
            "kontakt",
            "customer service",
            "kundeservice",
            "mail",
            "support",
        ]
    ):
        return "Communication / Support"

    if any(
        keyword in text_lower
        for keyword in [
            "teslimat",
            "levering",
            "chauffør",
            "transport",
            "delivery",
            "tøj",
            "missing",
            "lost",
        ]
    ):
        return "Transport / Logistics"

    return "General Operations"


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    """Load and prepare the review dataset."""

    try:
        if Path(PRIMARY_DATASET).exists():
            df = pd.read_csv(PRIMARY_DATASET)
        elif Path(FALLBACK_DATASET).exists():
            df = pd.read_csv(FALLBACK_DATASET)
        else:
            st.error(
                f"Could not find either dataset:\n"
                f"- {PRIMARY_DATASET}\n"
                f"- {FALLBACK_DATASET}"
            )
            return None

        # Normalize response column.
        if "Sirket_Cevabi" in df.columns and "Cevap" not in df.columns:
            df = df.rename(columns={"Sirket_Cevabi": "Cevap"})

        # Normalize rating.
        if "Yildiz_Sayisi" not in df.columns:
            st.error("Dataset is missing the 'Yildiz_Sayisi' column.")
            return None

        df["Yildiz_Sayisi"] = pd.to_numeric(
            df["Yildiz_Sayisi"],
            errors="coerce",
        )

        # Create integer rating used by filters.
        df["Yildiz_Int"] = (
            df["Yildiz_Sayisi"]
            .fillna(0)
            .round()
            .astype(int)
        )

        # Find and normalize date column.
        date_columns = [
            "Tarih",
            "Yorum_Tarihi",
            "Date",
            "date",
        ]

        for date_col in date_columns:
            if date_col in df.columns:
                parsed_dates = pd.to_datetime(
                    df[date_col],
                    errors="coerce",
                    dayfirst=True,
                )

                df["_parsed_date"] = parsed_dates
                df = df.sort_values(
                    "_parsed_date",
                    ascending=False,
                    na_position="last",
                )

                # Keep original date display readable.
                df[date_col] = parsed_dates.dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                break

        # Identify review/comment column.
        comment_candidates = [
            "Musteri_Yorumu",
            "Yorum",
            "Cevap",
        ]

        comment_col = next(
            (
                column
                for column in comment_candidates
                if column in df.columns
            ),
            None,
        )

        if comment_col:
            df["Tespit_Edilen_Problem"] = df[
                comment_col
            ].apply(calculate_dynamic_category)
        else:
            df["Tespit_Edilen_Problem"] = "General Operations"

        return df.reset_index(drop=True)

    except Exception as error:
        st.error(f"Error loading dataset: {error}")
        return None


# ============================================================
# SIDEBAR FILTERS
# ============================================================

def render_sidebar():
    """Render dashboard filtering controls."""

    st.sidebar.title("🔍 Filter Controls")

    st.sidebar.write("### Filter by Rating")

    selected_stars = []

    for star in range(1, 6):
        if st.sidebar.checkbox(
            f"{star} ★ Reviews",
            value=True,
            key=f"star_pick_{star}",
        ):
            selected_stars.append(star)

    search_query = st.sidebar.text_input(
        "Keyword Search in Reviews",
        placeholder="Search terms...",
    )

    st.sidebar.markdown("---")

    st.sidebar.caption(
        "Use the filters above to dynamically update "
        "KPIs, charts, risk analysis and feedback."
    )

    return selected_stars, search_query


# ============================================================
# FILTER DATA
# ============================================================

def apply_filters(df, selected_stars, search_query):
    """Apply rating and keyword filters."""

    filtered_df = df[
        df["Yildiz_Int"].isin(selected_stars)
    ].copy()

    if search_query:
        comment_candidates = [
            "Musteri_Yorumu",
            "Yorum",
            "Cevap",
        ]

        comment_col = next(
            (
                column
                for column in comment_candidates
                if column in filtered_df.columns
            ),
            None,
        )

        if comment_col:
            filtered_df = filtered_df[
                filtered_df[comment_col]
                .fillna("")
                .astype(str)
                .str.contains(
                    search_query,
                    case=False,
                    na=False,
                )
            ]

    return filtered_df


# ============================================================
# KPI CARD
# ============================================================

def render_kpi(title, value, color="#0f172a", border_color=None):
    """Render a reusable KPI card."""

    border_style = (
        f"border-top: 4px solid {border_color};"
        if border_color
        else ""
    )

    st.markdown(
        f"""
        <div class="kpi-container" style="{border_style}">
            <span style="
                color:#64748b;
                font-size:14px;
                font-weight:600;
            ">
                {title}
            </span>

            <div style="
                font-size:32px;
                font-weight:bold;
                color:{color};
                margin-top:5px;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RISK CARD
# ============================================================

def render_risk_card(
    title,
    severity,
    description,
    risk_level="high",
):
    """Render an operational risk card."""

    css_class = (
        "risk-high"
        if risk_level.lower() == "high"
        else "risk-medium"
    )

    st.markdown(
        f"""
        <div class="risk-card {css_class}">
            <div class="risk-title">
                {title} — {risk_level.upper()} RISK
            </div>

            <div class="risk-meta">
                <strong>Severity:</strong> {severity}/100<br>
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HTML EXPORT
# ============================================================

def generate_html_report(
    filtered_df,
    bad_df,
    good_df,
    total_reviews,
    average_rating,
):
    """Generate a standalone HTML dashboard."""

    categories = [
        "Lost Items / Textiles",
        "Support & Communication",
        "Finance / Pricing",
    ]

    scores = [90, 85, 45]

    bad_counts = (
        bad_df["Tespit_Edilen_Problem"]
        .value_counts()
        if not bad_df.empty
        else pd.Series(dtype=int)
    )

    good_counts = (
        good_df["Tespit_Edilen_Problem"]
        .value_counts()
        if not good_df.empty
        else pd.Series(dtype=int)
    )

    # Escape text before injecting review content into HTML.
    rows_html = ""

    comment_candidates = [
        "Musteri_Yorumu",
        "Yorum",
        "Cevap",
    ]

    comment_col = next(
        (
            column
            for column in comment_candidates
            if column in filtered_df.columns
        ),
        None,
    )

    if comment_col:
        export_df = (
            filtered_df[
                filtered_df[comment_col]
                .fillna("")
                .astype(str)
                .str.strip()
                .ne("")
            ]
            .drop_duplicates(subset=[comment_col])
            .head(100)
        )

        for _, row in export_df.iterrows():
            date_value = row.get(
                "Tarih",
                row.get("Yorum_Tarihi", "N/A"),
            )

            name_value = row.get("Isim", "Anonymous")
            rating_value = row.get("Yildiz_Sayisi", 0)
            category_value = row.get(
                "Tespit_Edilen_Problem",
                "General Operations",
            )
            comment_value = row.get(comment_col, "")

            rows_html += f"""
            <tr>
                <td>{html.escape(str(date_value))}</td>
                <td>{html.escape(str(name_value))}</td>
                <td>{html.escape(str(rating_value))} ★</td>
                <td>{html.escape(str(category_value))}</td>
                <td>{html.escape(str(comment_value))}</td>
            </tr>
            """

    bad_labels = [
        str(label)
        for label in bad_counts.index.tolist()
    ]

    bad_values = [
        int(value)
        for value in bad_counts.values.tolist()
    ]

    good_labels = [
        str(label)
        for label in good_counts.index.tolist()
    ]

    good_values = [
        int(value)
        for value in good_counts.values.tolist()
    ]

    import json

    bad_labels_json = json.dumps(bad_labels)
    bad_values_json = json.dumps(bad_values)
    good_labels_json = json.dumps(good_labels)
    good_values_json = json.dumps(good_values)

    categories_json = json.dumps(categories)
    scores_json = json.dumps(scores)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Elis Danmark - Premium VoC Report</title>

    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                sans-serif;

            background: #f0f2f5;
            color: #1e293b;
            padding: 40px;
            margin: 0;
        }}

        .container {{
            max-width: 1400px;
            margin: auto;
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        }}

        .header-banner {{
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .header-banner h1 {{
            margin-bottom: 8px;
        }}

        .header-banner p {{
            color: #64748b;
        }}

        .kpi-row {{
            display: grid;
            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 25px;
            margin-bottom: 35px;
        }}

        .kpi {{
            text-align: center;
            background:
                linear-gradient(
                    135deg,
                    #ffffff 0%,
                    #f8fafc 100%
                );

            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
        }}

        .kpi-label {{
            color: #64748b;
            font-size: 13px;
            font-weight: 600;
        }}

        .kpi-val {{
            font-size: 28px;
            color: #0284c7;
            margin-top: 5px;
            font-weight: bold;
        }}

        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 35px;
            margin-top: 25px;
        }}

        .card {{
            background: #fff;
            border: 1px solid #e2e8f0;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }}

        .risk {{
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 12px;
            color: white;
        }}

        .risk-high {{
            background:
                linear-gradient(
                    135deg,
                    #ef4444,
                    #991b1b
                );
        }}

        .risk-medium {{
            background:
                linear-gradient(
                    135deg,
                    #eab308,
                    #854d0e
                );
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 25px;
        }}

        th,
        td {{
            padding: 14px;
            border-bottom: 1px solid #e2e8f0;
            text-align: left;
            font-size: 13px;
        }}

        th {{
            background: #f8fafc;
            font-weight: 600;
            color: #475569;
        }}

        tr:hover {{
            background-color: #f8fafc;
        }}

        @media (max-width: 900px) {{
            body {{
                padding: 15px;
            }}

            .container {{
                padding: 20px;
            }}

            .kpi-row,
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>

<body>

<div class="container">

    <div class="header-banner">
        <h1>
            📊 Elis Danmark —
            Executive Voice of Customer Report
        </h1>

        <p>
            Chronological customer review analysis
            and operational risk dashboard.
        </p>
    </div>

    <div class="kpi-row">

        <div class="kpi">
            <div class="kpi-label">TOTAL DATA POOL</div>
            <div class="kpi-val">
                {total_reviews}
            </div>
        </div>

        <div class="kpi">
            <div class="kpi-label">SATISFACTION SCORE</div>
            <div class="kpi-val">
                {average_rating:.2f} / 5.0
            </div>
        </div>

        <div class="kpi">
            <div class="kpi-label">CRITICAL GRIEVANCES</div>
            <div class="kpi-val" style="color:#dc2626;">
                {len(bad_df)}
            </div>
        </div>

        <div class="kpi">
            <div class="kpi-label">PROMOTER REVIEWS</div>
            <div class="kpi-val" style="color:#16a34a;">
                {len(good_df)}
            </div>
        </div>

    </div>

    <h2>📋 Operational Severity Diagnostics</h2>

    <div class="grid">

        <div class="card">
            <h3>Business Risk Assessment</h3>

            <div class="risk risk-high">
                <strong>
                    Lost Items / Textiles — HIGH RISK
                </strong>

                <br>
                Severity: 90/100

                <p>
                    Gaps in laundry tracking and
                    barcode scan discipline.
                </p>
            </div>

            <div class="risk risk-high">
                <strong>
                    Support & Communication — HIGH RISK
                </strong>

                <br>
                Severity: 85/100

                <p>
                    Long telephone queues and
                    delayed email responses.
                </p>
            </div>

            <div class="risk risk-medium">
                <strong>
                    Finance / Pricing — MEDIUM RISK
                </strong>

                <br>
                Severity: 45/100

                <p>
                    Periodic pricing and
                    indexation friction.
                </p>
            </div>
        </div>

        <div class="card">
            <div id="riskMatrixChart"
                 style="width:100%; height:400px;">
            </div>
        </div>

    </div>

    <div class="grid">

        <div class="card">
            <div id="badPieChart"
                 style="width:100%; height:420px;">
            </div>
        </div>

        <div class="card">
            <div id="goodPieChart"
                 style="width:100%; height:420px;">
            </div>
        </div>

    </div>

    <h2>
        📋 Cleaned Chronological Feedback Feed
    </h2>

    <div class="card">

        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Customer</th>
                    <th>Rating</th>
                    <th>Category</th>
                    <th>Comment</th>
                </tr>
            </thead>

            <tbody>
                {rows_html}
            </tbody>
        </table>

    </div>

</div>

<script>

const badLabels = {bad_labels_json};
const badValues = {bad_values_json};

const goodLabels = {good_labels_json};
const goodValues = {good_values_json};

const categories = {categories_json};
const scores = {scores_json};


Plotly.newPlot(
    "badPieChart",
    [{{
        values: badValues,
        labels: badLabels,
        type: "pie",
        hole: 0.35,
        marker: {{
            colors: [
                "#4c0519",
                "#881337",
                "#9f1239",
                "#be123c",
                "#e11d48",
                "#f43f5e"
            ]
        }}
    }}],
    {{
        title: {{
            text: "🔴 Complaints Distribution (1–2 Stars)"
        }},
        margin: {{
            t: 50,
            b: 20
        }}
    }},
    {{
        responsive: true
    }}
);


Plotly.newPlot(
    "goodPieChart",
    [{{
        values: goodValues,
        labels: goodLabels,
        type: "pie",
        hole: 0.35,
        marker: {{
            colors: [
                "#064e3b",
                "#065f46",
                "#0f766e",
                "#115e59",
                "#14b8a6",
                "#2dd4bf"
            ]
        }}
    }}],
    {{
        title: {{
            text: "🟢 Satisfaction Drivers (4–5 Stars)"
        }},
        margin: {{
            t: 50,
            b: 20
        }}
    }},
    {{
        responsive: true
    }}
);


Plotly.newPlot(
    "riskMatrixChart",
    [{{
        x: scores,
        y: categories,
        type: "bar",
        orientation: "h",

        marker: {{
            color: [
                "#b91c1c",
                "#dc2626",
                "#eab308"
            ],

            line: {{
                color: "#0f172a",
                width: 1
            }}
        }},

        text: scores.map(
            value => `${{value}}/100`
        ),

        textposition: "inside"
    }}],

    {{
        title: {{
            text: "Business Area Threat Index"
        }},

        xaxis: {{
            range: [0, 100],
            title: "Severity Score",
            gridcolor: "#e2e8f0"
        }},

        yaxis: {{
            autorange: "reversed"
        }},

        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",

        margin: {{
            t: 60,
            b: 50,
            l: 160
        }}
    }},

    {{
        responsive: true
    }}
);

</script>

</body>
</html>
"""


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    df = load_data()

    if df is None or df.empty:
        st.warning("No review data is available.")
        st.stop()

    selected_stars, search_query = render_sidebar()

    filtered_df = apply_filters(
        df,
        selected_stars,
        search_query,
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "📊 Elis Danmark — Executive Voice of Customer Dashboard"
    )

    st.caption(
        "Automated customer review analytics, "
        "operational risk detection and NLP categorization."
    )

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_reviews = len(filtered_df)

    average_rating = (
        filtered_df["Yildiz_Sayisi"].mean()
        if total_reviews > 0
        else 0
    )

    bad_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] <= 2
    ].copy()

    good_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] >= 4
    ].copy()

    # ========================================================
    # KPI SECTION
    # ========================================================

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        render_kpi(
            "TOTAL DATA POOL",
            total_reviews,
        )

    with k2:
        render_kpi(
            "SATISFACTION SCORE",
            f"{average_rating:.2f} / 5.0",
            color="#0284c7",
        )

    with k3:
        render_kpi(
            "CRITICAL GRIEVANCES",
            len(bad_df),
            color="#991b1b",
            border_color="#ef4444",
        )

    with k4:
        render_kpi(
            "PROMOTER REVIEWS",
            len(good_df),
            color="#166534",
            border_color="#22c55e",
        )

    st.markdown("---")

    # ========================================================
    # STRATEGIC FINDINGS
    # ========================================================

    st.header(
        "1. Core Strategic Findings & Root Cause Analysis"
    )

    c_neg, c_pos = st.columns(2)

    with c_neg:
        st.error(
            "🔴 Top Customer Grievances "
            "(1–2 Star Reviews)"
        )

        st.markdown(
            """
            - **Logistics & Lost Textiles:** Missing garments
              in wash lines.
            - **Customer Service:** Long telephone hold queues.
            - **Billing & Pricing:** Customer friction around
              prices and charges.
            """
        )

    with c_pos:
        st.success(
            "🟢 Key Drivers of Satisfaction "
            "(4–5 Star Reviews)"
        )

        st.markdown(
            """
            - **Driver Demeanor:** Friendly and polite route
              personnel.
            - **Integrity:** Secure return of found valuables.
            - **Service Reliability:** Positive experiences
              with regular deliveries.
            """
        )

    st.markdown("---")

    # ========================================================
    # CATEGORY BREAKDOWN
    # ========================================================

    st.header(
        "2. Core Problem Breakdown by Category"
    )

    cb_pie, cg_pie = st.columns(2)

    with cb_pie:

        if not bad_df.empty:

            fig_bad = px.pie(
                bad_df,
                names="Tespit_Edilen_Problem",
                title=(
                    "Complaints Distribution "
                    "(1–2 Stars)"
                ),
                hole=0.4,
                color_discrete_sequence=(
                    px.colors.sequential.Sunsetdark
                ),
            )

            fig_bad.update_layout(
                margin=dict(
                    t=50,
                    b=10,
                    l=10,
                    r=10,
                )
            )

            st.plotly_chart(
                fig_bad,
                use_container_width=True,
            )

        else:
            st.info(
                "No 1–2 star reviews match the current filters."
            )

    with cg_pie:

        if not good_df.empty:

            fig_good = px.pie(
                good_df,
                names="Tespit_Edilen_Problem",
                title=(
                    "Satisfaction Drivers "
                    "(4–5 Stars)"
                ),
                hole=0.4,
                color_discrete_sequence=(
                    px.colors.sequential.Viridis
                ),
            )

            fig_good.update_layout(
                margin=dict(
                    t=50,
                    b=10,
                    l=10,
                    r=10,
                )
            )

            st.plotly_chart(
                fig_good,
                use_container_width=True,
            )

        else:
            st.info(
                "No 4–5 star reviews match the current filters."
            )

    st.markdown("---")

    # ========================================================
    # RISK MATRIX
    # ========================================================

    st.header(
        "3. Operational Risk Level Assessment Matrix"
    )

    c_mat, c_card = st.columns(2)

    categories = [
        "Lost Items / Textiles",
        "Support & Communication",
        "Finance / Pricing",
    ]

    scores = [90, 85, 45]

    with c_mat:

        fig_matrix = go.Figure(
            go.Bar(
                x=scores,
                y=categories,
                orientation="h",
                marker=dict(
                    color=[
                        "#b91c1c",
                        "#dc2626",
                        "#eab308",
                    ],
                    line=dict(
                        color="#1e293b",
                        width=1.5,
                    ),
                ),
                text=[
                    f"Severity: {score}/100"
                    for score in scores
                ],
                textposition="inside",
                textfont=dict(
                    color="white",
                ),
            )
        )

        fig_matrix.update_layout(
            xaxis=dict(
                title="Severity Score",
                range=[0, 100],
                gridcolor="#e2e8f0",
            ),
            yaxis=dict(
                autorange="reversed",
            ),
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                t=20,
                b=40,
                l=150,
            ),
        )

        st.plotly_chart(
            fig_matrix,
            use_container_width=True,
        )

    with c_card:

        render_risk_card(
            "Lost Items / Textiles",
            90,
            "Gaps in laundry tracking and barcode scan discipline.",
            "high",
        )

        render_risk_card(
            "Support & Communication",
            85,
            "Long telephone queues and delayed email responses.",
            "high",
        )

        render_risk_card(
            "Finance / Pricing",
            45,
            "Periodic pricing and indexation friction.",
            "medium",
        )

    st.markdown("---")

    # ========================================================
    # CUSTOMER FEEDBACK
    # ========================================================

    st.header(
        "4. Recent Customer Raw Feedback"
    )

    comment_candidates = [
        "Musteri_Yorumu",
        "Yorum",
        "Cevap",
    ]

    comment_col = next(
        (
            column
            for column in comment_candidates
            if column in filtered_df.columns
        ),
        None,
    )

    if comment_col:

        clean_feed_df = (
            filtered_df[
                filtered_df[comment_col]
                .fillna("")
                .astype(str)
                .str.strip()
                .ne("")
            ]
            .loc[
                lambda data: ~data[comment_col]
                .str.contains(
                    "Belirtilmedi|Cevap Yok",
                    case=False,
                    na=False,
                )
            ]
            .drop_duplicates(
                subset=[comment_col]
            )
            .copy()
        )

        display_columns = [
            column
            for column in [
                "Tarih",
                "Yorum_Tarihi",
                "Isim",
                "Yildiz_Sayisi",
                "Tespit_Edilen_Problem",
                comment_col,
            ]
            if column in clean_feed_df.columns
        ]

        st.dataframe(
            clean_feed_df[
                display_columns
            ].head(50),
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.warning(
            "No customer review/comment column was found."
        )

    st.markdown("---")

    # ========================================================
    # EXPORT
    # ========================================================

    st.header(
        "💾 Export Full Dashboard as Interactive HTML"
    )

    st.caption(
        "Generate a standalone HTML report containing "
        "KPIs, Plotly charts, operational risk analysis "
        "and the customer feedback table."
    )

    html_payload = generate_html_report(
        filtered_df=filtered_df,
        bad_df=bad_df,
        good_df=good_df,
        total_reviews=total_reviews,
        average_rating=average_rating,
    )

    st.download_button(
        label=(
            "📥 Download Complete Premium "
            "Interactive HTML Dashboard"
        ),
        data=html_payload,
        file_name="elis_danmark_premium_dashboard.html",
        mime="text/html",
        use_container_width=True,
    )

    # ========================================================
    # EMPTY FILTER WARNING
    # ========================================================

    if filtered_df.empty:
        st.warning(
            "No reviews match the current filters. "
            "Try selecting additional star ratings "
            "or clearing the keyword search."
        )


# ============================================================
# APPLICATION ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()
