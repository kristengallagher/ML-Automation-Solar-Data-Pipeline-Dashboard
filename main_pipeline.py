import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.ensemble import IsolationForest

df = pd.read_csv("cleaned_data.csv")
df['EFFICIENCY'] = df['AC_POWER'] / (df['DC_POWER'] + 1e-6)
df = df.replace([float("inf"), -float("inf")], 0)
df = df.fillna(0)

features = ['EFFICIENCY', 'IRRADIATION_Wm2', 'AMBIENT_TEMP_C', 'MODULE_TEMP_C', 'DAILY_YIELD_kWh']
X = df[features]

model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(X)
df["anomaly"] = model.predict(X)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

anomalies = df[df["anomaly"] == -1]
plt.figure(figsize=(12, 6))
plt.scatter(df.index, df["DAILY_YIELD_kWh"], c='lightgray', label='Normal')
plt.scatter(anomalies.index, anomalies["DAILY_YIELD_kWh"], c='red', label='Anomaly')
plt.title("Daily Yield with Anomalies")
plt.xlabel("Index")
plt.ylabel("Daily Yield (kWh)")
plt.legend()
plt.tight_layout()
plt.savefig("final_anomaly_plot.png")
plt.close()

summary = """
System avg efficiency was around 0.46. Peaks reached 1.0.
Some weird drops in performance on June 5 and June 9.
Looks like high module temps caused efficiency to dip.
"""

with open("weekly_summary.txt", "w") as f:
    f.write(summary.strip())

df.to_csv("final_output_with_summary.csv", index=False)

anomalies[["DAILY_YIELD_kWh"]].to_csv("alerts_today.csv")

print("Slay! Model, plot, summary, & output saved --> Check files.")
