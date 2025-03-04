"""Create plots for the Swiss Chess Tournament."""
import random
from typing import List

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from skimage import transform

from swiss_chess.utils.player import Player


def show_standings(all_players: List[Player], col2: st.delta_generator.DeltaGenerator):
    """Show the standings of the Swiss Chess Tournament."""
    col2.write("# Standings")
    sorted_players = sorted(all_players, key=lambda x: (x.points, x.tiebreaker), reverse=True)
    for player in sorted_players:
        col2.write(
            f"""**{player.name}**: {np.round(player.points, 1)} points
            <span style='color:grey'>({np.round(player.tiebreaker, 1)})</span>""",
            unsafe_allow_html=True,
        )


def create_image_score(player, loc_x_text, loc_y_text, loc_x_pic, loc_y_pic, zoom, outline, ax, final=True, pawn=False):
    """Create image with score and name."""
    if final:
        ax.text(loc_x_text, loc_y_text, f"{player.name}", size=11, ha=outline, va="center")
    if pawn:
        img = mpimg.imread(f"data/images/{player}_pawn.png")
    else:
        img = player.img

    # Improve image quality by using anti-aliasing
    scale = (100 / img.shape[0]) * zoom
    img = transform.rescale(img, scale, channel_axis=2, anti_aliasing=True)

    imagebox = OffsetImage(img, zoom=1)
    ab = AnnotationBbox(imagebox, (loc_x_pic, loc_y_pic), frameon=False, box_alignment=(0.5, 0.0))
    ax.add_artist(ab)
    return ax


def show_matchup(sorted_players: List[Player], is_final: bool = False, third_place_match: bool = False):
    """Show the matchup for the semi-finals or finals."""
    if is_final and not third_place_match:
        fig = plt.figure(figsize=(7, 1))
    else:
        fig = plt.figure(figsize=(7, 4))

    ax = fig.add_subplot(111)
    if is_final:
        random_color1 = ["white", "black"]
        random_color2 = ["white", "black"]
        random.shuffle(random_color1)
        random.shuffle(random_color2)
    else:
        random_color1 = ["white", "black"]
        random_color2 = ["white", "black"]
        random.shuffle(random_color1)
        random.shuffle(random_color2)

    # Text
    if is_final:
        ax.text(0, 8, "Grand Final", size=14, ha="center", va="center")
    else:
        ax.text(0, 8, "Semi Finals", size=14, ha="center", va="center")

    # Text
    if not is_final:
        ax.text(0, 6, "Seed 1 vs. Seed 4", size=11, ha="center", va="center")
    elif third_place_match:
        ax.text(0, 6, "Winner match", size=11, ha="center", va="center")
    # Player 1
    if is_final and not third_place_match:
        ax = create_image_score(sorted_players[0], -1.5, 10.7, -1.5, 3, 1, "center", ax, final=True)
    else:
        ax = create_image_score(sorted_players[0], -1.5, 7.9, -1.5, 3, 1, "center", ax, final=True)

    # Dash
    if is_final and not third_place_match:
        ax.plot([-0.5, 0.5], [6, 6], "k", linewidth=3.0)
    else:
        ax.plot([-0.5, 0.5], [5, 5], "k", linewidth=3.0)

    # Player 4
    if is_final and not third_place_match:
        ax = create_image_score(sorted_players[3], 1.5, 10.7, 1.5, 3, 1, "center", ax, final=True)
    else:
        ax = create_image_score(sorted_players[3], 1.5, 7.9, 1.5, 3, 1, "center", ax, final=True)
    # pawn color
    ax = create_image_score(random_color1[0], 0, 0, -0.7, 3.5, 0.3, "center", ax, final=False, pawn=True)
    ax = create_image_score(random_color1[1], 0, 0, 0.7, 3.5, 0.3, "center", ax, final=False, pawn=True)

    # Text
    if not is_final or third_place_match:
        if not is_final:
            ax.text(0, 0, "Seed 2 vs. Seed 3", size=11, ha="center", va="center")
        elif third_place_match:
            ax.text(0, 0, "Third place match", size=11, ha="center", va="center")
        # Player 2
        ax = create_image_score(sorted_players[1], -1.5, 1.9, -1.5, -3, 1, "center", ax, final=True)
        # Dash
        ax.plot([-0.5, 0.5], [-1, -1], "k", linewidth=3.0)
        # Player 3
        ax = create_image_score(sorted_players[2], 1.5, 1.9, 1.5, -3, 1, "center", ax, final=True)
        # Text
        ax = create_image_score(random_color2[0], 0, 0, -0.7, -2.5, 0.3, "center", ax, final=False, pawn=True)
        ax = create_image_score(random_color2[1], 0, 0, 0.7, -2.5, 0.3, "center", ax, final=False, pawn=True)

    ax.set_xlim([-2, 2])
    if is_final and not third_place_match:
        ax.set_ylim([3, 7])
    else:
        ax.set_ylim([-3, 7])
    plt.axis("off")
    st.pyplot(fig)
