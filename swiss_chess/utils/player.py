"""Player class for the Swiss Chess Tournament."""
from typing import List

import matplotlib.image as mpimg


class Player:
    """Player class for the Swiss Chess Tournament."""

    def __init__(self, player: str):
        """Initialize the player object."""
        self.name = player
        self.points = 0.0
        self.no_game_found = 0
        self.previous_opponents: List[str] = []
        self.game_result: List[float] = []
        self.previous_white = 0
        self.previous_black = 0
        self.win_percentage = 0
        self.tiebreaker = 0.0
        self.games_played = 0
        self.won_semi_final = False
        self.lost_semi_final = False
        self.won_loser_final = False
        self.lost_loser_final = False
        self.won_final = False
        self.lost_final = False
        self.add_player_image(player)

    def add_player_image(self, player: str):
        """Add player image to the player object."""
        try:
            self.img = mpimg.imread(f"data/images/{player}.png")
        except Exception:
            self.img = mpimg.imread("data/images/pikapolice.jpg")

    def add_point(self):
        """Add a point to the player (due to winning a game)."""
        self.points += 1.0

    def add_point_draw(self):
        """Add half a point to the player (due to drawing a game)."""
        self.points += 0.5

    def add_no_game(self):
        """Add a no game found to the player."""
        self.no_game_found += 1

    def add_opponent(self, opponent):
        """Add a played opponent to the player."""
        self.previous_opponents.append(opponent)

    def add_color(self, color: str):
        """Add the color the player played with to the player."""
        if color == "white":
            self.previous_white += 1
        else:
            self.previous_black += 1

    def add_game(self):
        """Add a game played to the player."""
        self.games_played += 1

    def calc_win_percentage(self):
        """Calculate the win percentage of the player."""
        self.win_percentage = int((self.points / self.games_played) * 100)
