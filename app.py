import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="COD Intelligence",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════
# MASTER CSS — Full dark premium theme
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ══ APP BACKGROUND ══════════════════════════════════════════════ */
.stApp { background: #FDFCE9; }

.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1500px !important;
}

/* ══ HIDE STREAMLIT CHROME ═══════════════════════════════════════ */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
.stDeployButton { display: none; }

/* ══ SIDEBAR ═════════════════════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: #0B0E1A !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    width: 260px !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] * {
    color: #94A3B8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown strong {
    font-size: 10px !important;
    font-weight: 800 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #334155 !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #161929 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #E2E8F0 !important;
    background: #161929 !important;
}
[data-testid="stSidebar"] input {
    background: #161929 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}
[data-testid="stSidebar"] .stNumberInput button {
    background: #1E293B !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #94A3B8 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 14px 0 !important;
}
[data-testid="stSidebar"] .stButton button {
    background: #161929 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #94A3B8 !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    transition: all 0.18s !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: #1E293B !important;
    color: #E2E8F0 !important;
    border-color: rgba(255,255,255,0.15) !important;
}

/* ══ TOPBAR ══════════════════════════════════════════════════════ */
.topbar {
    background: linear-gradient(135deg, #0F172A 0%, #1a2235 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.topbar::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 65%);
    pointer-events: none;
}
.topbar::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 300px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(16,185,129,0.07) 0%, transparent 65%);
    pointer-events: none;
}
.tb-left {
    display: flex;
    align-items: center;
    gap: 16px;
    z-index: 1;
    flex: 0 0 auto;
}
.tb-icon {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35);
    flex-shrink: 0;
}
.tb-center {
    flex: 1;
    text-align: center;
    z-index: 1;
    padding: 0 20px;
}
.tb-title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 4px;
    background: linear-gradient(135deg, #60A5FA, #818CF8, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.tb-sub {
    font-size: 12.5px;
    color: #64748B;
    font-weight: 500;
}
.tb-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
    z-index: 1;
    flex: 0 0 auto;
}
.live-pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34D399;
    font-size: 11px; font-weight: 800;
    padding: 6px 14px;
    border-radius: 30px;
    letter-spacing: 0.4px;
    white-space: nowrap;
}
.live-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #10B981;
    animation: blink 2s infinite;
    flex-shrink: 0;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }
.tb-meta {
    font-size: 11.5px;
    color: #475569;
    font-weight: 500;
    white-space: nowrap;
}

/* ══ SECTION TITLE ═══════════════════════════════════════════════ */
.sec-title {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #64748B;
    margin: 24px 0 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sec-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
}

/* ══ KPI CARDS ═══════════════════════════════════════════════════ */
.kcard {
    background: #161929;
    border-radius: 16px;
    padding: 20px 18px 16px;
    border: 1px solid rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    height: 100%;
    min-height: 130px;
}
.kcard:hover {
    border-color: rgba(255,255,255,0.12);
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.kcard-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kcard-glow {
    position: absolute;
    top: -30px; right: -20px;
    width: 100px; height: 100px;
    border-radius: 50%;
    opacity: 0.08;
    pointer-events: none;
}
.kcard-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
    position: relative;
}
.kcard-value {
    font-size: 30px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: -1.5px;
    font-family: 'JetBrains Mono', monospace;
    position: relative;
}
.kcard-sub {
    font-size: 11px;
    color: #334155;
    font-weight: 500;
    position: relative;
}

.kc-blue  .kcard-bar { background: linear-gradient(90deg,#3B82F6,#60A5FA); }
.kc-blue  .kcard-value { color: #60A5FA; }
.kc-blue  .kcard-glow { background: #3B82F6; }

.kc-green .kcard-bar { background: linear-gradient(90deg,#10B981,#34D399); }
.kc-green .kcard-value { color: #34D399; }
.kc-green .kcard-glow { background: #10B981; }

.kc-amber .kcard-bar { background: linear-gradient(90deg,#F59E0B,#FCD34D); }
.kc-amber .kcard-value { color: #FCD34D; }
.kc-amber .kcard-glow { background: #F59E0B; }

.kc-red   .kcard-bar { background: linear-gradient(90deg,#EF4444,#F87171); }
.kc-red   .kcard-value { color: #F87171; }
.kc-red   .kcard-glow { background: #EF4444; }

.kc-violet .kcard-bar { background: linear-gradient(90deg,#8B5CF6,#A78BFA); }
.kc-violet .kcard-value { color: #A78BFA; }
.kc-violet .kcard-glow { background: #8B5CF6; }

.kc-cyan  .kcard-bar { background: linear-gradient(90deg,#06B6D4,#22D3EE); }
.kc-cyan  .kcard-value { color: #22D3EE; }
.kc-cyan  .kcard-glow { background: #06B6D4; }

.kc-rose  .kcard-bar { background: linear-gradient(90deg,#F43F5E,#FB7185); }
.kc-rose  .kcard-value { color: #FB7185; }
.kc-rose  .kcard-glow { background: #F43F5E; }

/* ══ CHART WRAPPER ═══════════════════════════════════════════════ */
.chart-wrap {
    background: #161929;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.06);
    padding: 20px 20px 12px;
}
.chart-title {
    font-size: 14px;
    font-weight: 700;
    color: #E2E8F0;
    margin-bottom: 4px;
    letter-spacing: -0.2px;
}
.chart-sub {
    font-size: 11px;
    color: #475569;
    margin-bottom: 14px;
}

/* ══ INSIGHT CARDS ═══════════════════════════════════════════════ */
.icard {
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 12px;
    border: 1px solid;
    transition: transform 0.18s;
}
.icard:hover { transform: translateX(3px); }
.icard-title {
    font-size: 13.5px;
    font-weight: 700;
    margin-bottom: 7px;
    line-height: 1.3;
}
.icard-body {
    font-size: 12.5px;
    line-height: 1.7;
    color: #94A3B8;
}
.icard-body strong { color: #CBD5E1; }

.ic-green  { background: rgba(16,185,129,0.07);  border-color: rgba(16,185,129,0.2);  }
.ic-green  .icard-title { color: #34D399; }
.ic-amber  { background: rgba(245,158,11,0.07);  border-color: rgba(245,158,11,0.2);  }
.ic-amber  .icard-title { color: #FCD34D; }
.ic-red    { background: rgba(239,68,68,0.07);   border-color: rgba(239,68,68,0.2);   }
.ic-red    .icard-title { color: #F87171; }
.ic-blue   { background: rgba(59,130,246,0.07);  border-color: rgba(59,130,246,0.2);  }
.ic-blue   .icard-title { color: #60A5FA; }
.ic-violet { background: rgba(139,92,246,0.07);  border-color: rgba(139,92,246,0.2);  }
.ic-violet .icard-title { color: #A78BFA; }

/* ══ TABLE ═══════════════════════════════════════════════════════ */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stDataFrame"] table {
    background: #161929 !important;
}
[data-testid="stDataFrame"] thead tr th {
    background: #0F1623 !important;
    color: #64748B !important;
    font-size: 10px !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    padding: 12px 14px !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background: rgba(255,255,255,0.03) !important;
}

/* ══ CAPTION ════════════════════════════════════════════════════ */
.stCaption { color: #334155 !important; font-size: 12px !important; }

/* ══ DIVIDER ════════════════════════════════════════════════════ */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ══ SCROLLBAR ══════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 4px; }

/* ══ LOGIN ═══════════════════════════════════════════════════════ */
.login-wrap {
    max-width: 400px;
    margin: 60px auto;
    text-align: center;
}
.login-icon {
    width: 70px; height: 70px;
    background: linear-gradient(135deg,#6366F1,#8B5CF6);
    border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px;
    margin: 0 auto 20px;
    box-shadow: 0 8px 28px rgba(99,102,241,0.4);
}
.login-title {
    font-size: 26px;
    font-weight: 800;
    color: #E2E8F0;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}
.login-sub {
    font-size: 14px;
    color: #475569;
    margin-bottom: 28px;
    line-height: 1.6;
}

/* ══ SIDEBAR BRAND ═══════════════════════════════════════════════ */
.sb-wrap {
    padding: 18px 16px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 4px;
}
.sb-logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg,#6366F1,#8B5CF6);
    border-radius: 11px;
    display: flex; align-items:center; justify-content:center;
    font-size: 20px;
    margin-bottom: 10px;
    box-shadow: 0 4px 14px rgba(99,102,241,0.3);
}
.sb-name { font-size: 15px !important; font-weight: 800 !important; color: #E2E8F0 !important; letter-spacing: -0.3px; }
.sb-tag  { font-size: 10px !important; color: #334155 !important; font-weight: 600 !important; letter-spacing: 0.8px; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# CREDENTIALS
# ══════════════════════════════════════════════════════════════════
SUPABASE_URL = "https://obzbfrakrzkywshwrbne.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iemJmcmFrcnpreXdzaHdyYm5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5ODM0NDEsImV4cCI6MjA5MzU1OTQ0MX0.gKDqt9wWsZdriuXWUDNMi10F26zojmTzg-GKsbwImA0"

# ══════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("""
    <div class="login-wrap">
      <div class="login-icon">📦</div>
      <div class="login-title">COD Intelligence</div>
      <div class="login-sub">Pakistan's AI-powered eCommerce<br>order validation platform</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        pw = st.text_input("", type="password",
                           placeholder="🔐  Enter your password",
                           label_visibility="collapsed")
        if st.button("Sign In →", use_container_width=True, type="primary"):
            if pw == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    st.stop()

# ══════════════════════════════════════════════════════════════════
# DATA LOAD
# ══════════════════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-wrap">
      <div class="sb-logo">📦</div>
      <div class="sb-name">COD Intelligence</div>
      <div class="sb-tag">PAKISTAN · AI VALIDATION</div>
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

# ══════════════════════════════════════════════════════════════════
# LOAD + FILTER
# ══════════════════════════════════════════════════════════════════
df_raw = load_data()
if df_raw.empty:
    st.warning("No data found. Check Supabase connection.")
    st.stop()

all_cities = sorted(df_raw["city"].dropna().unique().tolist())
with st.sidebar:
    st.markdown("**🏙️ CITY**")
    city_filter = st.selectbox("cf", ["All"] + all_cities, label_visibility="collapsed")

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

# ══════════════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════════════
total     = len(df_proc)
confirmed = len(df_proc[df_proc["status"] == "Auto-Confirmed"])
flagged   = len(df_proc[df_proc["status"] == "Risk Flagged"])
rejected  = len(df_proc[df_proc["status"] == "Rejected"])
pending   = len(df_pending)

rto_unit      = shipping_cost + reverse_cost
clean_pct     = round(confirmed / total * 100, 1) if total else 0
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
daily_est     = max(1, round(total / 7))
net           = (saved * 4) - (rto_loss * 4)

# ══════════════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════════════
now_str = datetime.now().strftime("%d %b %Y · %I:%M %p")
st.markdown(f"""
<div class="topbar">
  <div class="tb-left">
    <div class="tb-icon">📦</div>
  </div>
  <div class="tb-center">
    <div class="tb-title">eCommerce Intelligence Dashboard</div>
    <div class="tb-sub">AI-powered COD Order Validation System &nbsp;·&nbsp; Pakistan</div>
  </div>
  <div class="tb-right">
    <div class="live-pill"><span class="live-dot"></span> LIVE &nbsp;·&nbsp; auto-refresh 60s</div>
    <div class="tb-meta">{now_str} &nbsp;·&nbsp; {total} processed &nbsp;·&nbsp; {pending} pending</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# KPI ROW 1 — ORDER OVERVIEW
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Order Overview</div>', unsafe_allow_html=True)

k1,k2,k3,k4,k5,k6 = st.columns(6)
order_kpis = [
    (k1,"Total Processed", total,     "",                        "blue",   "📊"),
    (k2,"Auto-Confirmed",  confirmed, f"{clean_pct}% clean rate","green",  "✅"),
    (k3,"Risk Flagged",    flagged,   "awaiting review",         "amber",  "⚠️"),
    (k4,"Rejected",        rejected,  "blocked before dispatch", "red",    "❌"),
    (k5,"Pending / Stuck", pending,   "not yet processed",       "violet", "⏳"),
    (k6,"Avg Risk Score",  avg_risk,  "0 = clean · 100 = fake", "cyan",   "🎯"),
]
for col, label, val, sub, color, icon in order_kpis:
    with col:
        st.markdown(f"""
        <div class="kcard kc-{color}">
          <div class="kcard-bar"></div>
          <div class="kcard-glow"></div>
          <div class="kcard-label">{label}</div>
          <div class="kcard-value">{val}</div>
          <div class="kcard-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# KPI ROW 2 — FINANCIAL
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Financial Impact</div>', unsafe_allow_html=True)

f1,f2,f3,f4,f5 = st.columns(5)
fin_kpis = [
    (f1,"Confirmed Revenue",   f"Rs {conf_revenue:,}",  "from clean orders",           "green",  "💰"),
    (f2,"Money at Risk",       f"Rs {money_at_risk:,}", "flagged, not dispatched",     "amber",  "⚠️"),
    (f3,"RTO Loss Cost",       f"Rs {rto_loss:,}",      "shipping + reverse cost",     "red",    "📦"),
    (f4,"Saved by AI",         f"Rs {saved:,}",         "bad orders blocked",          "green",  "🛡️"),
    (f5,"Worst Case Exposure", f"Rs {worst_case:,}",    "if all flagged fail",         "rose",   "⛔"),
]
for col, label, val, sub, color, icon in fin_kpis:
    with col:
        st.markdown(f"""
        <div class="kcard kc-{color}">
          <div class="kcard-bar"></div>
          <div class="kcard-glow"></div>
          <div class="kcard-label">{label}</div>
          <div class="kcard-value" style="font-size:22px;letter-spacing:-0.5px">{val}</div>
          <div class="kcard-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# CHARTS — Dark theme settings
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Analytics</div>', unsafe_allow_html=True)

PAPER   = "rgba(0,0,0,0)"
PLOT_BG = "rgba(0,0,0,0)"
FONT    = "Plus Jakarta Sans"
GRID    = "rgba(255,255,255,0.04)"
TICK    = "#475569"
TEXT    = "#94A3B8"
TITLE_C = "#E2E8F0"

c1, c2, c3 = st.columns([1.05, 1.5, 0.95])

# ── Donut chart ───────────────────────────────────────────────────
with c1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Order Status Split</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Distribution by decision type</div>', unsafe_allow_html=True)
    sc_df = df_proc["status"].value_counts().reset_index()
    sc_df.columns = ["status","count"]
    cmap = {"Auto-Confirmed":"#10B981","Risk Flagged":"#F59E0B",
            "Rejected":"#EF4444","Pending":"#8B5CF6"}
    fig1 = px.pie(sc_df, values="count", names="status", hole=0.62,
                  color="status", color_discrete_map=cmap)
    fig1.update_traces(
        textposition="outside",
        textfont=dict(size=11, color=TEXT, family=FONT),
        marker=dict(line=dict(color="#0D0F1A", width=3))
    )
    fig1.add_annotation(
        text=f"<b>{clean_pct}%</b><br><span style='font-size:11px'>confirmed</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color="#E2E8F0", family=FONT)
    )
    fig1.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PLOT_BG,
        font_family=FONT, font_color=TEXT,
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    font=dict(size=11, color=TEXT)),
        margin=dict(t=10, b=28, l=10, r=10), height=270
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Stacked city bar ──────────────────────────────────────────────
with c2:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Order Quality by City</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Confirmed vs Flagged/Rejected per city</div>', unsafe_allow_html=True)
    if "city" in df_proc.columns and total > 0:
        cs = df_proc.groupby("city")["status"].apply(
            lambda x: (x.isin(["Risk Flagged","Rejected"])).sum()
        ).reset_index()
        cs.columns = ["city","risky"]
        ct = df_proc.groupby("city").size().reset_index(name="total")
        cs = cs.merge(ct, on="city")
        cs["clean"] = cs["total"] - cs["risky"]
        cs = cs.sort_values("risky", ascending=True).tail(9)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=cs["city"], x=cs["clean"], name="Confirmed",
            orientation="h", marker_color="#10B981",
            text=[str(v) for v in cs["clean"]],
            textposition="inside",
            textfont=dict(size=11, color="#fff", family=FONT)
        ))
        fig2.add_trace(go.Bar(
            y=cs["city"], x=cs["risky"], name="Flagged/Rejected",
            orientation="h", marker_color="#EF4444",
            text=[str(v) if v > 0 else "" for v in cs["risky"]],
            textposition="inside",
            textfont=dict(size=11, color="#fff", family=FONT)
        ))
        fig2.update_layout(
            barmode="stack",
            paper_bgcolor=PAPER, plot_bgcolor=PLOT_BG,
            font_family=FONT, font_color=TEXT,
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(gridcolor=GRID, tickfont=dict(size=12, color="#CBD5E1")),
            legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center",
                        font=dict(size=11, color=TEXT)),
            margin=dict(t=10, b=10, l=10, r=10), height=270,
            bargap=0.25
        )
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Risk gauge ────────────────────────────────────────────────────
with c3:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Avg Risk Score</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Lower is healthier</div>', unsafe_allow_html=True)
    gc = "#10B981" if avg_risk < 30 else ("#F59E0B" if avg_risk < 60 else "#EF4444")
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_risk,
        delta={"reference":30,
               "increasing":{"color":"#EF4444"},
               "decreasing":{"color":"#10B981"},
               "font":{"size":13}},
        number={"font":{"size":44, "color":gc, "family":FONT}},
        gauge={
            "axis":{"range":[0,100],
                    "tickcolor":TICK,
                    "tickfont":{"size":10,"color":TICK}},
            "bar":{"color":gc, "thickness":0.22},
            "bgcolor":"rgba(0,0,0,0)",
            "bordercolor":"rgba(255,255,255,0.08)",
            "borderwidth":1,
            "steps":[
                {"range":[0,30],  "color":"rgba(16,185,129,0.08)"},
                {"range":[30,70], "color":"rgba(245,158,11,0.08)"},
                {"range":[70,100],"color":"rgba(239,68,68,0.08)"},
            ],
            "threshold":{"line":{"color":"#EF4444","width":2},"value":70}
        }
    ))
    fig3.update_layout(
        paper_bgcolor=PAPER, font_family=FONT,
        margin=dict(t=10, b=8, l=20, r=20), height=270
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# BUSINESS INSIGHTS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Business Insights</div>', unsafe_allow_html=True)

ins1, ins2 = st.columns(2)

with ins1:
    if clean_pct >= 70:
        cls,icon,title = "ic-green","✅","Order Quality is Healthy"
        body = f"<strong>{clean_pct}%</strong> of orders passing — strong baseline. Monitor for city-level spikes weekly."
    elif clean_pct >= 50:
        cls,icon,title = "ic-amber","⚠️","Order Quality Needs Attention"
        body = f"Only <strong>{clean_pct}%</strong> are clean. Review top-risk cities and add address hints at checkout."
    else:
        cls,icon,title = "ic-red","🚨","Order Quality is Critical"
        body = f"Only <strong>{clean_pct}%</strong> passing — over half carry risk. Review checkout flow immediately."
    st.markdown(f'<div class="icard {cls}"><div class="icard-title">{icon} {title}</div><div class="icard-body">{body}</div></div>', unsafe_allow_html=True)

    per1k = round(saved * 1000 / max(1, total))
    st.markdown(f"""<div class="icard ic-blue">
    <div class="icard-title">🛡️ AI System Value Generated</div>
    <div class="icard-body">Caught <strong>{rejected} bad orders</strong> before dispatch — protecting <strong>Rs {saved:,}</strong> from RTO losses.<br>
    At current rates: <strong>Rs {per1k:,} saved per 1,000 orders</strong> processed.</div>
    </div>""", unsafe_allow_html=True)

    nc = "#34D399" if net >= 0 else "#F87171"
    st.markdown(f"""<div class="icard ic-violet">
    <div class="icard-title">📈 Monthly Financial Projection (~{daily_est} orders/day)</div>
    <div class="icard-body">
    Projected RTO loss: <strong>Rs {rto_loss*4:,}</strong><br>
    Projected AI savings: <strong>Rs {saved*4:,}</strong><br>
    Net position: <strong style="color:{nc};font-size:15px">Rs {net:,}</strong>
    </div></div>""", unsafe_allow_html=True)

    if pending > 0:
        st.markdown(f"""<div class="icard ic-amber">
        <div class="icard-title">⏳ {pending} Orders Stuck in Pending</div>
        <div class="icard-body">AI validation hasn't run yet. Check your n8n workflow — may be stuck at the Wait node or Gemini step.</div>
        </div>""", unsafe_allow_html=True)

with ins2:
    if "city" in df_proc.columns and total > 0:
        cr = df_proc[df_proc["status"].isin(["Risk Flagged","Rejected"])]["city"].value_counts()
        ct = df_proc["city"].value_counts()
        if not cr.empty:
            tc = cr.index[0]; tn = cr.iloc[0]
            tt = ct.get(tc, 1); tp = round(tn/tt*100, 1)
            st.markdown(f"""<div class="icard ic-red">
            <div class="icard-title">🗺️ Highest Risk City: {tc}</div>
            <div class="icard-body"><strong>{tn} flagged/rejected</strong> out of {tt} orders from {tc} — <strong>{tp}% risk rate</strong>.<br>
            Add stricter address validation at checkout for {tc} orders.</div>
            </div>""", unsafe_allow_html=True)

        crate = {}
        for city in ct.index:
            cdf = df_proc[df_proc["city"] == city]
            if len(cdf) >= 2:
                crate[city] = len(cdf[cdf["status"].isin(["Risk Flagged","Rejected"])]) / len(cdf)
        if crate:
            sc2 = min(crate, key=crate.get)
            sp  = round(crate[sc2]*100, 1)
            st.markdown(f"""<div class="icard ic-green">
            <div class="icard-title">🟢 Most Reliable City: {sc2}</div>
            <div class="icard-body">Only <strong>{sp}% risk rate</strong> from {sc2}.<br>
            Consider fast-tracking low-value orders here to speed up dispatch.</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="icard ic-amber">
    <div class="icard-title">📊 Risk Score Breakdown</div>
    <div class="icard-body">
    <strong>{critical_cnt} orders</strong> scored 85+ — high confidence fake or invalid<br>
    <strong>{border_cnt} orders</strong> scored 60–84 — borderline, manual review advised<br>
    Overall avg: <strong>{avg_risk}</strong> &nbsp;·&nbsp; Flagged avg: <strong>{avg_fl_risk}</strong>
    </div></div>""", unsafe_allow_html=True)

    wce = money_at_risk + rto_loss
    st.markdown(f"""<div class="icard ic-red">
    <div class="icard-title">⛔ Total Financial Exposure</div>
    <div class="icard-body">
    <strong>Rs {wce:,}</strong> exposed to delivery risk<br>
    Rs {money_at_risk:,} — flagged, not yet dispatched (recoverable)<br>
    Rs {rto_loss:,} — already lost to shipping + reverse cost
    </div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ORDER TABLE
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Order Details</div>', unsafe_allow_html=True)

show_cols = ["order_id","name","phone","address","city","status",
             "risk_score","risk_level","risk_reason","map_status","created_at"]
show_cols = [c for c in show_cols if c in df_view.columns]

def style_status(val):
    m = {
        "Rejected":       "background:rgba(239,68,68,0.15);color:#F87171;font-weight:700",
        "Risk Flagged":   "background:rgba(245,158,11,0.15);color:#FCD34D;font-weight:700",
        "Auto-Confirmed": "background:rgba(16,185,129,0.15);color:#34D399;font-weight:700",
    }
    return m.get(val, "color:#94A3B8")

def style_risk(val):
    m = {
        "CRITICAL": "background:rgba(239,68,68,0.15);color:#F87171;font-weight:700",
        "HIGH":     "background:rgba(239,68,68,0.10);color:#F87171",
        "MEDIUM":   "background:rgba(245,158,11,0.10);color:#FCD34D",
        "LOW":      "background:rgba(16,185,129,0.10);color:#34D399",
    }
    return m.get(val, "color:#94A3B8")

st.caption(f"Showing **{len(df_view)}** of **{total}** processed orders · **{pending}** pending excluded")

styled = df_view[show_cols].style
if "status"     in show_cols: styled = styled.map(style_status, subset=["status"])
if "risk_level" in show_cols: styled = styled.map(style_risk,   subset=["risk_level"])
if "risk_score" in show_cols:
    styled = styled.background_gradient(
        subset=["risk_score"], cmap="RdYlGn_r", vmin=0, vmax=100
    )

st.dataframe(
    styled,
    use_container_width=True,
    height=440,
    column_config={
        "order_id":    st.column_config.TextColumn("Order ID",   width=165),
        "name":        st.column_config.TextColumn("Customer",   width=120),
        "phone":       st.column_config.TextColumn("Phone",      width=115),
        "address":     st.column_config.TextColumn("Address",    width=240),
        "city":        st.column_config.TextColumn("City",       width=90),
        "status":      st.column_config.TextColumn("Status",     width=135),
        "risk_score":  st.column_config.NumberColumn("Score",    width=70, format="%d"),
        "risk_level":  st.column_config.TextColumn("Level",      width=82),
        "risk_reason": st.column_config.TextColumn("Reason",     width=300),
        "map_status":  st.column_config.TextColumn("Maps",       width=115),
        "created_at":  st.column_config.TextColumn("Date",       width=90),
    }
)

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown(
    "<div style='text-align:center;padding:28px 0 6px;"
    "color:#1E293B;font-size:12px;font-weight:600;letter-spacing:0.5px'>"
    "COD Intelligence &nbsp;·&nbsp; Pakistan eCommerce &nbsp;·&nbsp; "
    "Powered by Supabase &nbsp;·&nbsp; Gemini AI &nbsp;·&nbsp; Google Maps"
    "</div>",
    unsafe_allow_html=True
)
