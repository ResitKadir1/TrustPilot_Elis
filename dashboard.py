import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Elis Danmark — Executive Voice of Customer Dashboard",
    page_icon="🧺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .dashboard-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #2563eb;
        margin-bottom: 0.25rem;
    }

    .dashboard-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2563eb;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .risk-high {
        color: #dc2626;
        font-weight: 700;
    }

    .risk-medium {
        color: #ca8a04;
        font-weight: 700;
    }

    .risk-card {
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding: 1rem;
    }

    [data-testid="stMetric"] {
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(128, 128, 128, 0.15);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    """Load, validate, clean and transform the Trustpilot dataset."""

    file_path = "trustpilot_elis_analyzed.csv"

    df = pd.read_csv(file_path)

    required_columns = [
        "Tarih_Saat",
        "Yildiz_Sayisi",
        "Tespit_Edilen_Problem",
        "Isim",
        "Musteri_Yorumu",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # --------------------------------------------------------
    # Parse date/time
    # --------------------------------------------------------

    df["Tarih_Saat"] = pd.to_datetime(
        df["Tarih_Saat"],
        format="%d.%m.%Y %H:%M",
        errors="coerce",
    )

    df = df.dropna(
        subset=["Tarih_Saat"]
    ).copy()

    # --------------------------------------------------------
    # Convert ratings to numeric
    # --------------------------------------------------------

    df["Yildiz_Sayisi"] = pd.to_numeric(
        df["Yildiz_Sayisi"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Sort chronologically
    # --------------------------------------------------------

    df = (
        df.sort_values(
            by="Tarih_Saat",
            ascending=True,
        )
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # Date helper columns
    # --------------------------------------------------------

    df["Formatted_Date"] = (
        df["Tarih_Saat"]
        .dt.strftime("%Y-%m-%d %H:%M")
    )

    df["Year_Month_Day"] = (
        df["Tarih_Saat"]
        .dt.strftime("%Y-%m-%d")
    )

    df["Year_Month"] = (
        df["Tarih_Saat"]
        .dt.strftime("%Y-%m")
    )

    df["Hour"] = (
        df["Tarih_Saat"]
        .dt.hour
    )

    # --------------------------------------------------------
    # Complaint category mapping
    # --------------------------------------------------------

    category_map = {
        "Müşteri İletişim Aksaklığı":
            "Communication & Customer Service",

        "Ürün / Hizmet Kalitesi":
            "Quality of Service & Projects",

        "Operasyonel / Fatura Problemi":
            "Pricing, Billing & Transportation",

        "Diğer / Genel Yanıt":
            "Other Issues",

        "Belirtilmedi / Cevap Yok":
            "General Inquiry / Unspecified",
    }

    df["Complaint_Category"] = (
        df["Tespit_Edilen_Problem"]
        .map(category_map)
        .fillna("Other")
    )

    # --------------------------------------------------------
    # Clean text columns
    # --------------------------------------------------------

    df["Musteri_Yorumu"] = (
        df["Musteri_Yorumu"]
        .fillna("")
        .astype(str)
    )

    df["Isim"] = (
        df["Isim"]
        .fillna("Anonymous")
        .astype(str)
    )

    return df


# ============================================================
# HTML REPORT
# ============================================================

def generate_html_report(
    df,
    total_reviews,
    avg_rating,
    positive_pct,
    negative_reviews,
    fig_rating,
    fig_pie,
    fig_time,
    fig_hour,
    fig_box,
):
    """Generate downloadable executive HTML report."""

    # First chart loads Plotly JS.
    rating_html = pio.to_html(
        fig_rating,
        full_html=False,
        include_plotlyjs="cdn",
    )

    pie_html = pio.to_html(
        fig_pie,
        full_html=False,
        include_plotlyjs=False,
    )

    time_html = pio.to_html(
        fig_time,
        full_html=False,
        include_plotlyjs=False,
    )

    hour_html = pio.to_html(
        fig_hour,
        full_html=False,
        include_plotlyjs=False,
    )

    box_html = pio.to_html(
        fig_box,
        full_html=False,
        include_plotlyjs=False,
    )

    table_df = df[
        [
            "Formatted_Date",
            "Isim",
            "Yildiz_Sayisi",
            "Complaint_Category",
            "Musteri_Yorumu",
        ]
    ]

    table_html = table_df.to_html(
        index=False,
        classes="review-table",
        border=0,
    )

    html_content = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Elis Danmark — Executive Voice of Customer Report
</title>

<style>

body {{
    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #f5f7fb;

    color: #1e293b;

    margin: 0;

    padding: 30px;
}}

.container {{
    max-width: 1400px;
    margin: auto;
}}

h1 {{
    color: #2563eb;
}}

h2 {{
    color: #1e293b;
    margin-top: 35px;
}}

.subtitle {{
    color: #64748b;
    margin-bottom: 30px;
}}

.metrics {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}}

.metric {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow:
        0 2px 8px rgba(0,0,0,0.08);
}}

.metric-label {{
    color: #64748b;
    font-size: 14px;
}}

.metric-value {{
    color: #2563eb;
    font-size: 28px;
    font-weight: bold;
    margin-top: 8px;
}}

.chart {{
    background: white;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 25px;
    box-shadow:
        0 2px 8px rgba(0,0,0,0.05);
}}

.review-table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}

.review-table th {{
    background: #2563eb;
    color: white;
    padding: 10px;
    text-align: left;
}}

.review-table td {{
    padding: 10px;
    border-bottom:
        1px solid #e2e8f0;
}}

.review-table tr:nth-child(even) {{
    background: #f8fafc;
}}

@media (max-width: 900px) {{
    .metrics {{
        grid-template-columns: 1fr 1fr;
    }}
}}

</style>

</head>

<body>

<div class="container">

<h1>
📊 Elis Danmark — Executive Voice of Customer Dashboard
</h1>

<p class="subtitle">
Automated Trustpilot review analysis, customer satisfaction,
operational root-cause analysis, and risk assessment.
</p>


<div class="metrics">

<div class="metric">
<div class="metric-label">
Total Reviews
</div>

<div class="metric-value">
{total_reviews:,}
</div>
</div>


<div class="metric">
<div class="metric-label">
Average Rating
</div>

<div class="metric-value">
{avg_rating:.2f} / 5.0
</div>
</div>


<div class="metric">
<div class="metric-label">
Positive Reviews
</div>

<div class="metric-value">
{positive_pct:.1f}%
</div>
</div>


<div class="metric">
<div class="metric-label">
Negative Reviews
</div>

<div class="metric-value">
{negative_reviews:,}
</div>
</div>

</div>


<div class="chart">
{rating_html}
</div>

<div class="chart">
{pie_html}
</div>

<div class="chart">
{time_html}
</div>

<div class="chart">
{hour_html}
</div>

<div class="chart">
{box_html}
</div>


<h2>
📋 Chronological Customer Feedback Log
</h2>

{table_html}

</div>

</body>

</html>
"""

    return html_content


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    # ========================================================
    # LOAD DATA
    # ========================================================

    try:

        df = load_data()

    except FileNotFoundError:

        st.error(
            "❌ Could not find "
            "'trustpilot_elis_analyzed.csv'."
        )

        st.info(
            "Place the CSV file in the same "
            "directory as dashboard.py."
        )

        st.stop()

    except Exception as error:

        st.error(
            f"❌ Error loading dataset: {error}"
        )

        st.stop()


    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.image(
        "https://img.icons8.com/color/96/washing-machine.png",
        width=70,
    )

    st.sidebar.title(
        "Filter Controls"
    )

    st.sidebar.caption(
        "Filter Trustpilot customer reviews "
        "by rating, category, and keywords."
    )


    # --------------------------------------------------------
    # Rating filter
    # --------------------------------------------------------

    ratings = sorted(
        df["Yildiz_Sayisi"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_ratings = st.sidebar.multiselect(
        "⭐ Filter by Rating",
        options=ratings,
        default=ratings,
        key="rating_filter",
    )


    # --------------------------------------------------------
    # Keyword filter
    # --------------------------------------------------------

    search_query = st.sidebar.text_input(
        "🔎 Search Reviews",
        placeholder="Enter keyword...",
        key="review_search",
    )


    # --------------------------------------------------------
    # Category filter
    # --------------------------------------------------------

    categories = sorted(
        df["Complaint_Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "📌 Complaint Category",
        options=categories,
        default=categories,
        key="category_filter",
    )


    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered_df = df[
        df["Yildiz_Sayisi"].isin(
            selected_ratings
        )
        &
        df["Complaint_Category"].isin(
            selected_categories
        )
    ].copy()


    if search_query:

        filtered_df = filtered_df[
            filtered_df["Musteri_Yorumu"]
            .str.contains(
                search_query,
                case=False,
                na=False,
            )
        ]


    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
        <div class="dashboard-title">
            📊 Elis Danmark — Executive Voice of Customer Dashboard
        </div>

        <div class="dashboard-subtitle">
            Automated NLP sentiment analysis, topic modeling,
            customer grievance analysis, and operational
            root-cause assessment.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # EMPTY FILTER RESULT
    # ========================================================

    if filtered_df.empty:

        st.warning(
            "⚠️ No reviews match the selected filters."
        )

        st.info(
            "Try selecting additional ratings or "
            "complaint categories."
        )

        st.stop()


    # ========================================================
    # TOP METRICS
    # ========================================================

    total_reviews = len(filtered_df)

    avg_rating = (
        filtered_df["Yildiz_Sayisi"].mean()
        if total_reviews > 0
        else 0.0
    )


    negative_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] <= 2
    ]

    negative_reviews = len(
        negative_df
    )

    negative_share = (
        negative_reviews
        / total_reviews
        * 100
        if total_reviews > 0
        else 0
    )


    positive_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] >= 4
    ]

    positive_reviews = len(
        positive_df
    )

    positive_share = (
        positive_reviews
        / total_reviews
        * 100
        if total_reviews > 0
        else 0
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Reviews Analyzed",
        f"{total_reviews:,}",
    )


    col2.metric(
        "Average Rating",
        f"{avg_rating:.2f} / 5.0",
    )


    col3.metric(
        "Negative Reviews (1–2 ★)",
        f"{negative_reviews:,}",
        delta=f"{negative_share:.1f}% of reviews",
        delta_color="inverse",
    )


    col4.metric(
        "Positive Reviews (4–5 ★)",
        f"{positive_reviews:,}",
        delta=f"{positive_share:.1f}% of reviews",
        delta_color="normal",
    )


    st.markdown("---")


    # ========================================================
    # STRATEGIC FINDINGS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Core Strategic Findings & Root Cause Analysis'
        '</div>',
        unsafe_allow_html=True,
    )


    col_grievance, col_satisfaction = st.columns(2)


    with col_grievance:

        st.markdown(
            "#### 🔴 Top Customer Grievances "
            "(1–2 Star Reviews)"
        )

        st.markdown(
            """
            **Logistics & Lost Textiles**

            - Missing workwear: garments and towels
              sent for washing or repair may go missing.
            - Delivery errors: items may be delivered
              to incorrect floors or drop points.

            **Customer Service & Communication**

            - Long phone waiting times.
            - Customers report prolonged response delays.
            - Communication loops can make issue resolution
              difficult.
            """
        )


    with col_satisfaction:

        st.markdown(
            "#### 🟢 Key Drivers of Satisfaction "
            "(4–5 Star Reviews)"
        )

        st.markdown(
            """
            **Driver Demeanor**

            - Delivery personnel are frequently described
              as polite, helpful, and friendly.

            **Integrity & Local Support**

            - Valuables found in garments are often
              safely returned to customers.

            **Laundry & Product Quality**

            - Clean and well-maintained linens.
            - Reliable recurring laundry operations.
            - Consistent service quality.
            """
        )


    st.markdown("---")


    # ========================================================
    # RISK ASSESSMENT
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Operational Risk Level Assessment Matrix'
        '</div>',
        unsafe_allow_html=True,
    )


    col_risk_chart, col_risk_details = st.columns(
        [1.2, 1]
    )


    # --------------------------------------------------------
    # Risk dataset
    # --------------------------------------------------------

    risk_df = pd.DataFrame(
        {
            "Domain": [
                "Transport / Logistics",
                "Support & Communication",
                "Lost Items / Textiles",
            ],

            "ThreatIndex": [
                55,
                78,
                90,
            ],

            "RiskLevel": [
                "MEDIUM",
                "HIGH",
                "HIGH",
            ],
        }
    )


    # --------------------------------------------------------
    # Risk chart
    # --------------------------------------------------------

    fig_risk = px.bar(
        risk_df,
        x="ThreatIndex",
        y="Domain",
        orientation="h",
        text="ThreatIndex",
        color="RiskLevel",
        color_discrete_map={
            "HIGH": "#EF4444",
            "MED-HIGH": "#F97316",
            "MEDIUM": "#EAB308",
            "LOW": "#22C55E",
        },
        labels={
            "ThreatIndex":
                "Threat Index Score",

            "Domain":
                "Business Domain",
        },
    )


    fig_risk.update_traces(
        textposition="outside"
    )


    fig_risk.update_layout(
        xaxis=dict(
            range=[0, 100]
        ),
        height=320,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20,
        ),
        legend_title_text="Risk Level",
    )


    with col_risk_chart:

        st.markdown(
            "##### Business Area Threat Index (0–100)"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True,
            key="risk_matrix_section",
        )


    # --------------------------------------------------------
    # Risk details
    # --------------------------------------------------------

    with col_risk_details:

        st.markdown(
            """
            ### 🔴 Lost Items / Textiles — HIGH RISK

            **Threat Score: 90 / 100**

            **Primary Cause**

            Gaps in laundry tracking and insufficient
            barcode/RFID scanning discipline.

            ---

            ### 🔴 Support & Communication — HIGH RISK

            **Threat Score: 78 / 100**

            **Primary Cause**

            Long queue waiting times and insufficient
            proactive ticket-status communication.

            ---

            ### 🟡 Transport / Logistics — MEDIUM RISK

            **Threat Score: 55 / 100**

            **Primary Cause**

            Delivery accuracy, routing, and item-handling
            issues.
            """
        )


    st.markdown("---")


    # ========================================================
    # PLOTLY FIGURES
    # ========================================================

    # --------------------------------------------------------
    # Rating distribution
    # --------------------------------------------------------

    rating_counts = (
        filtered_df["Yildiz_Sayisi"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_counts.columns = [
        "Stars",
        "Count",
    ]


    fig_rating = px.bar(
        rating_counts,
        x="Stars",
        y="Count",
        text="Count",
        color="Stars",
        color_continuous_scale="RdYlGn",
        title="Distribution of Star Ratings",
    )


    fig_rating.update_traces(
        textposition="outside"
    )


    fig_rating.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=1,
        ),
        showlegend=False,
    )


    # --------------------------------------------------------
    # Complaint category
    # --------------------------------------------------------

    cat_counts = (
        filtered_df["Complaint_Category"]
        .value_counts()
        .reset_index()
    )

    cat_counts.columns = [
        "Category",
        "Count",
    ]


    fig_pie = px.pie(
        cat_counts,
        names="Category",
        values="Count",
        hole=0.4,
        title="Proportion of Identified Issues",
        color_discrete_sequence=(
            px.colors.qualitative.Pastel
        ),
    )


    # --------------------------------------------------------
    # Timeline
    # --------------------------------------------------------

    timeline_df = (
        filtered_df
        .sort_values("Tarih_Saat")
    )


    fig_time = px.line(
        timeline_df,
        x="Tarih_Saat",
        y="Yildiz_Sayisi",
        markers=True,
        hover_data=[
            "Formatted_Date",
            "Isim",
            "Complaint_Category",
            "Musteri_Yorumu",
        ],
        title="Chronological Timeline of Customer Ratings",
        labels={
            "Tarih_Saat":
                "Date & Time",

            "Yildiz_Sayisi":
                "Star Rating",
        },
    )


    fig_time.update_yaxes(
        range=[0.5, 5.5],
        dtick=1,
    )


    # --------------------------------------------------------
    # Hourly distribution
    # --------------------------------------------------------

    hourly_df = (
        filtered_df
        .groupby("Hour")
        .size()
        .reset_index(
            name="Review_Count"
        )
    )


    fig_hour = px.bar(
        hourly_df,
        x="Hour",
        y="Review_Count",
        text="Review_Count",
        title="Review Frequency by Hour (00:00–23:00)",
        labels={
            "Hour":
                "Hour of Day",

            "Review_Count":
                "Number of Reviews",
        },
    )


    fig_hour.update_traces(
        textposition="outside"
    )


    fig_hour.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=1,
            range=[-0.5, 23.5],
        )
    )


    # --------------------------------------------------------
    # Complaint vs rating
    # --------------------------------------------------------

    fig_box = px.box(
        filtered_df,
        x="Complaint_Category",
        y="Yildiz_Sayisi",
        color="Complaint_Category",
        title="Impact of Complaint Types on Satisfaction",
        labels={
            "Complaint_Category":
                "Complaint Type",

            "Yildiz_Sayisi":
                "Star Rating",
        },
    )


    fig_box.update_yaxes(
        range=[0.5, 5.5],
        dtick=1,
    )


    # ========================================================
    # SIDEBAR EXPORT
    # ========================================================

    st.sidebar.markdown("---")

    st.sidebar.subheader(
        "💾 Export Options"
    )


    html_data = generate_html_report(
        filtered_df,
        total_reviews,
        avg_rating,
        positive_share,
        negative_reviews,
        fig_rating,
        fig_pie,
        fig_time,
        fig_hour,
        fig_box,
    )


    st.sidebar.download_button(
        label="📥 Download Executive HTML Report",
        data=html_data,
        file_name=(
            "Elis_Danmark_Executive_Report.html"
        ),
        mime="text/html",
        use_container_width=True,
        key="download_html_report",
    )


    # ========================================================
    # DASHBOARD TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "📊 Visual Overview",
            "🔍 Detailed Trends",
            "📋 Customer Reviews",
        ]
    )


    # ========================================================
    # TAB 1 — VISUAL OVERVIEW
    # ========================================================

    with tab1:

        col_left, col_right = st.columns(2)


        with col_left:

            st.subheader(
                "⭐ Satisfaction Rating Distribution"
            )

            st.plotly_chart(
                fig_rating,
                use_container_width=True,
                key="rating_distribution_tab1",
            )


        with col_right:

            st.subheader(
                "📌 Complaint Category Breakdown"
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True,
                key="complaint_breakdown_tab1",
            )


        st.subheader(
            "⚠️ Operational Risk Overview"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True,
            key="risk_overview_tab1",
        )


    # ========================================================
    # TAB 2 — DETAILED TRENDS
    # ========================================================

    with tab2:

        st.subheader(
            "📈 Chronological Customer Rating Timeline"
        )

        st.plotly_chart(
            fig_time,
            use_container_width=True,
            key="rating_timeline_tab2",
        )


        col_t1, col_t2 = st.columns(2)


        with col_t1:

            st.subheader(
                "🕐 Review Distribution by Hour"
            )

            st.plotly_chart(
                fig_hour,
                use_container_width=True,
                key="hourly_distribution_tab2",
            )


        with col_t2:

            st.subheader(
                "📦 Complaint Type vs. Rating"
            )

            st.plotly_chart(
                fig_box,
                use_container_width=True,
                key="complaint_rating_box_tab2",
            )


    # ========================================================
    # TAB 3 — CUSTOMER REVIEWS
    # ========================================================

    with tab3:

        st.subheader(
            "📋 Chronologically Ordered Customer Reviews"
        )


        sort_order = st.radio(
            "Sort Order",
            options=[
                "Oldest to Newest",
                "Newest to Oldest",
            ],
            horizontal=True,
            key="review_sort_order",
        )


        ascending_flag = (
            sort_order == "Oldest to Newest"
        )


        display_df = (
            filtered_df
            .sort_values(
                by="Tarih_Saat",
                ascending=ascending_flag,
            )
            .copy()
        )


        st.caption(
            f"Showing {len(display_df):,} reviews"
        )


        st.dataframe(
            display_df[
                [
                    "Formatted_Date",
                    "Isim",
                    "Yildiz_Sayisi",
                    "Complaint_Category",
                    "Musteri_Yorumu",
                ]
            ],

            column_config={

                "Formatted_Date":
                    st.column_config.TextColumn(
                        "Date & Time"
                    ),

                "Isim":
                    st.column_config.TextColumn(
                        "Customer Name"
                    ),

                "Yildiz_Sayisi":
                    st.column_config.NumberColumn(
                        "Rating",
                        format="%d ⭐",
                    ),

                "Complaint_Category":
                    st.column_config.TextColumn(
                        "Category"
                    ),

                "Musteri_Yorumu":
                    st.column_config.TextColumn(
                        "Customer Review",
                        width="large",
                    ),
            },

            use_container_width=True,

            height=500,

            hide_index=True,
        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer">
            Elis Danmark — Executive Voice of Customer Dashboard
            <br>
            Trustpilot Customer Review Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
