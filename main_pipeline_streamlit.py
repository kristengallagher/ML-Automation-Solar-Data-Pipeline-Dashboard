import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from generate_mock_summary import generate_mock_summary
import ai_module
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

st.set_page_config(
    page_title="Solaire",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://rsms.me/inter/inter.css');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        background: linear-gradient(180deg, #fafafa 0%, #ffffff 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }

    button[kind="header"] {
        background-color: #667eea !important;
        color: white !important;
    }

    button[kind="header"]:hover {
        background-color: #5568d3 !important;
    }

    [data-testid="stSidebar"] h3 {
        color: #111827 !important;
    }

    [data-testid="stSidebar"] label {
        color: #111827 !important;
    }

    [data-testid="stSidebar"] p {
        color: #111827 !important;
    }

    [data-baseweb="calendar"] {
        background: white !important;
    }

    [data-baseweb="calendar"] *,
    [data-baseweb="calendar"] button,
    [data-baseweb="calendar"] div,
    [data-baseweb="calendar"] span {
        color: #111827 !important;
        background-color: transparent !important;
    }

    [data-baseweb="calendar"] button {
        color: #111827 !important;
        background-color: white !important;
    }

    [data-baseweb="calendar"] button:hover {
        background-color: #f3f4f6 !important;
        color: #111827 !important;
    }

    [data-testid="stDateInput"] input {
        color: #111827 !important;
        background-color: white !important;
    }

    [data-baseweb="calendar"] [role="heading"],
    [data-baseweb="select"],
    [data-baseweb="select"] * {
        color: #111827 !important;
        background-color: white !important;
    }

    [data-baseweb="popover"] * {
        color: #111827 !important;
    }

    input, select, textarea {
        color: #111827 !important;
        background-color: white !important;
    }

    [data-testid="stFileUploader"] {
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #667eea 0%, #764ba2 100%) border-box !important;
        border: 2px dashed transparent !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        background: linear-gradient(#f9fafb, #f9fafb) padding-box,
                    linear-gradient(135deg, #667eea 0%, #764ba2 100%) border-box !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2) !important;
    }

    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] div,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: #111827 !important;
    }

    [data-testid="stFileUploader"] * {
        color: #111827 !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }

    [data-testid="stFileUploadDropzone"] *,
    [data-testid="stFileUploadDropzone"] button,
    [data-testid="stFileUploadDropzone"] span {
        color: #111827 !important;
        background-color: transparent !important;
    }

    [data-testid="stFileUploader"] small {
        color: #6b7280 !important;
    }

    [data-testid="stFileUploader"] button[kind="secondary"] {
        color: #111827 !important;
        background-color: white !important;
        border: 1px solid #e5e7eb !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stFileUploader"] button[kind="secondary"]:hover {
        background-color: #dc2626 !important;
        color: white !important;
        border-color: #dc2626 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3) !important;
    }

    h1, h2, h3, h4 {
        color: #111827 !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }

    h3 {
        font-size: 1.125rem;
        margin-bottom: 1rem;
        color: #111827 !important;
    }

    p, span, div, label {
        color: #111827 !important;
    }

    [data-testid="stSidebar"] h3 {
        color: #111827 !important;
    }

    [data-testid="stSidebar"] p {
        color: #4b5563 !important;
    }

    [data-testid="stSidebar"] label {
        color: #111827 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }

    .stDownloadButton>button {
        background: white !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
    }

    .stDownloadButton>button:hover {
        background: #f0f4ff !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #e5e7eb;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 0;
        color: #6b7280;
        font-weight: 500;
        font-size: 0.875rem;
        border-bottom: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        color: #111827;
        border-bottom: 2px solid #111827;
    }

    .stTextInput>div>div>input {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.625rem 0.875rem;
        font-size: 0.875rem;
        transition: all 0.2s;
    }

    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    [data-testid="stFileUploader"] {
        border: 2px dashed #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        background: #fafafa;
        transition: all 0.2s;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: #f9fafb;
    }

    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stMetricValue"] {
        font-size: 0;
    }

    .stPlotlyChart {
        background-color: #ffffff !important;
    }

    [data-testid="stHorizontalBlock"] {
        background-color: transparent !important;
    }

    .element-container {
        background-color: transparent !important;
    }

    [data-testid="column"] {
        background-color: transparent !important;
    }

    .block-container {
        background-color: #ffffff !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }

    [data-testid="stHeader"] {
        background-color: #ffffff !important;
    }

    .main .block-container {
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');

    .header-container * {
        color: #ffffff !important;
    }
    </style>

    <div class='header-container' style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    '>
        <div style='max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 1.5rem;'>
            <div style='flex: 1;'>
                <h1 style='
                    font-family: "Montserrat", sans-serif;
                    color: #ffffff !important;
                    margin: 0 0 0.5rem 0;
                    font-size: 3.5rem;
                    font-weight: 700;
                    letter-spacing: 0.02em;
                '>Solaire</h1>
                <p style='
                    font-family: "Montserrat", sans-serif;
                    color: #ffffff !important;
                    opacity: 0.95;
                    margin: 0;
                    font-size: 1.125rem;
                    font-weight: 400;
                    letter-spacing: 0.03em;
                '>Remedies for a Greener Future</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h3 style='margin-top: 0;'>Data Source</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type="csv", label_visibility="collapsed")

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv("cleaned_data.csv")

    data['Date'] = pd.to_datetime(data['DATE_TIME'], format='mixed', errors='coerce')
    data = data.sort_values("Date")
    data['Efficiency'] = data['AC_POWER'] / (data['DC_POWER'] + 1e-6)
    data = data.replace([float("inf"), -float("inf")], 0).fillna(0)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Filters</h3>", unsafe_allow_html=True)

    min_date, max_date = data['Date'].min(), data['Date'].max()
    start_date, end_date = st.date_input(
        "Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

filtered_data = data[(data["Date"] >= pd.to_datetime(start_date)) & (data["Date"] <= pd.to_datetime(end_date))].copy()

features = ['Efficiency', 'IRRADIATION_Wm2', 'AMBIENT_TEMP_C', 'MODULE_TEMP_C', 'DAILY_YIELD_kWh']
model = ai_module.train_model(filtered_data[features])
filtered_data['Anomaly'] = ai_module.predict(model, filtered_data[features])
anomalies = filtered_data[filtered_data['Anomaly'] == -1].copy()

total_energy = filtered_data['DAILY_YIELD_kWh'].sum()
num_anomalies = len(anomalies)
avg_efficiency = filtered_data['Efficiency'].mean()
max_temp = filtered_data['MODULE_TEMP_C'].max()

st.markdown("<h3 style='margin-bottom: 1.5rem;'>Performance Overview</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div style='
            background: white;
            padding: 1.75rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: all 0.2s;
        '>
            <p style='
                color: #6b7280;
                font-size: 0.8125rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin: 0 0 0.5rem 0;
            '>Total Energy</p>
            <h2 style='
                color: #111827;
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: -0.02em;
            '>{total_energy:,.0f}</h2>
            <p style='
                color: #9ca3af;
                font-size: 0.8125rem;
                margin: 0.25rem 0 0 0;
            '>kWh</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style='
            background: white;
            padding: 1.75rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: all 0.2s;
        '>
            <p style='
                color: #6b7280;
                font-size: 0.8125rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin: 0 0 0.5rem 0;
            '>Anomalies</p>
            <h2 style='
                color: #dc2626;
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: -0.02em;
            '>{num_anomalies}</h2>
            <p style='
                color: #9ca3af;
                font-size: 0.8125rem;
                margin: 0.25rem 0 0 0;
            '>flagged</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style='
            background: white;
            padding: 1.75rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: all 0.2s;
        '>
            <p style='
                color: #6b7280;
                font-size: 0.8125rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin: 0 0 0.5rem 0;
            '>Efficiency</p>
            <h2 style='
                color: #059669;
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: -0.02em;
            '>{avg_efficiency:.1%}</h2>
            <p style='
                color: #9ca3af;
                font-size: 0.8125rem;
                margin: 0.25rem 0 0 0;
            '>average</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div style='
            background: white;
            padding: 1.75rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: all 0.2s;
        '>
            <p style='
                color: #6b7280;
                font-size: 0.8125rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin: 0 0 0.5rem 0;
            '>Peak Temp</p>
            <h2 style='
                color: #111827;
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: -0.02em;
            '>{max_temp:.1f}</h2>
            <p style='
                color: #9ca3af;
                font-size: 0.8125rem;
                margin: 0.25rem 0 0 0;
            '>°C</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Analytics", "Anomalies", "Advanced Insights"])

with tab1:
    st.markdown("<h3>Energy Output</h3>", unsafe_allow_html=True)

    fig = go.Figure()

    normal_data = filtered_data[filtered_data['Anomaly'] == 1]
    fig.add_trace(go.Scatter(
        x=normal_data['Date'],
        y=normal_data['DAILY_YIELD_kWh'],
        mode='markers',
        name='Normal',
        marker=dict(
            color='#667eea',
            size=5,
            opacity=0.6,
            line=dict(width=0)
        ),
        hovertemplate='<b>%{x}</b><br>Output: %{y:.2f} kWh<extra></extra>'
    ))

    anomaly_data = filtered_data[filtered_data['Anomaly'] == -1]
    fig.add_trace(go.Scatter(
        x=anomaly_data['Date'],
        y=anomaly_data['DAILY_YIELD_kWh'],
        mode='markers',
        name='Anomaly',
        marker=dict(
            color='#dc2626',
            size=8,
            symbol='diamond',
            line=dict(width=1, color='white')
        ),
        hovertemplate='<b>%{x}</b><br>Output: %{y:.2f} kWh<br><i>Anomaly detected</i><extra></extra>'
    ))

    fig.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family='Inter, sans-serif', size=12, color='#111827'),
        xaxis=dict(
            title='',
            showgrid=True,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb',
            zeroline=False,
            tickfont=dict(color='#111827')
        ),
        yaxis=dict(
            title=dict(text='Daily Yield (kWh)', font=dict(color='#111827')),
            showgrid=True,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb',
            zeroline=False,
            tickfont=dict(color='#111827')
        ),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=0,
            font=dict(size=11, color='#111827'),
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#e5e7eb',
            borderwidth=1
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=450,
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family='Inter, sans-serif',
            font_color='#111827'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br><h3>Performance Summary</h3>", unsafe_allow_html=True)
    summary = generate_mock_summary(filtered_data)
    st.markdown(f"""
        <div style='
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            color: #4b5563;
            line-height: 1.6;
            font-size: 0.9375rem;
        '>
            {summary}
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("<h3>Anomaly Detection</h3>", unsafe_allow_html=True)

    if len(anomalies) > 0:
        panel_issues = anomalies['SOURCE_KEY'].value_counts().head(5)

        st.markdown("<h4 style='margin-top: 0; font-size: 1rem; color: #6b7280;'>Top Problem Panels</h4>",
                    unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for idx, (panel_id, count) in enumerate(panel_issues.items()):
            if idx < 5:
                with cols[idx]:
                    st.markdown(f"""
                        <div style='
                            background: #fef2f2;
                            padding: 1rem;
                            border-radius: 8px;
                            border-left: 3px solid #dc2626;
                            text-align: center;
                        '>
                            <p style='
                                color: #6b7280;
                                font-size: 0.75rem;
                                margin: 0 0 0.25rem 0;
                                text-transform: uppercase;
                                letter-spacing: 0.05em;
                            '>Panel</p>
                            <p style='
                                color: #111827;
                                font-size: 0.875rem;
                                font-weight: 600;
                                margin: 0 0 0.5rem 0;
                                overflow: hidden;
                                text-overflow: ellipsis;
                                white-space: nowrap;
                            '>{panel_id}</p>
                            <p style='
                                color: #dc2626;
                                font-size: 1.25rem;
                                font-weight: 700;
                                margin: 0;
                            '>{count}</p>
                            <p style='
                                color: #9ca3af;
                                font-size: 0.7rem;
                                margin: 0.25rem 0 0 0;
                            '>issues</p>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    alerts_df = anomalies[['Date', 'SOURCE_KEY', 'DAILY_YIELD_kWh', 'Efficiency', 'MODULE_TEMP_C']].copy()
    alerts_df.rename(columns={
        'SOURCE_KEY': 'Panel ID',
        'DAILY_YIELD_kWh': 'Daily Yield (kWh)',
        'MODULE_TEMP_C': 'Module Temp (°C)'
    }, inplace=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input(
            "Search anomalies",
            placeholder="Search by panel ID, date, yield, or temperature...",
            label_visibility="collapsed"
        ).lower()

    if search_term:
        alerts_filtered = alerts_df[alerts_df.apply(
            lambda row: any(search_term in str(v).lower() for v in row.values),
            axis=1
        )]
    else:
        alerts_filtered = alerts_df

    if len(anomalies) > 0:
        st.markdown("<br><h4 style='font-size: 1rem; color: #6b7280;'>Anomalies by Panel</h4>", unsafe_allow_html=True)

        panel_counts = anomalies['SOURCE_KEY'].value_counts().head(10)

        fig_panels = go.Figure(data=[
            go.Bar(
                x=panel_counts.index,
                y=panel_counts.values,
                marker=dict(
                    color='#dc2626',
                    line=dict(color='#991b1b', width=1)
                ),
                text=panel_counts.values,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Anomalies: %{y}<extra></extra>'
            )
        ])

        fig_panels.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family='Inter, sans-serif', size=11, color='#111827'),
            xaxis=dict(
                title='Panel ID',
                showgrid=False,
                showline=True,
                linecolor='#e5e7eb',
                tickfont=dict(color='#111827')
            ),
            yaxis=dict(
                title=dict(text='Number of Anomalies', font=dict(color='#111827')),
                showgrid=True,
                gridcolor='#f3f4f6',
                showline=True,
                linecolor='#e5e7eb',
                tickfont=dict(color='#111827')
            ),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            showlegend=False
        )

        st.plotly_chart(fig_panels, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.dataframe(
        alerts_filtered.style.format({
            'Daily Yield (kWh)': '{:.2f}',
            'Efficiency': '{:.2%}',
            'Module Temp (°C)': '{:.1f}'
        }),
        use_container_width=True,
        height=400
    )

    csv = alerts_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export Data",
        data=csv,
        file_name=f"solaire_anomalies_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with tab3:
    st.markdown("<h3>Advanced Analytics</h3>", unsafe_allow_html=True)

    st.markdown("<h4 style='font-size: 1rem; color: #6b7280; margin-top: 1rem;'>Financial Impact Analysis</h4>",
                unsafe_allow_html=True)

    PRICE_PER_KWH = 0.12

    if len(anomalies) > 0:
        avg_normal_yield = filtered_data[filtered_data['Anomaly'] == 1]['DAILY_YIELD_kWh'].mean()
        avg_anomaly_yield = anomalies['DAILY_YIELD_kWh'].mean()
        energy_loss_per_anomaly = max(0, avg_normal_yield - avg_anomaly_yield)
        total_energy_loss = energy_loss_per_anomaly * len(anomalies)
        lost_revenue = total_energy_loss * PRICE_PER_KWH
        downtime_hours = len(anomalies) * 0.5
        hourly_revenue = (total_energy / 24) * PRICE_PER_KWH if total_energy > 0 else 0
    else:
        total_energy_loss = 0
        lost_revenue = 0
        downtime_hours = 0
        hourly_revenue = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div style='
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            '>
                <p style='
                    color: #6b7280;
                    font-size: 0.8125rem;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin: 0 0 0.5rem 0;
                '>Lost Revenue</p>
                <h2 style='
                    color: #dc2626;
                    margin: 0;
                    font-size: 1.75rem;
                    font-weight: 700;
                '>${lost_revenue:,.2f}</h2>
                <p style='
                    color: #9ca3af;
                    font-size: 0.8125rem;
                    margin: 0.25rem 0 0 0;
                '>from anomalies</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style='
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            '>
                <p style='
                    color: #6b7280;
                    font-size: 0.8125rem;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin: 0 0 0.5rem 0;
                '>Energy Loss</p>
                <h2 style='
                    color: #111827;
                    margin: 0;
                    font-size: 1.75rem;
                    font-weight: 700;
                '>{total_energy_loss:,.0f}</h2>
                <p style='
                    color: #9ca3af;
                    font-size: 0.8125rem;
                    margin: 0.25rem 0 0 0;
                '>kWh lost</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style='
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            '>
                <p style='
                    color: #6b7280;
                    font-size: 0.8125rem;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin: 0 0 0.5rem 0;
                '>Downtime</p>
                <h2 style='
                    color: #111827;
                    margin: 0;
                    font-size: 1.75rem;
                    font-weight: 700;
                '>{downtime_hours:.1f}</h2>
                <p style='
                    color: #9ca3af;
                    font-size: 0.8125rem;
                    margin: 0.25rem 0 0 0;
                '>hours estimated</p>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div style='
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            '>
                <p style='
                    color: #6b7280;
                    font-size: 0.8125rem;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin: 0 0 0.5rem 0;
                '>Revenue Rate</p>
                <h2 style='
                    color: #059669;
                    margin: 0;
                    font-size: 1.75rem;
                    font-weight: 700;
                '>${hourly_revenue:,.2f}</h2>
                <p style='
                    color: #9ca3af;
                    font-size: 0.8125rem;
                    margin: 0.25rem 0 0 0;
                '>per hour</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4 style='font-size: 1rem; color: #6b7280;'>Temperature vs. Efficiency</h4>",
                    unsafe_allow_html=True)

        optimal_temp = 25
        temp_coefficient = -0.004

        filtered_data['Expected_Efficiency'] = filtered_data['MODULE_TEMP_C'].apply(
            lambda t: max(0, avg_efficiency * (1 + temp_coefficient * (t - optimal_temp)))
        )

        fig_temp = go.Figure()

        fig_temp.add_trace(go.Scatter(
            x=filtered_data['MODULE_TEMP_C'],
            y=filtered_data['Efficiency'],
            mode='markers',
            name='Actual',
            marker=dict(color='#667eea', size=6, opacity=0.6),
            hovertemplate='<b>Temp:</b> %{x:.1f}°C<br><b>Efficiency:</b> %{y:.1%}<extra></extra>'
        ))

        temp_sorted = filtered_data.sort_values('MODULE_TEMP_C')
        fig_temp.add_trace(go.Scatter(
            x=temp_sorted['MODULE_TEMP_C'],
            y=temp_sorted['Expected_Efficiency'],
            mode='lines',
            name='Expected',
            line=dict(color='#10b981', width=2, dash='dash'),
            hovertemplate='<b>Temp:</b> %{x:.1f}°C<br><b>Expected:</b> %{y:.1%}<extra></extra>'
        ))

        fig_temp.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family='Inter, sans-serif', size=11, color='#111827'),
            xaxis=dict(
                title=dict(text='Module Temperature (°C)', font=dict(color='#111827')),
                showgrid=True,
                gridcolor='#f3f4f6',
                showline=True,
                linecolor='#e5e7eb',
                tickfont=dict(color='#111827')
            ),
            yaxis=dict(
                title=dict(text='Efficiency', font=dict(color='#111827')),
                showgrid=True,
                gridcolor='#f3f4f6',
                showline=True,
                linecolor='#e5e7eb',
                tickfont=dict(color='#111827'),
                tickformat='.0%'
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='left',
                x=0,
                font=dict(size=11, color='#111827')
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            height=350
        )

        st.plotly_chart(fig_temp, use_container_width=True)

    with col2:
        st.markdown("<h4 style='font-size: 1rem; color: #6b7280;'>Irradiation vs. Energy Output</h4>",
                    unsafe_allow_html=True)

        fig_irrad = go.Figure()

        normal_data = filtered_data[filtered_data['Anomaly'] == 1]
        fig_irrad.add_trace(go.Scatter(
            x=normal_data['IRRADIATION_Wm2'],
            y=normal_data['DAILY_YIELD_kWh'],
            mode='markers',
            name='Normal',
            marker=dict(color='#667eea', size=6, opacity=0.6),
            hovertemplate='<b>Irradiation:</b> %{x:.0f} W/m²<br><b>Output:</b> %{y:.0f} kWh<extra></extra>'
        ))

        anomaly_points = filtered_data[filtered_data['Anomaly'] == -1]
        fig_irrad.add_trace(go.Scatter(
            x=anomaly_points['IRRADIATION_Wm2'],
            y=anomaly_points['DAILY_YIELD_kWh'],
            mode='markers',
            name='Anomaly',
            marker=dict(color='#dc2626', size=8, symbol='diamond'),
            hovertemplate='<b>Irradiation:</b> %{x:.0f} W/m²<br><b>Output:</b> %{y:.0f} kWh<br><i>Anomaly</i><extra></extra>'
        ))

        fig_irrad.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family='Inter, sans-serif', size=11, color='#111827'),
            xaxis=dict(
                title=dict(text='Solar Irradiation (W/m²)', font=dict(color='#111827')),
                showgrid=True,
                gridcolor='#f3f4f6',
                showline=True,
                linecolor='#e5e7eb',
                tickfont=dict(color='#111827')
            ),
            yaxis=dict(
                title=dict(text='Daily Yield (kWh)', font=dict(color='#111827')),
                showgrid=True,
                gridcolor='#f3f4f6',
                showline=True,
                linecolor='#e5e7eb',
                tickfont=dict(color='#111827')
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='left',
                x=0,
                font=dict(size=11, color='#111827')
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            height=350
        )

        st.plotly_chart(fig_irrad, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h4 style='font-size: 1rem; color: #6b7280;'>Panel Health Dashboard</h4>", unsafe_allow_html=True)

    panel_health = []

    for panel_id in filtered_data['SOURCE_KEY'].unique():
        panel_data = filtered_data[filtered_data['SOURCE_KEY'] == panel_id]

        anomaly_count = len(panel_data[panel_data['Anomaly'] == -1])
        avg_eff = panel_data['Efficiency'].mean()
        efficiency_score = min(100, avg_eff * 200)
        anomaly_penalty = min(50, anomaly_count * 5)

        health_score = max(0, efficiency_score - anomaly_penalty)

        if health_score >= 80:
            status = "Healthy"
            color = "#059669"
        elif health_score >= 60:
            status = "Monitor"
            color = "#f59e0b"
        else:
            status = "Critical"
            color = "#dc2626"

        panel_health.append({
            'Panel ID': panel_id,
            'Health Score': health_score,
            'Status': status,
            'Color': color,
            'Anomalies': anomaly_count,
            'Avg Efficiency': avg_eff
        })

    panel_health_sorted = sorted(panel_health, key=lambda x: x['Health Score'])

    st.markdown(
        "<p style='color: #6b7280; font-size: 0.875rem; margin-bottom: 1rem;'>Critical Panels Requiring Attention</p>",
        unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, panel in enumerate(panel_health_sorted[:5]):
        with cols[idx]:
            st.markdown(f"""
                <div style='
                    background: white;
                    padding: 1.25rem;
                    border-radius: 10px;
                    border-left: 4px solid {panel['Color']};
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                    text-align: center;
                '>
                    <p style='
                        color: #6b7280;
                        font-size: 0.7rem;
                        margin: 0 0 0.25rem 0;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    '>Panel</p>
                    <p style='
                        color: #111827;
                        font-size: 0.8rem;
                        font-weight: 600;
                        margin: 0 0 0.75rem 0;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    '>{panel['Panel ID'][:12]}...</p>
                    <div style='
                        background: {panel['Color']};
                        color: white;
                        padding: 0.5rem;
                        border-radius: 8px;
                        margin-bottom: 0.5rem;
                    '>
                        <p style='
                            font-size: 1.5rem;
                            font-weight: 700;
                            margin: 0;
                        '>{panel['Health Score']:.0f}</p>
                        <p style='
                            font-size: 0.7rem;
                            margin: 0;
                            opacity: 0.9;
                        '>Score</p>
                    </div>
                    <p style='
                        color: {panel['Color']};
                        font-size: 0.75rem;
                        font-weight: 600;
                        margin: 0;
                    '>{panel['Status'].upper()}</p>
                    <p style='
                        color: #9ca3af;
                        font-size: 0.7rem;
                        margin: 0.25rem 0 0 0;
                    '>{panel['Anomalies']} issues</p>
                </div>
            """, unsafe_allow_html=True)

google_drive_path = "/Users/kristengallagher/Library/CloudStorage/GoogleDrive-kristengallagher999@gmail.com/My Drive/Solaire_Alerts"
os.makedirs(google_drive_path, exist_ok=True)

zapier_alerts = anomalies[['Date', 'DAILY_YIELD_kWh']].copy()
zapier_alerts.rename(columns={'Date': 'date', 'DAILY_YIELD_kWh': 'output_kwh'}, inplace=True)
zapier_alerts.to_csv(os.path.join(google_drive_path, "alerts_today.csv"), index=False)

today_str = datetime.now().strftime('%Y-%m-%d')
alerts_csv_path = os.path.join(google_drive_path, f"alerts_{today_str}.csv")
alerts_df.to_csv(alerts_csv_path, index=False)

with open(os.path.join(google_drive_path, "alerts_today.csv"), "a") as f:
    f.write(
        f"SUMMARY, Avg. Efficiency: {avg_efficiency:.2f}, Max Temp: {max_temp:.1f}°C, Total Energy: {total_energy:,.0f} kWh\n")

summary_only_path = os.path.join(google_drive_path, "alerts_summary_only.csv")
with open(summary_only_path, "w") as f:
    f.write(
        f"SUMMARY, Avg. Efficiency: {avg_efficiency:.2f}, Max Temp: {max_temp:.1f}°C, Total Energy: {total_energy:,.0f} kWh\n")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

if len(anomalies) > 0:
    top_problem_panels = anomalies['SOURCE_KEY'].value_counts().head(3)
    panel_list = "\n".join([f"• {panel}: {count} issues" for panel, count in top_problem_panels.items()])

    PRICE_PER_KWH = 0.12
    avg_normal_yield = filtered_data[filtered_data['Anomaly'] == 1]['DAILY_YIELD_kWh'].mean()
    avg_anomaly_yield = anomalies['DAILY_YIELD_kWh'].mean()
    energy_loss_per_anomaly = avg_normal_yield - avg_anomaly_yield
    total_energy_loss = energy_loss_per_anomaly * len(anomalies)
    lost_revenue = total_energy_loss * PRICE_PER_KWH

    if num_anomalies > 50:
        severity = "CRITICAL"
    elif num_anomalies > 20:
        severity = "WARNING"
    else:
        severity = "INFO"

    message = (
        f"SOLAIRE ALERT - {severity}\n\n"
        f"Overview:\n"
        f"• Total Anomalies: {num_anomalies}\n"
        f"• Energy Output: {total_energy:,.0f} kWh\n"
        f"• Average Efficiency: {avg_efficiency:.1%}\n"
        f"• Max Module Temp: {max_temp:.1f}°C\n\n"
        f"Top Problem Panels:\n{panel_list}\n\n"
        f"Financial Impact:\n"
        f"• Estimated Energy Loss: {total_energy_loss:,.0f} kWh\n"
        f"• Lost Revenue: ${lost_revenue:,.2f}\n\n"
        f"Recommended Action:\n"
        f"• Immediate inspection of top {min(3, len(top_problem_panels))} panels\n"
        f"• Check for: soiling, shading, equipment failure\n\n"
        f"Full report available in Solaire_Alerts folder"
    )
else:
    message = (
        "SOLAIRE STATUS: All Clear\n\n"
        f"No anomalies detected in current period.\n"
        f"Total Energy: {total_energy:,.0f} kWh\n"
        f"Average Efficiency: {avg_efficiency:.1%}"
    )

try:
    response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=5)
    if response.status_code == 200:
        print("✓ Slack alert sent successfully.")
    else:
        print(f"⚠ Slack alert failed: {response.status_code} - {response.text}")
except requests.exceptions.RequestException as e:
    print(f"⚠ Slack alert skipped: {str(e)}")
except Exception as e:
    print(f"⚠ Slack alert error: {str(e)}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='
        text-align: center;
        padding: 2rem 0;
        color: #9ca3af;
        font-size: 0.8125rem;
        border-top: 1px solid #e5e7eb;
    '>
        <strong style='color: #111827;'>Solaire</strong> - Remedies for a Greener Future
    </div>
""", unsafe_allow_html=True)
