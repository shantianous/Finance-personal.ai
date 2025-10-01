# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----- Page Config -----
st.set_page_config(page_title="EconoPsych Finance AI", layout="centered")

# ----- Style -----
st.markdown("""
<style>
body {
    background-color: #FFF8F0;
}
.css-1aumxhk {
    background-color: #FFF8F0;
}
.stButton>button {
    background-color: #D32F2F;
    color: white;
    font-weight: bold;
}
h1, h2, h3 {
    color: #D32F2F;
}
</style>
""", unsafe_allow_html=True)

# ----- Title -----
st.title("EconoPsych Finance AI")
st.subheader("Optimize your spending with behavioral insights")

# ----- Simulated Data -----
np.random.seed(42)
num_days = 7
planned_spend = np.random.randint(10, 50, num_days)
actual_spend = planned_spend + np.random.randint(-5, 10, num_days)
savings_goal = np.random.randint(10, 50, num_days)
impulse_level = np.random.randint(1, 6, num_days)

data = pd.DataFrame({
    'Day': range(1, num_days+1),
    'Planned Spend': planned_spend,
    'Actual Spend': actual_spend,
    'Savings Goal': savings_goal,
    'Impulse Level': impulse_level
})

# ----- Bias Detection -----
def detect_bias(row):
    biases = []
    if row['Actual Spend'] > row['Planned Spend']:
        biases.append('Impulse Spending')
    if row['Savings Goal'] > row['Actual Spend']:
        biases.append('Present Bias')
    if row['Actual Spend'] < row['Planned Spend']*0.5:
        biases.append('Loss Aversion')
    return ', '.join(biases) if biases else 'No Bias Detected'

data['Bias Detected'] = data.apply(detect_bias, axis=1)

# ----- Sidebar Input -----
st.sidebar.header("Simulate Your Data")
planned_today = st.sidebar.number_input("Planned Spend Today ($)", min_value=0, value=20)
actual_today = st.sidebar.number_input("Actual Spend Today ($)", min_value=0, value=25)
savings_today = st.sidebar.number_input("Savings Goal Today ($)", min_value=0, value=15)
impulse_today = st.sidebar.slider("Impulse Level (1-5)", min_value=1, max_value=5, value=3)

if st.sidebar.button("Add Today"):
    new_row = {
        'Day': len(data)+1,
        'Planned Spend': planned_today,
        'Actual Spend': actual_today,
        'Savings Goal': savings_today,
        'Impulse Level': impulse_today
    }
    new_row['Bias Detected'] = detect_bias(new_row)
    # Fixed for pandas 2.x
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

# ----- Nudges -----
st.subheader("Personalized Nudges")
for index, row in data.iterrows():
    if 'Impulse Spending' in row['Bias Detected']:
        st.markdown(f"**Day {row['Day']}:** Try automating ${row['Actual Spend']-row['Planned Spend']} into savings to prevent overspending.")
    if 'Present Bias' in row['Bias Detected']:
        st.markdown(f"**Day {row['Day']}:** Consider small investments to grow savings over time.")
    if 'Loss Aversion' in row['Bias Detected']:
        st.markdown(f"**Day {row['Day']}:** You may be avoiding necessary spending; try allocating funds strategically.")

# ----- Charts -----
st.subheader("Spending vs Planned")
fig, ax = plt.subplots(figsize=(8,4))
ax.plot(data['Day'], data['Planned Spend'], label='Planned Spend', marker='o', color='#D32F2F')
ax.plot(data['Day'], data['Actual Spend'], label='Actual Spend', marker='o', color='green')
ax.set_xlabel('Day')
ax.set_ylabel('Amount ($)')
ax.legend()
st.pyplot(fig)

st.subheader("Cumulative Savings")
data['Cumulative Savings'] = data['Planned Spend'].cumsum() - data['Actual Spend'].cumsum()
fig2, ax2 = plt.subplots(figsize=(8,4))
ax2.bar(data['Day'], data['Cumulative Savings'], color='#D32F2F')
st.pyplot(fig2)

st.subheader("Bias Heatmap")
bias_matrix = pd.get_dummies(data['Bias Detected'].str.get_dummies(sep=', '))
sns.heatmap(bias_matrix.T, annot=True, cmap='Reds', cbar=False)
st.pyplot()
