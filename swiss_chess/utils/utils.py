"""Utils file for swiss_chess package."""
import requests  # type: ignore
import streamlit as st


@st.cache_data
def chess_puzzle_api(
    rating: int, moves: int, iteration: int, count: int = 1, deviation: int = 100
) -> requests.models.Response:
    """Get a chess puzzle from the chess-puzzles API."""
    # To avoid having the same puzzle created multiple times
    _ = iteration

    url = "https://chess-puzzles.p.rapidapi.com/"

    querystring = {
        "rating": str(rating),
        "playerMoves": str(moves),
        "count": str(count),
        "ratingdeviation": str(deviation),
    }

    headers = {
        "x-rapidapi-key": "4f0b83448emsh7e58e9aa99360b9p12231djsn80558b96a14a",
        "x-rapidapi-host": "chess-puzzles.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response
