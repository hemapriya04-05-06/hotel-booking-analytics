import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Hotel Booking Analytics",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS - EARTHY / NEUTRAL THEME
# ============================================================
st.markdown("""
<style>
    :root {
        --bg: #f4efe7;
        --panel: rgba(255, 252, 246, 0.78);
        --panel-solid: #fffaf2;
        --text: #3f3830;
        --muted: #7d7267;
        --brown: #7b6652;
        --brown-dark: #5e4b3b;
        --sage: #7d8970;
        --sand: #c8b59b;
        --line: #ddd2c3;
        --good: #6f8565;
        --warning: #b8895b;
        --danger: #a66a5b;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(200,181,155,.20), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(125,137,112,.14), transparent 28%),
            linear-gradient(135deg, #f7f2ea 0%, #eee6da 100%);
        color: var(--text);
    }

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    .block-container {
        max-width: 1450px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    /* Sticky header */
    .sticky-header {
        position: sticky;
        top: 0;
        z-index: 999;
        padding: 12px 22px;
        margin-bottom: 18px;
        background: rgba(247, 242, 234, .88);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-bottom: 1px solid rgba(123,102,82,.12);
    }

    .title {
        font-size: 2.35rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #4c4035;
        margin: 0;
    }

    .subtitle {
        color: #807468;
        font-size: .98rem;
        margin-top: 3px;
    }

    /* Glass panels */
    .glass-card {
        background: var(--panel);
        border: 1px solid rgba(123,102,82,.14);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(77,61,46,.10);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
    }

    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 38px rgba(77,61,46,.16);
        border-color: rgba(123,102,82,.28);
    }

    /* Filter card */
    .filter-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #5e4b3b;
        margin-bottom: 10px;
    }

    .filter-caption {
        font-size: .82rem;
        color: #8b7e70;
        margin-bottom: 12px;
    }

    /* KPI cards */
    .kpi-card {
        background: rgba(255, 250, 242, .82);
        border: 1px solid rgba(123,102,82,.14);
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 112px;
        box-shadow: 0 8px 24px rgba(77,61,46,.09);
        transition: all .25s ease;
    }

    .kpi-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 14px 32px rgba(77,61,46,.16);
    }

    .kpi-label {
        color: #85786a;
        font-size: .83rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    .kpi-value {
        color: #4e4237;
        font-size: 1.9rem;
        font-weight: 800;
        margin-top: 5px;
    }

    .kpi-note {
        color: #8d8174;
        font-size: .78rem;
        margin-top: 3px;
    }

    /* Section headings */
    .section-heading {
        font-size: 1.18rem;
        font-weight: 800;
        color: #594a3c;
        margin: 8px 0 10px 2px;
    }

    .section-note {
        color: #817568;
        font-size: .84rem;
        margin: -4px 0 10px 2px;
    }

    /* Insight card */
    .insight-card {
        background: linear-gradient(135deg, rgba(125,137,112,.13), rgba(200,181,155,.17));
        border-left: 4px solid #7d8970;
        border-radius: 14px;
        padding: 14px 17px;
        margin-top: 8px;
        color: #5c5147;
        box-shadow: 0 5px 18px rgba(77,61,46,.06);
    }

    .insight-title {
        font-weight: 800;
        color: #5a644f;
        margin-bottom: 4px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid #cdbda9 !important;
        background: #fffaf2 !important;
        color: #5e4b3b !important;
        font-weight: 700 !important;
        transition: all .2s ease !important;
    }

    .stButton > button:hover {
        background: #7b6652 !important;
        color: white !important;
        border-color: #7b6652 !important;
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(94,75,59,.22);
    }

    .stButton > button:active {
        transform: scale(.97);
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background: rgba(255,250,242,.88) !important;
        border-color: #d5c7b7 !important;
        border-radius: 11px !important;
    }

    /* Plotly containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255,252,246,.72);
        border-radius: 18px;
        border: 1px solid rgba(123,102,82,.10);
        box-shadow: 0 8px 25px rgba(77,61,46,.07);
        padding: 4px;
        transition: transform .25s ease, box-shadow .25s ease;
    }

    div[data-testid="stPlotlyChart"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 13px 30px rgba(77,61,46,.12);
    }

    /* Expander */
    details {
        background: rgba(255,250,242,.72) !important;
        border: 1px solid rgba(123,102,82,.12) !important;
        border-radius: 14px !important;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8b7e70;
        font-size: .78rem;
        padding: 25px 0 5px;
    }

    /* Small-screen adjustments */
    @media (max-width: 900px) {
        .title {font-size: 1.8rem;}
        .block-container {padding-left: 1rem; padding-right: 1rem;}
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    possible_files = [
        "cleaned_hotel_data.csv",
        "hotel_bookings_data.csv"
    ]

    for file in possible_files:
        try:
            data = pd.read_csv(file)
            break
        except FileNotFoundError:
            data = None

    if data is None:
        raise FileNotFoundError(
            "CSV file not found. Put cleaned_hotel_data.csv or "
            "hotel_bookings_data.csv in the same folder as app.py."
        )

    # Make sure required derived columns exist
    if "children" in data.columns:
        data["children"] = data["children"].fillna(0)

    if "city" in data.columns:
        data["city"] = data["city"].fillna("Unknown")

    if "total_stay" not in data.columns:
        data["total_stay"] = (
            data["stays_in_weekend_nights"].fillna(0)
            + data["stays_in_weekdays_nights"].fillna(0)
        )

    if "total_guests" not in data.columns:
        data["total_guests"] = (
            data["adults"].fillna(0)
            + data["children"].fillna(0)
            + data["babies"].fillna(0)
        )

    if "lead_time_group" not in data.columns:
        bins = [0, 30, 60, 90, 180, 365, np.inf]
        labels = ["0-30", "31-60", "61-90", "91-180", "181-365", "366+"]
        data["lead_time_group"] = pd.cut(
            data["lead_time"],
            bins=bins,
            labels=labels,
            include_lowest=True
        )

    return data


try:
    df = load_data()
except Exception as e:
    st.error(str(e))
    st.stop()

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="sticky-header">
    <div class="title">Hotel Booking Analytics</div>
    <div class="subtitle">
        Booking patterns, seasonality and cancellation behaviour
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FILTERS - MAIN PAGE, NOT SIDEBAR
# ============================================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="filter-title">Dashboard Filters</div>'
    '<div class="filter-caption">Use the filters below to explore the data interactively.</div>',
    unsafe_allow_html=True
)

f1, f2, f3, f4 = st.columns(4)

with f1:
    hotel_options = ["All Hotels"] + sorted(df["hotel"].dropna().unique().tolist())
    selected_hotel = st.selectbox("Hotel Type", hotel_options)

with f2:
    year_options = ["All Years"] + sorted(
        df["arrival_date_year"].dropna().unique().tolist()
    )
    selected_year = st.selectbox("Year", year_options)

with f3:
    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    available_months = [
        m for m in month_order
        if m in df["arrival_date_month"].dropna().unique()
    ]
    selected_month = st.selectbox(
        "Arrival Month",
        ["All Months"] + available_months
    )

with f4:
    status_options = ["All Bookings", "Not Cancelled", "Cancelled"]
    selected_status = st.selectbox("Booking Status", status_options)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# APPLY FILTERS
# ============================================================
filtered_df = df.copy()

if selected_hotel != "All Hotels":
    filtered_df = filtered_df[filtered_df["hotel"] == selected_hotel]

if selected_year != "All Years":
    filtered_df = filtered_df[
        filtered_df["arrival_date_year"] == selected_year
    ]

if selected_month != "All Months":
    filtered_df = filtered_df[
        filtered_df["arrival_date_month"] == selected_month
    ]

if selected_status == "Cancelled":
    filtered_df = filtered_df[filtered_df["is_canceled"] == 1]
elif selected_status == "Not Cancelled":
    filtered_df = filtered_df[filtered_df["is_canceled"] == 0]

# ============================================================
# KPI CALCULATIONS
# ============================================================
total_bookings = len(filtered_df)

cancellation_rate = (
    filtered_df["is_canceled"].mean() * 100
    if total_bookings > 0 else 0
)

avg_lead_time = (
    filtered_df["lead_time"].mean()
    if total_bookings > 0 else 0
)

avg_stay = (
    filtered_df["total_stay"].mean()
    if total_bookings > 0 else 0
)

# ============================================================
# KPI ROW
# ============================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Bookings</div>
        <div class="kpi-value">{total_bookings:,}</div>
        <div class="kpi-note">Bookings after selected filters</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    status_class = "danger" if cancellation_rate >= 30 else "good"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Cancellation Rate</div>
        <div class="kpi-value">{cancellation_rate:.1f}%</div>
        <div class="kpi-note">Higher values indicate greater risk</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average Lead Time</div>
        <div class="kpi-value">{avg_lead_time:.0f} days</div>
        <div class="kpi-note">Average days before arrival</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average Stay</div>
        <div class="kpi-value">{avg_stay:.1f} nights</div>
        <div class="kpi-note">Average total stay duration</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# PLOTLY COMMON STYLE
# ============================================================
plot_bg = "rgba(0,0,0,0)"
paper_bg = "rgba(0,0,0,0)"
font_color = "#594a3c"
grid_color = "#e2d8cb"

def style_fig(fig, height=410):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(
            family="Arial",
            color=font_color
        ),
        margin=dict(l=45, r=25, t=65, b=55),
        hoverlabel=dict(
            bgcolor="#fffaf2",
            font_size=13,
            font_color="#4e4237"
        ),
        transition=dict(
            duration=450,
            easing="cubic-in-out"
        ),
        legend=dict(
            bgcolor="rgba(255,250,242,.75)",
            bordercolor="#ded2c4",
            borderwidth=1
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#d8cbbb"
    )

    fig.update_yaxes(
        gridcolor=grid_color,
        zeroline=False
    )

    return fig

# ============================================================
# CHART 1 - MONTHLY BOOKINGS
# ============================================================
st.markdown(
    '<div class="section-heading">Monthly Booking Trend</div>'
    '<div class="section-note">Explore booking demand across months and hotel types.</div>',
    unsafe_allow_html=True
)

monthly = (
    filtered_df.groupby(["arrival_date_month", "hotel"])
    .size()
    .reset_index(name="bookings")
)

monthly["arrival_date_month"] = pd.Categorical(
    monthly["arrival_date_month"],
    categories=month_order,
    ordered=True
)

monthly = monthly.sort_values("arrival_date_month")

fig1 = px.line(
    monthly,
    x="arrival_date_month",
    y="bookings",
    color="hotel",
    markers=True,
    title="Monthly Bookings"
)

fig1.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig1.update_layout(
    xaxis_title="Arrival Month",
    yaxis_title="Number of Bookings"
)

style_fig(fig1, 430)
st.plotly_chart(fig1, use_container_width=True, key="monthly_chart")

# Dynamic insight
if not monthly.empty:
    peak_row = monthly.loc[monthly["bookings"].idxmax()]
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Insight</div>
        The highest booking volume in the current selection is
        <b>{int(peak_row["bookings"]):,}</b> bookings for
        <b>{peak_row["hotel"]}</b> in <b>{peak_row["arrival_date_month"]}</b>.
        Use this pattern to plan room availability, staffing and seasonal promotions.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHARTS 2 & 3
# ============================================================
c1, c2 = st.columns(2)

# ---------- Chart 2: Hotel distribution ----------
with c1:
    st.markdown(
        '<div class="section-heading">Hotel Type Distribution</div>',
        unsafe_allow_html=True
    )

    hotel_counts = (
        filtered_df["hotel"]
        .value_counts()
        .reset_index()
    )
    hotel_counts.columns = ["hotel", "bookings"]

    fig2 = px.pie(
        hotel_counts,
        names="hotel",
        values="bookings",
        hole=0.58,
        title="Booking Share by Hotel Type"
    )

    fig2.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Bookings: %{value:,}<br>Share: %{percent}<extra></extra>"
    )

    style_fig(fig2, 390)
    st.plotly_chart(fig2, use_container_width=True, key="hotel_chart")

# ---------- Chart 3: Cancellation rate ----------
with c2:
    st.markdown(
        '<div class="section-heading">Cancellation Rate</div>',
        unsafe_allow_html=True
    )

    cancellation = (
        filtered_df.groupby("hotel")["is_canceled"]
        .mean()
        .mul(100)
        .reset_index(name="cancellation_rate")
    )

    fig3 = px.bar(
        cancellation,
        x="hotel",
        y="cancellation_rate",
        text="cancellation_rate",
        title="Cancellation Rate by Hotel Type",
        color="cancellation_rate",
        color_continuous_scale=[
            [0, "#8a9a7b"],
            [0.5, "#b99b78"],
            [1, "#a66a5b"]
        ]
    )

    fig3.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Cancellation Rate: %{y:.1f}%<extra></extra>"
    )

    fig3.update_layout(
        xaxis_title="Hotel Type",
        yaxis_title="Cancellation Rate (%)",
        coloraxis_showscale=False,
        yaxis=dict(range=[0, max(100, cancellation["cancellation_rate"].max() * 1.2)])
    )

    style_fig(fig3, 390)
    st.plotly_chart(fig3, use_container_width=True, key="cancel_chart")

# ============================================================
# CHARTS 4 & 5
# ============================================================
c3, c4 = st.columns(2)

# ---------- Chart 4: Stay duration ----------
with c3:
    st.markdown(
        '<div class="section-heading">Stay Duration vs Cancellation</div>',
        unsafe_allow_html=True
    )

    stay_data = (
        filtered_df.groupby(["total_stay", "hotel"])["is_canceled"]
        .mean()
        .mul(100)
        .reset_index(name="cancellation_rate")
    )

    # Keep the visual readable; long stays are usually sparse.
    stay_data = stay_data[stay_data["total_stay"] <= 15]

    fig4 = px.line(
        stay_data,
        x="total_stay",
        y="cancellation_rate",
        color="hotel",
        markers=True,
        title="Cancellation Rate by Stay Duration"
    )

    fig4.update_traces(
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate="<b>%{fullData.name}</b><br>Stay: %{x} nights<br>Cancellation: %{y:.1f}%<extra></extra>"
    )

    fig4.update_layout(
        xaxis_title="Total Stay (Nights)",
        yaxis_title="Cancellation Rate (%)"
    )

    style_fig(fig4, 410)
    st.plotly_chart(fig4, use_container_width=True, key="stay_chart")

# ---------- Chart 5: Lead time ----------
with c4:
    st.markdown(
        '<div class="section-heading">Lead Time vs Cancellation</div>',
        unsafe_allow_html=True
    )

    lead_data = (
        filtered_df.groupby(
            ["lead_time_group", "hotel"],
            observed=True
        )["is_canceled"]
        .mean()
        .mul(100)
        .reset_index(name="cancellation_rate")
    )

    lead_order = ["0-30", "31-60", "61-90", "91-180", "181-365", "366+"]

    lead_data["lead_time_group"] = pd.Categorical(
        lead_data["lead_time_group"].astype(str),
        categories=lead_order,
        ordered=True
    )

    lead_data = lead_data.sort_values("lead_time_group")

    fig5 = px.line(
        lead_data,
        x="lead_time_group",
        y="cancellation_rate",
        color="hotel",
        markers=True,
        title="Cancellation Rate by Lead Time"
    )

    fig5.update_traces(
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate="<b>%{fullData.name}</b><br>Lead Time: %{x} days<br>Cancellation: %{y:.1f}%<extra></extra>"
    )

    fig5.update_layout(
        xaxis_title="Lead Time Group (Days)",
        yaxis_title="Cancellation Rate (%)"
    )

    style_fig(fig5, 410)
    st.plotly_chart(fig5, use_container_width=True, key="lead_chart")

# ============================================================
# DRILL-DOWN / DETAILED VIEW
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("Explore Detailed Data / Drill Down", expanded=False):
    st.write(
        "Use this section to inspect the records behind the dashboard "
        "after applying your filters."
    )

    detail_cols = [
        c for c in [
            "hotel", "arrival_date_year", "arrival_date_month",
            "lead_time", "total_stay", "adults", "children",
            "adr", "market_segment", "customer_type", "is_canceled"
        ]
        if c in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[detail_cols].head(100),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# BUSINESS INSIGHTS
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-heading">Business Insights</div>',
    unsafe_allow_html=True
)

ins1, ins2, ins3 = st.columns(3)

with ins1:
    st.markdown("""
    <div class="glass-card">
        <b>1. Demand Planning</b>
        <p style="color:#7d7267;">
        Use monthly booking patterns to plan staffing, room
        availability and seasonal promotions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with ins2:
    st.markdown("""
    <div class="glass-card">
        <b>2. Cancellation Management</b>
        <p style="color:#7d7267;">
        Monitor hotel types and booking segments with higher
        cancellation risk and use suitable booking policies.
        </p>
    </div>
    """, unsafe_allow_html=True)

with ins3:
    st.markdown("""
    <div class="glass-card">
        <b>3. Advance Bookings</b>
        <p style="color:#7d7267;">
        Long lead-time reservations can be supported with
        reminders, confirmation messages and rescheduling options.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    Hotel Booking Analytics Dashboard • Built with Python, Pandas,
    Plotly and Streamlit
</div>
""", unsafe_allow_html=True)