import streamlit as st
import pandas as pd
from datetime import datetime
from database import (
    init_db, register_user, authenticate_user, 
    fetch_shop_transactions, insert_shop_transaction
)
from predictor import predict_future_sales, get_top_items
from scheme import get_eligible_schemes
from pdf_generator import generate_pdf_report

st.set_page_config(page_title="Rural AI Assistant - SIH26091", layout="wide")

# Ensure DB initialized on startup
init_db()

# Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# ==========================================
# AUTHENTICATION SCREEN
# ==========================================
if not st.session_state.authenticated:
    st.title("🌾 Rural Micro-Entrepreneur Portal")
    
    auth_tab1, auth_tab2 = st.tabs(["📝 New Registration (Dukaan Register Karein)", "🔑 Login"])

    with auth_tab1:
        st.subheader("Register New Micro-Enterprise")
        st.write("Apni dukaan ki details bharein. System aapko ek unique **Shop ID** allot karega.")
        
        reg_owner_name = st.text_input("Owner Name (Dukaan Malik Ka Naam)")
        reg_shop_name = st.text_input("Shop / Enterprise Name (Dukaan Ka Naam)")
        reg_password = st.text_input("Set Password", type="password")

        if st.button("Register & Generate Shop ID"):
            if reg_owner_name and reg_shop_name and reg_password:
                ok, allotted_id = register_user(reg_owner_name, reg_shop_name, reg_password)
                if ok:
                    st.success("✅ Business Successfully Registered!")
                    st.balloons()
                    st.info(f"🔑 **Aapki Allotted Shop ID Hai:** `{allotted_id}`")
                    st.warning("⚠️ Kripya is **Shop ID** aur apne Password ko note kar lein. Isse hi Login hoga.")
                else:
                    st.error(f"Error: {allotted_id}")
            else:
                st.warning("Kripya saari details bharein!")

    with auth_tab2:
        st.subheader("Shopkeeper Login")
        st.caption("💡 **Demo Credentials:** Shop ID: `SHOP-9001` | Password: `password123`")
        
        login_shop_id = st.text_input("Shop ID (e.g. SHOP-1234)", key="login_id")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            success, user_data = authenticate_user(login_shop_id, login_password)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_info = {
                    "shop_id": login_shop_id.strip().upper(),
                    "owner_name": user_data["owner_name"],
                    "shop_name": user_data["shop_name"]
                }
                st.success(f"Welcome {user_data['owner_name']}!")
                st.rerun()
            else:
                st.error("Galat Shop ID ya Password!")

    st.stop()

# ==========================================
# MAIN DASHBOARD
# ==========================================
user = st.session_state.user_info

# Sidebar User Info & Logout
st.sidebar.title(f"🏪 {user['shop_name']}")
st.sidebar.write(f"**Owner:** {user['owner_name']}")
st.sidebar.write(f"**Shop ID:** `{user['shop_id']}`")

if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.rerun()

st.sidebar.divider()

# Transaction Entry
st.sidebar.header("➕ Add Transaction")
item = st.sidebar.selectbox("Select Item", [
    "Chawal(Rice)", "Aata(Wheat Flour)", "Daal(Lentils)", 
    "Cooking Oil(Tel)", "Tea & Biscuits", "Sugar"
])
tx_type = st.sidebar.radio("Type", ["Income", "Expense"])
amount = st.sidebar.number_input("Amount (₹)", min_value=1.0, value=100.0)

if st.sidebar.button("Log Transaction"):
    today_str = datetime.now().strftime('%Y-%m-%d')
    insert_shop_transaction(user['shop_id'], today_str, tx_type, item, amount)
    st.sidebar.success("Transaction Logged!")
    st.rerun()

# Fetch Isolated Data
df = fetch_shop_transactions(user['shop_id'])

st.title(f"🌾 AI Assistant - {user['shop_name']}")

# Tabs Setup
tab1, tab2 = st.tabs(["📊 Dashboard & Analytics", "🏛️ Know About Loans & MoSJE Schemes"])

# TAB 1: FINANCIALS & AI FORECAST
with tab1:
    st.subheader("📊 Financial Summary")
    col1, col2, col3 = st.columns(3)
    total_income = df[df['type'] == 'Income']['amount'].sum() if not df.empty else 0.0
    total_expense = df[df['type'] == 'Expense']['amount'].sum() if not df.empty else 0.0
    net_profit = total_income - total_expense

    col1.metric("Total Revenue", f"₹{round(total_income, 2)}")
    col2.metric("Total Expenses", f"₹{round(total_expense, 2)}")
    col3.metric("Net Profit", f"₹{round(net_profit, 2)}")

    st.divider()

    st.subheader("📈 7-Day Sales & Inventory Forecast")
    forecast_df, insights = predict_future_sales(df)

    if forecast_df is not None:
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg Daily Revenue", f"₹{insights['avg_daily']}")
        m2.metric("Expected 7-Day Revenue", f"₹{insights['total_revenue']}")
        m3.metric("Suggested Stock Budget", f"₹{insights['stock_budget']}")
        
        st.line_chart(forecast_df.set_index('Date'))
        
        top = get_top_items(df)
        st.info(f"💡 **Stock Advisory:** Top demand items to re-order: **{', '.join(top)}**")
    else:
        st.warning("Needs at least 30 days of transaction data to generate AI forecasting.")

    st.divider()
    st.subheader("📋 Recent Ledger Transactions")
    if not df.empty:
        st.dataframe(df.tail(10), use_container_width=True)

# TAB 2: SCHEMES & BANK REPORT
with tab2:
    st.subheader("🏛️ Government Credit Schemes & Financial Structuring")
    st.write(f"Automated credit line analysis for **{user['shop_name']}** (`ID: {user['shop_id']}`).")

    monthly_profit = max(0.0, net_profit / 3.0)
    col_scheme, col_report = st.columns([2, 1])

    with col_scheme:
        st.markdown("### Matching MoSJE & Concessional Schemes")
        matched_schemes = get_eligible_schemes(monthly_profit)
        
        for scheme in matched_schemes:
            with st.expander(f"📌 {scheme['name']} ({scheme['max_loan']})"):
                st.write(f"**Ministry:** {scheme['ministry']}")
                st.write(f"**Interest Rate:** {scheme['interest']}")
                st.write(f"**Purpose:** {scheme['purpose']}")
                st.write(f"**Eligibility Match:** {scheme['eligibility_match']}")

    with col_report:
        st.markdown("### Auto-Generated Bank Report")
        st.write("Report will automatically fetch shop name & owner details from session.")
        
        if st.button("📄 Prepare Bank Report PDF"):
            forecast_rev = insights['total_revenue'] if 'insights' in locals() and insights else 0.0
            
            pdf_path = generate_pdf_report(
                shop_name=user['shop_name'],
                total_income=total_income,
                total_expense=total_expense,
                net_profit=net_profit,
                forecast_revenue=forecast_rev
            )
            
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📥 Download Official Loan PDF",
                    data=file,
                    file_name=f"{user['shop_id']}_Loan_Report.pdf",
                    mime="application/pdf"
                )