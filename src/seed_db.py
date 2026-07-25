import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.database import SessionLocal, engine, Base
from src.models.team_stats import TeamStat
from src.models.news_documents import NewsDocument

def seed_full_tournament():
    db = SessionLocal()
    try:
        # Wipe existing records to clear out the old 5-team dataset
        print("Wiping old database records...")
        db.query(TeamStat).delete()
        db.query(NewsDocument).delete()
        db.commit()

        print("Seeding all 48 FIFA World Cup 2026 Teams...")
        
        groups = {
            "A": ["Mexico", "South Korea", "South Africa", "Greece"],
            "B": ["Canada", "Switzerland", "Qatar", "Ghana"],
            "C": ["USA", "Australia", "Senegal", "Serbia"],
            "D": ["Spain", "Uruguay", "Japan", "Nigeria"],
            "E": ["Argentina", "Austria", "Saudi Arabia", "Algeria"],
            "F": ["France", "Denmark", "Iran", "Ecuador"],
            "G": ["Brazil", "Morocco", "Ukraine", "Egypt"],
            "H": ["England", "Croatia", "Uzbekistan", "Ivory Coast"],
            "I": ["Belgium", "Colombia", "Iraq", "Cameroon"],
            "J": ["Portugal", "Netherlands", "Tunisia", "Chile"],
            "K": ["Germany", "Peru", "Norway", "Mali"],
            "L": ["Italy", "Poland", "Costa Rica", "Paraguay"]
        }

        team_objects = []
        for group_letter, teams in groups.items():
            for team in teams:
                team_objects.append(
                    TeamStat(
                        team_name=team, 
                        group_letter=group_letter,
                        total_points=random.randint(0, 9), 
                        goals_scored=random.randint(1, 8), 
                        goals_conceded=random.randint(0, 6)
                    )
                )
        db.add_all(team_objects)

        print("Seeding tactical news reports...")
        sample_reports = [
            ("Spain's High Press", "Spain uses a 4-3-3 high-intensity counter-press with inverted wingers."),
            ("Portugal's Wide Overloads", "Portugal focuses on rapid wing rotations and midfield overloads."),
            ("Argentina's Central Transition", "Argentina operates via central possession hooks targeting key passes."),
            ("France's Rapid Counter", "France prioritizes rapid wing transitions in a 4-2-3-1 structure."),
            ("Brazil's Asymmetric Attack", "Brazil relies on fluid wing rotation and full-back overlaps."),
            ("Japan's Compact Block", "Japan deploys a mid-block 5-4-1 designed to exploit turnover spaces quickly.")
        ]
        
        news_objects = [
            NewsDocument(
                title=title,
                content=content,
                embedding=[random.uniform(-1, 1) for _ in range(1536)]
            )
            for title, content in sample_reports
        ]
        db.add_all(news_objects)

        db.commit()
        print("✓ Successfully seeded all 48 World Cup teams into PostgreSQL!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_full_tournament()