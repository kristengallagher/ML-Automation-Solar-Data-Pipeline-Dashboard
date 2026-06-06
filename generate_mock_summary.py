import anthropic

def generate_mock_summary(df):
    # pulls real numbers from your actual data
    avg_efficiency = df['Efficiency'].mean()
    max_efficiency = df['Efficiency'].max()
    avg_temp = df['MODULE_TEMP_C'].mean()
    max_temp = df['MODULE_TEMP_C'].max()
    total_yield = df['DAILY_YIELD_kWh'].sum()
    anomaly_count = (df['Anomaly'] == -1).sum()
    date_range = f"{df['Date'].min().strftime('%b %d')} – {df['Date'].max().strftime('%b %d, %Y')}"

    # exporta data to Claude and generates summary
    stats = f"..."  # formatted string of all the above stats

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=300,
        system="You are a solar energy analyst...",
        messages=[{"role": "user", "content": stats}]
    )
    return response.content[0].text
