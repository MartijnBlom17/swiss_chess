"""The puzzle battle for the swiss chess tournament."""
from typing import List

import chess
import chess.svg
import numpy as np
import streamlit as st

from swiss_chess.utils.player import Player
from swiss_chess.utils.utils import chess_puzzle_api


def puzzle_battle(player1: Player, player2: Player, cnt: int):
    """Determine the winner of the puzzle battle."""
    st.write("Because of a tie in the final standings there will be a puzzle battle!")
    st.write(f"The battle will be between {player1.name} and {player2.name}.")
    rating = st.selectbox(
        "Select the rating for the puzzle battle:", [1000, 1500, 2000, 2500, 3000], key=f"rating_{cnt}"
    )
    moves = st.selectbox("Select the number of moves for the puzzle battle:", [1, 2, 3, 4], key=f"moves_{cnt}")

    submit_key = f"puzzle_choice_{player1.name}_{player2.name}_{cnt}"
    if submit_key not in st.session_state:
        st.session_state[submit_key] = False

    if st.button("Confirm choice", key=f"button_puzzle__choice_{player1.name}_{player2.name}_{cnt}"):
        st.session_state[submit_key] = True

    if not st.session_state[submit_key]:
        st.stop()

    response = chess_puzzle_api(rating, moves)
    fen = response.json()["puzzles"][0]["fen"]

    split_respnse = fen.split(" ")
    if split_respnse[1] == "w":
        color = "White"
    else:
        color = "Black"
    st.title(f"{color} to move with {moves} move(s).")
    board = chess.Board(fen)
    svg = chess.svg.board(board, size=700)
    st.image(svg, output_format="SVG")

    winner = st.selectbox(
        "Provide the name of the winner of the puzzle battle:",
        [player1.name, player2.name],
        key=f"puzzle_battle_{cnt}",
    )
    winner = winner.replace("'", "").replace('"', "")

    submit_key = f"puzzle_{player1.name}_{player2.name}_{cnt}"
    if submit_key not in st.session_state:
        st.session_state[submit_key] = False

    if st.button("Submit", key=f"button_puzzle_{player1.name}_{player2.name}_{cnt}"):
        st.session_state[submit_key] = True

    if not st.session_state[submit_key]:
        st.stop()

    if winner == player1.name:
        player1.tiebreaker = np.round(player1.tiebreaker + 0.1, 1)
    else:
        player2.tiebreaker = np.round(player2.tiebreaker + 0.1, 1)
    return None


def determine_rounds_standings(all_players: List[Player], tiebreaker):
    """Create the puzzle battle."""
    if tiebreaker == "Opponent points":
        sorted_players = sorted(all_players, key=lambda x: (x.points, x.tiebreaker), reverse=True)
        all_points = [(player.points, player.tiebreaker) for player in sorted_players]
    else:
        sorted_players = sorted(all_players, key=lambda x: x.points, reverse=True)
        all_points = [(player.points, 0) for player in sorted_players]

    all_points2 = [point for point in all_points if point >= all_points[3]]
    top_players = sorted_players[: len(all_points2)]
    cnt = 0
    while len(all_points2) != len(set(all_points2)):
        for i, player in enumerate(top_players):
            for j, player2 in enumerate(top_players):
                if (
                    (i != j)
                    and (player.points == player2.points)
                    and (tiebreaker != "Opponent points" or player.tiebreaker == player2.tiebreaker)
                ):
                    cnt += 1
                    puzzle_battle(player, player2, cnt)
                    if tiebreaker == "Opponent points":
                        all_points2 = [(player.points, player.tiebreaker) for player in top_players]
                    else:
                        all_points2 = [(player.points, 0) for player in top_players]
                    break

    if tiebreaker == "Opponent points":
        sorted_players = sorted(all_players, key=lambda x: (x.points, x.tiebreaker), reverse=True)
    else:
        sorted_players = sorted(all_players, key=lambda x: x.points, reverse=True)
    return sorted_players
