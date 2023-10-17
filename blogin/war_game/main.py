import mysql.connector
import random
from datetime import datetime, timedelta
from models.country import Country
from utilities.date_utils import end_of_next_month
from config.db_config import DB_CONFIG

# Database configuration
db_config = DB_CONFIG

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor(dictionary=True)


def simulate():
    
    # Fetch countries from the database
    cursor.execute("SELECT * FROM countries")
    rows = cursor.fetchall()

    countries = [Country(
        row["name"],
        row["population"],
        row["tax_rate"],
        row["treasury_balance"],
        row["budget_non_military"],
        row["budget_military"],
        row["military_roi"],
        row["gdp"],
        row["gdp_growth_rate"],
        row["gdp_growth_drive"],
        row["military_attack"],
        row["attack_cost"],
        row["military_defense"],
        row["land_units_total"],
        row["land_units_functional"]) for row in rows]

    current_date = datetime.strptime('2022-12-31', '%Y-%m-%d')
    end_date = current_date + timedelta(days=365*20)

    while current_date < end_date:
        damages = {}

        for country in countries:
            if country.is_conquered:  # If country is conquered, it cannot act
                continue

            decision = random.choice(['war', 'attack', 'peace', 'skip'])
            
            if decision == 'war':
                potential_targets = [c for c in countries if c != country and c not in country.in_war_with]
                if not potential_targets:
                    continue
                target = random.choice(potential_targets)
                country.declare_war(target)

            elif decision == 'attack':
                if country.in_war_with:
                    target = random.choice(country.in_war_with)
                    country.attack(target, damages)

            elif decision == 'peace':
                if country.in_war_with:
                    target = random.choice(country.in_war_with)
                    country.in_war_with.remove(target)

        for (attacker, defender), damage in damages.items():
            defender.military_defense -= damage
            defender.military_attack -= damage
            if defender.military_defense <= 0:
                defender.is_conquered = True
                defender.affiliated_to = attacker

        if current_date.month == 12:
            for country in countries:
                country.end_of_year_process()

        current_date = end_of_next_month(current_date)

    print("End of Simulation")
    # First, print free countries
    free_countries = [country for country in countries if not country.is_conquered]
    for country in free_countries:
        print(f"Country: {country.name}, Status: Free")

    # Then, print conquered countries
    conquered_countries = [country for country in countries if country.is_conquered]
    for country in conquered_countries:
        status = "Conquered by " + country.affiliated_to.name
        print(f"Country: {country.name}, Status: {status}")
    
if __name__ == "__main__":
    simulate()
    cursor.close()
    connection.close()




