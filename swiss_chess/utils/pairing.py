"""Find the optimal pairing for the rounds of the Swiss Chess tournament."""
from typing import List

import networkx as nx
import numpy as np
import streamlit as st
from scipy.optimize import linear_sum_assignment

from swiss_chess.utils.player import Player


def take_odd_player_out(sorted_players: List[Player]):
    """Take out the player with the lowest points if there's an odd number of players."""
    player_loc = 0
    for player in sorted_players:
        if player.no_game_found == 0:
            odd_player = sorted_players.pop(player_loc)
            odd_player.add_no_game()
            st.warning(f"Player {odd_player.name} has no pair.")
            break
        player_loc += 1
    return sorted_players


def get_pairs(players: List[Player], cost_matrix: np.array) -> List[tuple[Player, Player]]:
    """Get the optimal pairs of players based on the cost matrix using nx Graph method."""
    # Assuming `symmetric_cost_matrix` is the symmetric cost matrix already generated
    # Create an undirected graph
    G = nx.Graph()
    # Add nodes with the node for each row/column
    n = cost_matrix.shape[0]
    G.add_nodes_from(range(n))
    # Add edges with weights from the symmetric cost matrix
    for i in range(n):
        for j in range(i + 1, n):  # Only go through upper triangle to avoid duplicates
            G.add_edge(i, j, weight=cost_matrix[i][j])
    # Find the minimum weight full matching.
    matching = nx.algorithms.matching.min_weight_matching(G, weight="weight")

    # Create the pairs
    pairs = [(players[i], players[j]) for (i, j) in list(matching)]

    return pairs


def get_pairs_sophisticated(players: List[Player], row_indices: List[int], col_indices: List[int]):
    """Get the optimal pairs of players based on the cost matrix using the sophisticated Hungarian algorithm."""
    solutionlist1 = []
    solutionlist2 = []
    already_assigned = []
    for i in range(8):
        if i not in already_assigned:
            if (row_indices[i] not in solutionlist1) & (col_indices[i] not in solutionlist1):
                solutionlist1.append(row_indices[i])
                solutionlist1.append(col_indices[i])
                already_assigned.append(i)
                prev_assigned = "list1"
            else:
                solutionlist2.append(row_indices[i])
                solutionlist2.append(col_indices[i])
                already_assigned.append(i)
                prev_assigned = "list2"
            j = col_indices.index(row_indices[i])
            k = row_indices.index(col_indices[i])
            while (j not in already_assigned) | (k not in already_assigned):
                if j not in already_assigned:
                    if prev_assigned == "list1":
                        solutionlist2.append(row_indices[j])
                        solutionlist2.append(col_indices[j])
                    else:
                        solutionlist1.append(row_indices[j])
                        solutionlist1.append(col_indices[j])
                    already_assigned.append(j)
                if k not in already_assigned:
                    if prev_assigned == "list1":
                        solutionlist2.append(row_indices[k])
                        solutionlist2.append(col_indices[k])
                    else:
                        solutionlist1.append(row_indices[k])
                        solutionlist1.append(col_indices[k])
                    already_assigned.append(k)
                if prev_assigned == "list1":
                    prev_assigned = "list2"
                else:
                    prev_assigned = "list1"
                j = col_indices.index(row_indices[k])
                k = row_indices.index(col_indices[k])

    assert len(solutionlist1) == len(solutionlist2), f"{solutionlist1} and {solutionlist2}"

    first_score = sum(
        [
            abs(players[solutionlist1[i]].points - players[solutionlist1[i + 1]].points)
            for i in range(0, len(solutionlist1), 2)
        ]
    )
    second_score = sum(
        [
            abs(players[solutionlist2[i]].points - players[solutionlist2[i + 1]].points)
            for i in range(0, len(solutionlist2), 2)
        ]
    )

    # Filter out pairs where a player is paired with itself
    if first_score <= second_score:
        pairs = [(players[solutionlist1[i]], players[solutionlist1[i + 1]]) for i in range(0, len(solutionlist1), 2)]
    else:
        pairs = [(players[solutionlist2[i]], players[solutionlist2[i + 1]]) for i in range(0, len(solutionlist2), 2)]

    return pairs


def get_pairs_simple(
    players: List[Player], row_indices: List[int], col_indices: List[int]
) -> List[tuple[Player, Player]]:
    """Get the optimal pairs of players based on the cost matrix using the simple Hungarian algorithm."""
    first_pairing = [row_indices[0], col_indices[0]]
    second_pairing = []
    first_score = abs(players[row_indices[0]].points - players[col_indices[0]].points)
    second_score = 0.0
    for x in range(1, len(row_indices)):
        if (row_indices[x] in first_pairing) | (col_indices[x] in first_pairing):
            second_pairing.append(row_indices[x])
            second_pairing.append(col_indices[x])
            second_score += abs(players[row_indices[x]].points - players[col_indices[x]].points)
        else:
            first_pairing.append(row_indices[x])
            first_pairing.append(col_indices[x])
            first_score += abs(players[row_indices[x]].points - players[col_indices[x]].points)

    assert len(first_pairing) == len(second_pairing), f"{first_pairing} and {second_pairing}"

    # Filter out pairs where a player is paired with itself
    if first_score <= second_score:
        pairs = [(players[first_pairing[i]], players[first_pairing[i + 1]]) for i in range(0, len(first_pairing), 2)]
    else:
        pairs = [(players[second_pairing[i]], players[second_pairing[i + 1]]) for i in range(0, len(second_pairing), 2)]

    return pairs


def pairing_by_hand(players: List[Player], row_indices: List[int], col_indices: List[int]):
    """Pair players by hand if the algorithm fails."""
    st.write(f"row_indices: {row_indices}")
    st.write(f"col_indices: {col_indices}")

    st.write("Each list needs to be provided as the following [1, 2, 3, 4]")

    solutionlist1 = st.text_input("List 1:")
    solutionlist2 = st.text_input("List 2:")

    first_score = sum(
        [
            abs(players[solutionlist1[i]].points - players[solutionlist1[i + 1]].points)
            for i in range(0, len(solutionlist1), 2)
        ]
    )
    second_score = sum(
        [
            abs(players[solutionlist2[i]].points - players[solutionlist2[i + 1]].points)
            for i in range(0, len(solutionlist2), 2)
        ]
    )

    # Filter out pairs where a player is paired with itself
    if first_score <= second_score:
        pairs = [(players[solutionlist1[i]], players[solutionlist1[i + 1]]) for i in range(0, len(solutionlist1), 2)]
    else:
        pairs = [(players[solutionlist2[i]], players[solutionlist2[i + 1]]) for i in range(0, len(solutionlist2), 2)]

    return pairs


def create_cost_matrix(players: List[Player]) -> np.array:
    """Create the cost matrix based on the absolute differences in points."""
    num_players = len(players)

    cost_matrix = np.zeros((num_players, num_players))
    for i in range(num_players):
        for j in range(num_players):
            cost_matrix[i, j] = (players[i].points - players[j].points) ** 2
            if i == j:
                cost_matrix[i, j] = 999
            if players[j].name in players[i].previous_opponents:
                cost_matrix[i, j] += 100
    return cost_matrix


def optimal_pairing(players: List[Player]) -> List[tuple[Player, Player]]:
    """Find the optimal pairing for the rounds of the Swiss Chess tournament."""
    cost_matrix = create_cost_matrix(players)

    try:
        pairs = get_pairs(players, cost_matrix)
    except Exception:
        # Use the Hungarian algorithm to find the optimal assignment
        row_indices, col_indices = linear_sum_assignment(cost_matrix, maximize=False)

        st.error("!!!!!!!!!!! First pairing method failed, trying second method !!!!!!!!!!!")
        try:
            pairs = get_pairs_sophisticated(players, list(row_indices), list(col_indices))
        except Exception as e:
            st.error("!!!!!!!!!!! Second pairing method failed, trying third method !!!!!!!!!!!")
            st.error(e)
            try:
                pairs = get_pairs_simple(players, row_indices, col_indices)
            except Exception as e2:
                st.error(e2)
                st.error("!!!!!!!!!!! Third pairing method failed, provide pairing by hand !!!!!!!!!!!")
                pairs = pairing_by_hand(players, row_indices, col_indices)

    return pairs


def pairing(all_players: List[Player]) -> List[tuple[Player, Player]]:
    """Pair the players based on the Swiss Chess tournament rules."""
    sorted_players = sorted(all_players, key=lambda x: x.points, reverse=False)

    if len(sorted_players) % 2 != 0:
        # If there's an odd number of players, one player will have no pair
        sorted_players = take_odd_player_out(sorted_players)

    # Find the optimal pairing for the remaining players
    pairs = optimal_pairing(sorted_players)

    return pairs
