import pandas as pd

# Load your massive CSV file locally
df = pd.read_csv("/Users/JHB/Desktop/synergy GIH/game_data_public.FRA.PremierDraft.csv")

# Save it as a highly compressed Parquet file
df.to_parquet("game_data.parquet", compression="snappy")
