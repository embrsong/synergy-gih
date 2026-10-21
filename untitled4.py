import pandas as pd
import numpy as np
setlen = 280 + 5 + 10 # main set, 5 basics, 10 SPG

# Load your massive CSV file locally
df = pd.read_csv("/Users/JHB/Desktop/synergy GIH/game_data_public.FRA.PremierDraft.csv")


# Load the CSV file into a DataFrame
sample = round(len(df)/100)

cols_oh = np.arange(18, 18 + 5 * setlen, 5)
cols_gd = np.arange(19, 19 + 5 * setlen, 5)

# Extract data as a NumPy array
cards_oh = df.iloc[:sample, cols_oh].to_numpy()
cards_gd = df.iloc[:sample, cols_gd].to_numpy()
# combine OH and GD
cards = cards_oh + cards_gd

#%%

wins = df.iloc[:sample, 17].to_numpy(dtype=bool)
cardnames = []
for ID in range(setlen):
    index = 18+5*ID+3
    cardnames.append(df.columns[index][5:])

#%%

np.save('cards', cards)
np.save('wins', wins)
np.save('cardnames', cardnames)
