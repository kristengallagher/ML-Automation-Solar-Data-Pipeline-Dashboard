## What I did:
Built a fully functional Streamlit app for solar anomaly detection and performance visualization
Implemented file upload with automatic data cleaning and standardization using pandas(pd.to_datetime, fillna, replace)
Developed KPI tracking (Total Yield, Efficiency, Module Temp, Anomalies)
Built interactive visualizations with Plotly for anomaly detection and yield trends
Integrated a tabbed dashboard with searchable alert logs
Enabled file export functionality (CSV) and Google Drive output automation
Triggered Zapier and Slack alerts using requests and Zapier-exported CSVs
Delivered summaries using an LLM fallback function (mock summary generator)
Polished frontend styling with custom CSS for professional, branded UI

## What I would work on with more time:
-  Create login screen with specific user profiles
- Get API key to autogenerate summaries using ChatGPT
- Refine UI to look more professional (tailor it to my liking)
- Implement an anomaly classification model (not just detection)
- Add a notification center with history tracking and read/unread states
- Refine GPT summary with live API integration
- Switch to React 

## What I Learned:
- How to rapidly prototype a real-world AI dashboard using Python, Streamlit, and ML libraries
- How to work around API constraints 
- The value of clear UI/UX in explaining technical results to non-technical users
- Real-world alerting pipelines using Slack, Zapier, and Google Drive integration
- How to break down user needs (like Roberto’s) and match technical features to their workflows

## Bugs and Fixes:
Bug: Zapier wasn’t triggering email alerts from the output CSV
Fix: Zapier trigger failed due CSV file being too large → created alerts_summary_only.csv so Zapier could read in the data and output email with data collected from updated CSV files. 

Bug: streamlit run command wasn’t launching the app
Fix: Initially ran python script.py instead of streamlit run script.py →  updated launch method and confirmed local server opened correctly

Bug: pd.to_datetime() failed on some date inputs
Fix: Added consistent data['Date'] = pd.to_datetime(data['DATE_TIME']) conversion and cleaned source files to remove bad rows.

Bug: CSVs with lowercase column headers broke the pipeline
Fix: Added .str.upper() to standardize column names before processing so different naming styles wouldn’t cause key errors.

Bug: Anomalies weren’t showing in chart color-coding
Fix: IsolationForest output (-1/1) wasn’t mapped to labels. Added .map({-1: "Anomaly", 1: "Normal"}) and confirmed it reflected in Plotly chart colors.

ug: Summary panel displayed nothing with new uploads
Fix: generate_mock_summary() wasn’t being called after file upload → added if uploaded_file: logic to reprocess data and trigger new summary generation.
