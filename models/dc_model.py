# models/dc_model.py

class DCModel:
    def __init__(self, home_attack, away_attack, home_defense, away_defense):
        self.home_attack = home_attack
        self.away_attack = away_attack
        self.home_defense = home_defense
        self.away_defense = away_defense

    def predict(self):
        # Example Poisson-based prediction logic
        home_goals = self.home_attack * self.away_defense
        away_goals = self.away_attack * self.home_defense
        return home_goals, away_goals
