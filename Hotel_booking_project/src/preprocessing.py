
import pandas as pd
import numpy as np
from dataloader import df_r

# df = pd.read_csv("hotel_bookings.csv")



df_r = df_r.drop_duplicates()

df_r["Booking_Date"] = pd.to_datetime(df_r["Booking_Date"], errors="coerce")
df_r["Arrival_Date"] = pd.to_datetime(df_r["Arrival_Date"], errors="coerce")

print(df_r.isnull().sum())
print(df_r["Is_Canceled"].value_counts(dropna=False))

df = df_r
print(df)


# print(df['Booking_Channel'])


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