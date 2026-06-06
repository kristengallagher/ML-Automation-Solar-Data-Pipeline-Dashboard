import streamlit as st
import pandas as pd
import plotly.express as px
import ai_module
from generate_mock_summary import generate_mock_summary

st.set_page_config(page_title="VoltView Energy Dashboard", layout="wide")

st.markdown("""
   <style>
       .main { background-color: #f0f8ff; }
       h1, h2, h3 { color: #003366; }
       .stButton>button { background-color: #007acc; color: white; }
       .stDataFrame { background-color: #ffffff; }
       footer {visibility: hidden;}
   </style>
""", unsafe_allow_html=True)

st.markdown("# VoltView Energy Dashboard")
st.markdown("### Remedies for a Greener Future™")

with st.sidebar:
   st.markdown("""
       <style>
       [data-testid="stSidebar"] {
           background-color: #003366;
           color: white;
       }
       </style>
   """, unsafe_allow_html=True)

   st.header("🔄 Upload & Filter")
   uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

   if uploaded_file:
       data = pd.read_csv(uploaded_file)
   else:
       data = pd.read_csv("cleaned_data.csv")

   data['Date'] = pd.to_datetime(data['DATE_TIME'])
   data = data.sort_values("Date")
   data['Efficiency'] = data['AC_POWER'] / (data['DC_POWER'] + 1e-6)
   data = data.replace([float("inf"), -float("inf")], 0).fillna(0)

   min_date, max_date = data['Date'].min(), data['Date'].max()
   start_date, end_date = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

filtered_data = data[(data["Date"] >= pd.to_datetime(start_date)) & (data["Date"] <= pd.to_datetime(end_date))]

features = ['Efficiency', 'IRRADIATION_Wm2', 'AMBIENT_TEMP_C', 'MODULE_TEMP_C', 'DAILY_YIELD_kWh']
model = ai_module.train_model(filtered_data[features])
filtered_data['Anomaly'] = ai_module.predict(model, filtered_data[features])
anomalies = filtered_data[filtered_data['Anomaly'] == -1]

kpi1 = filtered_data['DAILY_YIELD_kWh'].sum()
kpi2 = len(anomalies)
kpi3 = filtered_data['Efficiency'].mean()
kpi4 = filtered_data['MODULE_TEMP_C'].max()

st.markdown("### Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
kpi_col1.metric("Total Energy (kWh)", f"{kpi1:.2f}")
kpi_col2.metric("Anomalies Flagged", kpi2)
kpi_col3.metric("Avg. Efficiency", f"{kpi3:.2f}")
kpi_col4.metric("Max Module Temp (°C)", f"{kpi4:.1f}")

tab1, tab2 = st.tabs(["Dashboard", "Anomaly Logs"])

with tab1:
   st.markdown("### Energy Output Over Time")
   color_map = filtered_data['Anomaly'].map({-1: "Anomaly", 1: "Normal"})
   fig = px.scatter(
       filtered_data,
       x="Date",
       y="DAILY_YIELD_kWh",
       color=color_map,
       color_discrete_map={"Normal": "#87CEFA", "Anomaly": "red"},
       hover_data=["Efficiency", "MODULE_TEMP_C"],
       title="Energy Output with Anomaly Detection"
   )
   fig.update_traces(marker=dict(size=6))
   fig.update_layout(
       xaxis_title="Date",
       yaxis_title="Daily Yield (kWh)",
       plot_bgcolor='#f0f8ff',
       paper_bgcolor='#f0f8ff',
   )
   st.plotly_chart(fig, use_container_width=True)

   st.markdown("### Weekly Summary")
   summary = generate_mock_summary(filtered_data)
   st.markdown(summary)

with tab2:
   st.markdown("### Search Anomaly Alerts")
   alerts_df = anomalies[['Date', 'DAILY_YIELD_kWh', 'Efficiency', 'MODULE_TEMP_C']].copy()
   alerts_df.rename(columns={
       'DAILY_YIELD_kWh': 'Daily Yield (kWh)',
       'MODULE_TEMP_C': 'Module Temp (°C)'
   }, inplace=True)

   search_term = st.text_input("Search by date (YYYY-MM-DD) or yield (e.g. 3200):").lower()
   if search_term:
       alerts_filtered = alerts_df[alerts_df.apply(lambda row: search_term in str(row['Date']) or search_term in str(row['Daily Yield (kWh)']), axis=1)]
   else:
       alerts_filtered = alerts_df

   st.dataframe(alerts_filtered, use_container_width=True)

   st.markdown("### Alert Log")

   log_search = st.text_input("Search log by any field (e.g. 2025-07-06, 3200, 0.87):", key="log_search").lower()
   if log_search:
       filtered_log = alerts_filtered[alerts_filtered.apply(
           lambda row: any(log_search in str(v).lower() for v in row.values), axis=1)]
   else:
       filtered_log = alerts_filtered

   for _, row in filtered_log.iterrows():
       date_str = row['Date'].strftime('%Y-%m-%d %H:%M')
       st.markdown(f"- **{date_str}** | Yield: **{row['Daily Yield (kWh)']:.2f} kWh**, Efficiency: **{row['Efficiency']:.2f}**, Module Temp: **{row['Module Temp (°C)']:.1f}°C**")

csv = alerts_df.to_csv(index=False).encode('utf-8')
st.download_button(
   label="Download Anomalies (CSV)",
   data=csv,
   file_name="anomaly_alerts.csv",
   mime="text/csv"
)
from datetime import datetime
import os

google_drive_path = "/Users/kristengallagher/Library/CloudStorage/GoogleDrive-kristengallagher999@gmail.com/My Drive/VoltView_Alerts"
os.makedirs(google_drive_path, exist_ok=True)

zapier_alerts = anomalies[['Date', 'DAILY_YIELD_kWh']].copy()
zapier_alerts.rename(columns={
    'Date': 'date',
    'DAILY_YIELD_kWh': 'output_kwh'
}, inplace=True)
zapier_alerts.to_csv(os.path.join(google_drive_path, "alerts_today.csv"), index=False)

today_str = datetime.now().strftime('%Y-%m-%d')
alerts_csv_path = os.path.join(google_drive_path, f"alerts_{today_str}.csv")
alerts_df.to_csv(alerts_csv_path, index=False)

avg_eff = anomalies['Efficiency'].mean()
max_temp = anomalies['MODULE_TEMP_C'].max()
total_energy = anomalies['DAILY_YIELD_kWh'].sum()

with open(os.path.join(google_drive_path, "alerts_today.csv"), "a") as f:
    f.write(f"SUMMARY, Avg. Efficiency: {kpi3:.2f}, Max Temp: {kpi4:.1f}°C, Total Energy: {kpi1:,.0f} kWh\n")

summary_only_path = os.path.join(google_drive_path, "alerts_summary_only.csv")
with open(summary_only_path, "w") as f:
    f.write(f"SUMMARY, Avg. Efficiency: {kpi3:.2f}, Max Temp: {kpi4:.1f}°C, Total Energy: {kpi1:,.0f} kWh\n")

import requests

slack_webhook_url = "https://hooks.slack.com/services/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"

 USE KPI variables
message = (
    "Anomaly Detected in Today's Solar Output\n\n"
    f"Energy Output: {kpi1:,.0f} kWh\n"
    f"Average Efficiency: {kpi3:.2f}\n"
    f"Max Module Temp: {kpi4:.1f}°C\n\n"
    "Check your VoltView_Alerts folder for full data."
)

response = requests.post(slack_webhook_url, json={"text": message})

if response.status_code == 200:
    print("Slack alert sent.")
else:
    print("Slack alert failed:", response.text)

st.markdown("""
   <div style='text-align: center; padding: 10px; color: #003366;'>
       <strong>VoltView</strong> | Your Renewable Remedy™
   </div>
""", unsafe_allow_html=True)

