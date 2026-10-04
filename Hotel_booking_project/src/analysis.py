import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


import numpy as np


from preprocessing import df

print(df)


# Overall Cancellation Analysis
print("Overall Cancellation Analysis")
total_bookings = len(df)
cancelled = df["Is_Canceled"].sum()
not_cancelled = total_bookings - cancelled

cancellation_rate = cancelled / total_bookings * 100

print("Total Bookings:", total_bookings)
print("Cancelled:", cancelled)
print("Not Cancelled:", not_cancelled)
print("Cancellation Rate:", round(cancellation_rate, 2), "%")


#  Cancellation Rate by Season
print("Cancellation Rate by Season")
season_analysis = (
    df.groupby("Season")
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancelled_Bookings=("Is_Canceled", "sum"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)

season_analysis["Cancellation_Rate"] *= 100
print(season_analysis.sort_values("Cancellation_Rate", ascending=False))





# Cancellation Rate by Room Type
print("Cancellation Rate by Room Type")
room_analysis = (
    df.groupby("Room_Type")
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancelled_Bookings=("Is_Canceled", "sum"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)

room_analysis["Cancellation_Rate"] *= 100
print(room_analysis.sort_values("Cancellation_Rate", ascending=False))

#  Lead-Time Analysis
print("Lead-Time Analysis")

bins = [-1, 7, 30, 60, 90, 180, float("inf")]
labels = ["0-7 Days", "8-30 Days", "31-60 Days", "61-90 Days", "91-180 Days", "181+ Days"]

df["Lead_Time_Band"] = pd.cut(
    df["Lead_Time_Days"],
    bins=bins,
    labels=labels
)

lead_analysis = (
    df.groupby("Lead_Time_Band", observed=False)
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancelled_Bookings=("Is_Canceled", "sum"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)
lead_analysis["Cancellation_Rate"] *= 100
print(lead_analysis)


# Cancellation Rate by Customer Type
print("Cancellation Rate by Customer Type")

customer_analysis = (
    df.groupby("Customer_Type")
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancelled_Bookings=("Is_Canceled", "sum"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)

customer_analysis["Cancellation_Rate"] *= 100
print(customer_analysis.sort_values("Cancellation_Rate", ascending=False))




# High-Risk Booking Pattern Analysis
print("High-Risk Booking Pattern Analysis")
segment_analysis = (
    df.groupby(["Season", "Room_Type", "Lead_Time_Band", "Customer_Type"], observed=False)
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancelled_Bookings=("Is_Canceled", "sum"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)

segment_analysis["Cancellation_Rate"] *= 100

# Example threshold: only inspect segments with at least 30 bookings
print("Example threshold: only inspect segments with at least 30 bookings")
high_risk = segment_analysis[
    (segment_analysis["Total_Bookings"] >= 30) &
    (segment_analysis["Cancellation_Rate"] >= 40)
].sort_values("Cancellation_Rate", ascending=False)
print(high_risk.head(20))

# Heatmap Analysis
heatmap_data = df.pivot_table(
    index="Season",
    columns="Customer_Type",
    values="Is_Canceled",
    aggfunc="mean"
) * 100




# Booking Channel
print("Booking Channel")
channel_analysis = (
    df.groupby("Booking_Channel")
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)

channel_analysis["Cancellation_Rate"] *= 100
print(channel_analysis.sort_values("Cancellation_Rate", ascending=False))


# Deposit Type
print("Deposit Type")
deposit_analysis = (
    df.groupby("Deposit_Type")
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)

deposit_analysis["Cancellation_Rate"] *= 100
print(deposit_analysis)


# Previous Cancellation History
print("Previous Cancellation History")
history_analysis = (
    df.groupby("Previous_Cancellations")
      .agg(
          Total_Bookings=("Booking_ID", "count"),
          Cancellation_Rate=("Is_Canceled", "mean")
      )
      .reset_index()
)

history_analysis["Cancellation_Rate"] *= 100
print(history_analysis)


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


