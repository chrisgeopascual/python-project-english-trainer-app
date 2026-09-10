"""
Session navigation logic for Speak Easy Trainer.

SessionController tracks position within a word list (next/prev/restart)
with no dependency on tkinter, so it can be unit tested directly.
"""


class SessionController:
    """Tracks the current position within a practice session's word list."""

    def __init__(self, words: list[str]):
        if not words:
            raise ValueError("words list cannot be empty")
        self.words: list[str] = list(words)
        self.current_index: int = 0

    @property
    def current_word(self) -> str:
        return self.words[self.current_index]

    @property
    def total(self) -> int:
        return len(self.words)

    @property
    def position(self) -> int:
        """1-indexed position for display (e.g. 'Word 3 of 25')."""
        return self.current_index + 1

    @property
    def is_first(self) -> bool:
        return self.current_index == 0

    @property
    def is_last(self) -> bool:
        return self.current_index == self.total - 1

    def next(self) -> bool:
        """Advance to the next word.

        Returns:
            True if advanced, False if already at the last word.
        """
        if self.is_last:
            return False
        self.current_index += 1
        return True

    def prev(self) -> bool:
        """Move back to the previous word.

        Returns:
            True if moved back, False if already at the first word.
        """
        if self.is_first:
            return False
        self.current_index -= 1
        return True

    def restart(self) -> None:
        """Reset to the first word."""
        self.current_index = 0

    def progress_ratio(self) -> float:
        """Fraction of the session completed, from just past 0 to 1.0."""
        return self.position / self.total
