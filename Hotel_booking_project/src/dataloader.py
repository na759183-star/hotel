import pandas as pd


    

    
df_r = pd.read_csv("hotel_bookings.csv")
print(df_r)
print(df_r.head())
print(df_r.shape)
print(df_r.columns)
print(df_r.info())
print(df_r.describe(include="all"))

