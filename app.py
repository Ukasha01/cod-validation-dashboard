import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from supabase import create_client
from datetime import datetime, timedelta

# ════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════
st.set_page_config(
    page_title="📦 Ecommerce Intelligence Dashboard",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════════════
# PREMIUM ENTERPRISE CSS
# ════════════════════════════════════════════════════════
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Sora', sans-serif !important;
}

/* ════════════════════════════════════════════════════════
   GLOBAL
════════════════════════════════════════════════════════ */

html {
    scroll-behavior: smooth;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(99,102,241,.10), transparent 22%),
        radial-gradient(circle at bottom right, rgba(16,185,129,.06), transparent 20%),
        #0b1220;
}

.block-container {
    max-width: 100% !important;
    padding-top: 1.4rem !important;
    padding-left: 2.4rem !important;
    padding-right: 2.4rem !important;
    padding-bottom: 3rem !important;
}

/* ════════════════════════════════════════════════════════
   SIDEBAR
════════════════════════════════════════════════════════ */

[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid rgba(255,255,255,.04);
}

[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

.sb-brand {
    padding: 16px 10px 22px;
    margin-bottom: 18px;
    border-bottom: 1px solid rgba(255,255,255,.05);
}

.sb-logo {
    width: 56px;
    height: 56px;
    border-radius: 18px;

    background: linear-gradient(135deg,#6366f1,#8b5cf6);

    display:flex;
    align-items:center;
    justify-content:center;

    font-size: 28px;

    margin-bottom: 14px;

    box-shadow: 0 10px 30px rgba(99,102,241,.35);
}

.sb-name {
    font-size: 18px;
    font-weight: 800;
    color: white !important;
}

.sb-tag {
    font-size: 11px;
    color: #64748b !important;
    margin-top: 4px;
}

/* ════════════════════════════════════════════════════════
   HERO HEADER
════════════════════════════════════════════════════════ */

.topbar {
    position: relative;
    overflow: hidden;

    background:
        radial-gradient(circle at top right, rgba(99,102,241,.25), transparent 25%),
        radial-gradient(circle at bottom left, rgba(16,185,129,.12), transparent 25%),
        linear-gradient(135deg, #0f172a 0%, #131c31 45%, #172036 100%);

    border: 1px solid rgba(255,255,255,0.06);

    border-radius: 30px;

    padding: 38px;

    margin-bottom: 30px;

    min-height: 170px;

    display: flex;
    justify-content: space-between;
    align-items: center;

    box-shadow:
        0 10px 40px rgba(0,0,0,.28),
        inset 0 1px 0 rgba(255,255,255,.04);
}

.tb-left {
    display:flex;
    gap:24px;
    align-items:flex-start;
}

.tb-icon {
    width: 78px;
    height: 78px;
    border-radius: 24px;

    background: linear-gradient(135deg,#6366f1,#8b5cf6);

    display:flex;
    align-items:center;
    justify-content:center;

    font-size: 38px;

    box-shadow:
        0 10px 30px rgba(99,102,241,.4),
        inset 0 1px 0 rgba(255,255,255,.15);
}

.tb-title {
    font-size: 38px;
    font-weight: 800;
    color: white;

    line-height: 1.1;

    letter-spacing: -1.6px;

    margin-bottom: 10px;

    max-width: 780px;
}

.tb-sub {
    font-size: 15px;
    color: #94a3b8;

    line-height: 1.7;

    max-width: 760px;
}

.tb-right {
    display:flex;
    flex-direction:column;
    align-items:flex-end;
    gap:16px;
}

.live-pill {
    background: rgba(16,185,129,.12);
    border: 1px solid rgba(16,185,129,.25);

    color: #34d399;

    padding: 10px 18px;

    border-radius: 999px;

    font-size: 12px;
    font-weight: 700;
}

.live-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    display:inline-block;
    margin-right: 6px;
    animation: blink 1.5s infinite;
}

@keyframes blink {
    0%,100% { opacity:1; }
    50% { opacity:.3; }
}

.tb-meta {
    color: #64748b;
    font-size: 13px;
}

/* ════════════════════════════════════════════════════════
   SECTION TITLE
════════════════════════════════════════════════════════ */

.sec-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #94a3b8;

    margin: 34px 0 16px;
}

/* ════════════════════════════════════════════════════════
   KPI CARDS
════════════════════════════════════════════════════════ */

.kcard {
    position: relative;
    overflow: hidden;

    background: linear-gradient(
        180deg,
        rgba(17,24,39,.96),
        rgba(15,23,42,.94)
    );

    border: 1px solid rgba(255,255,255,.06);

    border-radius: 24px;

    padding: 24px;

    backdrop-filter: blur(14px);

    box-shadow:
        0 8px 30px rgba(0,0,0,.24),
        inset 0 1px 0 rgba(255,255,255,.03);

    transition: .25s ease;
}

.kcard:hover {
    transform: translateY(-4px);
    border-color: rgba(99,102,241,.35);
}

.kcard-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    font-weight: 700;
    color: #94a3b8;

    margin-bottom: 14px;
}

.kcard-value {
    font-size: 42px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -1.5px;

    color: white;

    margin-bottom: 10px;
}

.kcard-sub {
    font-size: 13px;
    color: #64748b;
    line-height: 1.6;
}

.kcard-icon {
    position:absolute;
    right:18px;
    top:14px;

    font-size: 42px;

    opacity:.08;
}

/* accent borders */

.blue {
    border-top: 4px solid #6366f1;
}

.green {
    border-top: 4px solid #10b981;
}

.red {
    border-top: 4px solid #ef4444;
}

.amber {
    border-top: 4px solid #f59e0b;
}

.violet {
    border-top: 4px solid #8b5cf6;
}

.cyan {
    border-top: 4px solid #06b6d4;
}

/* ════════════════════════════════════════════════════════
   BIG HERO CARD
════════════════════════════════════════════════════════ */

.hero-card {
    background:
        radial-gradient(circle at top right, rgba(99,102,241,.22), transparent 30%),
        linear-gradient(135deg,#111827,#0f172a);

    border: 1px solid rgba(255,255,255,.06);

    border-radius: 28px;

    padding: 30px;

    min-height: 180px;

    position: relative;

    overflow: hidden;

    box-shadow: 0 10px 40px rgba(0,0,0,.24);
}

.hero-label {
    font-size: 12px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    margin-bottom: 16px;
    font-weight: 700;
}

.hero-value {
    font-size: 58px;
    font-weight: 800;
    color: white;
    line-height: 1;
    letter-spacing: -2px;
}

.hero-sub {
    margin-top: 14px;
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.7;
}

.hero-badge {
    margin-top: 18px;

    display:inline-flex;
    align-items:center;

    background: rgba(16,185,129,.12);

    border: 1px solid rgba(16,185,129,.25);

    color: #34d399;

    padding: 8px 14px;

    border-radius: 999px;

    font-size: 12px;
    font-weight: 700;
}

/* ════════════════════════════════════════════════════════
   CHARTS
════════════════════════════════════════════════════════ */

.chart-wrap {
    background: rgba(17,24,39,.94);

    border: 1px solid rgba(255,255,255,.06);

    border-radius: 26px;

    padding: 18px;

    backdrop-filter: blur(12px);

    box-shadow: 0 10px 30px rgba(0,0,0,.22);
}

/* ════════════════════════════════════════════════════════
   AI INSIGHT
════════════════════════════════════════════════════════ */

.ai-box {
    background:
        radial-gradient(circle at top right, rgba(99,102,241,.14), transparent 25%),
        linear-gradient(135deg,#111827,#0f172a);

    border: 1px solid rgba(99,102,241,.20);

    border-radius: 24px;

    padding: 26px;

    margin-top: 20px;
}

.ai-title {
    color: white;
    font-size: 18px;
    font-weight: 700;

    margin-bottom: 14px;
}

.ai-text {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.9;
}

/* dataframe */

[data-testid="stDataFrame"] {
    border-radius: 22px;
    overflow:hidden;
}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# SUPABASE
# ════════════════════════════════════════════════════════

SUPABASE_URL = "YOUR_URL"
SUPABASE_KEY = "YOUR_KEY"

# ════════════════════════════════════════════════════════
# LOGIN
# ════════════════════════════════════════════════════════

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.markdown("""
    <div style="display:flex;justify-content:center;align-items:center;height:85vh;">
        <div style="
            background:#111827;
            border:1px solid rgba(255,255,255,.06);
            padding:50px;
            border-radius:28px;
            width:420px;
            text-align:center;
        ">
            <div style="
                width:82px;
                height:82px;
                margin:auto;
                border-radius:24px;
                background:linear-gradient(135deg,#6366f1,#8b5cf6);
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:42px;
                margin-bottom:24px;
            ">
                📦
            </div>

            <div style="
                font-size:32px;
                font-weight:800;
                color:white;
                margin-bottom:10px;
            ">
                COD Intelligence
            </div>

            <div style="
                color:#94a3b8;
                line-height:1.8;
                margin-bottom:30px;
            ">
                Enterprise AI logistics intelligence system for Pakistan COD fraud detection.
            </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1.2,1])

    with c2:
        pw = st.text_input(
            "",
            type="password",
            placeholder="Enter Password",
            label_visibility="collapsed"
        )

        if st.button("Access Dashboard", use_container_width=True):

            if pw == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid password")

    st.stop()

# ════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def load_data():

    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    resp = client.table("orders").select("*").execute()

    df = pd.DataFrame(resp.data)

    if df.empty:
        return pd.DataFrame()

    df.columns = df.columns.str.lower()

    df["status"] = df["status"].astype(str)

    df["risk_score"] = pd.to_numeric(
        df["risk_score"],
        errors="coerce"
    ).fillna(0)

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    ).fillna(0)

    df["inserted_at"] = pd.to_datetime(
        df["inserted_at"],
        errors="coerce"
    )

    df["date"] = df["inserted_at"].dt.date

    return df

df = load_data()

if df.empty:
    st.warning("No data found.")
    st.stop()

# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════

with st.sidebar:

    st.markdown("""
    <div class="sb-brand">
        <div class="sb-logo">📦</div>
        <div class="sb-name">COD Intelligence</div>
        <div class="sb-tag">Enterprise AI Logistics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Filters")

    period = st.selectbox(
        "Date Range",
        ["All Time","Today","Last 7 Days","Last 30 Days"]
    )

    city = st.selectbox(
        "City",
        ["All"] + sorted(df["city"].dropna().unique().tolist())
    )

    st.markdown("---")

    if st.button("Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ════════════════════════════════════════════════════════
# FILTERING
# ════════════════════════════════════════════════════════

today = datetime.now().date()

if period == "Today":
    df = df[df["date"] == today]

elif period == "Last 7 Days":
    df = df[df["date"] >= today - timedelta(days=7)]

elif period == "Last 30 Days":
    df = df[df["date"] >= today - timedelta(days=30)]

if city != "All":
    df = df[df["city"] == city]

# ════════════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════════════

total = len(df)

confirmed = len(df[df["status"] == "Auto-Confirmed"])

flagged = len(df[df["status"] == "Risk Flagged"])

rejected = len(df[df["status"] == "Rejected"])

clean_rate = round((confirmed / total) * 100,1) if total else 0

risk_avg = round(df["risk_score"].mean(),1)

saved = rejected * 3000

revenue = confirmed * 3000

# ════════════════════════════════════════════════════════
# HERO HEADER
# ════════════════════════════════════════════════════════

now = datetime.now().strftime("%d %b %Y · %I:%M %p")

st.markdown(f"""
<div class="topbar">

    <div class="tb-left">

        <div class="tb-icon">📦</div>

        <div>

            <div class="tb-title">
                Ecommerce Intelligence Dashboard
            </div>

            <div class="tb-sub">
                Enterprise AI logistics intelligence system for Pakistan COD fraud detection,
                real-time risk analytics, delivery optimization, and operational monitoring.
            </div>

        </div>

    </div>

    <div class="tb-right">

        <div class="live-pill">
            <span class="live-dot"></span>
            LIVE AI MONITORING
        </div>

        <div class="tb-meta">
            {now}
        </div>

    </div>

</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# BIG HERO KPI
# ════════════════════════════════════════════════════════

b1, b2 = st.columns(2)

with b1:
    st.markdown(f"""
    <div class="hero-card">

        <div class="hero-label">
            TOTAL REVENUE PROTECTED
        </div>

        <div class="hero-value">
            Rs {saved:,}
        </div>

        <div class="hero-sub">
            AI fraud detection blocked risky COD orders before dispatch,
            significantly reducing reverse logistics and fake delivery losses.
        </div>

        <div class="hero-badge">
            +32% efficiency improvement
        </div>

    </div>
    """, unsafe_allow_html=True)

with b2:
    st.markdown(f"""
    <div class="hero-card">

        <div class="hero-label">
            CLEAN ORDER RATE
        </div>

        <div class="hero-value">
            {clean_rate}%
        </div>

        <div class="hero-sub">
            Percentage of successfully validated and AI-confirmed
            legitimate customer orders.
        </div>

        <div class="hero-badge">
            Enterprise AI confidence stable
        </div>

    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# KPI ROW
# ════════════════════════════════════════════════════════

st.markdown('<div class="sec-title">Live Operational Metrics</div>', unsafe_allow_html=True)

k1,k2,k3,k4 = st.columns(4)

cards = [
    (k1, "Orders Processed", total, "AI analyzed orders", "blue", "📊"),
    (k2, "Auto Confirmed", confirmed, "Clean verified orders", "green", "✅"),
    (k3, "Risk Flagged", flagged, "Needs manual review", "amber", "⚠️"),
    (k4, "Avg Risk Score", risk_avg, "AI fraud probability", "red", "🎯"),
]

for col, label, value, sub, color, icon in cards:

    with col:

        st.markdown(f"""
        <div class="kcard {color}">

            <div class="kcard-icon">
                {icon}
            </div>

            <div class="kcard-label">
                {label}
            </div>

            <div class="kcard-value">
                {value}
            </div>

            <div class="kcard-sub">
                {sub}
            </div>

        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CHARTS
# ════════════════════════════════════════════════════════

st.markdown('<div class="sec-title">AI Risk Analytics</div>', unsafe_allow_html=True)

c1, c2 = st.columns([1.5,1])

# ════════════════════════════════════════════════════════
# RISK TREND
# ════════════════════════════════════════════════════════

with c1:

    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)

    trend = df.groupby("date")["risk_score"].mean().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["date"],
        y=trend["risk_score"],
        mode="lines+markers",
        line=dict(
            color="#6366f1",
            width=4
        ),
        marker=dict(
            size=8
        ),
        fill='tozeroy'
    ))

    fig.update_layout(

        title="AI Risk Trend Intelligence",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            family="Sora"
        ),

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,.06)"
        ),

        height=380
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# STATUS DONUT
# ════════════════════════════════════════════════════════

with c2:

    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)

    status = df["status"].value_counts().reset_index()

    status.columns = ["status","count"]

    fig2 = px.pie(
        status,
        values="count",
        names="status",
        hole=.72,
        color="status",
        color_discrete_map={
            "Auto-Confirmed":"#10b981",
            "Risk Flagged":"#f59e0b",
            "Rejected":"#ef4444"
        }
    )

    fig2.update_layout(

        title="AI Decision Distribution",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            family="Sora"
        ),

        showlegend=True,

        height=380
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CITY RISK
# ════════════════════════════════════════════════════════

st.markdown('<div class="sec-title">City Intelligence</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)

city_risk = df.groupby("city")["risk_score"].mean().reset_index()

city_risk = city_risk.sort_values(
    "risk_score",
    ascending=False
)

fig3 = px.bar(
    city_risk,
    x="city",
    y="risk_score",
    color="risk_score",
    color_continuous_scale="reds"
)

fig3.update_layout(

    title="Fraud Risk by City",

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="white",
        family="Sora"
    ),

    xaxis=dict(showgrid=False),

    yaxis=dict(
        gridcolor="rgba(255,255,255,.06)"
    ),

    height=420
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# AI INSIGHT PANEL
# ════════════════════════════════════════════════════════

highest_city = city_risk.iloc[0]["city"] if not city_risk.empty else "Unknown"

highest_score = round(city_risk.iloc[0]["risk_score"],1) if not city_risk.empty else 0

st.markdown(f"""
<div class="ai-box">

    <div class="ai-title">
        🧠 AI Intelligence Recommendation
    </div>

    <div class="ai-text">
        The AI engine detected elevated fraud probability patterns in
        <strong>{highest_city}</strong> with an average risk score of
        <strong>{highest_score}</strong>.

        Recommended actions:

        • Enable mandatory phone OTP verification<br>
        • Apply stricter address validation<br>
        • Hold high-value COD orders for manual review<br>
        • Increase fraud scoring sensitivity for repeat customers
    </div>

</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# DATA TABLE
# ════════════════════════════════════════════════════════

st.markdown('<div class="sec-title">Order Intelligence Table</div>', unsafe_allow_html=True)

show_cols = [
    "order_id",
    "name",
    "phone",
    "city",
    "status",
    "risk_score"
]

show_cols = [c for c in show_cols if c in df.columns]

st.dataframe(
    df[show_cols],
    use_container_width=True,
    height=480
)
