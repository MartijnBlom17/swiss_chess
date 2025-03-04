"""Determines the winner of the game and gives the player a point based on the winner."""
import base64
import io
from typing import List

import streamlit as st
from PIL import Image

from swiss_chess.utils.player import Player


def find_best_color(player1: Player, player2: Player):
    """Find the best color for each player based on the previous games."""
    player1_ratio = player1.previous_white - player1.previous_black
    player2_ratio = player2.previous_white - player2.previous_black
    if player1_ratio > player2_ratio:
        color1 = "black"
        color2 = "white"
    else:
        color1 = "white"
        color2 = "black"
    player1.add_color(color1)
    player2.add_color(color2)
    return color1, color2


def give_player_point(all_players: List[Player], pair: tuple[Player, Player], winner: str):
    """Give the player a point based on the winner of the game."""
    for player in all_players:
        if winner == "draw":
            if (player.name == pair[0].name) | (player.name == pair[1].name):
                player.add_point_draw()
                player.game_result.append(0.5)
        elif player.name == winner:
            player.add_point()
            player.game_result.append(1.0)
        elif (player.name in [pair[0].name, pair[1].name]) & (player.name != winner):
            player.game_result.append(0.0)


def determine_secondary_points(all_players: List[Player]):
    """Create the secondary points for the players based on the points of the opponents."""
    for player in all_players:
        player.tiebreaker = 0.0
        for opponent in all_players:
            if opponent.name in player.previous_opponents:
                player.tiebreaker += opponent.points


def img_to_bytes(img_path, resize_factor: int = 1):
    """Convert an image to bytes."""
    img = Image.open(img_path)
    img = img.resize((img.width // resize_factor, img.height // resize_factor))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, resize_factor: int = 1):
    """Convert an image to HTML."""
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes(img_path, resize_factor))
    return img_html


def collect_results(
    all_players: List[Player],
    pairs: List[tuple[Player, Player]],
    round_number: int,
    col1: st.delta_generator.DeltaGenerator,
):
    """Collect the results of the games."""
    all_winners = []
    cnt = 0
    for pair in pairs:
        cnt += 1
        color1, color2 = find_best_color(pair[0], pair[1])
        col11, col12 = col1.columns(2)
        col11.write("")
        col11.write("")
        col11.markdown(
            f"""Pairing {cnt}: {pair[0].name} ({img_to_html(f'data/images/{color1}_pawn.png', 25)}) - {pair[1].name}
            ({img_to_html(f'data/images/{color2}_pawn.png', 25)})""",
            unsafe_allow_html=True,
        )
        winner = col12.selectbox(
            "Select winner or 'draw':",
            ["draw", pair[0].name, pair[1].name],
            key=f"winner_{pair[0].name}_{pair[1].name}_{round_number}",
        )
        pair[0].add_opponent(pair[1].name)
        pair[1].add_opponent(pair[0].name)
        all_winners.append(winner)

    submit_key = f"submit_{pair[0].name}_{pair[1].name}_{round_number}"
    if submit_key not in st.session_state:
        st.session_state[submit_key] = False

    if col1.button("Submit", key=f"button_{pair[0].name}_{pair[1].name}_{round_number}"):
        st.session_state[submit_key] = True

    if not st.session_state[submit_key]:
        st.stop()

    for pair, winner in zip(pairs, all_winners):
        give_player_point(all_players, pair, winner)
        determine_secondary_points(all_players)
