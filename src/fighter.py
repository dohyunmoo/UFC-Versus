from src.misc import *


class Fighter:
    def __init__(
        self, name, age, height, losses, wins, strikes, takedowns, weight_class, fights
    ):
        self.name = name
        self.age = age
        self.height = height_to_num(height)
        self.losses = losses
        self.wins = wins
        self.strikes = strikes
        self.takedowns = takedowns
        self.weight_class = weight_class
        self.takedown_defence_rate = int(takedowns["takedown defense"]) / (
            self._total_fights()
        )
        self.takedown_attempt_per_fight = int(takedowns["attempted"]) / (
            self._total_fights()
        )
        self.takedown_landed_per_fight = int(takedowns["landed"]) / (
            self._total_fights()
        )
        self.strike_defence_rate = int(strikes["striking defense"]) / (
            self._total_fights()
        )
        self.strike_attempt_per_fight = int(strikes["attempted"]) / (
            self._total_fights()
        )
        self.strike_landed_per_fight = int(strikes["landed"]) / (self._total_fights())
        self.total_fights_in_UFC = self._fights_in_UFC(fights)

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

    def _total_fights(self):
        return int(self.wins["total"]) + int(self.losses["total"])

    def _fights_in_UFC(self, fights: list):
        ufc_fights = 0
        for fight in fights:
            if "ufc" in fight["name"].lower():
                ufc_fights += 1
        return ufc_fights

    def get_fight_relevant_data(self):
        return
