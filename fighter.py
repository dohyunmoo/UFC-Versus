class Fighter:
    def __init__(self, name, height, losses, wins, strikes, takedowns, weight_class):
        self.name = name
        self.height = height
        self.losses = losses
        self.wins = wins
        self.strikes = strikes
        self.takedowns = (takedowns,)
        self.weight_class = weight_class
        self.takedown_defence_rate = int(takedowns["takedown defense"]) / (
            int(wins["total"]) + int(losses["total"])
        )

    def _total_strikes(self):
        total = 0
        for key, value in self.strikes:
            if (
                key != "attempted"
                and key != "strikes per minute"
                and key != "striking defense"
            ):
                total += int(value)
        return total
