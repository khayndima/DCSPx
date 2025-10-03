import pandas as pd
from datetime import datetime
from models.dc_model import DCModel
from models.external_model import ExternalModel
from odds_api import fetch_live_odds
from predictor import predict_match
from betting_utils import optimize_parlay

API_KEY = "YOUR_API_KEY"
LEAGUE = "Premier League"
TODAY = datetime.today().strftime("%Y-%m-%d")

odds_data = fetch_live_odds(API_KEY, league=LEAGUE, date=TODAY)

fixtures = [{
    'home': m['home_team'], 'away': m['away_team'], 'date': TODAY,
    'odds_home': m['markets']['1X2']['home'],
    'odds_draw': m['markets']['1X2']['draw'],
