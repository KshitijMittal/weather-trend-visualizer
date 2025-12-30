import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys


def main():
    """
    Main function to analyze weather data and generate visualizations.
    Reads weather data from CSV, calculates statistics, and creates a dual-axis plot.
    """
    try:
        # Define file paths
        csv_file = Path(__file__).parent / 'weather.csv'
        output_dir = Path(__file__).parent / 'plots'
        output_file = output_dir / 'weather_overview.png'
        
        # Verify CSV file exists
        if not csv_file.exists():
            print(f"Error: {csv_file} not found. Please ensure weather.csv is in the project directory.")
            return
        
        # Create plots directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)
        
        # Load data
        print("Loading weather data...")
        df = pd.read_csv(csv_file)
        
        # Add a date column (assuming sequential daily data starting from Jan 1)
        # If your CSV has a Date column, uncomment the line below and comment out the next line
        # df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
        
        # Extract temperature columns for analysis
        # Using Temp3pm (afternoon temperature) as the daily temperature
        df['Temperature'] = df['Temp3pm']
        
        # Calculate 7-day moving average using numpy
        print("Calculating 7-day moving average...")
        temperature_values = df['Temperature'].values
        moving_avg_window = 7
        # Create moving average using numpy convolve
        moving_avg = np.convolve(temperature_values, np.ones(moving_avg_window) / moving_avg_window, mode='valid')
        
        # Align moving average with original dataframe (pad with NaN at the beginning)
        moving_avg_aligned = np.concatenate([np.full(moving_avg_window - 1, np.nan), moving_avg])
        df['Moving_Avg_7d'] = moving_avg_aligned
        
        # Extract rainfall data
        df['Rainfall'] = df['Rainfall']
        
        # ==================== STATISTICS ====================
        print("\n" + "="*60)
        print("WEATHER ANALYSIS REPORT")
        print("="*60)
        
        # 1. Hottest day
        hottest_idx = df['Temperature'].idxmax()
        hottest_date = df.loc[hottest_idx, 'Date']
        hottest_temp = df.loc[hottest_idx, 'Temperature']
        print(f"\n📊 Hottest Day of the Year:")
        print(f"   Date: {hottest_date.strftime('%B %d, %Y')}")
        print(f"   Temperature: {hottest_temp:.1f}°C")
        
        # 2. July vs Annual Average
        df['Month'] = df['Date'].dt.month
        july_data = df[df['Month'] == 7]['Temperature']
        annual_avg = df['Temperature'].mean()
        july_avg = july_data.mean()
        
        print(f"\n🌡️  Temperature Comparison:")
        print(f"   Annual Average Temperature: {annual_avg:.2f}°C")
        if len(july_data) > 0:
            print(f"   July Average Temperature: {july_avg:.2f}°C")
            if july_avg > annual_avg:
                print(f"   ✓ Yes, July was {july_avg - annual_avg:.2f}°C hotter than the annual average!")
            else:
                print(f"   ✗ No, July was {annual_avg - july_avg:.2f}°C cooler than the annual average.")
        else:
            print(f"   ⚠️  No July data available in the dataset.")
        
        # 3. Total annual rainfall
        total_rainfall = df['Rainfall'].sum()
        print(f"\n💧 Total Annual Rainfall:")
        print(f"   {total_rainfall:.1f} mm")
        print("="*60 + "\n")
        
        # ==================== VISUALIZATION ====================
        print("Creating dual-axis visualization...")
        
        # Create figure with dual y-axes
        fig, ax1 = plt.subplots(figsize=(14, 7))
        
        # Left axis: Temperature and Moving Average
        color_temp = '#FF6B6B'
        color_ma = '#4ECDC4'
        ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)', color=color_temp, fontsize=12, fontweight='bold')
        ax1.plot(df['Date'], df['Temperature'], color=color_temp, linewidth=1.5, alpha=0.7, label='Daily Temperature')
        ax1.plot(df['Date'], df['Moving_Avg_7d'], color=color_ma, linewidth=2.5, linestyle='--', label='7-Day Moving Average')
        ax1.tick_params(axis='y', labelcolor=color_temp)
        ax1.grid(True, alpha=0.3)
        
        # Right axis: Rainfall
        ax2 = ax1.twinx()
        color_rain = '#45B7D1'
        ax2.set_ylabel('Rainfall (mm)', color=color_rain, fontsize=12, fontweight='bold')
        ax2.bar(df['Date'], df['Rainfall'], color=color_rain, alpha=0.4, width=1, label='Rainfall')
        ax2.tick_params(axis='y', labelcolor=color_rain)
        
        # Title and layout
        plt.title('Weather Trend Analysis: Temperature & Rainfall', fontsize=14, fontweight='bold', pad=20)
        
        # Combine legends from both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
        
        fig.tight_layout()
        
        # Save the figure
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved to: {output_file}")
        
        # Display the plot
        plt.show()
        
        print("\n✓ Analysis complete!")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"Error: Failed to parse CSV file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
