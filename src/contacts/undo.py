import pickle
from pathlib import Path

UNDO_FILE = Path("data/undo_state.pkl")


def save_undo_state(book):
    """Saves the current state of the address book before modification."""
    UNDO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(UNDO_FILE, "wb") as f:
        pickle.dump(book, f)


def load_undo_state():
    """Restores the last saved state of the address book."""
    if not UNDO_FILE.exists():
        return None
    with open(UNDO_FILE, "rb") as f:
        return pickle.load(f)
