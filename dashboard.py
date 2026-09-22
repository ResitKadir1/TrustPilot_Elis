import re
from collections import Counter

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
    "og", "i", "jeg", "det", "at", "en", "den", "til", "er", "som",
    "på", "de", "med", "han", "af", "for", "ikke", "der", "var",
    "mig", "seg", "men", "et", "har", "om", "vi", "min", "hadde",
    "fra", "ud", "da", "særdeles", "kan", "så", "være", "dem",
    "os", "blive", "eller",
    "and", "the", "to", "a", "of", "in", "is", "that", "it",
    "you", "was", "with", "on", "as", "have", "but", "be",
    "they", "we",
    "elis", "dk", "com",
    "star", "stjerne", "stjerner",
}


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    """
    Load the analyzed dataset.

    Tries the analyzed dataset first and falls back to the
    raw review dataset if the analyzed file does not exist.
    """

    try:
        try:
            df = pd.read_csv(PRIMARY_DATASET)
        except FileNotFoundError:
            df = pd.read_csv(FALLBACK_DATASET)

        # Normalize company response column name.
        if "Sirket_Cevabi" in df.columns and "Cevap" not in df.columns:
            df = df.rename(columns={"Sirket_Cevabi": "Cevap"})

        return df

    except Exception as error:
        st.error(f"Error loading dataset: {error}")
        return None


# ============================================================
# NLP FUNCTIONS
# ============================================================

def clean_and_tokenize(text):
    """
    Clean a review and return useful tokens.
    """

    if not isinstance(text, str):
        return []

    text = text.lower()

    # Remove punctuation.
    text = re.sub(r"[^\w\s]", "", text)

    tokens = [
        word
        for word in text.split()
        if word not in STOPWORDS and len(word) > 2
    ]

    return tokens


def extract_ngrams(text_list, n=1, top_k=15):
    """
    Extract the most common unigrams or bigrams from a list of texts.
    """

    ngrams = []

    for text in text_list:
        tokens = clean_and_tokenize(text)

        if n == 1:
            ngrams.extend(tokens)

        elif n == 2:
            bigrams = [
                f"{tokens[i]} {tokens[i + 1]}"
                for i in range(len(tokens) - 1)
            ]
            ngrams.extend(bigrams)

    return Counter(ngrams).most_common(top_k)


# ============================================================
# CHART FUNCTIONS
# ============================================================

def create_ngram_chart(texts, ngram_type, color_scale, title):
    """
    Create a horizontal bar chart for the most common n-grams.
    """

    n = 1 if ngram_type == "Single Words (Unigrams)" else 2

    top_words = extract_ngrams(
        texts,
        n=n,
        top_k=15,
    )

    if not top_words:
        return None

    words_df = pd.DataFrame(
        top_words,
        columns=["Phrase/Word", "Frequency"],
    )

    fig = px.bar(
        words_df,
        x="Frequency",
        y="Phrase/Word",
        orientation="h",
        title=title,
        color="Frequency",
        color_continuous_scale=color_scale,
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# ============================================================
# SIDEBAR FILTERS
# ============================================================

def render_sidebar(df):
    """
    Render sidebar filters and return the selected values.
    """

    st.sidebar.title("🔍 Filter Controls")

    available_stars = sorted(
        df["Yildiz_Sayisi"].dropna().unique()
    )

    selected_stars = st.sidebar.multiselect(
        "Filter by Rating (Stars):",
        options=available_stars,
        default=available_stars,
    )

    search_query = st.sidebar.text_input(
        "Keyword Search in Reviews:"
    )

    return selected_stars, search_query


def apply_filters(df, selected_stars, search_query):
    """
    Apply rating and keyword filters to the dataset.
    """

    filtered = df[
        df["Yildiz_Sayisi"].isin(selected_stars)
    ].copy()

    if search_query:
        filtered = filtered[
            filtered["Musteri_Yorumu"]
            .fillna("")
            .str.contains(
                search_query,
                case=False,
                na=False,
            )
        ]

    return filtered


# ============================================================
# HEADER & METRICS
# ============================================================

def render_header(filtered_df):
    """
    Render dashboard title and KPI metrics.
    """

    st.title(
        "📊 Elis Danmark — Executive Voice of Customer Dashboard"
    )

    st.caption(
        "Automated NLP Sentiment Analysis, Topic Modeling, "
        "and Operational Root Cause Breakdown"
    )

    total_reviews = len(filtered_df)

    average_rating = (
        filtered_df["Yildiz_Sayisi"].mean()
        if total_reviews > 0
        else 0
    )

    negative_reviews = len(
        filtered_df[
            filtered_df["Yildiz_Sayisi"] <= 2
        ]
    )

    positive_reviews = len(
        filtered_df[
            filtered_df["Yildiz_Sayisi"] >= 4
        ]
    )

    negative_share = (
        negative_reviews / total_reviews * 100
        if total_reviews > 0
        else 0
    )

    positive_share = (
        positive_reviews / total_reviews * 100
        if total_reviews > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Reviews Analyzed",
        total_reviews,
    )

    col2.metric(
        "Average Rating",
        f"{average_rating:.2f} / 5.0",
    )

    col3.metric(
        "Negative Reviews (1–2 ★)",
        negative_reviews,
        delta=f"{negative_share:.1f}% Share",
        delta_color="inverse",
    )

    col4.metric(
        "Positive Reviews (4–5 ★)",
        positive_reviews,
        delta=f"{positive_share:.1f}% Share",
    )


# ============================================================
# SECTION 1 — ROOT CAUSE ANALYSIS
# ============================================================

def render_root_cause_analysis():
    """
    Render the strategic root-cause analysis section.
    """

    st.header("1. Core Strategic Findings & Root Cause Analysis")

    col_negative, col_positive = st.columns(2)

    with col_negative:
        st.subheader(
            "🔴 Top Customer Grievances (1–2 Star Reviews)"
        )

        st.markdown(
            """
            * **Logistics & Lost Textiles (Transport/Loss)**
                * Missing workwear: Garments and towels sent to
                  wash/repair frequently go missing.
                * Delivery errors: Items may be delivered to
                  incorrect floors or drop points.

            * **Customer Service & Communication**
                * Long phone waiting times.
                * Unanswered or delayed emails.
                * Limited account-management support.
                * Slow resolution of complaints.

            * **Contractual & Billing Friction**
                * Unexpected price increases.
                * Auto-renewal concerns.
                * Difficult cancellation procedures.
            """
        )

    with col_positive:
        st.subheader(
            "🟢 Key Drivers of Satisfaction (4–5 Star Reviews)"
        )

        st.markdown(
            """
            * **Driver Demeanor**
                * Delivery personnel are frequently described
                  as polite, helpful, and friendly.

            * **Integrity & Local Support**
                * Valuables found in garments are often returned
                  to customers.

            * **Laundry & Product Quality**
                * Customers praise cleaning quality when operations
                  run normally.
                * Items generally arrive fresh and according to schedule.
            """
        )


# ============================================================
# SECTION 2 — NLP ANALYSIS
# ============================================================

def render_nlp_section(filtered_df):
    """
    Render negative and positive NLP frequency analysis.
    """

    st.header("2. NLP Text Mining: Frequency & Keyword Occurrence")

    negative_tab, positive_tab = st.tabs(
        [
            "🔴 Negative Feedback Word Count (1–2 Stars)",
            "🟢 Positive Feedback Word Count (4–5 Stars)",
        ]
    )

    # --------------------------------------------------------
    # NEGATIVE REVIEWS
    # --------------------------------------------------------

    with negative_tab:

        negative_reviews = filtered_df[
            filtered_df["Yildiz_Sayisi"] <= 2
        ]["Musteri_Yorumu"].dropna().tolist()

        if negative_reviews:

            ngram_type = st.radio(
                "Select N-Gram Depth (Negative):",
                [
                    "Single Words (Unigrams)",
                    "2-Word Phrases (Bigrams)",
                ],
                key="negative_ngram",
            )

            chart = create_ngram_chart(
                texts=negative_reviews,
                ngram_type=ngram_type,
                color_scale="Reds",
                title="Top N-Gram Keywords in Dissatisfied Reviews",
            )

            if chart:
                st.plotly_chart(
                    chart,
                    use_container_width=True,
                )

        else:
            st.info(
                "No negative reviews found in the current selection."
            )

    # --------------------------------------------------------
    # POSITIVE REVIEWS
    # --------------------------------------------------------

    with positive_tab:

        positive_reviews = filtered_df[
            filtered_df["Yildiz_Sayisi"] >= 4
        ]["Musteri_Yorumu"].dropna().tolist()

        if positive_reviews:

            ngram_type = st.radio(
                "Select N-Gram Depth (Positive):",
                [
                    "Single Words (Unigrams)",
                    "2-Word Phrases (Bigrams)",
                ],
                key="positive_ngram",
            )

            chart = create_ngram_chart(
                texts=positive_reviews,
                ngram_type=ngram_type,
                color_scale="Greens",
                title="Top N-Gram Keywords in Praised Reviews",
            )

            if chart:
                st.plotly_chart(
                    chart,
                    use_container_width=True,
                )

        else:
            st.info(
                "No positive reviews found in the current selection."
            )


# ============================================================
# SECTION 3 — RISK MATRIX
# ============================================================

def get_risk_data():
    """
    Return operational risk assessment data.
    """

    return pd.DataFrame(
        [
            {
                "Domain": "Lost Items / Textiles",
                "Risk Level": "HIGH",
                "Severity Score": 90,
                "Root Cause": (
                    "Gaps in laundry tracking "
                    "(lack of barcode/RFID scan discipline)"
                ),
            },
            {
                "Domain": "Support & Communication",
                "Risk Level": "HIGH",
                "Severity Score": 85,
                "Root Cause": (
                    "Slow resolution turnaround "
                    "and difficult phone reachability"
                ),
            },
            {
                "Domain": "Transport / Logistics",
                "Risk Level": "MED-HIGH",
                "Severity Score": 70,
                "Root Cause": (
                    "Wrong drop-point deliveries "
                    "and incomplete bundles"
                ),
            },
            {
                "Domain": "Laundry Quality",
                "Risk Level": "MEDIUM",
                "Severity Score": 45,
                "Root Cause": (
                    "Occasional stains; lost items "
                    "remain a greater concern"
                ),
            },
        ]
    )


def render_risk_section():
    """
    Render the operational risk matrix.
    """

    st.header("3. Operational Risk Level Assessment Matrix")

    risk_df = get_risk_data()

    col_chart, col_details = st.columns(2)

    # --------------------------------------------------------
    # RISK CHART
    # --------------------------------------------------------

    with col_chart:

        fig = px.bar(
            risk_df,
            x="Severity Score",
            y="Domain",
            orientation="h",
            color="Risk Level",
            color_discrete_map={
                "HIGH": "#ff4b4b",
                "MED-HIGH": "#ffa500",
                "MEDIUM": "#f1c40f",
            },
            title="Business Area Threat Index (0–100 Scale)",
        )

        fig.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            },
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # RISK DETAILS
    # --------------------------------------------------------

    with col_details:

        for _, row in risk_df.iterrows():

            st.markdown(
                f"""
                ### {row['Domain']} — {row['Risk Level']} RISK

                **Severity Score:** {row['Severity Score']}/100

                **Primary Cause:**  
                {row['Root Cause']}
                """
            )

            st.divider()


# ============================================================
# SECTION 4 — REVIEW EXPLORER
# ============================================================

def render_review_explorer(filtered_df):
    """
    Display filtered raw review data.
    """

    st.header("4. Review Explorer & Raw Data")

    columns_to_display = [
        "Isim",
        "Tarih_Saat",
        "Yildiz_Sayisi",
        "Musteri_Yorumu",
        "Cevap",
    ]

    # Only display columns that actually exist.
    available_columns = [
        column
        for column in columns_to_display
        if column in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    df = load_data()

    # --------------------------------------------------------
    # DATASET CHECK
    # --------------------------------------------------------

    if df is None:
        st.warning(
            "Please run 'elis2.py' or 'analyze.py' first "
            "to generate the dataset file."
        )
        return

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    selected_stars, search_query = render_sidebar(df)

    filtered_df = apply_filters(
        df,
        selected_stars,
        search_query,
    )

    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    render_header(filtered_df)

    st.markdown("---")

    render_root_cause_analysis()

    st.markdown("---")

    render_nlp_section(filtered_df)

    st.markdown("---")

    render_risk_section()

    st.markdown("---")

    render_review_explorer(filtered_df)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
#### streamlit run app.py