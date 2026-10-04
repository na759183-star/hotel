import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import df

from analysis  import heatmap_data,customer_analysis,lead_analysis,season_analysis,channel_analysis

total_bookings = len(df)
cancelled = df["Is_Canceled"].sum()
not_cancelled = total_bookings - cancelled

cancellation_rate = cancelled / total_bookings * 100

print("Total Bookings:", total_bookings)
print("Cancelled:", cancelled)
print("Not Cancelled:", not_cancelled)
print("Cancellation Rate:", round(cancellation_rate, 2), "%")



# Data from your calculations
categories = ['Not Cancelled', 'Cancelled']
counts = [not_cancelled, cancelled]
colors = ['#2ec4b6', '#e71d36']

# Create the bar chart
plt.figure(figsize=(7, 5))
bars = plt.bar(categories, counts, color=colors, width=0.6)
plt.show()




# season analysis visualization
plt.figure(figsize=(10, 5))
sns.barplot(data=season_analysis, x="Season", y="Cancellation_Rate")
plt.title("Cancellation Rate by Season")
plt.ylabel("Cancellation Rate (%)")
plt.xlabel("Season")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()



# lead analysis visualization
plt.figure(figsize=(11, 5))
sns.barplot(data=lead_analysis, x="Lead_Time_Band", y="Cancellation_Rate")
plt.title("Cancellation Rate by Lead-Time Band")
plt.xlabel("Lead-Time Band")
plt.ylabel("Cancellation Rate (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()



# customer analysis visualization
plt.figure(figsize=(10, 5))
sns.barplot(data=customer_analysis, x="Customer_Type", y="Cancellation_Rate")
plt.title("Cancellation Rate by Customer Type")
plt.ylabel("Cancellation Rate (%)")
plt.xlabel("Customer Type")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()



# heatmap season vs customer type
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".1f")
plt.title("Cancellation Rate: Season vs Customer Type")
plt.xlabel("Customer Type")
plt.ylabel("Season")
plt.tight_layout()
plt.show()


# 1. Define the Lead Time Bands (matching your original logic)
bins = [-1, 7, 30, 60, 90, 180, float("inf")]
labels = [
    "0-7 Days",
    "8-30 Days",
    "31-60 Days",
    "61-90 Days",
    "91-180 Days",
    "181+ Days",
]
df["Lead_Time_Band"] = pd.cut(df["Lead_Time_Days"], bins=bins, labels=labels)

# 2. Group by both dimensions and calculate the mean cancellation rate
heatmap_data = (
    df.groupby(["Room_Type", "Lead_Time_Band"], observed=False)["Is_Canceled"]
    .mean()
    .reset_index()
)

# Convert to percentage
heatmap_data["Is_Canceled"] *= 100

# 3. Pivot the dataframe to create a matrix format suitable for heatmaps
# Rows = Room Types, Columns = Lead Time Bands, Values = Cancellation Rate (%)
pivot_matrix = heatmap_data.pivot(
    index="Room_Type", columns="Lead_Time_Band", values="Is_Canceled"
)

# 4. Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    pivot_matrix,
    annot=True,  # Shows the actual percentage numbers in the cells
    fmt=".1f",  # Rounds to 1 decimal place
    cmap="YlOrRd",  # Color gradient: Yellow (Low) to Red (High)
    cbar_kws={"label": "Cancellation Rate (%)"},
    linewidths=0.5,
)

plt.title("Cancellation Rate (%) by Room Type vs. Lead-Time Band", fontsize=14)
plt.xlabel("Lead-Time Band", fontsize=12)
plt.ylabel("Room Type", fontsize=12)
plt.tight_layout()
plt.show()


#  booking channel cancellation comparison

# Set style and figure size
sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(10, 6))

# 1. Plot Total Bookings (Bar Chart - Left Axis)
sns.barplot(
    data=channel_analysis,
    x="Booking_Channel",
    y="Total_Bookings",
    alpha=0.6,
    color="steelblue",
    ax=ax1,
)
ax1.set_title(
    "Booking Channel Comparison: Volume vs. Cancellation Rate",
    fontsize=14,
    pad=20,
)
ax1.set_xlabel("Booking Channel", fontsize=12)
ax1.set_ylabel("Total Bookings", color="steelblue", fontsize=12)
ax1.tick_params(axis="y", labelcolor="steelblue")

# 2. Plot Cancellation Rate (Line Chart - Right Axis)
ax2 = ax1.twinx()
sns.lineplot(
    data=channel_analysis,
    x="Booking_Channel",
    y="Cancellation_Rate",
    color="crimson",
    marker="o",
    linewidth=2.5,
    ax=ax2,
    sort=False,  # Keeps the sorting from the DataFrame
)
ax2.set_ylabel("Cancellation Rate (%)", color="crimson", fontsize=12)
ax2.tick_params(axis="y", labelcolor="crimson")
ax2.yaxis.set_major_formatter("{x:.1f}%")

# Tight layout to avoid clipping labels
plt.tight_layout()
plt.show()








# Create a Month column
df['Month'] = df['Booking_Date'].dt.to_period('M')

# Monthly total bookings
monthly_bookings = df.groupby('Month').size()

# Monthly cancelled bookings
monthly_cancellations = df[df['Is_Canceled'] == 1].groupby('Month').size()

# Monthly cancellation rate
monthly_cancellation_rate = (
    df.groupby('Month')['Is_Canceled'].mean() * 100
)

# Display the results
monthly_analysis = pd.DataFrame({
    'Total_Bookings': monthly_bookings,
    'Cancelled_Bookings': monthly_cancellations,
    'Cancellation_Rate': monthly_cancellation_rate
}).fillna(0)

print(monthly_analysis)






# Monthly analysis
monthly_analysis = df.groupby('Month').agg(
    Total_Bookings=('Is_Canceled', 'count'),
    Cancelled_Bookings=('Is_Canceled', 'sum'),
    Cancellation_Rate=('Is_Canceled', 'mean')
)

# Convert rate to percentage
monthly_analysis['Cancellation_Rate'] = (
    monthly_analysis['Cancellation_Rate'] * 100
)

print(monthly_analysis.round(2))


# Convert Booking_Date to datetime
df['Booking_Date'] = pd.to_datetime(df['Booking_Date'], errors='coerce')

# Create Month column
df['Month'] = df['Booking_Date'].dt.to_period('M')

# Monthly total bookings
monthly_bookings = df.groupby('Month').size()

# Monthly cancellations
monthly_cancellations = df[df['Is_Canceled'] == 1].groupby('Month').size()

# Combine both series
monthly_trend = pd.DataFrame({
    'Total Bookings': monthly_bookings,
    'Cancellations': monthly_cancellations
}).fillna(0)

# Convert Period to string for plotting
monthly_trend.index = monthly_trend.index.astype(str)

# Plot combined line graph
plt.figure(figsize=(14, 7))

plt.plot(
    monthly_trend.index,
    monthly_trend['Total Bookings'],
    marker='o',
    linewidth=2,
    label='Monthly Booking Volume'
)

plt.plot(
    monthly_trend.index,
    monthly_trend['Cancellations'],
    marker='o',
    linewidth=2,
    label='Monthly Cancellation Trend'
)

plt.title('Monthly Booking Volume and Cancellation Trend', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Number of Bookings', fontsize=12)

plt.xticks(rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
