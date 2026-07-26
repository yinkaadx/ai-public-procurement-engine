import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="AI Public Procurement Engine", layout="wide")

st.title("Serverless E-Procurement Pipeline")
st.caption("Real-Time AI Vendor Evaluation & Supply Chain Integrity Monitoring")

st.sidebar.header("Government Marketplace Configuration")
selected_sector = st.sidebar.selectbox("Target Procurement Sector", ["National Healthcare Logistics", "Defense & Aerospace Commissioning", "Smart City Infrastructure (SME Network)"])
anomaly_severity = st.sidebar.slider("Simulate Vendor Anomaly / Friction", 1.0, 5.0, 2.5)
run_simulation = st.sidebar.button("Initialize AI Procurement Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: E-Procurement API -> AWS Lambda -> XGBoost Vendor Scoring")

if run_simulation:
    st.subheader(f"Active Public Contracting Monitor: {selected_sector}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_bids = col1.empty()
    metric_latency = col2.empty()
    metric_integrity = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(2121)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    bid_volumes = []
    integrity_scores = []
    
    base_bids = 500 
    base_integrity = 95.0
    
    for i in range(100):
        if i < 30:
            current_bids = base_bids + int(np.random.uniform(-50, 100))
            current_integrity = base_integrity + np.random.uniform(-2.0, 2.0)
            latency = np.random.uniform(15.0, 25.0)
        elif i >= 30 and i < 65:
            current_bids = base_bids + int((i - 30) * (50 * anomaly_severity)) + int(np.random.uniform(-100, 100))
            current_integrity = base_integrity - (i - 30) * (0.8 * anomaly_severity) + np.random.uniform(-5.0, 5.0)
            latency = np.random.uniform(25.0, 45.0)
        else:
            current_bids = current_bids - int(np.random.uniform(50, 150))
            current_bids = max(base_bids, current_bids)
            current_integrity = min(98.0, current_integrity + np.random.uniform(2.0, 5.0))
            latency = np.random.uniform(20.0, 30.0)
            
        bid_volumes.append(current_bids)
        integrity_scores.append(current_integrity)
        
        metric_bids.metric("Live Bid Submissions (API)", f"{current_bids:,} / hr")
        metric_latency.metric("AWS Ingestion Latency", f"{latency:.1f} ms", "- Serverless Optimized")
        metric_integrity.metric("Vendor Integrity Score", f"{current_integrity:.1f} pts")
        
        if current_integrity < 75.0:
            metric_status.metric("AI Contracting Assessment", "HIGH RISK ANOMALY", "Review Required")
        else:
            metric_status.metric("AI Contracting Assessment", "CLEARED FOR COMMISSIONING", "Standard")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=bid_volumes, mode='lines', name='Procurement Marketplace Volume', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=integrity_scores, mode='lines', name='AI Integrity & Performance Score', yaxis='y2', line=dict(color='red', dash='dot')))
        
        fig.update_layout(
            title="Digital Public Procurement: Bid Ingestion Velocity vs AI-Driven Vendor Integrity",
            xaxis=dict(title="High-Frequency API Timestamp"),
            yaxis=dict(title="Bid Volume"),
            yaxis2=dict(title="Integrity Score (Pts)", overlaying='y', side='right', range=[0, 100]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if current_integrity < 75.0 and i == 45:
            log_placeholder.error(f"PROCUREMENT ALERT: Severe anomaly detected in SME supply chain logistics at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine actively red-flagging contract bids for compliance review.")
        elif current_integrity >= 75.0 and i % 5 == 0:
            log_placeholder.success(f"Log: E-Procurement telemetry tick {i} ingested via serverless middleware. Vendor metrics operating within optimal institutional parameters.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The cloud-native machine learning pipeline successfully identified hidden vendor risks and optimized public sector performance evaluation.")
else:
    st.info("Click 'Initialize AI Procurement Engine' in the sidebar to simulate high-frequency digital government data ingestion.")