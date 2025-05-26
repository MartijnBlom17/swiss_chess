"""Create the semifinals of the tournament."""
from typing import List

import streamlit as st

from swiss_chess.utils.player import Player
from swiss_chess.utils.plotting import show_matchup


def sort_players_final(sorted_players: List[Player]):
    """Sort the players for the final."""
    if sorted_players[0].won_semi_final:
        if sorted_players[1].won_semi_final:
            return [sorted_players[0], sorted_players[3], sorted_players[2], sorted_players[1]]
        else:
            return [sorted_players[0], sorted_players[3], sorted_players[1], sorted_players[2]]
    else:
        if sorted_players[1].won_semi_final:
            return [sorted_players[3], sorted_players[0], sorted_players[2], sorted_players[1]]
        else:
            return [sorted_players[3], sorted_players[0], sorted_players[1], sorted_players[2]]


def create_semis(sorted_players: List[Player]):
    """Create the semi-finals of the tournament."""
    show_matchup(sorted_players)
    return determine_winners_semi(sorted_players)


def create_finals(sorted_players: List[Player], third_place_match: bool):
    """Create the finals of the tournament."""
    sorted_players_final = sort_players_final(sorted_players)
    show_matchup(sorted_players_final, is_final=True, third_place_match=third_place_match)
    determine_winner_final(sorted_players_final, third_place_match)


def determine_winners_semi(sorted_players: List[Player]):
    """Determine the winners of the semi-finals."""
    st.write("### In case of a draw, a 3+2 will determine the winner")
    # Semi-final one
    winner = st.selectbox(
        f"Provide name of winner between {sorted_players[0].name} and {sorted_players[3].name}: ",
        [sorted_players[0].name, sorted_players[3].name],
        key="semi_final_one",
    )
    if winner == sorted_players[0].name:
        sorted_players[0].won_semi_final = True
        sorted_players[3].lost_semi_final = True
    elif winner == sorted_players[3].name:
        sorted_players[0].lost_semi_final = True
        sorted_players[3].won_semi_final = True

    # Semi-final two
    winnerr = st.selectbox(
        f"Provide name of winner between {sorted_players[1].name} and {sorted_players[2].name}: ",
        [sorted_players[1].name, sorted_players[2].name],
        key="semi_final_two",
    )
    winnerr = winnerr.replace("'", "").replace('"', "")
    if winnerr == sorted_players[1].name:
        sorted_players[1].won_semi_final = True
        sorted_players[2].lost_semi_final = True
    elif winnerr == sorted_players[2].name:
        sorted_players[1].lost_semi_final = True
        sorted_players[2].won_semi_final = True

    submit_key = "semi"
    if submit_key not in st.session_state:
        st.session_state[submit_key] = False

    if st.button("Submit", key=f"button_{submit_key}"):
        st.session_state[submit_key] = True

    if not st.session_state[submit_key]:
        st.stop()

    return sorted_players


def determine_winner_final(sorted_players: List[Player], third_place_match: bool):
    """Determine the winner of the final."""
    st.write("### In case of a draw, a 3+2 will determine the winner")

    # Final
    winner = st.selectbox(
        f"Provide name of winner between {sorted_players[0].name} and {sorted_players[3].name}: ",
        [sorted_players[0].name, sorted_players[3].name],
    )
    if winner == sorted_players[0].name:
        sorted_players[0].won_final = True
        sorted_players[3].lost_final = True
    elif winner == sorted_players[3].name:
        sorted_players[0].lost_final = True
        sorted_players[3].won_final = True

    # third-place
    if third_place_match:
        winnerr = st.selectbox(
            f"Provide name of winner between {sorted_players[1].name} and {sorted_players[2].name}: ",
            [sorted_players[1].name, sorted_players[2].name],
        )
        if winnerr == sorted_players[1].name:
            sorted_players[1].won_loser_final = True
            sorted_players[2].lost_loser_final = True
        elif winnerr == sorted_players[2].name:
            sorted_players[1].lost_loser_final = True
            sorted_players[2].won_loser_final = True

    submit_key = "final"
    if submit_key not in st.session_state:
        st.session_state[submit_key] = False

    if st.button("Submit", key=f"button_{submit_key}"):
        st.session_state[submit_key] = True

    if not st.session_state[submit_key]:
        st.stop()
