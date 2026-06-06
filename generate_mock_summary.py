import anthropic


def generate_mock_summary(df):
    avg_efficiency = df['Efficiency'].mean()
    max_efficiency = df['Efficiency'].max()
    avg_temp = df['MODULE_TEMP_C'].mean()
    max_temp = df['MODULE_TEMP_C'].max()
    avg_irradiation = df['IRRADIATION_Wm2'].mean()
    total_yield = df['DAILY_YIELD_kWh'].sum()
    anomaly_count = (df['Anomaly'] == -1).sum() if 'Anomaly' in df.columns else 0
    date_range = f"{df['Date'].min().strftime('%b %d')} – {df['Date'].max().strftime('%b %d, %Y')}" if 'Date' in df.columns else "the selected period"

    stats = f"""
Solar panel performance data for {date_range}:
- Total energy yield: {total_yield:,.0f} kWh
- Average efficiency: {avg_efficiency:.3f} (max: {max_efficiency:.3f})
- Average module temperature: {avg_temp:.1f}°C (max: {max_temp:.1f}°C)
- Average irradiation: {avg_irradiation:.4f} W/m²
- Anomalies detected: {anomaly_count} readings
"""

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=300,
            system="You are a solar energy analyst. Write a concise 3-sentence weekly summary of solar panel performance based on the data provided. Be specific and actionable. No bullet points — plain flowing sentences only.",
            messages=[{"role": "user", "content": stats}]
        )
        return response.content[0].text
    except Exception as e:
        return (
            f"System averaged {avg_efficiency:.2f} efficiency over {date_range} with {total_yield:,.0f} kWh total yield. "
            f"Module temperatures peaked at {max_temp:.1f}°C. "
            f"{anomaly_count} anomalous readings were flagged for review."
        )
