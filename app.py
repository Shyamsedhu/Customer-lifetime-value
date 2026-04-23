import streamlit as st
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Customer Value Analytics",
    layout="wide"
)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("CLV_Final_Output.csv")

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>
.main {
    background-color:#f5f7fa;
}
.block-container {
    padding-top:2rem;
    padding-bottom:2rem;
}
.big-card {
    background:white;
    padding:30px;
    border-radius:18px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
}
.blue-box {
    background:#E3F2FD;
    padding:22px;
    border-radius:16px;
    border-left:8px solid #1565C0;
}
.yellow-box {
    background:#FFF8E1;
    padding:22px;
    border-radius:16px;
    border-left:8px solid #F9A825;
}
.red-box {
    background:#FFEBEE;
    padding:22px;
    border-radius:16px;
    border-left:8px solid #C62828;
}
div.stButton > button:first-child {
    background-color:#1565C0;
    color:white;
    border:none;
    border-radius:8px;
    padding:0.6em 1.2em;
    font-weight:600;
}
div.stButton > button:first-child:hover {
    background-color:#0D47A1;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR INPUTS
# ---------------------------
st.sidebar.title("Customer Inputs")

age = st.sidebar.slider("Age", 18, 80, 35)
credit = st.sidebar.slider("Credit Score", 300, 900, 650)
balance = st.sidebar.number_input("Account Balance", 0, 300000, 100000)
salary = st.sidebar.number_input("Estimated Salary", 10000, 300000, 70000)
tenure = st.sidebar.slider("Tenure (Years)", 0, 10, 5)
products = st.sidebar.selectbox("Products Used", [1,2,3,4])
active = st.sidebar.selectbox("Active Member", ["Yes","No"])
country = st.sidebar.selectbox("Country", ["France","Germany","Spain"])
gender = st.sidebar.selectbox("Gender", ["Male","Female"])

predict = st.sidebar.button("Predict Customer Value")

# ---------------------------
# HEADER
# ---------------------------
st.title("Customer Value Analytics Report")
st.caption("Real-time Customer Lifetime Value scoring for banking relationship management.")

# ---------------------------
# DEFAULT SCREEN
# ---------------------------
if not predict:
    st.info("Enter customer details in the sidebar and click Predict Customer Value.")

# ---------------------------
# PREDICTION
# ---------------------------
if predict:

    active_num = 1 if active == "Yes" else 0

    clv = (
        balance * 0.35 +
        tenure * 5000 +
        products * 15000 +
        active_num * 20000 +
        credit * 40 +
        salary * 0.05
    )

    # FIXED BUSINESS THRESHOLDS
    if clv < 100000:
        segment = "Low Value Customer"
        recommendation = "Increase engagement through offers, product awareness, and cross-sell campaigns."
        color_box = "red-box"

    elif clv <= 150000:
        segment = "Medium Value Customer"
        recommendation = "Upsell suitable products and maintain regular engagement."
        color_box = "yellow-box"

    else:
        segment = "High Value Customer"
        recommendation = "Retain with premium offers, loyalty rewards, and dedicated relationship manager."
        color_box = "blue-box"

    # ---------------------------
    # OUTPUT
    # ---------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='big-card'>
        <h4>Predicted Customer Lifetime Value</h4>
        <h1>₹{clv:,.0f}</h1>
        <h3>{segment}</h3>
        <p>
        Low Value: Below ₹100,000<br>
        Medium Value: ₹100,000 – ₹150,000<br>
        High Value: Above ₹150,000
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='{color_box}'>
        <h4>Recommendation</h4>
        <p>{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------
# FOOTER
# ---------------------------
st.write("")
st.caption("Applied Business Analytics Final Project")
