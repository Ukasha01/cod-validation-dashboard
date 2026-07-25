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
    page_title="Wapsi — AI Operational Intelligence",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

PAKISTAN_TZ = ZoneInfo("Asia/Karachi")

# ════════════════════════════════════════════════════════
# BRAND ASSETS & ICONS (Replaced Emojis with Enterprise SVGs)
# ════════════════════════════════════════════════════════
ICON_DARK_B64  = "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荨"
ICON_LIGHT_B64 = "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荨"

def brand_icon_tag(b64, size):
    return f'<img src="data:image/png;base64,{b64}" style="width:{size}px;height:{size}px;border-radius:{max(8,size//4)}px;display:block;" />'

# SVG Icons (Replacing Emojis)
SVG = {
    "box": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
    "x_circle": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
    "ban": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>',
    "clock": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
    "target": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>',
    "dollar": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>',
    "shield": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
    "trend": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>',
    "map": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" y1="3" x2="9" y2="21"></line><line x1="15" y1="3" x2="15" y2="21"></line></svg>'
}

# ════════════════════════════════════════════════════════
# UNIFIED ENTERPRISE CSS
# ════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
    box-sizing: border-box;
}

/* ══ MAIN APP BACKGROUND ══ */
.stApp { background: #F8FAFC !important; } /* Clean, enterprise slate-50 */
.block-container { padding: 2rem 2.4rem 3rem !important; max-width: 100% !important; }

/* ══ SIDEBAR (DARK) ══ */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
    background-color: #0F172A !important;
    border-right: 1px solid #1E293B !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] hr { border-color: #1E293B !important; }
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stNumberInput > label {
    font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: 1px !important; text-transform: uppercase !important; color: #64748B !important;
}

.sb-brand { padding: 20px 8px 16px; border-bottom: 1px solid #1E293B; margin-bottom: 8px; }
.sb-name { font-size: 18px !important; font-weight: 800 !important; color: #FFFFFF !important; letter-spacing: -0.5px; margin-top: 10px; }
.sb-tag { font-size: 10px !important; font-weight: 700 !important; letter-spacing: 1.5px !important; color: #f59e0b !important; text-transform: uppercase; }

/* ══ TOPBAR ══ */
.topbar {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border: 1px solid #334155; border-radius: 20px; padding: 24px 36px; margin-bottom: 30px;
    display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
}
.tb-left { justify-self: start; display: flex; align-items: center; gap: 20px; }
.tb-center { justify-self: center; text-align: center; }
.tb-right { justify-self: end; display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
.tb-title { font-size: 30px; font-weight: 800; background: linear-gradient(to right, #f59e0b, #65a30d); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px; margin-bottom: 6px; }
.tb-sub { font-size: 14px; color: #94A3B8; font-weight: 500; }
.live-pill { display: inline-flex; align-items: center; gap: 8px; background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.4); color: #34D399; font-size: 12px; font-weight: 800; padding: 6px 16px; border-radius: 30px; }
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #10b981; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }
.tb-meta { font-size: 13px; color: #64748B; font-weight: 600; }

/* ══ BUTTON OVERRIDES (Fixing the Red Default) ══ */
[data-testid="baseButton-primary"] {
    background-color: #65a30d !important;
    border-color: #65a30d !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}
[data-testid="baseButton-primary"]:hover {
    background-color: #4d7c0f !important;
    border-color: #4d7c0f !important;
}

/* ══ PASSWORD INPUT FIX ══ */
[data-baseweb="input"] {
    padding-right: 2.5rem !important; /* Prevents eye icon clipping */
}

/* ══ SECTION TITLE ══ */
.sec-title { font-size: 11px; font-weight: 800; letter-spacing: 1.4px; text-transform: uppercase; color: #64748B; margin: 28px 0 14px; display: flex; align-items: center; gap: 12px; }
.sec-title::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, #CBD5E1, transparent); }

/* ══ KPI CARDS (Unified Semantic Design) ══ */
.kcard {
    background: #ffffff; border-radius: 12px; padding: 18px 16px; border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05); position: relative; overflow: hidden;
    height: 120px; display: flex; flex-direction: column; justify-content: space-between;
}
.kcard-bg-icon { position: absolute; right: 14px; top: 14px; color: #CBD5E1; opacity: 0.4; }
.kcard-bg-icon svg { width: 32px; height: 32px; }
.kcard-label { font-size: 10px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; color: #64748B; }
.kcard-value { font-size: 24px; font-weight: 800; line-height: 1; margin-top: 8px; letter-spacing: -0.5px; color: #0F172A; }
.kcard-sub { font-size: 11px; color: #94A3B8; font-weight: 500; margin-top: 4px; }

/* Semantic Accents */
.kc-brand .kcard-value { color: #0F172A; }
.kc-success { border-bottom: 3px solid #10b981; }
.kc-success .kcard-value { color: #059669; }
.kc-warning { border-bottom: 3px solid #f59e0b; }
.kc-warning .kcard-value { color: #d97706; }
.kc-danger { border-bottom: 3px solid #ef4444; }
.kc-danger .kcard-value { color: #dc2626; }

/* ══ INSIGHT CARDS ══ */
.icard { border-radius: 12px; padding: 16px 20px; margin-bottom: 14px; border: 1px solid #E2E8F0; background: #ffffff; }
.icard-title { font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.icard-title svg { width: 16px; height: 16px; }
.icard-body { font-size: 12.5px; color: #475569; line-height: 1.6; }
.ic-success .icard-title { color: #059669; }
.ic-danger .icard-title { color: #dc2626; }
.ic-brand .icard-title { color: #4f46e5; }

/* ══ CHART WRAPPER ══ */
.chart-wrap { background: #ffffff; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(15,23,42,0.05); padding: 12px; height: 100%; }

/* ══ LOGIN ══ */
.login-wrapper { max-width: 440px; margin: 80px auto; background: #ffffff; padding: 48px; border-radius: 24px; border: 1px solid #E2E8F0; box-shadow: 0 12px 32px rgba(15,23,42,0.08); text-align: center; }
.login-title { font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 8px; }
.login-tagline { font-size: 14px; font-weight: 500; color: #475569; margin-bottom: 32px; line-height: 1.5; }
.lt-orange { color: #f59e0b; font-weight: 700; }
.lt-green  { color: #65a30d; font-weight: 700; }
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
if "auth" not in st.session_state: st.session_state.auth = False
if "client_id" not in st.session_state: st.session_state.client_id = None

if not st.session_state.auth:
    login_icon_tag = brand_icon_tag(ICON_LIGHT_B64, 64)
    st.markdown(f"""
    <div class="login-wrapper">
      <div style="display:flex;justify-content:center;margin-bottom:20px;">{login_icon_tag}</div>
      <div class="login-title">Wapsi</div>
      <div class="login-tagline">
        The <span class="lt-orange">AI</span> Operational Intelligence System<br>
        <span class="lt-green">for eCommerce Logistics</span>
      </div>
    """, unsafe_allow_html=True)
    
    # Form elements centered cleanly inside the CSS container logic
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        pw = st.text_input("Password", type="password", placeholder="Enter store password", label_visibility="collapsed")
        if st.button("Sign In →", use_container_width=True, type="primary"):
            if pw in CLIENT_CREDENTIALS:
                st.session_state.auth = True
                st.session_state.client_id = CLIENT_CREDENTIALS[pw]
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

CURRENT_CLIENT_ID = st.session_state.client_id

# ════════════════════════════════════════════════════════
# STATUS NORMALIZATION
# ════════════════════════════════════════════════════════
CLEAN_STATUSES = ["Auto-Confirmed", "Confirmed"]
ALL_KNOWN_STATUSES = ["Auto-Confirmed", "Confirmed", "Risk Flagged", "Rejected", "Cancelled", "Manual Review"]

STATUS_COLOR_MAP = {
    "Auto-Confirmed": "#10b981", "Confirmed": "#059669",
    "Risk Flagged": "#f59e0b", "Rejected": "#ef4444",
    "Cancelled": "#64748b", "Manual Review": "#6366f1",
    "Pending": "#94a3b8"
}

# ════════════════════════════════════════════════════════
# DATA LOAD (Cached 60s)
# ════════════════════════════════════════════════════════
@st.cache_data(ttl=60)
def load_data(client_id: str):
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        resp = client.table("orders").select("*").eq("store_id", client_id).order("inserted_at", desc=True).execute()
        df = pd.DataFrame(resp.data)
        if df.empty: return pd.DataFrame()
        df.columns = df.columns.str.strip().str.lower()
        df["status"] = df["status"].astype(str).str.strip()
        
        # SANITIZE CITY NAMES (Removes garbled/emoji/unicode text causing chart bugs)
        df["city"] = df["city"].astype(str).str.strip().str.title()
        df["city"] = df["city"].str.replace(r'[^\x00-\x7F]+', '', regex=True).str.strip()
        
        df["risk_level"] = df.get("risk_level", pd.Series(dtype=str)).astype(str).str.strip().str.upper()
        df["risk_score"] = pd.to_numeric(df.get("risk_score", 0), errors="coerce").fillna(0)
        df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
        if "inserted_at" in df.columns:
            df["inserted_at"] = pd.to_datetime(df["inserted_at"], errors="coerce", utc=True)
            df["inserted_at_pk"] = df["inserted_at"].dt.tz_convert(PAKISTAN_TZ)
            df["date"] = df["inserted_at_pk"].dt.date
        return df
    except Exception as e:
        return pd.DataFrame()

# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
      {brand_icon_tag(ICON_DARK_B64, 40)}
      <div class="sb-name">Wapsi</div>
      <div class="sb-tag">{CURRENT_CLIENT_ID}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**DATE RANGE**")
    date_range = st.selectbox("dr", ["All time","Today","Last 7 days","Last 30 days"], label_visibility="collapsed")
    st.markdown("**ORDER STATUS**")
    status_filter = st.selectbox("sf", ["All"] + ALL_KNOWN_STATUSES, label_visibility="collapsed")
    st.markdown("**RISK LEVEL**")
    risk_filter = st.selectbox("rf", ["All","CRITICAL","HIGH","MEDIUM","LOW"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**FINANCIAL SETTINGS**")
    avg_order_val = st.number_input("Avg Order Value (Rs)", value=3000, step=500, min_value=0)
    shipping_cost = st.number_input("Shipping Cost (Rs)", value=250, step=50, min_value=0)
    reverse_cost  = st.number_input("Reverse Cost (Rs)", value=150, step=50, min_value=0)
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.auth = False
        st.session_state.client_id = None
        st.rerun()

# ════════════════════════════════════════════════════════
# DATA PREP
# ════════════════════════════════════════════════════════
df_raw = load_data(CURRENT_CLIENT_ID)
df_raw['clean_address'] = df_raw.get('clean_address', pd.Series()).fillna('Not Generated')
df_raw['city'] = df_raw['city'].fillna('Unknown')
# Filter out obvious test data to maintain demo credibility (can be removed later)
df_raw = df_raw[~df_raw["city"].str.contains("Gdsdgsd", case=False, na=False)]

if df_raw.empty:
    st.warning("No data found for this client.")
    st.stop()

df = df_raw.copy()
today = datetime.now(PAKISTAN_TZ).date()
if "date" in df.columns:
    if date_range == "Today": df = df[df["date"] == today]
    elif date_range == "Last 7 days": df = df[df["date"] >= today - timedelta(days=7)]
    elif date_range == "Last 30 days": df = df[df["date"] >= today - timedelta(days=30)]

df_pending = df[df["status"].isin(["Pending", "", "Not Checked"])]
df_proc    = df[~df["status"].isin(["Pending","","Not Checked"])]
df_view    = df_proc.copy()

if status_filter == "Pending": df_view = df_pending.copy()
elif status_filter != "All": df_view = df_view[df_view["status"] == status_filter]
if risk_filter != "All": df_view = df_view[df_view["risk_level"] == risk_filter]

# Metrics Calculation
total = len(df_proc)
confirmed = len(df_proc[df_proc["status"].isin(CLEAN_STATUSES)])
flagged = len(df_proc[df_proc["status"] == "Risk Flagged"])
rejected = len(df_proc[df_proc["status"] == "Rejected"])
cancelled = len(df_proc[df_proc["status"] == "Cancelled"])
pending = len(df_pending)

rto_unit = shipping_cost + reverse_cost
clean_pct = round(confirmed / total * 100, 1) if total else 0
avg_risk = round(df_proc["risk_score"].mean(), 1) if total else 0
saved = rejected * avg_order_val
rto_loss = rejected * rto_unit

# ════════════════════════════════════════════════════════
# UI RENDERING
# ════════════════════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
  <div class="tb-left">{brand_icon_tag(ICON_DARK_B64, 60)}</div>
  <div class="tb-center">
    <div class="tb-title">Wapsi</div>
    <div class="tb-sub">AI Operational Intelligence System for Ecommerce</div>
  </div>
  <div class="tb-right">
    <div class="live-pill"><span class="live-dot"></span> LIVE · 60s Sync</div>
    <div class="tb-meta">{total} Processed · {pending} Pending</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ROW 1: ORDER OVERVIEW
st.markdown('<div class="sec-title">Order Flow Overview</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5, k6 = st.columns(6)
order_kpis = [
    (k1, "Total Processed", total, "kc-brand", SVG["box"]),
    (k2, "Confirmed", confirmed, "kc-success", SVG["check"]),
    (k3, "Risk Flagged", flagged, "kc-warning", SVG["alert"]),
    (k4, "Rejected", rejected, "kc-danger", SVG["x_circle"]),
    (k5, "Cancelled", cancelled, "kc-brand", SVG["ban"]),
    (k6, "Pending", pending, "kc-brand", SVG["clock"])
]
for col, lbl, val, cls, icon in order_kpis:
    with col:
        st.markdown(f'<div class="kcard {cls}"><div class="kcard-bg-icon">{icon}</div><div class="kcard-label">{lbl}</div><div class="kcard-value">{val}</div></div>', unsafe_allow_html=True)

# ROW 2: FINANCIAL
st.markdown('<div class="sec-title">Financial Impact</div>', unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
fin_kpis = [
    (f1, "AI Value Saved", f"Rs {saved:,}", "kc-success", SVG["shield"]),
    (f2, "Money At Risk", f"Rs {flagged * avg_order_val:,}", "kc-warning", SVG["alert"]),
    (f3, "Lost to RTO", f"Rs {rto_loss:,}", "kc-danger", SVG["dollar"])
]
for col, lbl, val, cls, icon in fin_kpis:
    with col:
        st.markdown(f'<div class="kcard {cls}"><div class="kcard-bg-icon">{icon}</div><div class="kcard-label">{lbl}</div><div class="kcard-value">{val}</div></div>', unsafe_allow_html=True)

# CHARTS
st.markdown('<div class="sec-title">Analytics</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1.5, 1])

# Chart 1
with c1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    sc = df_proc["status"].value_counts().reset_index()
    sc.columns = ["status","count"]
    fig1 = px.pie(sc, values="count", names="status", hole=0.6, color="status", color_discrete_map=STATUS_COLOR_MAP)
    fig1.update_layout(title="Order Status", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Arial, sans-serif", margin=dict(t=40, b=0, l=0, r=0), height=280)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Chart 2
with c2:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    if "city" in df_proc.columns and total > 0:
        cs = df_proc.groupby("city")["status"].apply(lambda x: (x.isin(["Risk Flagged","Rejected"])).sum()).reset_index(name="risky")
        ct = df_proc.groupby("city").size().reset_index(name="total")
        cs = cs.merge(ct, on="city")
        cs["clean"] = cs["total"] - cs["risky"]
        cs = cs.sort_values("total", ascending=True).tail(8) # Top 8 by volume
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=cs["city"], x=cs["clean"], name="Clean", orientation="h", marker_color="#10b981"))
        fig2.add_trace(go.Bar(y=cs["city"], x=cs["risky"], name="Risk", orientation="h", marker_color="#ef4444"))
        fig2.update_layout(barmode="stack", title="Top Cities by Volume", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Arial, sans-serif", margin=dict(t=40, b=0, l=0, r=0), height=280)
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Chart 3
with c3:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    gc = "#10b981" if avg_risk < 30 else ("#f59e0b" if avg_risk < 60 else "#ef4444")
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number", value=avg_risk, title={"text":"Avg Risk Score"},
        number={"font":{"color":gc}},
        gauge={"axis":{"range":[0,100]}, "bar":{"color":gc}, "steps":[{"range":[0,30],"color":"#f8fafc"},{"range":[30,70],"color":"#f1f5f9"},{"range":[70,100],"color":"#e2e8f0"}]}
    ))
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Arial, sans-serif", margin=dict(t=40, b=0, l=0, r=0), height=280)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# INSIGHTS
st.markdown('<div class="sec-title">Business Insights</div>', unsafe_allow_html=True)
i1, i2 = st.columns(2)
with i1:
    if clean_pct >= 60:
        st.markdown(f'<div class="icard ic-success"><div class="icard-title">{SVG["check"]} Healthy Baseline</div><div class="icard-body"><strong>{clean_pct}%</strong> of orders are passing validation cleanly. Monitoring normal.</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="icard ic-danger"><div class="icard-title">{SVG["alert"]} High Risk Volume</div><div class="icard-body">Only <strong>{clean_pct}%</strong> of orders passed. Review checkout address requirements.</div></div>', unsafe_allow_html=True)
with i2:
    st.markdown(f'<div class="icard ic-brand"><div class="icard-title">{SVG["shield"]} Fraud Prevention</div><div class="icard-body">By blocking {rejected} bad orders, the system successfully prevented <strong>Rs {saved:,}</strong> in potential RTO losses.</div></div>', unsafe_allow_html=True)

# TABLE
st.markdown('<div class="sec-title">Data Ledger</div>', unsafe_allow_html=True)
show_cols = ["name","phone","address","city","status","risk_score","risk_level","created_at"]
show_cols = [c for c in show_cols if c in df_view.columns]

def style_status(val):
    m = {"Rejected": "color:#dc2626;font-weight:700", "Risk Flagged": "color:#d97706;font-weight:700", "Auto-Confirmed": "color:#059669;font-weight:700"}
    return m.get(val, "")

styled = df_view[show_cols].style
if "status" in show_cols: styled = styled.map(style_status, subset=["status"])

st.dataframe(styled, use_container_width=True, height=400, hide_index=True)
