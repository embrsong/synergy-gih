import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path

st.title('Synergy GIHWR for FRA')
setlen = 280 + 5 + 10 # main set, 5 basics, 10 SPG

@st.cache_data
def load():
    os.chdir(Path(__file__).resolve().parent)
    cards = np.load('cards.npy')
    wins = np.load('wins.npy')
    cardnames = np.load('cardnames.npy')
    cardnames = cardnames.tolist()
    return cards, wins, cardnames

def print_synergy(card_id):
    Nmin = 100
    # calculate stuff for the correlation
    s_card_games = np.zeros(setlen)
    s_card_wins = np.zeros(setlen)
    
    for i in range(len(cards)):
        game = cards[i]
        s = cards[i][card_id]
        if s>0:
            for c in range(len(game)):
                s_card_games[c] += s*game[c]
            if wins[i]:
                for c in range(len(game)):
                    s_card_wins[c] += s*game[c]
    
    s_card_gih = np.zeros(setlen)
    for i in range(len(s_card_gih)):
        if s_card_wins[i] != 0:
            s_card_gih[i] = s_card_wins[i]/s_card_games[i]
    
    # regular GIH calculation
    # Total games/cards per column
    FRA_GS = cards.sum(axis=0)
    
    # Total cards for winning rows, excluding zero values
    FRA_WINS = np.where(wins[:, None] & (cards != 0), cards, 0).sum(axis=0)
    
    FRA_GIH = np.zeros(setlen)
    for i in range(setlen):
        if FRA_GS[i] !=0:
            FRA_GIH[i] = FRA_WINS[i]/FRA_GS[i]
            
    # now need to adjust by wr of other card
    adjusted = s_card_gih - FRA_GIH
    adjusted += s_card_gih - FRA_GIH[card_id] # this might be important - account for each card being good/bad
    
    # sort
    data = {
        "Card": cardnames,
        "SGIH with named card (% improvement)": adjusted,
        "N": s_card_games,
    }
    
    df2 = pd.DataFrame(data)
    # sort by wr
    df_sorted = df2.sort_values(by='SGIH with named card (% improvement)', ascending=False)
    
    #print top 10
    #df_culled = df_sorted[df_sorted['N'] >= Nmin][:10]
    df_culled = df_sorted[df_sorted['N'] >= Nmin]
    
    st.dataframe(df_culled, hide_index=True)



cards, wins, cardnames = load()

@st.fragment
def card_lookup():
    I = st.text_input("enter exact card name", placeholder="Ajani's Anguish")
    st.write('')
    if I in cardnames:
        ID = cardnames.index(I)
        print_synergy(ID)
    else:
        st.write('unknown cardname or command\n')

card_lookup()




