import random

class Country:
    country_id = 0

    def __init__(self, name, population, tax_rate, treasury_balance, budget_non_military, budget_military, military_roi,
                 gdp, gdp_growth_rate, gdp_growth_drive, military_attack, attack_cost, military_defense, 
                 land_units_total, land_units_functional):
        
        self.id = Country.country_id
        Country.country_id += 1
        
        self.name = name
        self.population = population
        self.tax_rate = tax_rate
        self.treasury_balance = treasury_balance
        self.budget_non_military = budget_non_military
        self.budget_military = budget_military
        self.military_roi = military_roi
        self.gdp = gdp
        self.gdp_growth_rate = gdp_growth_rate
        self.gdp_growth_drive = gdp_growth_drive
        self.military_attack = military_attack
        self.attack_cost = attack_cost
        self.military_defense = military_defense
        self.land_units_total = land_units_total
        self.land_units_functional = land_units_functional
        self.in_war_with = []
        self.is_conquered = False
        self.affiliated_to = None

    def declare_war(self, target):
        self.in_war_with.append(target)
        self.gdp_growth_rate *= 0.95  # Example value
        target.gdp_growth_rate *= 0.90  # Example value

    def attack(self, target, damages):
        remaining_points_of_attack = self.military_attack
        points_of_attack = random.random() * remaining_points_of_attack
        cost_of_attack = points_of_attack * self.attack_cost
        self.treasury_balance -= cost_of_attack

        damage = points_of_attack * max(0, (self.military_attack - target.military_defense) / target.military_defense / 12)
        damages[(self, target)] = damage
        print(f"{self.name} attacked {target.name} causing {damage} damage.")

    def end_of_year_process(self):
        tax = self.gdp * self.tax_rate
        self.treasury_balance += tax
        self.treasury_balance -= self.budget_non_military
        self.gdp_growth_rate = (self.budget_non_military / self.population) * self.gdp_growth_drive
        self.gdp *= (1 + self.gdp_growth_rate)
        military_increase = self.budget_military * self.military_roi
        self.military_attack += military_increase
        self.military_defense += military_increase
        print(f"Yearly stats for {self.name}: GDP: {self.gdp}, Treasury: {self.treasury_balance}, Attack: {self.military_attack}, Defense: {self.military_defense}")
