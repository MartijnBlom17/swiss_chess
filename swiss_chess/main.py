"""Main file to run the Swiss Chess tournament."""
import random
from typing import List

import streamlit as st

from swiss_chess.utils.finals import create_finals, create_semis
from swiss_chess.utils.pairing import pairing
from swiss_chess.utils.player import Player
from swiss_chess.utils.plotting import show_standings
from swiss_chess.utils.podium import create_podium
from swiss_chess.utils.puzzle_battle import determine_rounds_standings
from swiss_chess.utils.rounds import collect_results

st.cache_data()


def sidebar_input():
    """Create the sidebar for the input of the Swiss Chess tournament."""
    if "player_names" not in st.session_state:
        st.session_state.player_names = [""]

    with st.sidebar:
        button_result = st.button("Add Player")
        if button_result:
            st.session_state.player_names.append("")
            button_result = False

        for i, player_name in enumerate(st.session_state.player_names):
            st.session_state.player_names[i] = st.text_input(
                f"Player name {i+1}", value=player_name, key=f"player_name_{i}"
            )

        players = st.session_state.player_names
        rounds = int(st.text_input("Number of rounds", "4"))

        with st.expander("Additional settings", False):
            seed = int(st.text_input("Seed", "42"))
            tiebreaker = st.selectbox("Tiebreaker", ["Opponent points", "Puzzle battle"])
            third_place_match = st.checkbox("Third place match", False)
            finals_mode = st.checkbox("Create final bracket", True)

        if "start_button" not in st.session_state:
            st.session_state["start_button"] = False
        if st.button("Start Tournament"):
            st.session_state["start_button"] = True

    if not st.session_state["start_button"]:
        st.stop()

    if "shuffled_players" not in st.session_state:
        random.Random(seed).shuffle(players)
        st.session_state["shuffled_players"] = players
    else:
        players = st.session_state["shuffled_players"]

    all_players = []
    for player in players:
        all_players.append(Player(player))

    return rounds, all_players, third_place_match, tiebreaker, finals_mode


def create_rounds(all_players: List[Player], rounds: int):
    """Create the rounds of the Swiss Chess tournament."""
    extra = 0
    if len(all_players) % 2 != 0:
        extra = 38
    with st.expander("Rounds", True):
        for round in range(rounds):
            with st.container(height=160 + (len(all_players) // 2) * 80 + extra, border=True):
                col1, col2, col3 = st.columns([2, 0.2, 1])

                col1.write(f"## Round {round + 1}:")
                pairs = pairing(all_players)

                col2.empty()

                collect_results(all_players, pairs, round, col1)
                show_standings(all_players, col3)


def main() -> List[Player]:
    """Run the main function of the Swiss Chess tournament format."""
    st.set_page_config(page_title="Swiss Chess", page_icon="data/images/pikapolice.jpg", layout="wide")
    rounds, all_players, third_place_match, tiebreaker, finals_mode = sidebar_input()

    # Rounds
    create_rounds(all_players, rounds)

    # Puzzle battle
    with st.expander("Puzzle Battle", True):
        sorted_players = determine_rounds_standings(all_players, tiebreaker)

    # Semi-final and final
    if finals_mode:
        with st.expander("Semi-finals", True):
            sorted_players = create_semis(sorted_players)

        with st.expander("Finals", True):
            create_finals(sorted_players, third_place_match)

    # Podium
    with st.expander("Podium", True):
        fig = create_podium(all_players, third_place_match, finals_mode)
        st.pyplot(fig)

    return all_players


if __name__ == "__main__":
    all_players = main()
