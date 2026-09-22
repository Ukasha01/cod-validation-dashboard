6808c215d18205a0a36dfb40b523fcd4403c613eshow_cols = ["name","phone","address","clean_address","city","status",
             "risk_score","risk_level","risk_reason","map_status","created_at"]
show_cols = [c for c in show_cols if c in df_view.columns]

def style_status(val):
    m = {"Rejected":       "background:#FDF0EE;color:#C23A29;font-weight:700",
         "Risk Flagged":   "background:#FFF7EB;color:#B4650A;font-weight:700",
         "Auto-Confirmed": "background:#EEFBF5;color:#0B7A54;font-weight:700",
         "Confirmed":      "background:#EEFBF5;color:#0B7A54;font-weight:700",
         "Cancelled":      "background:#F5F3EA;color:#6B6449;font-weight:700",
         "Manual Review":  "background:#F5EEDD;color:#8A6D3B;font-weight:700"}
    return m.get(val, "")

def style_risk(val):
    m = {"CRITICAL": "background:#FDF0EE;color:#C23A29;font-weight:700",
         "HIGH":     "background:#FDF0EE;color:#C23A29",
         "MEDIUM":   "background:#FFF7EB;color:#B4650A",
         "LOW":      "background:#EEFBF5;color:#0B7A54"}
    return m.get(val, "")

st.caption(f"Showing **{len(df_view)}** of **{total}** processed orders · **{pending}** pending excluded")

styled = df_view[show_cols].style
if "status"     in show_cols: styled = styled.map(style_status, subset=["status"])
if "risk_level" in show_cols: styled = styled.map(style_risk,   subset=["risk_level"])
if "risk_score" in show_cols:
    styled = styled.background_gradient(subset=["risk_score"], cmap="RdYlGn_r", vmin=0, vmax=100)

table_config = {
    "name":          st.column_config.TextColumn("Customer",      width=120),
    "phone":         st.column_config.TextColumn("Phone",         width=115),
    "address":       st.column_config.TextColumn("Raw Address",   width=230),
    "clean_address": st.column_config.TextColumn("Clean Address", width=230),
    "city":          st.column_config.TextColumn("City",          width=95),
    "status":        st.column_config.TextColumn("Status",        width=135),
    "risk_score":    st.column_config.NumberColumn("Score",       width=72, format="%d"),
    "risk_level":    st.column_config.TextColumn("Level",         width=80),
    "risk_reason":   st.column_config.TextColumn("Reason",        width=290),
    "map_status":    st.column_config.TextColumn("Maps",          width=115),
    "created_at":    st.column_config.TextColumn("Date",          width=88),
}

@st.dialog("Full Screen Order Intelligence Log", width="large")
def fullscreen_table():
    st.dataframe(styled, use_container_width=True, height=700, column_config=table_config, hide_index=True)

with col_t2:
    st.write("")
    if st.button("⛶ Open Full Screen Table", use_container_width=True):
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
<div class="wapsi-footer">
  <span class="wf-brand">Wapsi</span> &nbsp;·&nbsp; AI Operational Intelligence System for Ecommerce &nbsp;·&nbsp;
  Powered by Supabase · Gemini AI · Google Maps
</div>
""", unsafe_allow_html=True)
