"""Create plots for the Swiss Chess Tournament."""
from typing import List

import matplotlib.pyplot as plt

from swiss_chess.utils.player import Player
from swiss_chess.utils.plotting import create_image_score


def player_won_final(all_players: List[Player]):
    """Return the player that won the final."""
    for player in all_players:
        if player.won_final:
            return player


def player_lost_final(all_players: List[Player]):
    """Return the player that lost the final."""
    for player in all_players:
        if player.lost_final:
            return player


def player_semi(all_players: List[Player]):
    """Return the players that won the semi-finals."""
    lost_semi: List = []
    for player in all_players:
        if player.lost_semi_final:
            if player.won_loser_final:
                lost_semi.insert(0, player)
            else:
                lost_semi.append(player)
    return lost_semi


def add_other_players(all_players: List[Player]):
    """Add other players the list of players and sort them."""
    no_semi = []
    for player in all_players:
        if (not player.lost_semi_final) & (not player.won_semi_final):
            no_semi.append(player)
    return sorted(no_semi, key=lambda x: x.points, reverse=True)


def draw_podium(ax, third_place_match: bool):
    """Draw the podium for the Swiss Chess Tournament."""
    ax.plot([-9, 9], [0, 0], "k")
    ax.plot([-9, -9], [0, 1.5], "k")
    ax.plot([-3, -3], [0, 2], "k")
    ax.plot([3, 3], [0, 2], "k")
    ax.plot([9, 9], [0, 1], "k")
    ax.plot([-9, -3], [1.5, 1.5], "k")
    ax.plot([-3, 3], [2, 2], "k")
    ax.plot([3, 9], [1, 1], "k")
    ax.text(0, 1.4, "1", size=32, ha="center", va="center")
    ax.text(-6, 0.9, "2", size=32, ha="center", va="center")
    if third_place_match:
        ax.text(6, 0.4, "3", size=32, ha="center", va="center")
    else:
        ax.text(6, 0.4, "3/4", size=32, ha="center", va="center")


def sort_players(all_players: List[Player], finals_mode: bool):
    """Sort the players based on the points and tiebreaker."""
    if finals_mode:
        sorted_players = [
            player_won_final(all_players),
            player_lost_final(all_players),
            player_semi(all_players)[0],
            player_semi(all_players)[1],
        ]
        return sorted_players + add_other_players(all_players)
    else:
        return sorted(all_players, key=lambda x: (x.points, x.tiebreaker), reverse=True)


def add_additional_players(ax, sorted_players: List[Player], third_place_match):
    """Add the rest of the players to the podium."""
    if (len(sorted_players) > 4) or (len(sorted_players) > 3 & third_place_match):
        x = 0
        if third_place_match:
            player_start = 3
        else:
            player_start = 4

        for player in sorted_players[player_start:]:
            x += 1
            ax.text(
                10,
                (len(sorted_players[player_start:]) - x) * 0.8 + 0.25,
                f"{x + player_start}",
                size=14,
                ha="right",
                va="center",
            )
            ax = create_image_score(
                player,
                11.8,
                (len(sorted_players[player_start:]) - x) * 0.8 + 0.25,
                11,
                (len(sorted_players[player_start:]) - x) * 0.8,
                0.4,
                "left",
                ax,
            )


def add_players_to_podium(ax, sorted_players: List[Player], third_place_match):
    """Add the players to the podium."""
    # Add picture first place
    ax = create_image_score(sorted_players[0], 0, 1.8, 0, 2.01, 1, "center", ax)

    # Add picture second place
    if len(sorted_players) > 1:
        ax = create_image_score(sorted_players[1], -6, 1.3, -6, 1.51, 1, "center", ax)

    # Add picture third place
    if len(sorted_players) > 3:
        if third_place_match:
            # In case of a third place match, put the winner on the podium
            ax = create_image_score(sorted_players[2], 6, 0.8, 6, 1.01, 1, "center", ax)
        else:
            # In case of no third place match, put both semi finalists on the podium
            ax = create_image_score(sorted_players[2], 4.7, 0.8, 4.7, 1.01, 0.5, "center", ax)
            ax = create_image_score(sorted_players[3], 7.3, 0.8, 7.3, 1.01, 0.5, "center", ax)

    # If there are less than 4 players, just put player 3 on the podium
    elif len(sorted_players) > 2:
        ax = create_image_score(sorted_players[2], 6, 0.8, 6, 1.01, 1, "center", ax)


def create_podium(all_players: List[Player], third_place_match: bool = False, finals_mode: bool = True):
    """Create the podium for the Swiss Chess Tournament."""
    sorted_players = sort_players(all_players, finals_mode)

    fig = plt.figure(figsize=(11, 4.5))
    ax = fig.add_subplot(111)

    # Create podium
    draw_podium(ax, third_place_match)

    # Add players to the podium
    add_players_to_podium(ax, sorted_players, third_place_match)

    # In case of more players, add the rest of the players on the right side
    add_additional_players(ax, sorted_players, third_place_match)

    ax.set_xlim([-10, 13])
    ax.set_ylim([-0.1, 3.5])
    plt.axis("off")
    return fig
