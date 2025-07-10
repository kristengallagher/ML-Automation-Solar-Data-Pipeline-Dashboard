<<<<<<< HEAD
## ML Problem
Workflow Pain Point: Manually predicting energy output and identifying abnormal patterns in soalr data is time consuming and error-prone. Automating this proccess will conserve time and allow teams to be proactive by predicting potential maintenance issues and forecast energy distribution in advance.

## Input Data: 
- Cleaned plant energy generation and weather data CSV:
Time series csv with daily energy output with dates

## Expected Output:
Indicators for each days output labeling it as either normal or anomalous then alerting technicians and drafting a summary of output performance.

### Outputs the User Sees
- Anomaly labels: data points are marked as normal or anomalous.
- Visuals: Scatterplot shows anomalies, line plot of daily yield, & histogram of efficiency.
- CSV output: Final dataset with predictions and summary (`final_output_with_summary.csv`).
- Text summary: Performance summary explaining trends and detected anomalies (`weekly_summary.txt`).

### Workflow – what it does
Uses ML to detect abnormal patterns in solar panel data. It alayzes efficiency, temp, and irradiance (sunlight), to automatically flag days with abnormal output. Its purpose is to replace manual data analysis with a faster, more accurate system that identifies potential issues and summarizes performance. It will eventually be used to alert technicians when a problem occurs so they can fix it immediately. 

## Model & Metrics Used
Isolation Forest model for anomaly detection—found outliers without labels →  tested different parameters to see which one flagged the lowest-efficiency points.

## Metric: 
Average efficiency of flagged anomalies (AC/DC power ratio) → model flags low-efficiency points as anomalies.
cont.: loop through different parameters and calculate mean EFFICIENCY of the detected anomalies. Lower = better (anomalies should be inefficient).


## Used streamlit to export my code and create an interactive dashboard that includes:
1. Anomaly Log (searchable by date and panel #)
2. Alert Log (searchable by date and panel #)
3. CSV upload & Filter button
4. Chart of Energy output overtime--interactive so you can see the details of each anomaly and the date they occurred and download if needed.
5. KPIs for CSV uploaded inc. Total energy, Max Module Temp, Avg Efficiency, Anomalies Flagged
6. Weekly Summary of Performance based on weather data and energy generation
7. Button to download anomalies
8. Trademark and Brand Name
9. Tabs to switch between summary/charts to searchable alert and anomaly log

## Zapier to automate alerts and notifications.
Created a Zapier flow that monitors my Google Drive for updated alerts_summary_only.csv files.
--> Sends  email alert when a new summary is detected, auto-fills body with these metrics:
Output (kWh)
Average Efficiency
Max Module Temp

## What I didn't Get finished and why:
- Connect ChatGPT API to my prototype to automate summaries (still uses mock summaries, I need to purchase and implement an API key)
- Figma → Pixel-perfect match: Final frontend diverged slightly from initial designs due to Streamlit layout limitations
- User login/authentication: Deemed out of scope for the current dashboard prototype

## I used streamlit to export my code and create an interactive dashboard that includes:
1. Anomaly Log (searchable by date and panel #)
2. Alert Log (searchable by date and panel #)
3. CSV upload & Filter button
4. Chart of Energy output overtime--interactive so you can see the details of each anomaly and the date they occurred and download if needed.
5. KPIs for CSV uploaded inc. Total energy, Max Module Temp, Avg Efficiency, Anomalies Flagged
6. Weekly Summary of Performance based on weather data and energy generation
7. Button to download anomalies
8. Trademark and Brand Name
9. Tabs to switch between summary/charts to searchable alert and anomaly log


## Zapier to automate alerts and notifications.
Created a Zapier flow that monitors my Google Drive for updated alerts_summary_only.csv files.
--> Sends  email alert when a new summary is detected, auto-fills body with these metrics:
Output (kWh)
Average Efficiency
Max Module Temp


## What I didn't Get finished:
- Connect ChatGPT API to my prototype to automate summaries (still uses mock summaries, I need to purchase and implement an API key)
- Refine my UI to look like my figma and add more complex features
- Login system not created yet


## What I will work on in week 5:
-  Create login screen with specific user profile
- Get API key to autogenerate summaries using ChatGPT
- Refine UI to look more professional (tailor it to my liking)
=======
# VoltView
Full Project Contents
