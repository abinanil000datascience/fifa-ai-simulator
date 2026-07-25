import sys
import os
import math
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def get_dynamic_rating(team_name: str) -> dict:
    elites = ["Argentina", "France", "Brazil", "Spain", "England", "Germany", "Portugal", "Italy"]
    if team_name in elites:
        return {"attack": 1.40, "defense": 0.70}
    return {"attack": 1.0, "defense": 1.0}

def simulate_match(home_team: str, away_team: str, stage: str = "group", num_simulations: int = 5000) -> dict:
    AVG_GOALS = 1.35
    home_rating = get_dynamic_rating(home_team)
    away_rating = get_dynamic_rating(away_team)

    lambda_home = AVG_GOALS * home_rating["attack"] * away_rating["defense"]
    lambda_away = AVG_GOALS * away_rating["attack"] * home_rating["defense"]

    home_wins = 0
    draws = 0
    away_wins = 0

    for _ in range(num_simulations):
        home_goals = sum(1 for _ in range(20) if random.random() < (lambda_home / 20))
        away_goals = sum(1 for _ in range(20) if random.random() < (lambda_away / 20))

        # Knockout Stage Logic: Extra Time & Penalties
        if stage != "group" and home_goals == away_goals:
            # 30 mins Extra Time (roughly 1/3 of normal lambda)
            home_goals += sum(1 for _ in range(20) if random.random() < ((lambda_home * 0.33) / 20))
            away_goals += sum(1 for _ in range(20) if random.random() < ((lambda_away * 0.33) / 20))
            
            # If still tied, 50/50 Penalty Shootout
            if home_goals == away_goals:
                if random.random() > 0.5:
                    home_goals += 1
                else:
                    away_goals += 1

        if home_goals > away_goals:
            home_wins += 1
        elif away_goals > home_goals:
            away_wins += 1
        else:
            draws += 1

    return {
        "matchup": f"{home_team} vs {away_team} ({stage.replace('_', ' ').title()})",
        "probabilities": {
            f"{home_team}_win": f"{(home_wins / num_simulations) * 100:.1f}%",
            "draw": f"{(draws / num_simulations) * 100:.1f}%" if stage == "group" else "0.0% (Knockout)",
            f"{away_team}_win": f"{(away_wins / num_simulations) * 100:.1f}%"
        }
    }