import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════
st.set_page_config(
    page_title="COD Intelligence Command",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

PAKISTAN_TZ = ZoneInfo("Asia/Karachi")

# ════════════════════════════════════════════════════════
# MASTER CSS — TACTICAL DARK / CYBERPUNK HUD
# ════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500;600&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
    box-sizing: border-box;
}

/* ══ MAIN APP BACKGROUND ══ */
.stApp { 
    background: radial-gradient(circle at top center, #111827 0%, #030712 100%) !important; 
    color: #F8FAFC;
}
.block-container { padding: 2rem 2.4rem 3rem !important; max-width: 100% !important; }

/* ══ SIDEBAR (DEEP OBSIDIAN) ══ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background-color: #0B0F19 !important;
    border-right: 1px solid rgba(30, 41, 59, 0.8) !important;
    min-width: 270px !important;
}
[data-testid="stSidebar"] * { color: #94A3B8 !important; }
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stNumberInput > label,
[data-testid="stSidebar"] strong {
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #38BDF8 !important; /* Neon Blue labels */
}
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    color: #F8FAFC !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    backdrop-filter: blur(10px);
}
[data-testid="stSidebar"] input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.2) !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(30, 41, 59, 0.8) !important; }

.sb-brand {
    padding: 20px 8px 16px;
    border-bottom: 1px solid rgba(30, 41, 59, 0.8);
    margin-bottom: 8px;
}
.sb-logo {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #0284C7, #38BDF8);
    border-radius: 12px;
    display: flex; align-items:center; justify-content:center;
    font-size: 22px; margin-bottom: 12px;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
}
.sb-name { 
    font-size: 18px !important; 
    font-weight: 800 !important; 
    color: #F8FAFC !important; 
    letter-spacing: -0.5px;
}
.sb-tag { 
    font-size: 10px !important; 
    font-weight: 700 !important; 
    letter-spacing: 1.5px !important; 
    color: #10B981 !important; /* Emerald Live Status */
    text-transform: uppercase; 
}

/* ══ TOPBAR (HUD STYLE) ══ */
.topbar {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(51, 65, 85, 0.5);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px 30px;
    margin-bottom: 30px;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.tb-icon {
    width: 56px; height: 56px;
    background: rgba(2, 132, 199, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    box-shadow: inset 0 0 15px rgba(56, 189, 248, 0.2);
}
.tb-title {
    font-size: 26px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.tb-sub { font-size: 13px; color: #94A3B8; font-weight: 500; font-family: 'DM Mono', monospace !important; }
.tb-right { display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }

.live-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.5);
    color: #34D399;
    font-size: 11px; font-weight: 800;
    padding: 4px 12px;
    border-radius: 4px;
    letter-spacing: 1px;
    font-family: 'DM Mono', monospace !important;
}
.live-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 8px #10B981;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
.tb-meta { font-size: 12px; color: #64748B; font-weight: 600; font-family: 'DM Mono', monospace !important;}

/* ══ SECTION TITLE (NEON) ══ */
.sec-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #38BDF8;
    margin: 30px 0 16px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.sec-title::before {
    content: '';
    width: 8px;
    height: 8px;
    background: #38BDF8;
    border-radius: 50%;
    box-shadow: 0 0 10px #38BDF8;
}
.sec-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(56, 189, 248, 0.3), transparent);
}

/* ══ KPI CARDS (GLASSMORPHISM) ══ */
.kcard {
    background: rgba(15, 23, 42, 0.4);
    border-radius: 12px;
    padding: 18px;
    border: 1px solid rgba(51, 65, 85, 0.6);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.kcard:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}
.kcard-bar {
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
}
.kcard-bg-icon {
    position: absolute;
    right: 14px;
    top: 14px;
    font-size: 24px;
    opacity: 0.15;
    filter: grayscale(100%);
}
.kcard-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #94A3B8;    
    margin-bottom: 8px;
}
.kcard-value {
    font-family: 'DM Mono', monospace !important;
    font-size: 28px;
    font-weight: 600;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: -1px;
}
.kcard-sub {
    font-size: 11px;
    color: #64748B;    
    font-weight: 500;
    line-height: 1.3;
}
/* Neon Accents for Cards */
.kc-blue { border-left: 1px solid rgba(56,189,248,0.3); }
.kc-blue .kcard-bar { background: #38BDF8; box-shadow: 0 0 10px #38BDF8; }
.kc-blue .kcard-value { color: #F8FAFC; text-shadow: 0 0 15px rgba(56,189,248,0.4); }

.kc-green { border-left: 1px solid rgba(16,185,129,0.3); }
.kc-green .kcard-bar { background: #10B981; box-shadow: 0 0 10px #10B981; }
.kc-green .kcard-value { color: #F8FAFC; text-shadow: 0 0 15px rgba(16,185,129,0.4); }

.kc-amber { border-left: 1px solid rgba(245,158,11,0.3); }
.kc-amber .kcard-bar { background: #F59E0B; box-shadow: 0 0 10px #F59E0B; }
.kc-amber .kcard-value { color: #F8FAFC; text-shadow: 0 0 15px rgba(245,158,11,0.4); }

.kc-red { border-left: 1px solid rgba(239,68,68,0.3); }
.kc-red .kcard-bar { background: #EF4444; box-shadow: 0 0 10px #EF4444; }
.kc-red .kcard-value { color: #F8FAFC; text-shadow: 0 0 15px rgba(239,68,68,0.4); }

.kc-slate { border-left: 1px solid rgba(100,116,139,0.3); }
.kc-slate .kcard-bar { background: #64748B; }
.kc-slate .kcard-value { color: #F8FAFC; }

.kc-violet { border-left: 1px solid rgba(139,92,246,0.3); }
.kc-violet .kcard-bar { background: #8B5CF6; box-shadow: 0 0 10px #8B5CF6; }
.kc-violet .kcard-value { color: #F8FAFC; text-shadow: 0 0 15px rgba(139,92,246,0.4); }

.kc-cyan { border-left: 1px solid rgba(6,182,212,0.3); }
.kc-cyan .kcard-bar { background: #06B6D4; box-shadow: 0 0 10px #06B6D4; }
.kc-cyan .kcard-value { color: #F8FAFC; text-shadow: 0 0 15px rgba(6,182,212,0.4); }

.kc-rose { border-left: 1px solid rgba(244,63,94,0.3); }
.kc-rose .kcard-bar { background: #F43F5E; box-shadow: 0 0 10px #F43F5E; }
.kc-rose .kcard-value { color: #F8FAFC; text-shadow: 0 0 15px rgba(244,63,94,0.4); }

/* ══ SYSTEM ALERTS (BUSINESS INSIGHTS) ══ */
.icard {
    background: rgba(15, 23, 42, 0.4);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 14px;
    border: 1px solid;
    backdrop-filter: blur(8px);
}
.icard-title { font-size: 13px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.icard-body  { font-size: 12px; color: #94A3B8; line-height: 1.6; font-family: 'DM Mono', monospace !important; }
.icard-body strong { color: #F8FAFC; font-weight: 600; }
.ic-green  { border-color: rgba(16,185,129,0.4); border-left: 4px solid #10B981; }
.ic-amber  { border-color: rgba(245,158,11,0.4); border-left: 4px solid #F59E0B; }
.ic-red    { border-color: rgba(239,68,68,0.4);  border-left: 4px solid #EF4444; }
.ic-blue   { border-color: rgba(56,189,248,0.4); border-left: 4px solid #38BDF8; }
.ic-violet { border-color: rgba(139,92,246,0.4); border-left: 4px solid #8B5CF6; }
.ic-cyan   { border-color: rgba(6,182,212,0.4);  border-left: 4px solid #06B6D4; }

/* ══ CHART WRAPPER ══ */
.chart-wrap {
    background: rgba(15, 23, 42, 0.3);
    border-radius: 12px;
    border: 1px solid rgba(51, 65, 85, 0.5);
    padding: 12px 8px;
    height: 100%;
    backdrop-filter: blur(10px);
}

/* ══ DATAFRAME (HACKER TERMINAL VIBE) ══ */
[data-testid="stDataFrame"] { border-radius: 8px !important; }
.stDataFrame { border: 1px solid rgba(51, 65, 85, 0.8) !important; border-radius: 8px !important; }

/* ══ LOGIN SCREEN (CYBERPUNK) ══ */
.login-bg { min-height: 80vh; display: flex; align-items: center; justify-content: center; }
.login-card { background: rgba(15,23,42,0.8); backdrop-filter: blur(20px); border-radius: 16px; border: 1px solid rgba(56,189,248,0.3); box-shadow: 0 0 40px rgba(56,189,248,0.1); padding: 48px; max-width: 400px; text-align: center; }
.login-icon { width: 64px; height: 64px; background: rgba(56,189,248,0.1); border: 1px solid #38BDF8; border-radius: 16px; display: flex; align-items:center; justify-content:center; font-size: 30px; margin: 0 auto 24px; box-shadow: inset 0 0 15px rgba(56,189,248,0.4); }
.login-title { font-size: 24px; font-weight: 800; color: #F8FAFC; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase; }
.login-sub   { font-size: 12px; color: #94A3B8; font-weight: 500; margin-bottom: 32px; font-family: 'DM Mono', monospace !important; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CREDENTIALS
# ════════════════════════════════════════════════════════
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
CLIENT_CREDENTIALS = dict(st.secrets["CLIENT_CREDENTIALS"])

# ════════════════════════════════════════════════════════
# LOGIN PAGE
# ════════════════════════════════════════════════════════
if "auth" not in st.session_state:
    st.session_state.auth = False
if "client_id" not in st.session_state:
    st.session_state.client_id = None
if "client_label" not in st.session_state:
    st.session_state.client_label = None

if not st.session_state.auth:
    st.markdown("""
    <div style="max-width:400px;margin:80px auto;text-align:center;" class="login-card">
      <div class="login-icon">🛡️</div>
      <div class="login-title">SYSTEM TERMINAL</div>
      <div class="login-sub">COD ORDER INTELLIGENCE NODE</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        pw = st.text_input("", type="password", placeholder="Enter Access Key...",
                           label_visibility="collapsed")
        if st.button("INITIALIZE SYSTEM", use_container_width=True, type="primary"):
            if pw in CLIENT_CREDENTIALS:
                st.session_state.auth = True
                st.session_state.client_id = CLIENT_CREDENTIALS[pw]
                st.session_state.client_label = st.session_state.client_id
                st.rerun()
            else:
                st.error("ACCESS DENIED: Invalid Authorization.")
    st.stop()

CURRENT_CLIENT_ID = st.session_state.client_id

# ════════════════════════════════════════════════════════
# STATUS NORMALIZATION
# ════════════════════════════════════════════════════════
CLEAN_STATUSES = ["Auto-Confirmed", "Confirmed"]
ALL_KNOWN_STATUSES = ["Auto-Confirmed", "Confirmed", "Risk Flagged", "Rejected", "Cancelled", "Manual Review"]

STATUS_COLOR_MAP = {
    "Auto-Confirmed": "#10B981", # Emerald
    "Confirmed":      "#059669", # Darker Emerald
    "Risk Flagged":   "#F59E0B", # Amber
    "Rejected":       "#EF4444", # Crimson
    "Cancelled":      "#64748B", # Slate
    "Manual Review":  "#8B5CF6", # Violet
    "Pending":        "#06B6D4", # Cyan
}

# ════════════════════════════════════════════════════════
# DATA LOAD
# ════════════════════════════════════════════════════════
@st.cache_data(ttl=60)
def load_data(client_id: str):
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        resp = (
            client.table("orders")
            .select("*")
            .eq("store_id", client_id)
            .order("inserted_at", desc=True)
            .execute()
        )
        df = pd.DataFrame(resp.data)
        if df.empty:
            return pd.DataFrame()
        df.columns   = df.columns.str.strip().str.lower()
        df["status"]     = df["status"].astype(str).str.strip()
        df["city"]       = df["city"].astype(str).str.strip().str.title()
        df["risk_level"] = df.get("risk_level", pd.Series(dtype=str)).astype(str).str.strip().str.upper()
        df["risk_score"] = pd.to_numeric(df.get("risk_score", 0), errors="coerce").fillna(0)
        df["price"]      = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
        if "inserted_at" in df.columns:
            df["inserted_at"] = pd.to_datetime(df["inserted_at"], errors="coerce", utc=True)
            df["inserted_at_pk"] = df["inserted_at"].dt.tz_convert(PAKISTAN_TZ)
            df["date"] = df["inserted_at_pk"].dt.date
        return df
    except Exception as e:
        st.error(f"Supabase connection disrupted: {e}")
        return pd.DataFrame()

# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
      <div class="sb-logo">🛡️</div>
      <div class="sb-name">SYS_COMMAND</div>
      <div class="sb-tag">NODE: {CURRENT_CLIENT_ID}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**📅 TIME FRAME**")
    date_range = st.selectbox("dr", ["All time","Today","Last 7 days","Last 30 days"],
                              label_visibility="collapsed")
    st.markdown("**📋 STATUS OVERRIDE**")
    status_filter = st.selectbox(
        "sf",
        ["All"] + ALL_KNOWN_STATUSES,
        label_visibility="collapsed"
    )
    st.markdown("**⚠️ THREAT LEVEL**")
    risk_filter = st.selectbox("rf", ["All","CRITICAL","HIGH","MEDIUM","LOW"],
                               label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**💰 LOGISTICS PARAMS**")
    avg_order_val = st.number_input("Avg Order (PKR)", value=3000, step=500, min_value=0)
    shipping_cost = st.number_input("Shipping (PKR)",   value=250,  step=50,  min_value=0)
    reverse_cost  = st.number_input("RTO Penalty (PKR)",    value=150,  step=50,  min_value=0)

    st.markdown("---")
    col_r, col_l = st.columns(2)
    with col_r:
        if st.button("🔄 SYNC", use_container_width=True):
            st.cache_data.clear(); st.rerun()
    with col_l:
        if st.button("🚪 DISCONNECT", use_container_width=True):
            st.session_state.auth = False
            st.session_state.client_id = None
            st.rerun()

# ════════════════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════════════════
df_raw = load_data(CURRENT_CLIENT_ID)
if df_raw.empty:
    st.warning("SYSTEM EMPTY: No transmission data received for this node.")
    st.stop()

all_cities = sorted(df_raw["city"].dropna().unique().tolist())
with st.sidebar:
    st.markdown("**🏙️ ZONE FILTER**")
    city_filter = st.selectbox("cf", ["All"] + all_cities, label_visibility="collapsed")

df = df_raw.copy()
today = datetime.now(PAKISTAN_TZ).date()
if "date" in df.columns:
    if date_range == "Today":
        df = df[df["date"] == today]
    elif date_range == "Last 7 days":
        df = df[df["date"] >= today - timedelta(days=7)]
    elif date_range == "Last 30 days":
        df = df[df["date"] >= today - timedelta(days=30)]

df_pending = df[df["status"].isin(["Pending", "", "Not Checked"])]
df_proc    = df[~df["status"].isin(["Pending","","Not Checked"])]

df_view = df_proc.copy()
if status_filter == "Pending":
    df_view = df_pending.copy()
elif status_filter != "All":
    df_view = df_view[df_view["status"] == status_filter]
if city_filter != "All": df_view = df_view[df_view["city"] == city_filter]
if risk_filter != "All": df_view = df_view[df_view["risk_level"] == risk_filter]

# ════════════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════════════
total      = len(df_proc)
confirmed  = len(df_proc[df_proc["status"].isin(CLEAN_STATUSES)])
flagged    = len(df_proc[df_proc["status"] == "Risk Flagged"])
rejected   = len(df_proc[df_proc["status"] == "Rejected"])
cancelled  = len(df_proc[df_proc["status"] == "Cancelled"])
manual_rev = len(df_proc[df_proc["status"] == "Manual Review"])
pending    = len(df_pending)

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
now_str = datetime.now(PAKISTAN_TZ).strftime("%d %b %Y // %H:%M PKT")
st.markdown(f"""
<div class="topbar">
  <div class="tb-icon">📡</div>
  <div>
    <div class="tb-title">INTELLIGENCE TERMINAL</div>
    <div class="tb-sub">AI NEURAL NET: ACTIVE // REGION: PAKISTAN</div>
  </div>
  <div class="tb-right">
    <div class="live-pill"><span class="live-dot"></span> UPLINK STABLE</div>
    <div class="tb-meta">{now_str} // PKT<br>PACKETS: {total} PROC // {pending} PEND</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# KPI ROW 1
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Operational Telemetry</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
order_kpis = [
    (k1, "VOLUME",          total,      "TOTAL PARSED",             "blue",   "📊"),
    (k2, "VERIFIED",        confirmed,  f"{clean_pct}% PURITY",     "green",  "✅"),
    (k3, "ANOMALIES",       flagged,    "AWAITING INPUT",           "amber",  "⚠️"),
    (k4, "THREATS BLOCKED", rejected,   "QUARANTINED",              "red",    "❌"),
    (k5, "ABORTED",         cancelled,  "USER TERMINATED",          "slate",  "🚫"),
    (k6, "IN QUEUE",        pending,    "PROCESSING...",            "violet", "⏳"),
    (k7, "THREAT INDEX",    avg_risk,   "SYSTEM AVERAGE",           "cyan",   "🎯"),
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
# KPI ROW 2
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Financial Telemetry</div>', unsafe_allow_html=True)

f1,f2,f3,f4,f5 = st.columns(5)
fin_kpis = [
    (f1, "SECURED REVENUE",   f"{conf_revenue:,}", "CLEARED FOR DISPATCH (PKR)", "green", "💰"),
    (f2, "CAPITAL AT RISK",   f"{money_at_risk:,}", "FLAGGED ASSETS (PKR)",       "amber", "⚠️"),
    (f3, "RTO PENALTY",       f"{rto_loss:,}",      "LOGISTICS BURN (PKR)",       "red",   "📦"),
    (f4, "SYSTEM SAVINGS",    f"{saved:,}",         "LOSS PREVENTED (PKR)",       "cyan",  "🛡️"),
    (f5, "MAX EXPOSURE",      f"{worst_case:,}",    "IF ALL FAIL (PKR)",          "rose",  "⛔"),
]
for col, label, val, sub, color, icon in fin_kpis:
    with col:
        st.markdown(f"""
        <div class="kcard kc-{color}">
          <div class="kcard-bar"></div>
          <div class="kcard-bg-icon">{icon}</div>
          <div class="kcard-label">{label}</div>
          <div class="kcard-value" style="font-size:24px;">{val}</div>
          <div class="kcard-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CHARTS
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">Data Visualization</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.05, 1.45, 0.95])
PAPER = "rgba(0,0,0,0)"
FONT  = "Sora"

# ── Chart 1: Status donut ─────
with c1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    sc = df_proc["status"].value_counts().reset_index()
    sc.columns = ["status","count"]
    fig1 = px.pie(sc, values="count", names="status", hole=0.7,
                  color="status", color_discrete_map=STATUS_COLOR_MAP,
                  title="NODE DISTRIBUTION")
    fig1.update_traces(
        textposition="outside", textfont=dict(size=12, family=FONT, color="#94A3B8"),
        marker=dict(line=dict(color="#0F172A", width=2))
    )
    fig1.add_annotation(
        text=f"<b style='font-size:22px; font-family:\"DM Mono\", monospace; color:#F8FAFC;'>{clean_pct}%</b><br><span style='color:#10B981; font-size:10px; letter-spacing:1px;'>PURITY</span>",
        x=0.5, y=0.5, showarrow=False,
    )
 fig1.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER, font_family=FONT,
        title_font=dict(size=12, color="#38BDF8", family=FONT), # ⬅️ Removed letter_spacing
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center", font=dict(size=10, color="#94A3B8")),
        margin=dict(t=40, b=20, l=10, r=10), height=280
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
        cs = cs.sort_values("risk_pct", ascending=True).tail(7)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=cs["city"], x=cs["clean"], name="VERIFIED",
            orientation="h", marker_color="#10B981",
            text=[f"{v}" for v in cs["clean"]],
            textposition="inside",
            textfont=dict(size=10, color="#0F172A", family='DM Mono')
        ))
        fig2.add_trace(go.Bar(
            y=cs["city"], x=cs["risky"], name="THREAT",
            orientation="h", marker_color="#EF4444",
            text=[f"{v}" if v > 0 else "" for v in cs["risky"]],
            textposition="inside",
            textfont=dict(size=10, color="#F8FAFC", family='DM Mono')
        ))
   fig2.update_layout(
            barmode="stack",
            title=dict(text="REGIONAL THREAT MAP", font=dict(size=12, color="#38BDF8", family=FONT)), # ⬅️ Removed letter_spacing
            paper_bgcolor=PAPER, plot_bgcolor=PAPER, font_family=FONT,
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(gridcolor="rgba(51, 65, 85, 0.3)", tickfont=dict(size=11, color="#94A3B8")),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", font=dict(size=10, color="#94A3B8")),
            margin=dict(t=40, b=10, l=10, r=10), height=280,
            bargap=0.3
        )
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 3: Risk gauge ────────────────────────────────
with c3:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    gc = "#10B981" if avg_risk < 30 else ("#F59E0B" if avg_risk < 60 else "#EF4444")
fig3 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_risk,
        delta={"reference":30, "increasing":{"color":"#EF4444"}, "decreasing":{"color":"#10B981"}, "font":{"size":12}},
        title={"text":"SYSTEM THREAT LEVEL", "font":{"size":12, "color":"#38BDF8", "family":FONT}}, # ⬅️ Removed letter_spacing
        number={"font":{"size":40, "color":gc, "family":"DM Mono"}},
        gauge={
            "axis":{"range":[0,100], "tickcolor":"#475569", "tickfont":{"size":10,"color":"#64748B"}},
            "bar":{"color":gc, "thickness":0.2},
            "bgcolor":"rgba(15, 23, 42, 0.5)",
            "bordercolor":"rgba(51, 65, 85, 0.5)",
            "borderwidth":1,
            "steps":[
                {"range":[0,30],  "color":"rgba(16, 185, 129, 0.1)"},
                {"range":[30,70], "color":"rgba(245, 158, 11, 0.1)"},
                {"range":[70,100],"color":"rgba(239, 68, 68, 0.1)"},
            ],
            "threshold":{"line":{"color":"#EF4444","width":3},"value":70}
        }
    ))
    fig3.update_layout(
        paper_bgcolor=PAPER, font_family=FONT,
        margin=dict(t=40, b=10, l=20, r=20), height=280
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# BUSINESS INSIGHTS (SYSTEM ALERTS)
# ════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">System Alerts & Diagnostics</div>', unsafe_allow_html=True)

ins1, ins2 = st.columns(2)

with ins1:
    if clean_pct >= 70:
        cls,icon,title = "ic-green","[OK]","NETWORK PURITY OPTIMAL"
        body = f"> <strong>{clean_pct}%</strong> of incoming traffic cleared validation protocols. Continue standard monitoring."
    elif clean_pct >= 50:
        cls,icon,title = "ic-amber","[WARN]","MODERATE ANOMALY DETECTED"
        body = f"> Only <strong>{clean_pct}%</strong> verified. Suggest deploying mandatory address fields in checkout node."
    else:
        cls,icon,title = "ic-red","[CRITICAL]","SEVERE RTO LEAK DETECTED"
        body = f"> <strong>{clean_pct}%</strong> verification rate. System is bleeding capital. Immediate checkout audit required."
    st.markdown(f'<div class="icard {cls}"><div class="icard-title">{icon} {title}</div><div class="icard-body">{body}</div></div>', unsafe_allow_html=True)

    per1k = round(saved * 1000 / max(1, total))
    st.markdown(f'''<div class="icard ic-blue">
    <div class="icard-title">[SHIELD] AI VALUE GENERATION LOG</div>
    <div class="icard-body">> Neutralized <strong>{rejected} hostile orders</strong>.<br>
    > Capital protected: <strong>PKR {saved:,}</strong><br>
    > Current efficiency: <strong>PKR {per1k:,} saved per 1K nodes</strong>.</div>
    </div>''', unsafe_allow_html=True)

    daily_est = max(1, round(total / 7))
    net       = (saved * 4) - (rto_loss * 4)
    nc        = "#10B981" if net >= 0 else "#EF4444"
    st.markdown(f'''<div class="icard ic-violet">
    <div class="icard-title">[PROJ] 30-DAY FORECAST</div>
    <div class="icard-body">
    > Traffic estimate: ~{daily_est} req/day<br>
    > Projected burn: <strong>PKR {rto_loss*4:,}</strong> | AI Savings: <strong>PKR {saved*4:,}</strong><br>
    > Net Position: <strong style="color:{nc}; font-size:14px;">PKR {net:,}</strong>
    </div></div>''', unsafe_allow_html=True)

with ins2:
    if "city" in df_proc.columns and total > 0:
        cr = df_proc[df_proc["status"].isin(["Risk Flagged","Rejected"])]["city"].value_counts()
        ct = df_proc["city"].value_counts()
        if not cr.empty:
            tc = cr.index[0]; tn = cr.iloc[0]
            tt = ct.get(tc, 1); tp = round(tn/tt*100,1)
            st.markdown(f'''<div class="icard ic-red">
            <div class="icard-title">[ALERT] HIGH-THREAT VECTOR: {tc.upper()}</div>
            <div class="icard-body">> <strong>{tn} flagged/rejected</strong> out of {tt} targets.<br>
            > Threat probability: <strong>{tp}%</strong>.<br>
            > Action: Deploy stricter geofence for {tc}.</div>
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
            <div class="icard-title">[SAFE] SECURE VECTOR: {sc2.upper()}</div>
            <div class="icard-body">> Threat probability: <strong>{sp}%</strong>.<br>
            > Action: Authorized for rapid-dispatch protocols.</div>
            </div>''', unsafe_allow_html=True)

    st.markdown(f'''<div class="icard ic-amber">
    <div class="icard-title">[DIAG] THREAT LEVEL BREAKDOWN</div>
    <div class="icard-body">
    > Level 85+ (CRITICAL): <strong>{critical_cnt} targets</strong><br>
    > Level 60-84 (ELEVATED): <strong>{border_cnt} targets</strong><br>
    > Mean Target Score: <strong>{avg_risk}</strong>
    </div></div>''', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ORDER TABLE
# ════════════════════════════════════════════════════════
col_t1, col_t2 = st.columns([8, 2])
with col_t1:
    st.markdown('<div class="sec-title">Raw Data Stream</div>', unsafe_allow_html=True)

show_cols = ["name","phone","address","clean_address","city","status",
             "risk_score","risk_level","risk_reason","map_status","created_at"]
show_cols = [c for c in show_cols if c in df_view.columns]

def style_status(val):
    m = {"Rejected":       "background:rgba(239, 68, 68, 0.1);color:#EF4444;font-family:'DM Mono'",
         "Risk Flagged":   "background:rgba(245, 158, 11, 0.1);color:#F59E0B;font-family:'DM Mono'",
         "Auto-Confirmed": "background:rgba(16, 185, 129, 0.1);color:#10B981;font-family:'DM Mono'",
         "Confirmed":      "background:rgba(16, 185, 129, 0.1);color:#10B981;font-family:'DM Mono'",
         "Cancelled":      "background:rgba(100, 116, 139, 0.1);color:#94A3B8;font-family:'DM Mono'",
         "Manual Review":  "background:rgba(139, 92, 246, 0.1);color:#8B5CF6;font-family:'DM Mono'"}
    return m.get(val, "color:#94A3B8;")

def style_risk(val):
    m = {"CRITICAL": "background:rgba(239, 68, 68, 0.1);color:#EF4444",
         "HIGH":     "color:#EF4444",
         "MEDIUM":   "color:#F59E0B",
         "LOW":      "color:#10B981"}
    return m.get(val, "color:#94A3B8;")

st.caption(f"Displaying **{len(df_view)}** records // **{pending}** pending omitted from stream")

styled = df_view[show_cols].style
if "status"     in show_cols: styled = styled.map(style_status, subset=["status"])
if "risk_level" in show_cols: styled = styled.map(style_risk,   subset=["risk_level"])
if "risk_score" in show_cols:
    styled = styled.background_gradient(subset=["risk_score"], cmap="RdYlGn_r", vmin=0, vmax=100)

table_config = {
    "name":          st.column_config.TextColumn("Customer",      width=120),
    "phone":         st.column_config.TextColumn("Phone",         width=115),
    "address":       st.column_config.TextColumn("Raw Target",    width=230),
    "clean_address": st.column_config.TextColumn("Parsed Vector", width=230),
    "city":          st.column_config.TextColumn("Zone",          width=95),
    "status":        st.column_config.TextColumn("Status",        width=135),
    "risk_score":    st.column_config.NumberColumn("Score",       width=72, format="%d"),
    "risk_level":    st.column_config.TextColumn("Level",         width=80),
    "risk_reason":   st.column_config.TextColumn("Diagnostics",   width=290),
    "map_status":    st.column_config.TextColumn("Geo-Verify",    width=115),
    "created_at":    st.column_config.TextColumn("Timestamp",     width=88),
}

@st.dialog("📡 FULL SPECTRUM DATA STREAM", width="large")
def fullscreen_table():
    st.dataframe(styled, use_container_width=True, height=700, column_config=table_config, hide_index=True)

with col_t2:
    st.write("")
    if st.button("⛶ EXPAND STREAM", use_container_width=True):
        fullscreen_table()

st.dataframe(
    styled,
    use_container_width=True,
    height=440,
    hide_index=True,
    column_config=table_config
)

# ════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:32px 0 8px;color:#475569;font-size:11px;font-family:'DM Mono',monospace;letter-spacing:1px">
  // COD_INTEL CORE v1.4 // SECURE ENCLAVE ACTIVE // PAKISTAN NODE //
</div>
""", unsafe_allow_html=True)
