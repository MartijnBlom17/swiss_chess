"""Utils file for swiss_chess package."""
import requests  # type: ignore


def chess_puzzle_api(rating: int, moves: int, count: int = 1) -> requests.models.Response:
    """Get a chess puzzle from the chess-puzzles API."""
    url = "https://chess-puzzles.p.rapidapi.com/"

    querystring = {"rating": str(rating), "playerMoves": str(moves), "count": str(count)}

    headers = {
        "x-rapidapi-key": "4f0b83448emsh7e58e9aa99360b9p12231djsn80558b96a14a",
        "x-rapidapi-host": "chess-puzzles.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response
