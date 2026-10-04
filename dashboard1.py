import re
from collections import Counter
from io import StringIO

import pandas as pd
import plotly.express as px
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
# CONSTANTS
# ============================================================

PRIMARY_DATASET = "trustpilot_elis_analyzed.csv"
FALLBACK_DATASET = "trustpilot_elis_reviews_all.csv"

STOPWORDS = {
    # Danish
    "og", "i", "jeg", "det", "at", "en", "den", "til", "er", "som",
    "på", "de", "med", "han", "af", "for", "ikke", "der", "var",
    "mig", "seg", "men", "et", "har", "om", "vi", "min", "hadde",
    "fra", "ud", "da", "særdeles", "kan", "så", "være", "dem",
    "os", "blive", "eller",

    # English
    "and", "the", "to", "a", "of", "in", "is", "that", "it",
    "you", "was", "with", "on", "as", "have", "but", "be",
    "they", "we",

    # Company / website noise
    "elis", "dk", "com",

    # Rating-related noise
    "star", "stjerne", "stjerner",
}


# ============================================================
# CATEGORY CLASSIFICATION
# ============================================================

def calculate_dynamic_category(text):
    """
    Categorize a review into an operational problem category.
    """

    if not isinstance(text, str) or not text.strip():
        return "General / Unspecified"

    text_lower = text.lower()

    category_keywords = {
        "Binding / Contract Issues": [
            "binding",
            "opsigelse",
            "kontrakt",
            "cancellation",
            "bindingstid",
            "aftale",
        ],
        "Finans / Price & Billing": [
            "fatura",
            "regning",
            "priser",
            "invoice",
            "finance",
            "penge",
            "gebyr",
            "pris",
        ],
        "Communication / Support": [
            "iletişim",
            "telefon",
            "svar",
            "kontakt",
            "customer service",
            "kundeservice",
            "mail",
        ],
        "Transport / Logistics": [
            "teslimat",
            "levering",
            "chauffør",
            "transport",
            "delivery",
            "tøj",
            "missing",
        ],
    }

    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return category

    return "General Operations"


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    try:

        try:
            df = pd.read_csv(PRIMARY_DATASET)
        except FileNotFoundError:
            df = pd.read_csv(FALLBACK_DATASET)

        # Normalize company response column
        if "Sirket_Cevabi" in df.columns and "Cevap" not in df.columns:
            df = df.rename(
                columns={
                    "Sirket_Cevabi": "Cevap"
                }
            )

        # Validate rating
        if "Yildiz_Sayisi" not in df.columns:
            st.error(
                "Dataset does not contain 'Yildiz_Sayisi'."
            )
            return None

        df["Yildiz_Sayisi"] = pd.to_numeric(
            df["Yildiz_Sayisi"],
            errors="coerce",
        )

        # ----------------------------------------------------
        # Date handling
        # ----------------------------------------------------

        date_columns = [
            "Tarih",
            "Yorum_Tarihi",
            "Date",
            "date",
        ]

        for date_column in date_columns:

            if date_column in df.columns:

                df[date_column] = pd.to_datetime(
                    df[date_column],
                    errors="coerce",
                    dayfirst=True,
                )

                df = df.sort_values(
                    by=date_column,
                    ascending=False,
                    na_position="last",
                )

                break

        # ----------------------------------------------------
        # Find review column
        # ----------------------------------------------------

        comment_column = next(
            (
                column
                for column in [
                    "Musteri_Yorumu",
                    "Yorum",
                    "Cevap",
                ]
                if column in df.columns
            ),
            None,
        )

        if comment_column:

            df["Tespit_Edilen_Problem"] = (
                df[comment_column]
                .apply(calculate_dynamic_category)
            )

        return df.reset_index(drop=True)

    except Exception as error:

        st.error(
            f"Error loading dataset: {error}"
        )

        return None


# ============================================================
# NLP
# ============================================================

def clean_and_tokenize(text):

    if pd.isna(text) or not isinstance(text, str):
        return []

    text = text.lower()

    text = re.sub(
        r"https?://\S+|www\.\S+",
        "",
        text,
    )

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return [
        word
        for word in text.split()
        if (
            word not in STOPWORDS
            and len(word) > 2
            and not word.isnumeric()
        )
    ]


def extract_keywords(text_list, top_k=15):

    words = []

    for text in text_list:
        words.extend(
            clean_and_tokenize(text)
        )

    return Counter(words).most_common(top_k)


# ============================================================
# PLOTLY CHARTS
# ============================================================

def create_sentiment_keyword_chart(
    texts,
    color_scale,
    title,
):

    top_words = extract_keywords(
        texts,
        top_k=15,
    )

    if not top_words:
        return None

    words_df = pd.DataFrame(
        top_words,
        columns=[
            "Keyword / Term",
            "Frequency",
        ],
    )

    fig = px.bar(
        words_df,
        x="Frequency",
        y="Keyword / Term",
        orientation="h",
        title=title,
        color="Frequency",
        color_continuous_scale=color_scale,
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        },
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    return fig


def create_category_pie_chart(
    df,
    title,
    colors=None,
):

    if (
        "Tespit_Edilen_Problem" not in df.columns
        or df.empty
    ):
        return None

    counts = (
        df["Tespit_Edilen_Problem"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Category / Problem",
        "Count",
    ]

    fig = px.pie(
        counts,
        values="Count",
        names="Category / Problem",
        title=title,
        color_discrete_sequence=(
            colors
            if colors
            else px.colors.qualitative.Pastel
        ),
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig.update_layout(
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar(df):

    st.sidebar.title(
        "🔍 Filter Controls"
    )

    available_stars = sorted(
        df["Yildiz_Sayisi"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_stars = st.sidebar.multiselect(
        "Filter by Rating (Stars)",
        options=available_stars,
        default=available_stars,
    )

    search_query = st.sidebar.text_input(
        "Keyword Search in Reviews",
        placeholder="e.g. delivery, service...",
    )

    return selected_stars, search_query


def apply_filters(
    df,
    selected_stars,
    search_query,
):

    filtered_df = df[
        df["Yildiz_Sayisi"].isin(
            selected_stars
        )
    ].copy()

    if search_query:

        comment_column = next(
            (
                column
                for column in [
                    "Musteri_Yorumu",
                    "Yorum",
                    "Cevap",
                ]
                if column in filtered_df.columns
            ),
            None,
        )

        if comment_column:

            filtered_df = filtered_df[
                filtered_df[comment_column]
                .fillna("")
                .astype(str)
                .str.contains(
                    search_query,
                    case=False,
                    na=False,
                    regex=False,
                )
            ]

    return filtered_df


# ============================================================
# KPI SECTION
# ============================================================

def calculate_kpis(df):

    total_reviews = len(df)

    average_rating = (
        df["Yildiz_Sayisi"].mean()
        if total_reviews
        else 0
    )

    negative_reviews = len(
        df[
            df["Yildiz_Sayisi"] <= 2
        ]
    )

    positive_reviews = len(
        df[
            df["Yildiz_Sayisi"] >= 4
        ]
    )

    negative_share = (
        negative_reviews
        / total_reviews
        * 100
        if total_reviews
        else 0
    )

    positive_share = (
        positive_reviews
        / total_reviews
        * 100
        if total_reviews
        else 0
    )

    return {
        "total": total_reviews,
        "average": average_rating,
        "negative": negative_reviews,
        "positive": positive_reviews,
        "negative_share": negative_share,
        "positive_share": positive_share,
    }


def render_header(df):

    st.title(
        "📊 Elis Danmark — Executive Voice of Customer Dashboard"
    )

    st.caption(
        "Automated NLP Sentiment Analysis, Customer Feedback "
        "Trends, and Operational Root Cause Analysis"
    )

    kpis = calculate_kpis(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Reviews",
        kpis["total"],
    )

    col2.metric(
        "Average Rating",
        f"{kpis['average']:.2f} / 5.0",
    )

    col3.metric(
        "Bad Reviews (1–2 ★)",
        kpis["negative"],
        f"{kpis['negative_share']:.1f}% Share",
        delta_color="inverse",
    )

    col4.metric(
        "Good Reviews (4–5 ★)",
        kpis["positive"],
        f"{kpis['positive_share']:.1f}% Share",
    )

    st.caption(
        "📅 Reviews sorted chronologically: newest first."
    )


# ============================================================
# CREATE HTML DASHBOARD
# ============================================================

def generate_html_dashboard(
    filtered_df,
    comment_column,
):
    """
    Generate the complete dashboard as one standalone HTML file.
    """

    # --------------------------------------------------------
    # KPI calculations
    # --------------------------------------------------------

    kpis = calculate_kpis(
        filtered_df
    )

    # --------------------------------------------------------
    # Split reviews
    # --------------------------------------------------------

    bad_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] <= 2
    ]

    good_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] >= 4
    ]

    # --------------------------------------------------------
    # Create charts
    # --------------------------------------------------------

    bad_pie = create_category_pie_chart(
        bad_df,
        "🔴 Complaints Breakdown — 1–2 Stars",
        colors=px.colors.sequential.Reds_r,
    )

    good_pie = create_category_pie_chart(
        good_df,
        "🟢 Positive Drivers — 4–5 Stars",
        colors=px.colors.sequential.Greens_r,
    )

    bad_texts = (
        bad_df[comment_column]
        .dropna()
        .tolist()
    )

    good_texts = (
        good_df[comment_column]
        .dropna()
        .tolist()
    )

    bad_keywords = create_sentiment_keyword_chart(
        bad_texts,
        "Reds",
        "💔 Key Words Inside Bad Feedback",
    )

    good_keywords = create_sentiment_keyword_chart(
        good_texts,
        "Greens",
        "💖 Key Words Inside Good Feedback",
    )

    # --------------------------------------------------------
    # Convert charts to HTML
    # --------------------------------------------------------

    chart_html = []

    for chart in [
        bad_pie,
        good_pie,
        bad_keywords,
        good_keywords,
    ]:

        if chart is not None:

            chart_html.append(
                chart.to_html(
                    full_html=False,
                    include_plotlyjs=False,
                )
            )

    charts_combined = "\n".join(
        chart_html
    )

    # --------------------------------------------------------
    # Review table
    # --------------------------------------------------------

    display_columns = [
        column
        for column in [
            "Tarih",
            "Isim",
            "Yildiz_Sayisi",
            "Tespit_Edilen_Problem",
            comment_column,
        ]
        if column in filtered_df.columns
    ]

    table_html = filtered_df[
        display_columns
    ].head(50).to_html(
        index=False,
        classes="review-table",
        border=0,
        escape=True,
    )

    # --------------------------------------------------------
    # Complete HTML document
    # --------------------------------------------------------

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Elis Danmark — Customer Review & NLP Dashboard
</title>

<script
src="https://cdn.plot.ly/plotly-2.35.2.min.js">
</script>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    font-family:
        Arial,
        Helvetica,
        sans-serif;
    background: #f4f7f9;
    color: #172b4d;
}}

.container {{
    max-width: 1500px;
    margin: auto;
    padding: 35px;
}}

.header {{
    background:
        linear-gradient(
            135deg,
            #005a70,
            #008b8b
        );
    color: white;
    padding: 35px;
    border-radius: 16px;
    margin-bottom: 30px;
    box-shadow:
        0 5px 20px
        rgba(0,0,0,0.12);
}}

.header h1 {{
    margin: 0;
    font-size: 32px;
}}

.header p {{
    margin-top: 10px;
    opacity: 0.9;
    font-size: 16px;
}}

.kpi-grid {{
    display: grid;
    grid-template-columns:
        repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 35px;
}}

.kpi {{
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.08);
}}

.kpi-title {{
    color: #6b778c;
    font-size: 14px;
    margin-bottom: 10px;
}}

.kpi-value {{
    font-size: 30px;
    font-weight: bold;
    color: #005a70;
}}

.section {{
    margin-top: 35px;
}}

.section h2 {{
    font-size: 24px;
    color: #005a70;
}}

.chart-grid {{
    display: grid;
    grid-template-columns:
        repeat(2, 1fr);
    gap: 20px;
}}

.chart {{
    background: white;
    border-radius: 14px;
    padding: 10px;
    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.08);
}}

.table-container {{
    background: white;
    padding: 20px;
    border-radius: 14px;
    overflow-x: auto;
    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.08);
}}

.review-table {{
    width: 100%;
    border-collapse: collapse;
}}

.review-table th {{
    background: #005a70;
    color: white;
    padding: 12px;
    text-align: left;
}}

.review-table td {{
    padding: 10px;
    border-bottom:
        1px solid #e5e7eb;
}}

.review-table tr:hover {{
    background: #f1f8fa;
}}

.footer {{
    margin-top: 40px;
    text-align: center;
    color: #6b778c;
    font-size: 13px;
}}

@media (max-width: 900px) {{

    .kpi-grid {{
        grid-template-columns:
            repeat(2, 1fr);
    }}

    .chart-grid {{
        grid-template-columns: 1fr;
    }}

}}

@media (max-width: 600px) {{

    .container {{
        padding: 15px;
    }}

    .kpi-grid {{
        grid-template-columns: 1fr;
    }}

}}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <h1>
            📊 Elis Danmark —
            Executive Voice of Customer Dashboard
        </h1>

        <p>
            Automated NLP Sentiment Analysis,
            Customer Feedback Trends,
            and Operational Root Cause Analysis
        </p>

    </div>


    <!-- KPI SECTION -->

    <div class="kpi-grid">

        <div class="kpi">

            <div class="kpi-title">
                Total Reviews
            </div>

            <div class="kpi-value">
                {kpis["total"]}
            </div>

        </div>


        <div class="kpi">

            <div class="kpi-title">
                Average Rating
            </div>

            <div class="kpi-value">
                {kpis["average"]:.2f} / 5.0
            </div>

        </div>


        <div class="kpi">

            <div class="kpi-title">
                Bad Reviews (1–2 ★)
            </div>

            <div class="kpi-value">
                {kpis["negative"]}
            </div>

            <small>
                {kpis["negative_share"]:.1f}% of reviews
            </small>

        </div>


        <div class="kpi">

            <div class="kpi-title">
                Good Reviews (4–5 ★)
            </div>

            <div class="kpi-value">
                {kpis["positive"]}
            </div>

            <small>
                {kpis["positive_share"]:.1f}% of reviews
            </small>

        </div>

    </div>


    <!-- CATEGORY SECTION -->

    <div class="section">

        <h2>
            1. Core Problem Breakdown by Category
        </h2>

        <div class="chart-grid">

"""

    # Add pie charts
    if bad_pie is not None:
        html += f"""
            <div class="chart">
                {bad_pie.to_html(
                    full_html=False,
                    include_plotlyjs=False
                )}
            </div>
"""

    if good_pie is not None:
        html += f"""
            <div class="chart">
                {good_pie.to_html(
                    full_html=False,
                    include_plotlyjs=False
                )}
            </div>
"""

    html += """
        </div>

    </div>


    <!-- KEYWORD SECTION -->

    <div class="section">

        <h2>
            2. Keyword Frequencies
        </h2>

        <div class="chart-grid">

"""

    if bad_keywords is not None:
        html += f"""
            <div class="chart">
                {bad_keywords.to_html(
                    full_html=False,
                    include_plotlyjs=False
                )}
            </div>
"""

    if good_keywords is not None:
        html += f"""
            <div class="chart">
                {good_keywords.to_html(
                    full_html=False,
                    include_plotlyjs=False
                )}
            </div>
"""

    html += f"""

        </div>

    </div>


    <!-- REVIEW TABLE -->

    <div class="section">

        <h2>
            3. Recent Customer Raw Feedback
        </h2>

        <div class="table-container">

            {table_html}

        </div>

    </div>


    <div class="footer">

        Generated from Elis Danmark customer review data.

        <br>

        Dashboard generated automatically
        from the selected Streamlit filters.

    </div>

</div>

</body>

</html>
"""

    return html


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    df = load_data()

    if df is None or df.empty:

        st.warning(
            "No review data is available."
        )

        st.stop()

    # --------------------------------------------------------
    # Determine comment column
    # --------------------------------------------------------

    comment_column = next(
        (
            column
            for column in [
                "Musteri_Yorumu",
                "Yorum",
                "Cevap",
            ]
            if column in df.columns
        ),
        None,
    )

    if comment_column is None:

        st.error(
            "No customer review/comment column was found."
        )

        st.stop()

    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    selected_stars, search_query = render_sidebar(
        df
    )

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    filtered_df = apply_filters(
        df,
        selected_stars,
        search_query,
    )

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    render_header(
        filtered_df
    )

    st.markdown("---")

    bad_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] <= 2
    ]

    good_df = filtered_df[
        filtered_df["Yildiz_Sayisi"] >= 4
    ]

    # --------------------------------------------------------
    # Category charts
    # --------------------------------------------------------

    st.header(
        "1. Core Problem Breakdown by Category"
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_bad = create_category_pie_chart(
            bad_df,
            "🔴 Complaints Breakdown — 1–2 Stars",
            colors=px.colors.sequential.Reds_r,
        )

        if fig_bad:

            st.plotly_chart(
                fig_bad,
                use_container_width=True,
            )

        else:

            st.info(
                "No bad reviews available."
            )

    with col2:

        fig_good = create_category_pie_chart(
            good_df,
            "🟢 Positive Drivers — 4–5 Stars",
            colors=px.colors.sequential.Greens_r,
        )

        if fig_good:

            st.plotly_chart(
                fig_good,
                use_container_width=True,
            )

        else:

            st.info(
                "No good reviews available."
            )

    st.markdown("---")

    # --------------------------------------------------------
    # Keyword charts
    # --------------------------------------------------------

    st.header(
        "2. Keyword Frequencies"
    )

    col1, col2 = st.columns(2)

    with col1:

        bad_texts = (
            bad_df[comment_column]
            .dropna()
            .tolist()
        )

        fig_bad_keywords = (
            create_sentiment_keyword_chart(
                bad_texts,
                "Reds",
                "💔 Key Words Inside Bad Feedback",
            )
        )

        if fig_bad_keywords:

            st.plotly_chart(
                fig_bad_keywords,
                use_container_width=True,
            )

    with col2:

        good_texts = (
            good_df[comment_column]
            .dropna()
            .tolist()
        )

        fig_good_keywords = (
            create_sentiment_keyword_chart(
                good_texts,
                "Greens",
                "💖 Key Words Inside Good Feedback",
            )
        )

        if fig_good_keywords:

            st.plotly_chart(
                fig_good_keywords,
                use_container_width=True,
            )

    st.markdown("---")

    # --------------------------------------------------------
    # Raw data
    # --------------------------------------------------------

    st.header(
        "3. Recent Customer Raw Feedback"
    )

    display_columns = [
        column
        for column in [
            "Tarih",
            "Isim",
            "Yildiz_Sayisi",
            "Tespit_Edilen_Problem",
            comment_column,
        ]
        if column in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[
            display_columns
        ].head(50),
        use_container_width=True,
        hide_index=True,
    )

    # ========================================================
    # HTML EXPORT
    # ========================================================

    st.markdown("---")

    st.header(
        "📥 Export Dashboard"
    )

    st.write(
        "Download the complete dashboard as a standalone HTML file."
    )

    html_dashboard = generate_html_dashboard(
        filtered_df,
        comment_column,
    )

    st.download_button(
        label="📄 Download Complete Dashboard as HTML",
        data=html_dashboard,
        file_name="elis_dashboard.html",
        mime="text/html",
        use_container_width=True,
    )

    st.success(
        "The HTML export contains the KPI cards, charts, "
        "keyword analysis, and review table using the "
        "currently selected filters."
    )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
