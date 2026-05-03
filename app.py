import streamlit as st
import pandas as pd
import time

# ======================
# ⚙️ PAGE CONFIG
# ======================
st.set_page_config(page_title="COD Intelligence", layout="wide", page_icon="📦")

st.markdown("""
<style>
.block-container { padding-top: 1rem; padding-bottom: 1rem; }

.insight-card {
    background: #f8f9fa;
    border-left: 4px solid #4CAF50;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.insight-card.warning {
    border-left-color: #FF9800;
    background: #fff8f0;
}
.insight-card.danger {
    border-left-color: #f44336;
    background: #fff5f5;
}
.insight-card.info {
    border-left-color: #2196F3;
    background: #f0f6ff;
}
.insight-title {
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 4px;
}
.insight-body {
    font-size: 13px;
    color: #444;
    line-height: 1.5;
}
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #333;
    margin: 16px 0 10px;
    border-bottom: 1px solid #eee;
    padding-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# 🔐 LOGIN
# ======================
st.markdown("### 🔐 Secure Access")
password = st.text_input("Enter Password", type="password")
if password != "admin123":
    st.warning("Access Denied")
    st.stop()

# ======================
# 🎯 HEADER
# ======================
st.markdown("""
<h2 style='text-align:center;'>📦 COD Intelligence Dashboard</h2>
<p style='text-align:center;color:gray;'>AI-powered Order Validation & Business Insights</p>
""", unsafe_allow_html=True)

# ======================
# 🔗 DATA LOAD
# ======================
CSV_URL = "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"

try:
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(axis=1, how='all')
    df = df.fillna("")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ======================
# 🧹 CLEAN DATA
# ======================
if 'status' in df.columns:
    df['status'] = df['status'].astype(str).str.strip()

if 'city' in df.columns:
    df['city'] = df['city'].astype(str).str.strip().str.title()

if 'risk_level' in df.columns:
    df['risk_level'] = df['risk_level'].astype(str).str.strip().str.upper()

df = df[~df['status'].isin(["", "new", "pending", "#NAME?", "Pending"])]

if 'risk_score' in df.columns:
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce').fillna(0)

if 'price' in df.columns:
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

# ======================
# 💰 BUSINESS INPUT
# ======================
col_input1, col_input2, col_input3 = st.columns(3)
with col_input1:
    avg_order_value = st.number_input("💰 Avg Order Value (Rs)", value=3000, step=500)
with col_input2:
    shipping_cost = st.number_input("🚚 Shipping Cost per Order (Rs)", value=250, step=50)
with col_input3:
    reverse_cost = st.number_input("↩️ Reverse Logistics Cost (Rs)", value=150, step=50)

st.divider()

# ======================
# 📊 CORE COUNTS
# ======================
total = len(df)
confirmed  = len(df[df['status'] == 'Auto-Confirmed'])
risk_flag  = len(df[df['status'] == 'Risk Flagged'])
rejected   = len(df[df['status'] == 'Rejected'])
partial    = len(df[df['status'] == 'Partial Match - Review'])

high_risk   = len(df[df['risk_level'] == 'HIGH'])   if 'risk_level' in df.columns else 0
medium_risk = len(df[df['risk_level'] == 'MEDIUM']) if 'risk_level' in df.columns else 0
low_risk    = len(df[df['risk_level'] == 'LOW'])    if 'risk_level' in df.columns else 0

avg_risk  = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns and total > 0 else 0
total_cost_per_rto = shipping_cost + reverse_cost

# ======================
# 💸 FINANCIAL CALCULATIONS
# ======================
# Money at risk (risk flagged orders that haven't been rejected yet)
money_at_risk       = risk_flag * avg_order_value
# Direct loss already confirmed (rejected orders = courier cost wasted)
confirmed_loss      = rejected * total_cost_per_rto
# Potential revenue from confirmed orders
confirmed_revenue   = confirmed * avg_order_value
# Money saved by catching rejected orders before dispatch
saved_by_rejection  = rejected * avg_order_value
# Total addressable loss if all risk-flagged orders also fail
worst_case_loss     = (risk_flag + rejected) * total_cost_per_rto
# Validation efficiency — what % of orders are clean
clean_rate          = round((confirmed / total) * 100, 1) if total > 0 else 0
# Risk rate
risk_rate           = round(((risk_flag + rejected) / total) * 100, 1) if total > 0 else 0
# Avg risk score of flagged orders only
flagged_df          = df[df['status'].isin(['Risk Flagged', 'Rejected'])]
avg_flagged_risk    = round(flagged_df['risk_score'].mean(), 1) if len(flagged_df) > 0 else 0

# ======================
# 📊 KPI ROW 1 — ORDER COUNTS
# ======================
st.markdown('<div class="section-title">📦 Order Overview</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Orders",     total)
k2.metric("✅ Confirmed",     confirmed,  delta=f"{clean_rate}% clean")
k3.metric("⚠️ Risk Flagged",  risk_flag)
k4.metric("❌ Rejected",      rejected)
k5.metric("🔁 Partial Match", partial)
k6.metric("📊 Avg Risk Score", avg_risk,  delta="lower is better", delta_color="inverse")

# ======================
# 📊 KPI ROW 2 — FINANCIAL
# ======================
st.markdown('<div class="section-title">💰 Financial Impact</div>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
f1.metric("✅ Confirmed Revenue",    f"Rs {confirmed_revenue:,}",  help="Expected revenue from auto-confirmed orders")
f2.metric("⚠️ Money at Risk",        f"Rs {money_at_risk:,}",      help="Value of orders currently flagged — not yet shipped")
f3.metric("💸 Loss from RTOs",       f"Rs {confirmed_loss:,}",     help="Shipping + reverse logistics already lost on rejected orders")
f4.metric("🛡️ Saved by AI",         f"Rs {saved_by_rejection:,}", help="Revenue protected by rejecting bad orders before dispatch")

# ======================
# 📊 KPI ROW 3 — RISK BREAKDOWN
# ======================
st.markdown('<div class="section-title">🎯 Risk Breakdown</div>', unsafe_allow_html=True)

r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("🔴 High Risk",    high_risk,   delta=f"{round(high_risk/total*100,1)}% of orders"   if total > 0 else "0%", delta_color="inverse")
r2.metric("🟡 Medium Risk",  medium_risk, delta=f"{round(medium_risk/total*100,1)}% of orders" if total > 0 else "0%", delta_color="inverse")
r3.metric("🟢 Low Risk",     low_risk,    delta=f"{round(low_risk/total*100,1)}% of orders"    if total > 0 else "0%")
r4.metric("📉 Risk Rate",    f"{risk_rate}%", delta="of total orders", delta_color="inverse")
r5.metric("🔥 Avg Risk (Flagged)", avg_flagged_risk, help="Average risk score among flagged/rejected orders only")

st.divider()

# ======================
# 🧠 BUSINESS INSIGHTS ENGINE
# ======================
st.markdown('<div class="section-title">🧠 Business Insights</div>', unsafe_allow_html=True)

ins_col1, ins_col2 = st.columns(2)

with ins_col1:

    # --- Insight 1: Overall health ---
    if clean_rate >= 70:
        card_type, icon, headline = "insight-card", "✅", "Order Quality: Healthy"
        body = f"{clean_rate}% of your orders are passing validation. This is a good baseline. Keep monitoring for city-specific spikes."
    elif clean_rate >= 50:
        card_type, icon, headline = "insight-card warning", "⚠️", "Order Quality: Needs Attention"
        body = f"Only {clean_rate}% of orders are confirmed clean. Review your top risk cities and consider tightening address requirements at checkout."
    else:
        card_type, icon, headline = "insight-card danger", "🚨", "Order Quality: Critical"
        body = f"Only {clean_rate}% of orders are passing. Over half your incoming orders carry risk. Immediate review of your checkout flow is recommended."

    st.markdown(f'<div class="{card_type}"><div class="insight-title">{icon} {headline}</div><div class="insight-body">{body}</div></div>', unsafe_allow_html=True)

    # --- Insight 2: Financial exposure ---
    total_exposure = money_at_risk + confirmed_loss
    st.markdown(f'''<div class="insight-card warning">
        <div class="insight-title">💸 Total Financial Exposure</div>
        <div class="insight-body">
            You currently have <strong>Rs {total_exposure:,}</strong> exposed to delivery risk.<br>
            Rs {money_at_risk:,} is sitting in flagged orders not yet dispatched (still recoverable).<br>
            Rs {confirmed_loss:,} is already lost to shipping + reverse logistics on rejected orders.
        </div>
    </div>''', unsafe_allow_html=True)

    # --- Insight 3: AI protection value ---
    st.markdown(f'''<div class="insight-card info">
        <div class="insight-title">🛡️ Value Your AI System Is Generating</div>
        <div class="insight-body">
            By catching <strong>{rejected} bad orders</strong> before dispatch, the system has protected 
            <strong>Rs {saved_by_rejection:,}</strong> in potential RTO losses.<br>
            At your current rejection rate, that's <strong>Rs {saved_by_rejection * 12 / max(1, total):,.0f}</strong> saved 
            per 1,000 orders processed — compounding as your order volume grows.
        </div>
    </div>''', unsafe_allow_html=True)

    # --- Insight 4: Worst case scenario ---
    st.markdown(f'''<div class="insight-card danger">
        <div class="insight-title">⛔ Worst Case Scenario (If Flagged Orders All Fail)</div>
        <div class="insight-body">
            If all <strong>{risk_flag} risk-flagged orders</strong> are dispatched without review and return,
            total logistics loss would reach <strong>Rs {worst_case_loss:,}</strong>.<br>
            Review and confirm these orders before dispatch to avoid this.
        </div>
    </div>''', unsafe_allow_html=True)

with ins_col2:

    # --- Insight 5: City intelligence ---
    if 'city' in df.columns and total > 0:
        city_risk = df[df['status'].isin(['Risk Flagged', 'Rejected'])]['city'].value_counts()
        city_total = df['city'].value_counts()

        if not city_risk.empty:
            top_risk_city = city_risk.index[0]
            top_risk_count = city_risk.iloc[0]
            top_city_total = city_total.get(top_risk_city, 1)
            top_city_risk_pct = round((top_risk_count / top_city_total) * 100, 1)

            st.markdown(f'''<div class="insight-card danger">
                <div class="insight-title">🗺️ Highest Risk City: {top_risk_city}</div>
                <div class="insight-body">
                    <strong>{top_risk_city}</strong> has the most problematic orders: <strong>{top_risk_count} flagged/rejected</strong> 
                    out of {top_city_total} total orders from this city ({top_city_risk_pct}% risk rate).<br>
                    Consider adding extra address validation steps specifically for orders from this city at checkout.
                </div>
            </div>''', unsafe_allow_html=True)

        # Safest city
        if len(city_total) > 1:
            city_risk_rate = {}
            for city in city_total.index:
                city_df = df[df['city'] == city]
                c_risk = len(city_df[city_df['status'].isin(['Risk Flagged', 'Rejected'])])
                city_risk_rate[city] = c_risk / len(city_df) if len(city_df) > 0 else 0

            safest_city = min(city_risk_rate, key=city_risk_rate.get)
            safest_pct  = round(city_risk_rate[safest_city] * 100, 1)

            st.markdown(f'''<div class="insight-card">
                <div class="insight-title">🟢 Most Reliable City: {safest_city}</div>
                <div class="insight-body">
                    Orders from <strong>{safest_city}</strong> have only a <strong>{safest_pct}% risk rate</strong> — 
                    your most reliable delivery city. You can consider auto-confirming low-value orders from here 
                    to speed up dispatch.
                </div>
            </div>''', unsafe_allow_html=True)

    # --- Insight 6: Risk score distribution ---
    if 'risk_score' in df.columns and total > 0:
        critical_orders = len(df[df['risk_score'] >= 85])
        borderline      = len(df[(df['risk_score'] >= 60) & (df['risk_score'] < 85)])

        st.markdown(f'''<div class="insight-card warning">
            <div class="insight-title">📊 Risk Score Distribution</div>
            <div class="insight-body">
                <strong>{critical_orders} orders</strong> scored 85+ (critical — high confidence fake/bad address).<br>
                <strong>{borderline} orders</strong> scored 60–84 (borderline — manual review strongly advised).<br>
                Average risk score across all orders: <strong>{avg_risk}</strong>.<br>
                Flagged orders average: <strong>{avg_flagged_risk}</strong>.
            </div>
        </div>''', unsafe_allow_html=True)

    # --- Insight 7: Partial match warning ---
    if partial > 0:
        partial_loss_risk = partial * total_cost_per_rto
        st.markdown(f'''<div class="insight-card warning">
            <div class="insight-title">🔁 Partial Match Orders Need Attention</div>
            <div class="insight-body">
                <strong>{partial} orders</strong> returned a partial match from Google Maps — meaning the address 
                exists but could not be precisely located.<br>
                If dispatched without review, these carry Rs {partial_loss_risk:,} in potential RTO cost.<br>
                Recommend calling or WhatsApp confirming these before dispatch.
            </div>
        </div>''', unsafe_allow_html=True)

    # --- Insight 8: Operational recommendation ---
    daily_estimate = round(total / 7) if total >= 7 else total
    monthly_loss_projection = confirmed_loss * 4

    st.markdown(f'''<div class="insight-card info">
        <div class="insight-title">📈 Monthly Projection</div>
        <div class="insight-body">
            Based on current data (~{daily_estimate} orders/day estimate):<br>
            • Projected monthly RTO loss: <strong>Rs {monthly_loss_projection:,}</strong><br>
            • Projected monthly savings from AI rejection: <strong>Rs {saved_by_rejection * 4:,}</strong><br>
            • Net position: <strong style="color:{'green' if saved_by_rejection*4 > monthly_loss_projection else 'red'}">
            Rs {(saved_by_rejection * 4) - monthly_loss_projection:,}</strong>
        </div>
    </div>''', unsafe_allow_html=True)

st.divider()

# ======================
# 🎛 FILTERS + TABLE
# ======================
st.markdown('<div class="section-title">📋 Order Details</div>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3)
with fc1:
    status_filter = st.selectbox("Filter by Status", ["All", "Auto-Confirmed", "Risk Flagged", "Rejected", "Partial Match - Review"])
with fc2:
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df['city'].unique().tolist()))
with fc3:
    risk_filter = st.selectbox("Filter by Risk Level", ["All", "HIGH", "MEDIUM", "LOW"])

df_filtered = df.copy()
if status_filter != "All":
    df_filtered = df_filtered[df_filtered['status'] == status_filter]
if city_filter != "All":
    df_filtered = df_filtered[df_filtered['city'] == city_filter]
if risk_filter != "All" and 'risk_level' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['risk_level'] == risk_filter]

st.caption(f"Showing {len(df_filtered)} of {total} orders")

# ======================
# 🎨 TABLE STYLING
# ======================
def color_status(val):
    if val == "Rejected":           return "background-color:#ffe5e5; color:#d63031;"
    elif val == "Risk Flagged":     return "background-color:#fff4e5; color:#e67e22;"
    elif val == "Auto-Confirmed":   return "background-color:#eafaf1; color:#27ae60;"
    elif val == "Partial Match - Review": return "background-color:#e8f4fd; color:#2980b9;"
    return ""

def color_risk(val):
    if val == "HIGH":   return "background-color:#ffd6d6; font-weight:600;"
    elif val == "MEDIUM": return "background-color:#fff0cc;"
    elif val == "LOW":  return "background-color:#e6ffe6;"
    return ""

styled = df_filtered.style
if 'status' in df_filtered.columns:
    styled = styled.map(color_status, subset=['status'])
if 'risk_level' in df_filtered.columns:
    styled = styled.map(color_risk, subset=['risk_level'])

st.dataframe(styled, use_container_width=True)

# ======================
# 🔄 AUTO REFRESH
# ======================
st.caption("🔄 Auto-refreshing every 30 seconds...")
time.sleep(30)
st.rerun()
