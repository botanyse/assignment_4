"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()

SCORE_NAMES = {
    "antisocial": "bpiA",
    "anxiety": "bpiB",
    "headstrong": "bpiC",
    "hyperactive": "bpiD",
    "peer": "bpiE",
}

__all__ = ["BLD", "SRC", "SCORE_NAMES"]

