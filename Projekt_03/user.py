class User:
    def __init__(self, name, role, coins=0):
        self.name = name
        self.role = role
        self.coins = coins
        self.activities = []


    def add_coins(self, amount):
        self.coins += amount

    def add_activity(self, activity_name, coins):
        self.activities.append((activity_name, coins))
        self.coins += coins

    def show_coins(self):
        print(f"{self.name} hat {self.coins} Coins.")

    def history_activities(self):
        print(f"Aktivitätshistorie für {self.name}:")
        for activity, coins in self.activities:
            print(f"{activity}: {coins} Coins")
    
    def to_dict(self):
        return {
            'name': self.name,
            'role': self.role,
            'coins': self.coins,
            'activities': self.activities
        }
    
    def __repr__(self):
        return f"User(name={self.name}, coins={self.coins})"