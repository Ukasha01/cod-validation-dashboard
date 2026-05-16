import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from datetime import datetime, timedelta

# ════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════
st.set_page_config(
    page_title="COD Intelligence",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════════════
# MASTER CSS
# ════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
    box-sizing: border-box;
}

.stApp { background: #f0f2f8; }
.block-container { padding: 2rem 2.4rem 3rem !important; max-width: 1480px !important; }

/* ══ SIDEBAR ══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #1a1d2e !important;
    border-right: none !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] * { color: #c8cde8 !important; }
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stNumberInput > label {
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    color: #5a6080 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #252840 !important;
    border-color: #32365a !important;
    color: #c8cde8 !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] input {
    background: #252840 !important;
    border-color: #32365a !important;
    color: #c8cde8 !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] hr { border-color: #252840 !important; }

/* ══ TOPBAR ═══════════════════════════════════════════ */
.topbar {
    background: linear-gradient(135deg, #1a1d2e 0%, #252840 50%, #1e2238 100%);
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 24px rgba(26,29,46,0.18);
    position: relative;
    overflow: hidden;
}
.topbar::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(99,102,241,0.25), transparent 70%);
    border-radius: 50%;
}
.topbar::after {
    content: '';
    position: absolute;
    bottom: -20px; left: 200px;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(16,185,129,0.15), transparent 70%);
    border-radius: 50%;
}
.tb-left { display: flex; align-items: center; gap: 18px; z-index: 1; }
.tb-icon {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    box-shadow: 0 6px 20px rgba(99,102,241,0.4);
    flex-shrink: 0;
}
.tb-title {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.3px;
    line-height: 1.2;
}
.tb-sub {
    font-size: 13px;
    color: #8890b8;
    font-weight: 400;
    margin-top: 3px;
}
.tb-right { display: flex; flex-direction: column; align-items: flex-end; gap: 8px; z-index: 1; }
.live-pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.35);
    color: #10b981;
    font-size: 11px; font-weight: 700;
    padding: 6px 14px;
    border-radius: 30px;
    letter-spacing: 0.5px;
}
.live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #10b981;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }
.tb-meta { font-size: 12px; color: #5a6080; }

/* ══ SECTION TITLE ════════════════════════════════════ */
.sec-title {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #6b7494;
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.sec-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #d4d9ee, transparent);
}

/* ══ KPI CARDS ════════════════════════════════════════ */
.kcard {
    background: #ffffff;
    border-radius: 18px;
    padding: 22px 20px 18px;
    border: 1.5px solid #e8ecf8;
    box-shadow: 0 1px 4px rgba(26,29,46,0.05), 0 4px 16px rgba(26,29,46,0.04);
    position: relative;
    overflow: hidden;
    transition: all 0.22s ease;
    height: 100%;
}
.kcard:hover {
    box-shadow: 0 4px 20px rgba(26,29,46,0.12);
    transform: translateY(-3px);
    border-color: #d0d5f0;
}
.kcard-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 18px 18px 0 0;
}
.kcard-bg-icon {
    position: absolute;
    right: 14px; top: 12px;
    font-size: 36px;
    opacity: 0.07;
    line-height: 1;
}
.kcard-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.9px;
    text-transform: uppercase;
    color: #8890b8;
    margin-bottom: 12px;
}
.kcard-value {
    font-size: 34px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: -1px;
}
.kcard-sub {
    font-size: 12px;
    color: #a0acc8;
    font-weight: 500;
}
/* color themes */
.kc-blue  .kcard-bar { background: linear-gradient(90deg,#6366f1,#818cf8); }
.kc-blue  .kcard-value { color: #4f46e5; }
.kc-green .kcard-bar { background: linear-gradient(90deg,#10b981,#34d399); }
.kc-green .kcard-value { color: #059669; }
.kc-amber .kcard-bar { background: linear-gradient(90deg,#f59e0b,#fbbf24); }
.kc-amber .kcard-value { color: #d97706; }
.kc-red   .kcard-bar { background: linear-gradient(90deg,#ef4444,#f87171); }
.kc-red   .kcard-value { color: #dc2626; }
.kc-violet .kcard-bar { background: linear-gradient(90deg,#8b5cf6,#a78bfa); }
.kc-violet .kcard-value { color: #7c3aed; }
.kc-cyan  .kcard-bar { background: linear-gradient(90deg,#06b6d4,#22d3ee); }
.kc-cyan  .kcard-value { color: #0891b2; }
.kc-rose  .kcard-bar { background: linear-gradient(90deg,#f43f5e,#fb7185); }
.kc-rose  .kcard-value { color: #e11d48; }

/* ══ INSIGHT CARDS ════════════════════════════════════ */
.icard {
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 13px;
    border: 1.5px solid;
    transition: transform 0.18s;
}
.icard:hover { transform: translateX(3px); }
.icard-title { font-size: 14px; font-weight: 700; color: #1a1d2e; margin-bottom: 7px; }
.icard-body  { font-size: 13px; color: #4a5278; line-height: 1.7; }
.icard-body strong { color: #1a1d2e; }

.ic-green  { background: #f0fdf8; border-color: #a7f3d0; }
.ic-amber  { background: #fffbf0; border-color: #fde68a; }
.ic-red    { background: #fff5f5; border-color: #fecaca; }
.ic-blue   { background: #f0f5ff; border-color: #bfdbfe; }
.ic-violet { background: #f8f5ff; border-color: #ddd6fe; }
.ic-cyan   { background: #f0fbff; border-color: #a5f3fc; }

/* ══ CHART WRAPPER ════════════════════════════════════ */
.chart-wrap {
    background: #ffffff;
    border-radius: 18px;
    border: 1.5px solid #e8ecf8;
    box-shadow: 0 1px 4px rgba(26,29,46,0.05);
    padding: 8px 6px 4px;
    height: 100%;
}

/* ══ DATAFRAME ════════════════════════════════════════ */
[data-testid="stDataFrame"] { border-radius: 16px !important; overflow: hidden; }
.stDataFrame { border: 1.5px solid #e8ecf8 !important; border-radius: 16px !important; }

/* ══ SIDEBAR BRAND ════════════════════════════════════ */
.sb-brand {
    padding: 20px 8px 16px;
    border-bottom: 1px solid #252840;
    margin-bottom: 8px;
}
.sb-logo {
    width: 40px; height: 40px;
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    border-radius: 12px;
    display: flex; align-items:center; justify-content:center;
    font-size: 20px; margin-bottom: 10px;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35);
}
.sb-name { font-size: 16px; font-weight: 800; color: #e8ecff !important; }
.sb-tag  { font-size: 9.5px; font-weight: 700; letter-spacing: 1.5px; color: #4a5080 !important; text-transform: uppercase; }

/* ══ LOGIN ════════════════════════════════════════════ */
.login-bg {
    min-height: 80vh;
    display: flex; align-items: center; justify-content: center;
}
.login-card {
    background: #fff;
    border-radius: 24px;
    border: 1.5px solid #e8ecf8;
    box-shadow: 0 12px 48px rgba(26,29,46,0.10);
    padding: 48px 44px;
    max-width: 420px;
    text-align: center;
}
.login-icon {
    width: 72px; height: 72px;
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    border-radius: 20px;
    display: flex; align-items:center; justify-content:center;
    font-size: 34px; margin: 0 auto 24px;
    box-shadow: 0 8px 24px rgba(99,102,241,0.35);
}
.login-title { font-size: 26px; font-weight: 800; color: #1a1d2e; letter-spacing: -0.5px; margin-bottom: 6px; }
.login-sub   { font-size: 13.5px; color: #8890b8; font-weight: 400; margin-bottom: 32px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CREDENTIALS
# ════════════════════════════════════════════════════════
SUPABASE_URL = "https://obzbfrakrzkywshwrbne.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iemJmcmFrcnpreXdzaHdyYm5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5ODM0NDEsImV4cCI6MjA5MzU1OTQ0MX0.gKDqt9wWsZdriuXWUDNMi10F26zojmTzg-GKsbwImA0"

# ════════════════════════════════════════════════════════
# LOGIN PAGE
# ════════════════════════════════════════════════════════
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("""
    <div style="max-width:420px;margin:60px auto;text-align:center;">
      <div class="login-icon">📦</div>
      <div class="login-title">COD Intelligence</div>
      <div class="login-sub">Pakistan's AI-powered eCommerce<br>order validation platform</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.6, 1])
    with c2:
        pw = st.text_input("", type="password", placeholder="🔐  Enter your password",
                           label_visibility="collapsed")
        if st.button("Sign In  →", use_container_width=True, type="primary"):
            if pw == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    st.stop()

# ════════════════════════════════════════════════════════
# DATA LOAD  (cached 60s)
# ════════════════════════════════════════════════════════
@st.cache_data(ttl=60)
def load_data():
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        resp   = client.table("orders").select("*").order("inserted_at", desc=True).execute()
        df     = pd.DataFrame(resp.data)
        if df.empty:
            return pd.DataFrame()
        df.columns   = df.columns.str.strip().str.lower()
        df["status"]     = df["status"].astype(str).str.strip()
        df["city"]       = df["city"].astype(str).str.strip().str.title()
        df["risk_level"] = df.get("risk_level", pd.Series(dtype=str)).astype(str).str.strip().str.upper()
        df["risk_score"] = pd.to_numeric(df.get("risk_score", 0), errors="coerce").fillna(0)
        df["price"]      = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
        if "inserted_at" in df.columns:
            df["inserted_at"] = pd.to_datetime(df["inserted_at"], errors="coerce")
            df["date"]        = df["inserted_at"].dt.date
        return df
    except Exception as e:
        st.error(f"Supabase error: {e}")
        return pd.DataFrame()

# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-logo">📦</div>
      <div class="sb-name">COD Intelligence</div>
      <div class="sb-tag">Pakistan · AI Validation</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**📅 DATE RANGE**")
    date_range = st.selectbox("dr", ["All time","Today","Last 7 days","Last 30 days"],
                              label_visibility="collapsed")
    st.markdown("**📋 ORDER STATUS**")
    status_filter = st.selectbox("sf", ["All","Auto-Confirmed","Risk Flagged","Rejected","Pending"],
                                 label_visibility="collapsed")
    st.markdown("**⚠️ RISK LEVEL**")
    risk_filter = st.selectbox("rf", ["All","CRITICAL","HIGH","MEDIUM","LOW"],
                               label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**💰 FINANCIAL SETTINGS**")
    avg_order_val = st.number_input("Avg Order Value (Rs)", value=3000, step=500, min_value=0)
    shipping_cost = st.number_input("Shipping Cost (Rs)",   value=250,  step=50,  min_value=0)
    reverse_cost  = st.number_input("Reverse Cost (Rs)",    value=150,  step=50,  min_value=0)

    st.markdown("---")
    col_r, col_l = st.columns(2)
    with col_r:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear(); st.rerun()
    with col_l:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False; st.rerun()

# ════════════════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════════════════
df_raw = load_data()
if df_raw.empty:
    st.warning("No data found in Supabase. Check your connection.")
    st.stop()

all_cities = sorted(df_raw["city"].dropna().unique().tolist())
with st.sidebar:
    st.markdown("**🏙️ CITY**")
    city_filter = st.selectbox("cf", ["All"] + all_cities, label_visibility="collapsed")

# Date filter
df = df_raw.copy()
today = datetime.now().date()
if "date" in df.columns:
    if date_range == "Today":
        df = df[df["date"] == today]
    elif date_range == "Last 7 days":
        df = df[df["date"] >= today - timedelta(days=7)]
    elif date_range == "Last 30 days":
        df = df[df["date"] >= today - timedelta(days=30)]

df_pending = df[df["status"] == "Pending"]
df_proc    = df[~df["status"].isin(["Pending","","Not Checked"])]

df_view = df_proc.copy()
if status_filter != "All": df_view = df_view[df_view["status"]     == status_filter]
if city_filter   != "All": df_view = df_view[df_view["city"]       == city_filter]
if risk_filter   != "All": df_view = df_view[df_view["risk_level"] == risk_filter]

# ════════════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════════════
total     = len(df_proc)
confirmed = len(df_proc[df_proc["status"] == "Auto-Confirmed"])
flagged   = len(df_proc[df_proc["status"] == "Risk Flagged"])
rejected  = len(df_proc[df_proc["status"] == "Rejected"])
pending   = len(df_pending)

rto_unit      = shipping_cost + reverse_cost
clean_pct     = round(confirmed / total * 100, 1) if total else 0
risk_pct      = round((flagged + rejected) / total * 100, 1) if total else 0
avg_risk      = round(df_proc["risk_score"].mean(), 1) if total else 0

saved         = rejected  * avg_order_val
money_at_risk = flagged   * avg_order_val
rto_loss      = rejected  * rto_unit
conf_revenue  = confirmed * avg_order_val
worst_case    = (flagged + rejected) * rto_unit

fl_df         = df_proc[df_proc["status"].isin(["Risk Flagged","Rejected"])]
avg_fl_risk   = round(fl_df["risk_score"].mean(), 1) if len(fl_df) else 0
critical_cnt  = len(df_proc[df_proc["risk_score"] >= 85])
border_cnt    = len(df_proc[(df_proc["risk_score"] >= 60) & (df_proc["risk_score"] < 85)])

# ════════════════════════════════════════════════════════
# TOP BAR
# ════════════════════════════════════════════════════════
now_str = datetime.now().strftime("%d %b %Y · %I:%M %p")
st.markdown(f"""
<div class="topbar">
  <div class="tb-left">
    <div class="tb-icon">📦</div>
    <div>
      <div class="tb-title">eCommerce Intelligence Dashboard</div>
      <div class="tb-sub">AI-powered COD Order Validation System · Pakistan</div>
    </div>
  </div>
  <div class="tb-right">
    <div class="live-pill"><span class="live-dot"></span> LIVE · auto-refresh 60s</div>
    <div class="tb-meta">{now_str} &nbsp;·&nbsp; {total} processed &nbsp;·&nbsp; {pending} pending</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# KPI ROW 1  — ORDER OVERVIEW
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Order Overview</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
order_kpis = [
    (k1, "Total Processed",  total,     "",                        "blue",   "📊"),
    (k2, "Auto-Confirmed",   confirmed, f"{clean_pct}% clean rate","green",  "✅"),
    (k3, "Risk Flagged",     flagged,   "awaiting manual review",  "amber",  "⚠️"),
    (k4, "Rejected",         rejected,  "blocked before dispatch", "red",    "❌"),
    (k5, "Pending / Stuck",  pending,   "AI not yet processed",    "violet", "⏳"),
    (k6, "Avg Risk Score",   avg_risk,  "0 = clean · 100 = fake", "cyan",   "🎯"),
]
for col, label, val, sub, color, icon in order_kpis:
    with col:
        st.markdown(f"""
        <div class="kcard kc-{color}">
          <div class="kcard-bar"></div>
          <div class="kcard-bg-icon">{icon}</div>
          <div class="kcard-label">{label}</div>
          <div class="kcard-value">{val}</div>
          <div class="kcard-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)
# ════════════════════════════════════════════════════════
# KPI ROW 2  — FINANCIAL
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Financial Impact</div>', unsafe_allow_html=True)

f1,f2,f3,f4,f5 = st.columns(5)
fin_kpis = [
    (f1, "Confirmed Revenue",   f"Rs {conf_revenue:,}",   "from clean orders",            "green",  "💰"),
    (f2, "Money at Risk",       f"Rs {money_at_risk:,}",  "flagged, not dispatched",      "amber",  "⚠️"),
    (f3, "RTO Loss Cost",       f"Rs {rto_loss:,}",       "shipping + reverse logistics", "red",    "📦"),
    (f4, "Saved by AI",         f"Rs {saved:,}",          "bad orders blocked",           "green",  "🛡️"),
    (f5, "Worst Case Exposure", f"Rs {worst_case:,}",     "if all flagged orders return", "rose",   "⛔"),
]
# CORRECT  — columns are already inside fin_kpis
fin_kpis = [
    (f1, "Confirmed Revenue",   f"Rs {conf_revenue:,}",  "from clean orders",            "green", "💰"),
    (f2, "Money at Risk",       f"Rs {money_at_risk:,}", "flagged, not dispatched",      "amber", "⚠️"),
    (f3, "RTO Loss Cost",       f"Rs {rto_loss:,}",      "shipping + reverse logistics", "red",   "📦"),
    (f4, "Saved by AI",         f"Rs {saved:,}",         "bad orders blocked",           "green", "🛡️"),
    (f5, "Worst Case Exposure", f"Rs {worst_case:,}",    "if all flagged orders return", "rose",  "⛔"),
]
for col, label, val, sub, color, icon in fin_kpis:
    with col:
        st.markdown(f"""...""", unsafe_allow_html=True)    with col:
        <div class="kcard kc-{color}">
          <div class="kcard-bar"></div>
          <div class="kcard-bg-icon">{icon}</div>
          <div class="kcard-label">{label}</div>
          <div class="kcard-value" style="font-size:24px;letter-spacing:-0.5px">{val}</div>
          <div class="kcard-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CHARTS  (3 columns)
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Analytics</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.05, 1.45, 0.95])

PAPER = "rgba(0,0,0,0)"
FONT  = "Sora"

# ── Chart 1: Status donut ──────────────────────────────
with c1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    sc = df_proc["status"].value_counts().reset_index()
    sc.columns = ["status","count"]
    cmap = {"Auto-Confirmed":"#10b981","Risk Flagged":"#f59e0b",
            "Rejected":"#ef4444","Pending":"#8b5cf6"}
    fig1 = px.pie(sc, values="count", names="status", hole=0.62,
                  color="status", color_discrete_map=cmap,
                  title="Order Status Split")
    fig1.update_traces(
        textposition="outside", textfont=dict(size=12, family=FONT),
        marker=dict(line=dict(color="#f0f2f8", width=3))
    )
    fig1.add_annotation(
        text=f"<b style='font-size:20px'>{clean_pct}%</b><br>confirmed",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#1a1d2e", family=FONT)
    )
    fig1.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER, font_family=FONT,
        title_font=dict(size=14, color="#1a1d2e", family=FONT),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center",
                    font=dict(size=11, color="#4a5278")),
        margin=dict(t=44, b=28, l=10, r=10), height=300
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 2: Stacked city bar ──────────────────────────
with c2:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    if "city" in df_proc.columns and total > 0:
        cs = df_proc.groupby("city")["status"].apply(
            lambda x: (x.isin(["Risk Flagged","Rejected"])).sum()
        ).reset_index()
        cs.columns = ["city","risky"]
        ct = df_proc.groupby("city").size().reset_index(name="total")
        cs = cs.merge(ct, on="city")
        cs["clean"] = cs["total"] - cs["risky"]
        cs["risk_pct"] = (cs["risky"] / cs["total"] * 100).round(1)
        cs = cs.sort_values("risk_pct", ascending=True).tail(9)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=cs["city"], x=cs["clean"], name="Confirmed",
            orientation="h", marker_color="#10b981",
            text=[f"{v}" for v in cs["clean"]],
            textposition="inside",
            textfont=dict(size=11, color="#fff", family=FONT)
        ))
        fig2.add_trace(go.Bar(
            y=cs["city"], x=cs["risky"], name="Flagged/Rejected",
            orientation="h", marker_color="#ef4444",
            text=[f"{v}" if v > 0 else "" for v in cs["risky"]],
            textposition="inside",
            textfont=dict(size=11, color="#fff", family=FONT)
        ))
        fig2.update_layout(
            barmode="stack",
            title=dict(text="Order Quality by City", font=dict(size=14, color="#1a1d2e", family=FONT)),
            paper_bgcolor=PAPER, plot_bgcolor=PAPER, font_family=FONT,
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(gridcolor="#f0f2f8", tickfont=dict(size=12.5, color="#1a1d2e")),
            legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center",
                        font=dict(size=11, color="#4a5278")),
            margin=dict(t=48, b=12, l=10, r=16), height=300,
            bargap=0.28
        )
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 3: Risk gauge ────────────────────────────────
with c3:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    gc = "#10b981" if avg_risk < 30 else ("#f59e0b" if avg_risk < 60 else "#ef4444")
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_risk,
        delta={"reference":30,
               "increasing":{"color":"#ef4444"},
               "decreasing":{"color":"#10b981"},
               "font":{"size":14}},
        title={"text":"Avg Risk Score<br><span style='font-size:11px;color:#8890b8'>lower = healthier</span>",
               "font":{"size":14, "color":"#1a1d2e", "family":FONT}},
        number={"font":{"size":46, "color":gc, "family":FONT}},
        gauge={
            "axis":{"range":[0,100],
                    "tickcolor":"#cbd5e8",
                    "tickfont":{"size":10,"color":"#8890b8"}},
            "bar":{"color":gc, "thickness":0.25},
            "bgcolor":"#f8fafd",
            "bordercolor":"#e8ecf8",
            "borderwidth":1.5,
            "steps":[
                {"range":[0,30],  "color":"#f0fdf8"},
                {"range":[30,70], "color":"#fffbf0"},
                {"range":[70,100],"color":"#fff5f5"},
            ],
            "threshold":{"line":{"color":"#ef4444","width":2.5},"value":70}
        }
    ))
    fig3.update_layout(
        paper_bgcolor=PAPER, font_family=FONT,
        margin=dict(t=44, b=8, l=22, r=22), height=300
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# BUSINESS INSIGHTS
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Business Insights</div>', unsafe_allow_html=True)

ins1, ins2 = st.columns(2)

with ins1:
    # Overall health
    if clean_pct >= 70:
        cls,icon,title = "ic-green","✅","Order Quality is Healthy"
        body = f"<strong>{clean_pct}%</strong> of orders are passing validation — a strong baseline. Keep monitoring for city-level spikes on a weekly basis."
    elif clean_pct >= 50:
        cls,icon,title = "ic-amber","⚠️","Order Quality Needs Attention"
        body = f"Only <strong>{clean_pct}%</strong> are confirmed clean. Review top-risk cities and add address hints at checkout to improve this number."
    else:
        cls,icon,title = "ic-red","🚨","Order Quality is Critical"
        body = f"Only <strong>{clean_pct}%</strong> passing — over half your orders carry risk. Review your checkout flow and address requirements immediately."
    st.markdown(f'<div class="icard {cls}"><div class="icard-title">{icon} {title}</div><div class="icard-body">{body}</div></div>', unsafe_allow_html=True)

    per1k = round(saved * 1000 / max(1, total))
    st.markdown(f'''<div class="icard ic-blue">
    <div class="icard-title">🛡️ AI System Value Generated</div>
    <div class="icard-body">Caught <strong>{rejected} bad orders</strong> before dispatch —
    protecting <strong>Rs {saved:,}</strong> from RTO losses.<br>
    At current rates: <strong>Rs {per1k:,} saved per 1,000 orders</strong> processed.</div>
    </div>''', unsafe_allow_html=True)

    daily_est = max(1, round(total / 7))
    net       = (saved * 4) - (rto_loss * 4)
    nc        = "#059669" if net >= 0 else "#dc2626"
    st.markdown(f'''<div class="icard ic-violet">
    <div class="icard-title">📈 Monthly Financial Projection</div>
    <div class="icard-body">
    ~{daily_est} orders/day estimate based on current data<br>
    Projected RTO loss: <strong>Rs {rto_loss*4:,}</strong><br>
    Projected AI savings: <strong>Rs {saved*4:,}</strong><br>
    Net position: <strong style="color:{nc};font-size:15px">Rs {net:,}</strong>
    </div></div>''', unsafe_allow_html=True)

    if pending > 0:
        st.markdown(f'''<div class="icard ic-amber">
        <div class="icard-title">⏳ {pending} Orders Not Yet Processed</div>
        <div class="icard-body">These orders are stuck in <strong>Pending</strong> status — the AI validation hasn't run yet.
        Check your n8n workflow. They may be stuck at the Wait node or failed at the Gemini step.</div>
        </div>''', unsafe_allow_html=True)

with ins2:
    if "city" in df_proc.columns and total > 0:
        cr = df_proc[df_proc["status"].isin(["Risk Flagged","Rejected"])]["city"].value_counts()
        ct = df_proc["city"].value_counts()
        if not cr.empty:
            tc = cr.index[0]; tn = cr.iloc[0]
            tt = ct.get(tc, 1); tp = round(tn/tt*100,1)
            st.markdown(f'''<div class="icard ic-red">
            <div class="icard-title">🗺️ Highest Risk City: {tc}</div>
            <div class="icard-body"><strong>{tn} flagged or rejected</strong> out of {tt} orders from {tc}
            — that's a <strong>{tp}% risk rate</strong>.<br>
            Consider adding stricter address validation at checkout specifically for {tc} orders.</div>
            </div>''', unsafe_allow_html=True)

        crate = {}
        for city in ct.index:
            cdf = df_proc[df_proc["city"] == city]
            if len(cdf) >= 2:
                crate[city] = len(cdf[cdf["status"].isin(["Risk Flagged","Rejected"])]) / len(cdf)
        if crate:
            sc2 = min(crate, key=crate.get)
            sp  = round(crate[sc2]*100,1)
            st.markdown(f'''<div class="icard ic-green">
            <div class="icard-title">🟢 Most Reliable City: {sc2}</div>
            <div class="icard-body">Only <strong>{sp}% risk rate</strong> on orders from {sc2}.<br>
            Consider auto-confirming low-value orders from this city to speed up dispatch.</div>
            </div>''', unsafe_allow_html=True)

    st.markdown(f'''<div class="icard ic-amber">
    <div class="icard-title">📊 Risk Score Breakdown</div>
    <div class="icard-body">
    <strong>{critical_cnt} orders</strong> scored 85+ — high confidence fake or bad address<br>
    <strong>{border_cnt} orders</strong> scored 60–84 — borderline, manual review strongly advised<br>
    Overall average: <strong>{avg_risk}</strong> &nbsp;·&nbsp; Flagged orders average: <strong>{avg_fl_risk}</strong>
    </div></div>''', unsafe_allow_html=True)

    wce = money_at_risk + rto_loss
    st.markdown(f'''<div class="icard ic-red">
    <div class="icard-title">⛔ Total Current Exposure</div>
    <div class="icard-body">
    <strong>Rs {wce:,}</strong> currently exposed to delivery risk<br>
    Rs {money_at_risk:,} — flagged orders not dispatched (still recoverable)<br>
    Rs {rto_loss:,} — already lost to shipping + reverse logistics
    </div></div>''', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ORDER TABLE
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Order Details</div>', unsafe_allow_html=True)

show_cols = ["order_id","name","phone","address","city","status",
             "risk_score","risk_level","risk_reason","map_status","created_at"]
show_cols = [c for c in show_cols if c in df_view.columns]

def style_status(val):
    m = {"Rejected":       "background:#fff5f5;color:#dc2626;font-weight:700",
         "Risk Flagged":   "background:#fffbf0;color:#d97706;font-weight:700",
         "Auto-Confirmed": "background:#f0fdf8;color:#059669;font-weight:700"}
    return m.get(val, "")

def style_risk(val):
    m = {"CRITICAL": "background:#fff5f5;color:#dc2626;font-weight:700",
         "HIGH":     "background:#fff5f5;color:#dc2626",
         "MEDIUM":   "background:#fffbf0;color:#d97706",
         "LOW":      "background:#f0fdf8;color:#059669"}
    return m.get(val, "")

st.caption(f"Showing **{len(df_view)}** of **{total}** processed orders · **{pending}** pending excluded")

styled = df_view[show_cols].style
if "status"     in show_cols: styled = styled.map(style_status, subset=["status"])
if "risk_level" in show_cols: styled = styled.map(style_risk,   subset=["risk_level"])
if "risk_score" in show_cols:
    styled = styled.background_gradient(subset=["risk_score"], cmap="RdYlGn_r", vmin=0, vmax=100)

st.dataframe(
    styled,
    use_container_width=True,
    height=440,
    column_config={
        "order_id":    st.column_config.TextColumn("Order ID",   width=160),
        "name":        st.column_config.TextColumn("Customer",   width=120),
        "phone":       st.column_config.TextColumn("Phone",      width=115),
        "address":     st.column_config.TextColumn("Address",    width=230),
        "city":        st.column_config.TextColumn("City",       width=95),
        "status":      st.column_config.TextColumn("Status",     width=135),
        "risk_score":  st.column_config.NumberColumn("Score",    width=72, format="%d"),
        "risk_level":  st.column_config.TextColumn("Level",      width=80),
        "risk_reason": st.column_config.TextColumn("Reason",     width=290),
        "map_status":  st.column_config.TextColumn("Maps",       width=115),
        "created_at":  st.column_config.TextColumn("Date",       width=88),
    }
)

# ════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:32px 0 8px;color:#b0bcd4;font-size:12px;font-weight:500;letter-spacing:0.4px">
  COD Intelligence &nbsp;&nbsp; Pakistan eCommerce &nbsp;&nbsp;
  Powered by Supabase : Gemini AI : Google Maps
</div>
""", unsafe_allow_html=True)
