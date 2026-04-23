import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="Customer Value Analytics",
    layout="wide"
)

df = pd.read_csv("CLV_Final_Output.csv")

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.metric-box {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    text-align:center;
}
.big-card {
    background: white;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}
.side-note {
    background:#ffffff;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

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

st.title("Customer Value Analytics Report")
st.caption("Real-time Customer Lifetime Value scoring for banking relationship management.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='metric-box'>
    <h5>Average CLV</h5>
    <h2>₹{round(df['CLV'].mean(),0):,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-box'>
    <h5>Total Customers</h5>
    <h2>{len(df):,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    churn = round(df['Exited'].mean()*100,2)
    st.markdown(f"""
    <div class='metric-box'>
    <h5>Churn Rate</h5>
    <h2>{churn}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")

if predict:

    active_num = 1 if active=="Yes" else 0

    clv = (
        balance * 0.35 +
        tenure * 5000 +
        products * 15000 +
        active_num * 20000 +
        credit * 40 +
        salary * 0.05
    )

    if clv >= df["CLV"].quantile(0.75):
        segment = "High Value"
        action = "Retain with premium offers and relationship manager."
    elif clv <= df["CLV"].quantile(0.25):
        segment = "Low Value"
        action = "Cross-sell products and improve engagement."
    else:
        segment = "Medium Value"
        action = "Upsell products and maintain loyalty."

else:
    clv = round(df["CLV"].mean(),0)
    segment = "Not Calculated"
    action = "Enter values and click Predict."

left, right = st.columns([2,1])

with left:
    st.markdown(f"""
    <div class='big-card'>
    <h4>Predicted Customer Lifetime Value</h4>
    <h1>₹{clv:,.0f}</h1>
    <h3>{segment}</h3>
    <p>{action}</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.subheader("Average CLV by Country")
    geo = pd.DataFrame({
        "Country":["France","Germany","Spain"],
        "CLV":[
            df[df["Geography_Germany"]==0]["CLV"].mean(),
            df[df["Geography_Germany"]==1]["CLV"].mean(),
            df[df["Geography_Spain"]==1]["CLV"].mean()
        ]
    })
    st.bar_chart(geo.set_index("Country"))

with right:
    st.markdown("""
    <div class='side-note'>
    <h4>Business Recommendation</h4>
    <p>• Prioritize high-value customers.</p>
    <p>• Reduce churn in profitable accounts.</p>
    <p>• Promote multi-product adoption.</p>
    <p>• Target low-value users with campaigns.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class='side-note'>
    <h4>Model Inputs Used</h4>
    <p>Age</p>
    <p>Credit Score</p>
    <p>Balance</p>
    <p>Salary</p>
    <p>Products</p>
    <p>Tenure</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.caption("Applied Business Analytics Final Project")
