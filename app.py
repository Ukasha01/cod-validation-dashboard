import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from datetime import datetime, timedelta

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="COD Intelligence",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container { padding: 1.5rem 2rem 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e2e;
}
[data-testid="stSidebar"] * { color: #c9c9e0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label { color: #8888aa !important; font-size: 12px; }

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #2a2a4a;
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.kpi-label { font-size: 11px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #6b6b8d; margin-bottom: 6px; }
.kpi-value { font-size: 28px; font-weight: 700; color: #e0e0f0; line-height: 1; }
.kpi-sub   { font-size: 11px; color: #5a5a7a; margin-top: 4px; }

.kpi-card.green  { border-color: #1a3a2a; }
.kpi-card.green  .kpi-value { color: #4ade80; }
.kpi-card.yellow { border-color: #3a3010; }
.kpi-card.yellow .kpi-value { color: #fbbf24; }
.kpi-card.red    { border-color: #3a1a1a; }
.kpi-card.red    .kpi-value { color: #f87171; }
.kpi-card.blue   { border-color: #1a2a3a; }
.kpi-card.blue   .kpi-value { color: #60a5fa; }
.kpi-card.purple { border-color: #2a1a3a; }
.kpi-card.purple .kpi-value { color: #c084fc; }

/* ── Insight Cards ── */
.ins-card {
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
    border-left: 4px solid;
    font-size: 13px;
    line-height: 1.6;
}
.ins-card.success { background: #0d1f0f; border-color: #22c55e; }
.ins-card.warning { background: #1f160a; border-color: #f59e0b; }
.ins-card.danger  { background: #1f0a0a; border-color: #ef4444; }
.ins-card.info    { background: #0a0f1f; border-color: #3b82f6; }
.ins-card.purple  { background: #140a1f; border-color: #a855f7; }

.ins-title { font-weight: 700; font-size: 13px; color: #e0e0f0; margin-bottom: 5px; }
.ins-body  { color: #8888aa; }
.ins-body strong { color: #c9c9e0; }

/* ── Section Headers ── */
.sec-header {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    color: #5a5a7a;
    padding: 6px 0;
    border-bottom: 1px solid #1e1e2e;
    margin: 1.5rem 0 1rem;
}

/* ── Status Badges ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}
.badge-confirmed { background: #052010; color: #4ade80; border: 1px solid #166534; }
.badge-flagged   { background: #201500; color: #fbbf24; border: 1px solid #854d0e; }
.badge-rejected  { background: #200505; color: #f87171; border: 1px solid #991b1b; }

/* ── Login ── */
.login-wrap { max-width: 360px; margin: 80px auto; text-align: center; }
.login-title { font-size: 28px; font-weight: 700; color: #e0e0f0; margin-bottom: 8px; }
.login-sub   { font-size: 14px; color: #5a5a7a; margin-bottom: 24px; }

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 16px;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 1.5rem;
}
.topbar-title { font-size: 22px; font-weight: 700; color: #e0e0f0; }
.topbar-sub   { font-size: 12px; color: #5a5a7a; margin-top: 2px; }
.live-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #22c55e;
    display: inline-block;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Table ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Dark plotly fix ── */
.js-plotly-plot { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CREDENTIALS (move to st.secrets in prod)
# ─────────────────────────────────────────
SUPABASE_URL = "https://obzbfrakrzkywshwrbne.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iemJmcmFrcnpreXdzaHdyYm5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5ODM0NDEsImV4cCI6MjA5MzU1OTQ0MX0.gKDqt9wWsZdriuXWUDNMi10F26zojmTzg-GKsbwImA0"

# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div class="login-wrap">
        <div style="font-size:48px; margin-bottom:12px;">📦</div>
        <div class="login-title">COD Intelligence</div>
        <div class="login-sub">AI-powered order validation platform</div>
    </div>
    """, unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        pw = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
        if st.button("Sign In →", use_container_width=True, type="primary"):
            if pw == "admin123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    st.stop()

# ─────────────────────────────────────────
# DATA LOAD — cached 60s
# ─────────────────────────────────────────
@st.cache_data(ttl=60)
def load_data():
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        resp = client.table("orders").select("*").order("inserted_at", desc=True).execute()
        df = pd.DataFrame(resp.data)
        if df.empty:
            return pd.DataFrame()

        df.columns = df.columns.str.strip().str.lower()
        df['status']     = df['status'].astype(str).str.strip()
        df['city']       = df['city'].astype(str).str.strip().str.title()
        df['risk_level'] = df.get('risk_level', pd.Series(dtype=str)).astype(str).str.strip().str.upper()
        df['risk_score'] = pd.to_numeric(df.get('risk_score', 0), errors='coerce').fillna(0)
        df['price']      = pd.to_numeric(df.get('price', 0), errors='coerce').fillna(0)

        if 'inserted_at' in df.columns:
            df['inserted_at'] = pd.to_datetime(df['inserted_at'], errors='coerce')
            df['date'] = df['inserted_at'].dt.date

        return df
    except Exception as e:
        st.error(f"Supabase error: {e}")
        return pd.DataFrame()

# ─────────────────────────────────────────
# SIDEBAR — FILTERS + SETTINGS
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    st.markdown("---")

    st.markdown("**📅 Date Range**")
    date_range = st.selectbox("", ["All time", "Today", "Last 7 days", "Last 30 days"], label_visibility="collapsed")

    st.markdown("**🔍 Status Filter**")
    status_filter = st.selectbox("", ["All", "Auto-Confirmed", "Risk Flagged", "Rejected", "Pending"], label_visibility="collapsed")

    st.markdown("**🏙️ City Filter**")

    st.markdown("**⚠️ Risk Level**")
    risk_filter = st.selectbox("", ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**💰 Financial Settings**")
    avg_order_val  = st.number_input("Avg Order Value (Rs)", value=3000, step=500, min_value=0)
    shipping_cost  = st.number_input("Shipping Cost (Rs)",   value=250,  step=50,  min_value=0)
    reverse_cost   = st.number_input("Reverse Cost (Rs)",    value=150,  step=50,  min_value=0)

    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
df_raw = load_data()

if df_raw.empty:
    st.warning("No data found in Supabase. Check your connection.")
    st.stop()

# City filter options (after load)
all_cities = sorted(df_raw['city'].dropna().unique().tolist())
with st.sidebar:
    city_filter = st.selectbox("", ["All"] + all_cities, label_visibility="collapsed", key="city_sel")

# Apply date filter
df = df_raw.copy()
today = datetime.now().date()
if date_range == "Today" and 'date' in df.columns:
    df = df[df['date'] == today]
elif date_range == "Last 7 days" and 'date' in df.columns:
    df = df[df['date'] >= today - timedelta(days=7)]
elif date_range == "Last 30 days" and 'date' in df.columns:
    df = df[df['date'] >= today - timedelta(days=30)]

# Separate processed vs pending
df_pending   = df[df['status'] == 'Pending']
df_processed = df[~df['status'].isin(['Pending', '', 'Not Checked'])]

# Apply sidebar filters to processed
df_view = df_processed.copy()
if status_filter != "All":
    df_view = df_view[df_view['status'] == status_filter]
if city_filter != "All":
    df_view = df_view[df_view['city'] == city_filter]
if risk_filter != "All":
    df_view = df_view[df_view['risk_level'] == risk_filter]

# ─────────────────────────────────────────
# METRICS (always from processed df)
# ─────────────────────────────────────────
total     = len(df_processed)
confirmed = len(df_processed[df_processed['status'] == 'Auto-Confirmed'])
flagged   = len(df_processed[df_processed['status'] == 'Risk Flagged'])
rejected  = len(df_processed[df_processed['status'] == 'Rejected'])
pending   = len(df_pending)

rto_cost      = shipping_cost + reverse_cost
clean_pct     = round(confirmed / total * 100, 1) if total else 0
risk_pct      = round((flagged + rejected) / total * 100, 1) if total else 0
avg_risk      = round(df_processed['risk_score'].mean(), 1) if total else 0

saved         = rejected * avg_order_val
money_at_risk = flagged  * avg_order_val
rto_loss      = rejected * rto_cost
conf_revenue  = confirmed * avg_order_val
worst_case    = (flagged + rejected) * rto_cost

flagged_df    = df_processed[df_processed['status'].isin(['Risk Flagged', 'Rejected'])]
avg_flag_risk = round(flagged_df['risk_score'].mean(), 1) if len(flagged_df) else 0

high_risk   = len(df_processed[df_processed['risk_level'] == 'CRITICAL']) + len(df_processed[df_processed['risk_level'] == 'HIGH'])
medium_risk = len(df_processed[df_processed['risk_level'] == 'MEDIUM'])
low_risk    = len(df_processed[df_processed['risk_level'] == 'LOW'])

# ─────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div>
    <div class="topbar-title">📦 COD Intelligence Dashboard</div>
    <div class="topbar-sub">AI-powered order validation · Pakistan eCommerce</div>
  </div>
  <div style="text-align:right">
    <div style="font-size:12px;color:#5a5a7a"><span class="live-dot"></span>Live · auto-refreshes every 60s</div>
    <div style="font-size:11px;color:#3a3a5a;margin-top:2px">{total} orders processed · {pending} pending</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 1 — ORDER KPIs
# ─────────────────────────────────────────
st.markdown('<div class="sec-header">Order Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
kpis = [
    (c1, "Total Processed", total,      "",                  "blue"),
    (c2, "Auto-Confirmed",  confirmed,  f"{clean_pct}% clean", "green"),
    (c3, "Risk Flagged",    flagged,    "needs review",        "yellow"),
    (c4, "Rejected",        rejected,   "blocked",             "red"),
    (c5, "Pending",         pending,    "not processed yet",   "purple"),
    (c6, "Avg Risk Score",  avg_risk,   "lower = better",      "blue"),
]
for col, label, val, sub, color in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {color}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 2 — FINANCIAL KPIs
# ─────────────────────────────────────────
st.markdown('<div class="sec-header">Financial Impact</div>', unsafe_allow_html=True)

f1, f2, f3, f4, f5 = st.columns(5)
fin_kpis = [
    (f1, "Confirmed Revenue",  f"Rs {conf_revenue:,}",  "from auto-confirmed orders",  "green"),
    (f2, "Money at Risk",      f"Rs {money_at_risk:,}", "in flagged, not dispatched",  "yellow"),
    (f3, "RTO Loss",           f"Rs {rto_loss:,}",      "shipping + reverse cost",     "red"),
    (f4, "Saved by AI",        f"Rs {saved:,}",         "bad orders blocked",          "green"),
    (f5, "Worst Case Exposure",f"Rs {worst_case:,}",    "if all flagged orders fail",  "red"),
]
for col, label, val, sub, color in fin_kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {color}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="font-size:20px">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 3 — CHARTS
# ─────────────────────────────────────────
st.markdown('<div class="sec-header">Analytics</div>', unsafe_allow_html=True)

ch1, ch2, ch3 = st.columns([1.2, 1.2, 1])

DARK_BG    = "rgba(0,0,0,0)"
GRID_COLOR = "#1e1e2e"
TEXT_COLOR = "#8888aa"

# Chart 1: Status donut
with ch1:
    status_counts = df_processed['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    color_map = {
        'Auto-Confirmed': '#4ade80',
        'Risk Flagged':   '#fbbf24',
        'Rejected':       '#f87171',
        'Pending':        '#c084fc',
    }
    fig1 = px.pie(
        status_counts, values='count', names='status',
        hole=0.62,
        color='status', color_discrete_map=color_map,
        title="Order Status Distribution"
    )
    fig1.update_traces(textposition='outside', textfont_size=11, textfont_color=TEXT_COLOR)
    fig1.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
        font_color=TEXT_COLOR,
        title_font_color="#c0c0d8", title_font_size=13,
        legend=dict(font_color=TEXT_COLOR, font_size=11),
        margin=dict(t=40, b=10, l=10, r=10),
        height=260
    )
    fig1.add_annotation(
        text=f"<b>{clean_pct}%</b><br>clean",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="#e0e0f0")
    )
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: City risk bar
with ch2:
    if 'city' in df_processed.columns:
        city_stats = df_processed.groupby('city')['status'].apply(
            lambda x: (x.isin(['Risk Flagged', 'Rejected'])).sum()
        ).reset_index()
        city_stats.columns = ['city', 'risk_count']
        city_total = df_processed.groupby('city').size().reset_index(name='total')
        city_stats = city_stats.merge(city_total, on='city')
        city_stats['risk_pct'] = (city_stats['risk_count'] / city_stats['total'] * 100).round(1)
        city_stats = city_stats.sort_values('risk_pct', ascending=True).tail(8)

        fig2 = px.bar(
            city_stats, x='risk_pct', y='city', orientation='h',
            color='risk_pct',
            color_continuous_scale=[[0,'#22c55e'],[0.5,'#f59e0b'],[1,'#ef4444']],
            title="Risk Rate by City (%)",
            labels={'risk_pct': 'Risk %', 'city': ''},
            text='risk_pct'
        )
        fig2.update_traces(texttemplate='%{text}%', textposition='outside', textfont_color=TEXT_COLOR)
        fig2.update_layout(
            paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
            font_color=TEXT_COLOR,
            title_font_color="#c0c0d8", title_font_size=13,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor=GRID_COLOR, color=TEXT_COLOR),
            yaxis=dict(gridcolor=GRID_COLOR, color=TEXT_COLOR),
            margin=dict(t=40, b=20, l=10, r=40),
            height=260
        )
        st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Risk score gauge
with ch3:
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_risk,
        delta={'reference': 30, 'increasing': {'color': '#f87171'}, 'decreasing': {'color': '#4ade80'}},
        title={'text': "Avg Risk Score", 'font': {'color': '#c0c0d8', 'size': 13}},
        number={'font': {'color': '#e0e0f0', 'size': 36}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': TEXT_COLOR, 'tickfont': {'color': TEXT_COLOR, 'size': 10}},
            'bar': {'color': '#f59e0b' if avg_risk > 50 else '#4ade80'},
            'bgcolor': '#1a1a2e',
            'bordercolor': '#2a2a4a',
            'steps': [
                {'range': [0, 30],  'color': '#0d2010'},
                {'range': [30, 70], 'color': '#1f1500'},
                {'range': [70, 100],'color': '#200505'},
            ],
            'threshold': {'line': {'color': '#f87171', 'width': 2}, 'value': 70}
        }
    ))
    fig3.update_layout(
        paper_bgcolor=DARK_BG,
        font_color=TEXT_COLOR,
        margin=dict(t=40, b=10, l=20, r=20),
        height=260
    )
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────
# ROW 4 — INSIGHTS + RISK TREND
# ─────────────────────────────────────────
st.markdown('<div class="sec-header">Business Insights</div>', unsafe_allow_html=True)

ins1, ins2 = st.columns(2)

with ins1:
    # Health
    if clean_pct >= 70:
        ins_type, icon, title = "success", "✅", "Order Quality: Healthy"
        body = f"<strong>{clean_pct}%</strong> of orders passing. Good baseline — monitor for city spikes."
    elif clean_pct >= 50:
        ins_type, icon, title = "warning", "⚠️", "Order Quality: Needs Attention"
        body = f"Only <strong>{clean_pct}%</strong> clean. Review top-risk cities and tighten checkout address fields."
    else:
        ins_type, icon, title = "danger", "🚨", "Order Quality: Critical"
        body = f"Only <strong>{clean_pct}%</strong> passing. Over half your orders carry risk — review checkout flow immediately."

    st.markdown(f'<div class="ins-card {ins_type}"><div class="ins-title">{icon} {title}</div><div class="ins-body">{body}</div></div>', unsafe_allow_html=True)

    # AI value
    per1k = round(saved * 1000 / max(1, total))
    st.markdown(f'''<div class="ins-card info">
    <div class="ins-title">🛡️ AI Value Generated</div>
    <div class="ins-body">Blocked <strong>{rejected} bad orders</strong> — protecting <strong>Rs {saved:,}</strong> from RTO losses.<br>
    At this rate: <strong>Rs {per1k:,}</strong> saved per 1,000 orders processed.</div>
    </div>''', unsafe_allow_html=True)

    # Worst case
    st.markdown(f'''<div class="ins-card danger">
    <div class="ins-title">⛔ Worst Case Scenario</div>
    <div class="ins-body">If all <strong>{flagged} flagged orders</strong> are dispatched without review and returned,
    logistics loss reaches <strong>Rs {worst_case:,}</strong>. Review before dispatch.</div>
    </div>''', unsafe_allow_html=True)

    # Pending alert
    if pending > 0:
        st.markdown(f'''<div class="ins-card warning">
        <div class="ins-title">⏳ {pending} Orders Not Processed</div>
        <div class="ins-body">These orders are in <strong>Pending</strong> status — AI validation hasn't run yet.
        Check your n8n workflow. They may be stuck after the Wait node.</div>
        </div>''', unsafe_allow_html=True)

with ins2:
    # Top risk city
    if 'city' in df_processed.columns and total > 0:
        city_risk_cnt = df_processed[df_processed['status'].isin(['Risk Flagged','Rejected'])]['city'].value_counts()
        city_tot_cnt  = df_processed['city'].value_counts()

        if not city_risk_cnt.empty:
            top_city    = city_risk_cnt.index[0]
            top_cnt     = city_risk_cnt.iloc[0]
            top_total   = city_tot_cnt.get(top_city, 1)
            top_pct     = round(top_cnt / top_total * 100, 1)
            st.markdown(f'''<div class="ins-card danger">
            <div class="ins-title">🗺️ Highest Risk City: {top_city}</div>
            <div class="ins-body"><strong>{top_cnt} flagged/rejected</strong> out of {top_total} orders
            from {top_city} — <strong>{top_pct}% risk rate</strong>.<br>
            Add extra address validation for {top_city} orders at checkout.</div>
            </div>''', unsafe_allow_html=True)

        # Safest city (min 2 orders)
        city_risk_rate = {}
        for city in city_tot_cnt.index:
            cdf = df_processed[df_processed['city'] == city]
            if len(cdf) >= 2:
                c_risk = len(cdf[cdf['status'].isin(['Risk Flagged','Rejected'])])
                city_risk_rate[city] = c_risk / len(cdf)

        if city_risk_rate:
            safe_city = min(city_risk_rate, key=city_risk_rate.get)
            safe_pct  = round(city_risk_rate[safe_city] * 100, 1)
            st.markdown(f'''<div class="ins-card success">
            <div class="ins-title">🟢 Most Reliable City: {safe_city}</div>
            <div class="ins-body">Only <strong>{safe_pct}% risk rate</strong> from {safe_city} — your most reliable delivery city.
            Consider fast-tracking low-value orders from here.</div>
            </div>''', unsafe_allow_html=True)

    # Monthly projection
    daily_est = max(1, round(total / 7))
    monthly_loss = rto_loss * 4
    monthly_save = saved * 4
    net = monthly_save - monthly_loss
    net_color = "#4ade80" if net >= 0 else "#f87171"
    st.markdown(f'''<div class="ins-card purple">
    <div class="ins-title">📈 Monthly Projection (~{daily_est} orders/day)</div>
    <div class="ins-body">
    Projected RTO loss: <strong>Rs {monthly_loss:,}</strong><br>
    AI savings: <strong>Rs {monthly_save:,}</strong><br>
    Net position: <strong style="color:{net_color}">Rs {net:,}</strong>
    </div>
    </div>''', unsafe_allow_html=True)

    # Risk distribution
    critical = len(df_processed[df_processed['risk_score'] >= 85])
    borderln = len(df_processed[(df_processed['risk_score'] >= 60) & (df_processed['risk_score'] < 85)])
    st.markdown(f'''<div class="ins-card warning">
    <div class="ins-title">📊 Risk Score Distribution</div>
    <div class="ins-body">
    <strong>{critical} orders</strong> scored 85+ (critical — likely fake/invalid)<br>
    <strong>{borderln} orders</strong> scored 60–84 (borderline — manual review advised)<br>
    Overall avg: <strong>{avg_risk}</strong> · Flagged avg: <strong>{avg_flag_risk}</strong>
    </div>
    </div>''', unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 5 — ORDER TABLE
# ─────────────────────────────────────────
st.markdown('<div class="sec-header">Order Details</div>', unsafe_allow_html=True)

# Column selector
all_cols = df_view.columns.tolist()
show_cols = ['order_id','name','phone','address','city','status','risk_score','risk_level','risk_reason','map_status','created_at']
show_cols = [c for c in show_cols if c in all_cols]

# Color mapping for dataframe
def style_status(val):
    if val == 'Rejected':       return 'background-color:#3a0a0a; color:#f87171'
    elif val == 'Risk Flagged': return 'background-color:#2a1a00; color:#fbbf24'
    elif val == 'Auto-Confirmed': return 'background-color:#0a2010; color:#4ade80'
    return ''

def style_risk(val):
    if val in ('HIGH','CRITICAL'): return 'background-color:#3a0a0a; color:#f87171; font-weight:600'
    elif val == 'MEDIUM':          return 'background-color:#2a1a00; color:#fbbf24'
    elif val == 'LOW':             return 'background-color:#0a2010; color:#4ade80'
    return ''

st.caption(f"Showing {len(df_view)} of {total} processed orders · {len(df_pending)} pending excluded")

styled_df = df_view[show_cols].style
if 'status' in show_cols:
    styled_df = styled_df.map(style_status, subset=['status'])
if 'risk_level' in show_cols:
    styled_df = styled_df.map(style_risk, subset=['risk_level'])
if 'risk_score' in show_cols:
    styled_df = styled_df.background_gradient(subset=['risk_score'], cmap='RdYlGn_r', vmin=0, vmax=100)

st.dataframe(styled_df, use_container_width=True, height=400)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:20px 0 0; color:#3a3a5a; font-size:11px;">
    COD Intelligence · Built for Pakistan eCommerce · Data from Supabase · Refreshes every 60s
</div>
""", unsafe_allow_html=True)

# Auto-refresh trigger (non-blocking via cache TTL)
st.markdown(f'<div style="display:none">{datetime.now()}</div>', unsafe_allow_html=True)
