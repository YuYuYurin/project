import time

class Transaction:
    def __init__(self, user_name, activity, coins, approver, confirmed=False):
        self.user_name = user_name
        self.activity = activity
        self.coins = coins
        self.approver = approver
        self.confirmed = confirmed
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'activity': self.activity,
            'coins': self.coins,
            'approver': self.approver,
            'confirmed': self.confirmed,
            'timestamp': self.timestamp,
        }

    def confirm(self):
        self.confirmed = True