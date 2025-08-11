import pandas as pd

vehicle_data_path = "/Users/aniketnamjoshi/Documents/GitHub/FIT5120---Onboarding-project/Datasets/vehicle_data.xls"

df1 = pd.read_excel(vehicle_data_path, sheet_name="Table_6")

# print(df1)

print(df1.isna().sum())
