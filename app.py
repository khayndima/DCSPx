import streamlit as st
import pandas as pd
from predictor import predict_match
from models.dc_model import DCModel
from models.external_model import ExternalModel
from odds_api import fetch_live_odds
from betting_utils import optimize_parlay

st.set_page_config(page_title="DCSPx Football Predictor", layout="wide")
st.title("⚽ DCSPx: Universal Football Prediction Engine")

api_key = st.secrets["core_data_services"]["api_key"]
league = st.text_input("League", value="Premier League")
date = st.date_input("Match Date")

odds_data = fetch_live_odds(api_key, league=league, date=str(date))

fixtures = pd.DataFrame([{
    'home': m['home_team'], 'away': m['away_team'], 'date': date,
    'odds_home': m['markets']['1X2']['home'],
    'odds_draw': m['markets']['1X2']['draw'],
    'odds_away': m['markets']['1X2']['away'],
    'odds_BTTS': m['markets']['btts']['yes'],
    'odds_Over25': m['markets']['over_under']['over_2.5']
} for m in odds_data])

dc_model = DCModel()
external_model = ExternalModel()

results = []
for _, f in fixtures.iterrows():
    result = predict_match(
        f['home'], f['away'], f['date'],
        {'home': f['odds_home'], 'draw': f['odds_draw'], 'away': f['odds_away']},
        dc_model, external_model
    )
    result.update({
        'odds_home': f['odds_home'],
        'odds_draw': f['odds_draw'],
        'odds_away': f['odds_away'],
        'odds_BTTS': f['odds_BTTS'],
        'odds_Over25': f['odds_Over25']
    })
    results.append(result)

df = pd.DataFrame(results)
st.dataframe(df)

st.sidebar.header("🎯 Parlay Settings")
max_legs = st.sidebar.slider("Max parlay legs", 2, 5, 3)
min_ev = st.sidebar.slider("Minimum EV per leg", 0.00, 0.20, 0.05, 0.01)
market_type = st.sidebar.selectbox("Market type", ["1X2", "BTTS", "Over/Under"])

parlays = optimize_parlay(results, max_legs=max_legs, min_ev=min_ev, market_type=market_type)
st.subheader("💰 Top Parlay Combos")
for p in parlays:
    st.markdown(f"**Expected Return:** {p['return']}")
    for leg in p['legs']:
        st.markdown(f"- {leg}")
    st.markdown("---")
