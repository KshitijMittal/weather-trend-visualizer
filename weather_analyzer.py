import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

csv_file = Path(__file__).parent / 'weather.csv'
output_dir = Path(__file__).parent / 'plots'

if not csv_file.exists():
    print(f"Can't find {csv_file}")
    exit()

output_dir.mkdir(exist_ok=True)

# load the data
df = pd.read_csv(csv_file)
df['Date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
df['Temp'] = df['Temp3pm']

# quick moving average
window = 7
temps = df['Temp'].values
ma = np.convolve(temps, np.ones(window) / window, mode='valid')
df['MA'] = np.concatenate([np.full(window - 1, np.nan), ma])

# find the hottest day
hottest_idx = df['Temp'].idxmax()
hottest_date = df.loc[hottest_idx, 'Date']
hottest_temp = df.loc[hottest_idx, 'Temp']
print(f"Hottest: {hottest_date.strftime('%B %d')} ({hottest_temp:.1f}°C)")

# july average vs yearly
df['Month'] = df['Date'].dt.month
july = df[df['Month'] == 7]['Temp']
yearly_avg = df['Temp'].mean()
july_avg = july.mean() if len(july) > 0 else None

if july_avg:
    diff = july_avg - yearly_avg
    direction = "hotter" if diff > 0 else "cooler"
    print(f"July avg: {july_avg:.1f}°C (yearly: {yearly_avg:.1f}°C - {abs(diff):.1f}°C {direction})")

# total rain
total_rain = df['Rainfall'].sum()
print(f"Total rainfall: {total_rain:.1f}mm\n")

# plot
fig, ax1 = plt.subplots(figsize=(14, 7))

ax1.plot(df['Date'], df['Temp'], color='#FF6B6B', linewidth=1.5, alpha=0.7, label='Temp')
ax1.plot(df['Date'], df['MA'], color='#4ECDC4', linewidth=2.5, linestyle='--', label='7d avg')
ax1.set_ylabel('Temperature (°C)', color='#FF6B6B', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#FF6B6B')
ax1.grid(True, alpha=0.2)

ax2 = ax1.twinx()
ax2.bar(df['Date'], df['Rainfall'], color='#45B7D1', alpha=0.35, width=1, label='Rain')
ax2.set_ylabel('Rainfall (mm)', color='#45B7D1', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#45B7D1')

ax1.set_xlabel('Date', fontweight='bold')
plt.title('Weather Overview', fontsize=13, fontweight='bold', pad=15)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

fig.tight_layout()
plt.savefig(output_dir / 'weather_overview.png', dpi=300, bbox_inches='tight')
print("Saved plot")
plt.show()
