import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="CODEX · AI Logistics Intelligence",
    layout="wide",
    page_icon="⬡",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# MASTER STYLES — Palantir × Stripe × Datadog aesthetic
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg:          #070B14;
  --bg2:         #0D1420;
  --bg3:         #111827;
  --card:        #0F1A2E;
  --card2:       #121F35;
  --border:      rgba(255,255,255,0.055);
  --border2:     rgba(255,255,255,0.10);
  --text:        #F1F5F9;
  --muted:       #64748B;
  --muted2:      #94A3B8;
  --green:       #10B981;
  --green-dim:   rgba(16,185,129,0.12);
  --green-glow:  rgba(16,185,129,0.25);
  --amber:       #F59E0B;
  --amber-dim:   rgba(245,158,11,0.12);
  --red:         #EF4444;
  --red-dim:     rgba(239,68,68,0.12);
  --blue:        #3B82F6;
  --blue-dim:    rgba(59,130,246,0.12);
  --purple:      #8B5CF6;
  --purple-dim:  rgba(139,92,246,0.12);
  --cyan:        #06B6D4;
  --cyan-dim:    rgba(6,182,212,0.12);
  --font:        'Plus Jakarta Sans', sans-serif;
  --mono:        'JetBrains Mono', monospace;
  --r:           16px;
  --r2:          20px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
  font-family: var(--font) !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

.block-container {
  padding: 0 1.8rem 3rem !important;
  max-width: 1600px !important;
}

/* ── HIDE STREAMLIT CHROME ────────────────────────────── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── SIDEBAR ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
  min-width: 252px !important; max-width: 252px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

.sb-wrap { padding: 24px 20px 16px; }

.sb-logo-row {
  display: flex; align-items: center; gap: 12px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}
.sb-hex {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--blue), var(--purple));
  clip-path: polygon(50% 0%,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%);
  display: flex; align-items:center; justify-content:center;
  flex-shrink:0;
}
.sb-brand-name { font-size:15px; font-weight:800; color:var(--text); letter-spacing:0.5px; }
.sb-brand-tag  { font-size:9px; font-weight:600; letter-spacing:2px; color:var(--muted); text-transform:uppercase; }

.sb-section { margin-bottom: 24px; }
.sb-label {
  font-size: 9px; font-weight: 700; letter-spacing: 1.8px;
  text-transform: uppercase; color: var(--muted);
  margin-bottom: 8px; display: block;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
  font-size: 13px !important;
}
[data-testid="stSidebar"] input[type="number"] {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
}
[data-testid="stSidebar"] label {
  font-size: 9px !important; font-weight: 700 !important;
  letter-spacing: 1.5px !important; text-transform: uppercase !important;
  color: var(--muted) !important;
}
[data-testid="stSidebar"] hr { border-color: var(--border) !important; }

.sb-btn-row { display: flex; gap: 8px; margin-top: 4px; }
.sb-status {
  display: flex; align-items: center; gap: 7px;
  padding: 10px 14px;
  background: var(--green-dim);
  border: 1px solid var(--green-glow);
  border-radius: 10px; margin-top: 16px;
}
.sb-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
  animation: pulse 2s infinite;
  flex-shrink: 0;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.85)} }
.sb-status-text { font-size: 11px; font-weight: 600; color: var(--green); }

/* ── TOP NAV ──────────────────────────────────────────── */
.topnav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 0 0;
  margin-bottom: 28px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 18px;
}
.tn-left { display: flex; align-items: center; gap: 20px; }
.tn-title { font-size: 19px; font-weight: 800; color: var(--text); letter-spacing: -0.4px; }
.tn-sub { font-size: 12px; color: var(--muted); font-weight: 500; }
.tn-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 12px;
  background: var(--green-dim);
  border: 1px solid rgba(16,185,129,0.3);
  border-radius: 999px;
  font-size: 11px; font-weight: 700; color: var(--green);
  letter-spacing: 0.3px;
}
.tn-right { display: flex; align-items: center; gap: 12px; }
.tn-time {
  font-family: var(--mono);
  font-size: 11px; color: var(--muted);
  background: var(--bg3);
  border: 1px solid var(--border);
  padding: 6px 12px; border-radius: 8px;
}
.tn-pill {
  padding: 5px 14px;
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: 999px;
  font-size: 11px; font-weight: 600; color: var(--muted2);
}

/* ── SECTION HEADERS ──────────────────────────────────── */
.sec {
  display: flex; align-items: center; gap: 14px;
  margin: 28px 0 16px;
}
.sec-ico {
  width: 28px; height: 28px;
  background: var(--blue-dim);
  border: 1px solid rgba(59,130,246,0.2);
  border-radius: 8px;
  display: flex; align-items:center; justify-content:center;
  font-size: 13px; flex-shrink:0;
}
.sec-label {
  font-size: 10px; font-weight: 800; letter-spacing: 1.6px;
  text-transform: uppercase; color: var(--muted);
}
.sec-line { flex:1; height:1px; background: linear-gradient(90deg, var(--border2), transparent); }

/* ── KPI CARDS ────────────────────────────────────────── */
.kpi {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r2);
  padding: 20px 18px 16px;
  position: relative; overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
  cursor: default;
  height: 100%;
}
.kpi::before {
  content: '';
  position: absolute; top:0; left:0; right:0; height:2px;
  border-radius: var(--r2) var(--r2) 0 0;
}
.kpi:hover { border-color: var(--border2); transform: translateY(-2px); }

.kpi-ghost {
  position: absolute; right:-4px; top:-4px;
  font-size: 44px; opacity: 0.035; line-height:1;
  pointer-events: none;
}
.kpi-tag {
  font-size: 9.5px; font-weight: 700; letter-spacing: 1.4px;
  text-transform: uppercase; color: var(--muted); margin-bottom: 14px;
}
.kpi-num {
  font-family: var(--mono);
  font-size: 36px; font-weight: 600; line-height: 1;
  margin-bottom: 8px; letter-spacing: -1px;
}
.kpi-sub { font-size: 11.5px; color: var(--muted); font-weight: 500; }
.kpi-bar { position:absolute; bottom:0; left:0; height:2px; transition:width .5s; }

/* color variants */
.kv-blue  .kpi-num { color: #60A5FA; }
.kv-blue::before  { background: linear-gradient(90deg,#3B82F6,#60A5FA); }
.kv-green .kpi-num { color: #34D399; }
.kv-green::before { background: linear-gradient(90deg,#10B981,#34D399); }
.kv-amber .kpi-num { color: #FCD34D; }
.kv-amber::before { background: linear-gradient(90deg,#F59E0B,#FCD34D); }
.kv-red   .kpi-num { color: #F87171; }
.kv-red::before   { background: linear-gradient(90deg,#EF4444,#F87171); }
.kv-purple .kpi-num { color: #A78BFA; }
.kv-purple::before { background: linear-gradient(90deg,#8B5CF6,#A78BFA); }
.kv-cyan  .kpi-num { color: #22D3EE; }
.kv-cyan::before  { background: linear-gradient(90deg,#06B6D4,#22D3EE); }
.kv-rose  .kpi-num { color: #FB7185; }
.kv-rose::before  { background: linear-gradient(90deg,#F43F5E,#FB7185); }
.kv-teal  .kpi-num { color: #2DD4BF; }
.kv-teal::before  { background: linear-gradient(90deg,#14B8A6,#2DD4BF); }

/* ── INSIGHT PANELS ───────────────────────────────────── */
.ins {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 16px 18px;
  margin-bottom: 12px;
  transition: border-color 0.18s, transform 0.18s;
  position: relative; overflow: hidden;
}
.ins::before {
  content:'';
  position:absolute; left:0; top:0; bottom:0; width:3px;
  border-radius: var(--r) 0 0 var(--r);
}
.ins:hover { border-color: var(--border2); transform: translateX(2px); }
.ins-title { font-size: 13px; font-weight: 700; color: var(--text); margin-bottom:7px; }
.ins-body  { font-size: 12.5px; color: var(--muted2); line-height: 1.75; }
.ins-body strong { color: var(--text); font-weight: 600; }

.iv-green::before { background: var(--green); }
.iv-amber::before { background: var(--amber); }
.iv-red::before   { background: var(--red); }
.iv-blue::before  { background: var(--blue); }
.iv-purple::before{ background: var(--purple); }
.iv-cyan::before  { background: var(--cyan); }

/* ── CHART PANELS ─────────────────────────────────────── */
.cpanel {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r2);
  padding: 6px 4px 2px;
  height: 100%;
}
.cpanel-head {
  padding: 14px 16px 10px;
  font-size: 11.5px; font-weight: 700; color: var(--muted2);
  letter-spacing: 0.3px; border-bottom: 1px solid var(--border);
  margin-bottom: 4px; display: flex; justify-content: space-between;
  align-items: center;
}
.cpanel-badge {
  font-family: var(--mono);
  font-size: 10px; padding: 2px 8px;
  background: var(--bg3); border: 1px solid var(--border);
  border-radius: 6px; color: var(--muted);
}

/* ── LIVE FEED ────────────────────────────────────────── */
.feed-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}
.feed-item:hover { background: var(--bg3); }
.feed-item:last-child { border-bottom: none; }
.feed-dot {
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 5px;
}
.feed-main { flex: 1; min-width: 0; }
.feed-name { font-size: 12.5px; font-weight: 600; color: var(--text); }
.feed-addr { font-size: 11px; color: var(--muted); margin-top: 2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.feed-right { text-align: right; flex-shrink: 0; }
.feed-score {
  font-family: var(--mono); font-size: 18px; font-weight: 600; line-height:1;
}
.feed-status { font-size: 10px; font-weight: 700; letter-spacing:0.5px; margin-top:3px; }
.feed-time { font-size: 10px; color: var(--muted); margin-top: 2px; font-family: var(--mono); }

/* ── STATUS BADGES ────────────────────────────────────── */
.badge {
  display: inline-block;
  font-size: 10px; font-weight: 700; letter-spacing: 0.6px;
  padding: 3px 9px; border-radius: 999px;
}
.b-green  { background: var(--green-dim);  color: var(--green);  border: 1px solid rgba(16,185,129,0.25); }
.b-amber  { background: var(--amber-dim);  color: var(--amber);  border: 1px solid rgba(245,158,11,0.25); }
.b-red    { background: var(--red-dim);    color: var(--red);    border: 1px solid rgba(239,68,68,0.25); }
.b-blue   { background: var(--blue-dim);   color: var(--blue);   border: 1px solid rgba(59,130,246,0.25); }
.b-purple { background: var(--purple-dim); color: var(--purple); border: 1px solid rgba(139,92,246,0.25); }
.b-muted  { background: var(--bg3); color: var(--muted); border: 1px solid var(--border); }

/* ── DATAFRAME OVERRIDES ──────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: 14px !important; }
iframe { border: none !important; }

/* ── BUTTON OVERRIDES ─────────────────────────────────── */
.stButton > button {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
  font-size: 12px !important; font-weight: 600 !important;
  border-radius: 10px !important;
  padding: 8px 16px !important;
  transition: all 0.18s !important;
}
.stButton > button:hover {
  background: var(--card2) !important;
  border-color: rgba(255,255,255,0.18) !important;
}

/* ── LOGIN ────────────────────────────────────────────── */
.login-wrap {
  min-height: 85vh; display:flex; align-items:center; justify-content:center;
}
.login-card {
  background: var(--card);
  border: 1px solid var(--border2);
  border-radius: 24px;
  box-shadow: 0 32px 80px rgba(0,0,0,0.6), 0 0 0 1px var(--border);
  padding: 48px 44px;
  max-width: 380px; width: 100%; text-align:center;
}
.login-hex {
  width: 64px; height: 64px;
  background: linear-gradient(135deg, #3B82F6, #8B5CF6);
  clip-path: polygon(50% 0%,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%);
  display:flex; align-items:center; justify-content:center;
  font-size:28px; margin: 0 auto 24px;
}
.login-title { font-size:22px; font-weight:800; color:var(--text); letter-spacing:-0.5px; margin-bottom:6px; }
.login-sub   { font-size:12.5px; color:var(--muted); line-height:1.6; margin-bottom:32px; }

/* ── METRIC ROW SEPARATOR ─────────────────────────────── */
.divider { height:1px; background: var(--border); margin: 8px 0 24px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════
SUPABASE_URL = "https://obzbfrakrzkywshwrbne.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iemJmcmFrcnpreXdzaHdyYm5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5ODM0NDEsImV4cCI6MjA5MzU1OTQ0MX0.gKDqt9wWsZdriuXWUDNMi10F26zojmTzg-GKsbwImA0"

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="Plus Jakarta Sans",
    font_color="#94A3B8",
    margin=dict(t=12, b=8, l=8, r=8),
)

# ═══════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        st.markdown("""
        <div class="login-card">
          <div class="login-hex">⬡</div>
          <div class="login-title">CODEX Intelligence</div>
          <div class="login-sub">Pakistan's AI-powered COD fraud detection<br>and address validation platform</div>
        </div>""", unsafe_allow_html=True)
        pw = st.text_input("", type="password", placeholder="Enter access key",
                           label_visibility="collapsed")
        if st.button("Access Platform →", use_container_width=True, type="primary"):
            if pw == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid access key")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_data(ttl=60)
def load_data():
    try:
        cl  = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = cl.table("orders").select("*").order("inserted_at", desc=True).execute()
        df  = pd.DataFrame(res.data)
        if df.empty: return pd.DataFrame()
        df.columns    = df.columns.str.strip().str.lower()
        df["status"]     = df["status"].astype(str).str.strip()
        df["city"]       = df["city"].astype(str).str.strip().str.title()
        df["risk_level"] = df.get("risk_level", pd.Series(dtype=str)).astype(str).str.strip().str.upper()
        df["risk_score"] = pd.to_numeric(df.get("risk_score", 0), errors="coerce").fillna(0)
        df["price"]      = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
        if "inserted_at" in df.columns:
            df["inserted_at"] = pd.to_datetime(df["inserted_at"], errors="coerce")
            df["date"]        = df["inserted_at"].dt.date
            df["hour"]        = df["inserted_at"].dt.hour
        return df
    except Exception as e:
        st.error(f"Connection error: {e}")
        return pd.DataFrame()

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-wrap">
      <div class="sb-logo-row">
        <div class="sb-hex"></div>
        <div>
          <div class="sb-brand-name">CODEX</div>
          <div class="sb-brand-tag">AI · Pakistan</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<span class="sb-label">Date Range</span>', unsafe_allow_html=True)
        date_range = st.selectbox("dr", ["All time","Today","Last 7 days","Last 30 days"],
                                  label_visibility="collapsed")
        st.markdown('<span class="sb-label" style="margin-top:16px;display:block">Status</span>',
                    unsafe_allow_html=True)
        status_filter = st.selectbox("sf",
                                     ["All","Auto-Confirmed","Risk Flagged","Rejected","Pending"],
                                     label_visibility="collapsed")
        st.markdown('<span class="sb-label" style="margin-top:16px;display:block">Risk Level</span>',
                    unsafe_allow_html=True)
        risk_filter = st.selectbox("rf", ["All","CRITICAL","HIGH","MEDIUM","LOW"],
                                   label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<span class="sb-label">Financial Settings</span>', unsafe_allow_html=True)
    avg_val  = st.number_input("Avg Order (Rs)", value=3000, step=500, min_value=0,
                               label_visibility="visible")
    ship_cost = st.number_input("Shipping (Rs)", value=250, step=50, min_value=0,
                                label_visibility="visible")
    rev_cost  = st.number_input("Reverse (Rs)",  value=150, step=50, min_value=0,
                                label_visibility="visible")

    st.markdown("---")

    col_r, col_l = st.columns(2)
    with col_r:
        if st.button("⟳ Refresh", use_container_width=True):
            st.cache_data.clear(); st.rerun()
    with col_l:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.auth = False; st.rerun()

    st.markdown("""
    <div class="sb-status">
      <div class="sb-dot"></div>
      <div class="sb-status-text">System Operational</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LOAD
# ═══════════════════════════════════════════════════════════════
df_raw = load_data()
if df_raw.empty:
    st.markdown('<div style="text-align:center;padding:80px;color:#64748B">No data in Supabase. Check connection.</div>',
                unsafe_allow_html=True)
    st.stop()

cities = sorted(df_raw["city"].dropna().unique().tolist())
with st.sidebar:
    st.markdown('<span class="sb-label" style="display:block;margin-top:12px">City</span>',
                unsafe_allow_html=True)
    city_filter = st.selectbox("cf", ["All"] + cities, label_visibility="collapsed")

# Filter pipeline
df = df_raw.copy()
today = datetime.now().date()
if "date" in df.columns:
    if date_range == "Today":
        df = df[df["date"] == today]
    elif date_range == "Last 7 days":
        df = df[df["date"] >= today - timedelta(days=7)]
    elif date_range == "Last 30 days":
        df = df[df["date"] >= today - timedelta(days=30)]

df_pend = df[df["status"] == "Pending"]
df_proc = df[~df["status"].isin(["Pending","","Not Checked"])]

df_view = df_proc.copy()
if status_filter != "All": df_view = df_view[df_view["status"]     == status_filter]
if city_filter   != "All": df_view = df_view[df_view["city"]       == city_filter]
if risk_filter   != "All": df_view = df_view[df_view["risk_level"] == risk_filter]

# ═══════════════════════════════════════════════════════════════
# METRICS
# ═══════════════════════════════════════════════════════════════
total     = len(df_proc)
confirmed = len(df_proc[df_proc["status"] == "Auto-Confirmed"])
flagged   = len(df_proc[df_proc["status"] == "Risk Flagged"])
rejected  = len(df_proc[df_proc["status"] == "Rejected"])
pending   = len(df_pend)

clean_pct   = round(confirmed / max(1, total) * 100, 1)
risk_pct    = round((flagged + rejected) / max(1, total) * 100, 1)
avg_risk    = round(df_proc["risk_score"].mean(), 1) if total else 0
rto_unit    = ship_cost + rev_cost

saved       = rejected  * avg_val
exposure    = flagged   * avg_val
rto_loss    = rejected  * rto_unit
conf_rev    = confirmed * avg_val
worst       = (flagged + rejected) * rto_unit
per_1k      = round(saved * 1000 / max(1, total))

crit_count  = len(df_proc[df_proc["risk_score"] >= 85])
fl_df       = df_proc[df_proc["status"].isin(["Risk Flagged","Rejected"])]
avg_fl_risk = round(fl_df["risk_score"].mean(), 1) if len(fl_df) else 0

# ═══════════════════════════════════════════════════════════════
# TOP NAV
# ═══════════════════════════════════════════════════════════════
now_str = datetime.now().strftime("%d %b %Y  %H:%M")
st.markdown(f"""
<div class="topnav">
  <div class="tn-left">
    <div>
      <div class="tn-title">eCommerce Intelligence</div>
      <div class="tn-sub">COD Fraud Detection · AI Validation Platform · Pakistan</div>
    </div>
    <div class="tn-badge">
      <span style="width:6px;height:6px;border-radius:50%;background:#10B981;
                   box-shadow:0 0 6px #10B981;display:inline-block"></span>
      LIVE
    </div>
  </div>
  <div class="tn-right">
    <div class="tn-pill">{total} processed · {pending} pending</div>
    <div class="tn-time">{now_str}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# KPI ROW 1 — OPERATIONAL
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec">
  <div class="sec-ico">📊</div>
  <div class="sec-label">Operational Overview</div>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

cols = st.columns(7)
kpis = [
    ("Total Orders",     total,        "",                         "blue",   "◈"),
    ("Auto-Confirmed",   confirmed,    f"{clean_pct}% pass rate",  "green",  "✓"),
    ("Risk Flagged",     flagged,      "manual review needed",     "amber",  "⚡"),
    ("Rejected",         rejected,     "blocked before dispatch",  "red",    "✕"),
    ("Pending",          pending,      "AI not processed",         "purple", "◷"),
    ("Avg Risk Score",   f"{avg_risk}", "0 safe · 100 fraud",      "cyan",   "◎"),
    ("Critical Alerts",  crit_count,   "score ≥ 85",              "rose",   "⚠"),
]
for col, (label, val, sub, color, icon) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi kv-{color}">
          <div class="kpi-ghost">{icon}</div>
          <div class="kpi-tag">{label}</div>
          <div class="kpi-num">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# KPI ROW 2 — FINANCIAL
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec" style="margin-top:20px">
  <div class="sec-ico" style="background:rgba(16,185,129,0.1);border-color:rgba(16,185,129,0.2)">💰</div>
  <div class="sec-label">Financial Intelligence</div>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

fcols = st.columns(5)
fkpis = [
    ("Confirmed Revenue", f"₨ {conf_rev:,}",  "clean orders pipeline",       "teal",   "₨"),
    ("AI Savings",        f"₨ {saved:,}",      f"₨ {per_1k:,} per 1K orders","green",  "🛡"),
    ("Exposure (Flagged)",f"₨ {exposure:,}",   "recoverable if reviewed",     "amber",  "⚡"),
    ("RTO Loss",          f"₨ {rto_loss:,}",   "shipping + reverse cost",     "red",    "📦"),
    ("Worst Case",        f"₨ {worst:,}",       "if all risky orders return",  "rose",   "⛔"),
]
for col, (label, val, sub, color, icon) in zip(fcols, fkpis):
    with col:
        st.markdown(f"""
        <div class="kpi kv-{color}">
          <div class="kpi-ghost">{icon}</div>
          <div class="kpi-tag">{label}</div>
          <div class="kpi-num" style="font-size:22px;letter-spacing:-0.5px">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CHARTS ROW 1
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec" style="margin-top:20px">
  <div class="sec-ico" style="background:rgba(139,92,246,0.1);border-color:rgba(139,92,246,0.2)">📈</div>
  <div class="sec-label">Analytics & Intelligence</div>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

ch1, ch2, ch3 = st.columns([1, 1.6, 1])

STATUS_COLORS = {
    "Auto-Confirmed": "#10B981",
    "Risk Flagged":   "#F59E0B",
    "Rejected":       "#EF4444",
    "Pending":        "#8B5CF6"
}

with ch1:
    st.markdown("""
    <div class="cpanel">
      <div class="cpanel-head">Order Status Split
        <span class="cpanel-badge">DONUT</span>
      </div>""", unsafe_allow_html=True)
    sc = df_proc["status"].value_counts().reset_index()
    sc.columns = ["status","count"]
    fig = px.pie(sc, values="count", names="status", hole=0.68,
                 color="status", color_discrete_map=STATUS_COLORS)
    fig.update_traces(
        textposition="outside", textfont_size=11,
        marker_line_color="#070B14", marker_line_width=2.5,
        pull=[0.03]*len(sc)
    )
    fig.add_annotation(
        text=f"<b>{clean_pct}%</b><br>clean",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=15, color="#F1F5F9", family="Plus Jakarta Sans")
    )
    fig.update_layout(**CHART_THEME,
        showlegend=True, height=290,
        legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                    font=dict(size=11, color="#94A3B8"), bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ch2:
    st.markdown("""
    <div class="cpanel">
      <div class="cpanel-head">Order Quality by City
        <span class="cpanel-badge">STACKED BAR</span>
      </div>""", unsafe_allow_html=True)
    if "city" in df_proc.columns and total > 0:
        ct = df_proc.groupby("city").size().reset_index(name="total")
        cr = df_proc[df_proc["status"].isin(["Risk Flagged","Rejected"])]\
               .groupby("city").size().reset_index(name="risky")
        cs = ct.merge(cr, on="city", how="left").fillna(0)
        cs["clean"] = cs["total"] - cs["risky"]
        cs["risk_pct"] = (cs["risky"] / cs["total"] * 100).round(1)
        cs = cs.sort_values("risk_pct", ascending=True).tail(10)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=cs["city"], x=cs["clean"], name="Confirmed",
                              orientation="h", marker_color="#10B981",
                              marker_line_width=0,
                              text=[f"{v:.0f}" if v > 0 else "" for v in cs["clean"]],
                              textposition="inside", insidetextanchor="middle",
                              textfont=dict(size=11, color="#fff", family="Plus Jakarta Sans")))
        fig2.add_trace(go.Bar(y=cs["city"], x=cs["risky"], name="Flagged/Rejected",
                              orientation="h", marker_color="#EF4444",
                              marker_line_width=0,
                              text=[f"{v:.0f}" if v > 0 else "" for v in cs["risky"]],
                              textposition="inside", insidetextanchor="middle",
                              textfont=dict(size=11, color="#fff", family="Plus Jakarta Sans")))
        fig2.update_layout(**CHART_THEME,
            barmode="stack", height=290,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)",
                       tickfont=dict(size=12, color="#94A3B8"), zeroline=False),
            legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center",
                        font=dict(size=11, color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
            bargap=0.3
        )
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ch3:
    st.markdown("""
    <div class="cpanel">
      <div class="cpanel-head">Risk Gauge
        <span class="cpanel-badge">LIVE</span>
      </div>""", unsafe_allow_html=True)
    gc = "#10B981" if avg_risk < 30 else ("#F59E0B" if avg_risk < 65 else "#EF4444")
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk,
        title={"text": f"<span style='font-size:12px;color:#64748B'>Avg Risk Score</span>",
               "font": {"size": 13, "family": "Plus Jakarta Sans"}},
        number={"font": {"size": 44, "color": gc, "family": "JetBrains Mono"}},
        gauge={
            "axis": {"range": [0,100], "tickcolor": "#1E293B",
                     "tickfont": {"size":10,"color":"#475569"}},
            "bar":  {"color": gc, "thickness": 0.22},
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": "rgba(255,255,255,0.06)", "borderwidth": 1,
            "steps": [
                {"range":[0,30],  "color":"rgba(16,185,129,0.08)"},
                {"range":[30,65], "color":"rgba(245,158,11,0.08)"},
                {"range":[65,100],"color":"rgba(239,68,68,0.08)"},
            ],
            "threshold": {"line":{"color":"#EF4444","width":2},"value":70}
        }
    ))
gauge_theme = CHART_THEME.copy()
gauge_theme["margin"] = dict(t=28, b=8, l=28, r=28)

fig3.update_layout(
    **gauge_theme,
    height=290
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CHARTS ROW 2 — Risk Distribution + Timeline
# ═══════════════════════════════════════════════════════════════
ch4, ch5 = st.columns([1, 1.8])

with ch4:
    st.markdown("""
    <div class="cpanel">
      <div class="cpanel-head">Risk Score Distribution
        <span class="cpanel-badge">HISTOGRAM</span>
      </div>""", unsafe_allow_html=True)
    fig4 = px.histogram(
        df_proc, x="risk_score", nbins=20,
        color_discrete_sequence=["#3B82F6"]
    )
    fig4.update_traces(marker_line_color="rgba(0,0,0,0)", opacity=0.85)
    fig4.update_layout(**CHART_THEME, height=240,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="",
                   tickfont=dict(size=11,color="#64748B"), zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="",
                   tickfont=dict(size=11,color="#64748B"), zeroline=False),
        showlegend=False,
        bargap=0.06
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ch5:
    st.markdown("""
    <div class="cpanel">
      <div class="cpanel-head">Order Volume Timeline
        <span class="cpanel-badge">AREA</span>
      </div>""", unsafe_allow_html=True)
    if "date" in df_proc.columns:
        daily = df_proc.groupby(["date","status"]).size().reset_index(name="n")
        fig5 = px.area(daily, x="date", y="n", color="status",
                       color_discrete_map=STATUS_COLORS)
        fig5.update_traces(line_width=1.5, opacity=0.75)
        fig5.update_layout(**CHART_THEME, height=240,
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="",
                       tickfont=dict(size=11,color="#64748B"), zeroline=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="",
                       tickfont=dict(size=11,color="#64748B"), zeroline=False),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center",
                        font=dict(size=11,color="#94A3B8"), bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.markdown('<div style="padding:80px;text-align:center;color:#64748B;font-size:12px">No timestamp data</div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# INSIGHTS + LIVE FEED
# ═══════════════════════════════════════════════════════════════
ins_col, feed_col = st.columns([1.15, 1])

st.markdown("""
<div class="sec" style="margin-top:20px">
  <div class="sec-ico" style="background:rgba(6,182,212,0.1);border-color:rgba(6,182,212,0.2)">🧠</div>
  <div class="sec-label">AI Business Insights</div>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

ins_col2, feed_col2 = st.columns([1.15, 1])

with ins_col2:
    # Health
    if clean_pct >= 70:
        cls,ico,t = "iv-green","✓","Order Quality Healthy"
        b = f"<strong>{clean_pct}%</strong> of orders pass validation — strong baseline for COD operations."
    elif clean_pct >= 50:
        cls,ico,t = "iv-amber","⚡","Order Quality Needs Attention"
        b = f"Only <strong>{clean_pct}%</strong> confirmed clean. Add address hints at checkout to improve."
    else:
        cls,ico,t = "iv-red","⚠","Order Quality Critical"
        b = f"Only <strong>{clean_pct}%</strong> passing. Review checkout flow immediately."
    st.markdown(f'<div class="ins {cls}"><div class="ins-title">{ico} {t}</div><div class="ins-body">{b}</div></div>',
                unsafe_allow_html=True)

    # AI value
    st.markdown(f"""
    <div class="ins iv-blue">
      <div class="ins-title">🛡 AI Protection Value</div>
      <div class="ins-body">
        Caught <strong>{rejected} bad orders</strong> before dispatch — protecting
        <strong>₨ {saved:,}</strong> in revenue.<br>
        System generating <strong>₨ {per_1k:,} in savings per 1,000 orders</strong>.
      </div>
    </div>""", unsafe_allow_html=True)

    # Top risk city
    if "city" in df_proc.columns and total > 0:
        cr = df_proc[df_proc["status"].isin(["Risk Flagged","Rejected"])]["city"].value_counts()
        ct2 = df_proc["city"].value_counts()
        if not cr.empty:
            tc = cr.index[0]; tn = cr.iloc[0]; tt = ct2.get(tc,1)
            tp = round(tn/tt*100,1)
            st.markdown(f"""
            <div class="ins iv-red">
              <div class="ins-title">🗺 Highest Risk City: {tc}</div>
              <div class="ins-body">
                <strong>{tn} flagged/rejected</strong> out of {tt} orders — <strong>{tp}% risk rate</strong>.<br>
                Recommend stricter checkout validation for {tc} orders.
              </div>
            </div>""", unsafe_allow_html=True)

    # Exposure
    st.markdown(f"""
    <div class="ins iv-amber">
      <div class="ins-title">⛔ Current Financial Exposure</div>
      <div class="ins-body">
        <strong>₨ {worst:,}</strong> total exposure if all risky orders return.<br>
        ₨ {exposure:,} flagged (recoverable) · ₨ {rto_loss:,} RTO costs incurred.
      </div>
    </div>""", unsafe_allow_html=True)

    # Pending warning
    if pending > 0:
        st.markdown(f"""
        <div class="ins iv-purple">
          <div class="ins-title">⏳ {pending} Orders Stuck in Pending</div>
          <div class="ins-body">
            AI validation hasn't run. Check your n8n workflow —
            likely stuck at Wait node or Gemini API timeout.
          </div>
        </div>""", unsafe_allow_html=True)

with feed_col2:
    st.markdown("""
    <div class="cpanel" style="height:auto">
      <div class="cpanel-head">Live Order Feed
        <span class="cpanel-badge">REAL-TIME</span>
      </div>""", unsafe_allow_html=True)

    recent = df_proc.sort_values("inserted_at", ascending=False).head(12) \
             if "inserted_at" in df_proc.columns \
             else df_proc.head(12)

    STATUS_DOT = {
        "Auto-Confirmed": "#10B981",
        "Risk Flagged":   "#F59E0B",
        "Rejected":       "#EF4444",
        "Pending":        "#8B5CF6",
    }
    STATUS_BADGE = {
        "Auto-Confirmed": "b-green",
        "Risk Flagged":   "b-amber",
        "Rejected":       "b-red",
        "Pending":        "b-purple",
    }
    SCORE_COLOR = lambda s: "#10B981" if s < 30 else ("#F59E0B" if s < 65 else "#EF4444")

    for _, row in recent.iterrows():
        st_val  = str(row.get("status",""))
        score   = int(row.get("risk_score",0))
        name    = str(row.get("name","—"))[:18]
        city    = str(row.get("city","—"))
        addr    = str(row.get("address","—"))[:42] + "…" \
                  if len(str(row.get("address",""))) > 42 else str(row.get("address","—"))
        dot_c   = STATUS_DOT.get(st_val,"#64748B")
        badge_c = STATUS_BADGE.get(st_val,"b-muted")
        sc      = SCORE_COLOR(score)
        ts      = row["inserted_at"].strftime("%H:%M") \
                  if "inserted_at" in row and pd.notna(row["inserted_at"]) else ""

        st.markdown(f"""
        <div class="feed-item">
          <div class="feed-dot" style="background:{dot_c};box-shadow:0 0 6px {dot_c}60"></div>
          <div class="feed-main">
            <div class="feed-name">{name}
              <span class="badge {badge_c}" style="margin-left:6px">{st_val}</span>
            </div>
            <div class="feed-addr">{addr}</div>
            <div class="feed-time">{city} · {ts}</div>
          </div>
          <div class="feed-right">
            <div class="feed-score" style="color:{sc}">{score}</div>
            <div class="feed-status" style="color:{sc}">RISK</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# ORDER TABLE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec" style="margin-top:20px">
  <div class="sec-ico" style="background:rgba(59,130,246,0.1);border-color:rgba(59,130,246,0.2)">☰</div>
  <div class="sec-label">Order Intelligence Table</div>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

show_cols = ["order_id","name","phone","city","status","risk_score",
             "risk_level","clean_address","risk_reason","map_status","created_at"]
show_cols = [c for c in show_cols if c in df_view.columns]

st.caption(f"**{len(df_view)}** orders shown · {pending} pending excluded · filtered view")

def style_status(v):
    m = {"Rejected":"background:#1A0A0A;color:#F87171;font-weight:700",
         "Risk Flagged":"background:#1A1200;color:#FCD34D;font-weight:700",
         "Auto-Confirmed":"background:#041A0E;color:#34D399;font-weight:700"}
    return m.get(v,"")

def style_risk(v):
    m = {"CRITICAL":"background:#1A0A0A;color:#F87171;font-weight:700",
         "HIGH":"color:#F87171","MEDIUM":"color:#FCD34D","LOW":"color:#34D399"}
    return m.get(v,"")

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
    height=460,
    column_config={
        "order_id":     st.column_config.TextColumn("Order ID",    width=160),
        "name":         st.column_config.TextColumn("Customer",    width=120),
        "phone":        st.column_config.TextColumn("Phone",       width=115),
        "city":         st.column_config.TextColumn("City",        width=95),
        "status":       st.column_config.TextColumn("Status",      width=135),
        "risk_score":   st.column_config.NumberColumn("Score",     width=72, format="%d"),
        "risk_level":   st.column_config.TextColumn("Level",       width=80),
        "clean_address":st.column_config.TextColumn("Clean Address",width=250),
        "risk_reason":  st.column_config.TextColumn("AI Reason",   width=280),
        "map_status":   st.column_config.TextColumn("Maps",        width=110),
        "created_at":   st.column_config.TextColumn("Date",        width=90),
    }
)

st.markdown(f"""
<div style="text-align:center;padding:24px 0 8px;font-size:11px;color:#1E293B;
            font-family:'JetBrains Mono',monospace;letter-spacing:0.5px">
  CODEX INTELLIGENCE · AI-POWERED COD VALIDATION · PAKISTAN
  &nbsp;·&nbsp; {datetime.now().strftime('%Y')}
</div>""", unsafe_allow_html=True)
