import pytest

from speak_easy_trainer.session import SessionController


def test_cannot_create_session_with_empty_words():
    with pytest.raises(ValueError):
        SessionController([])


def test_initial_state_starts_at_first_word():
    s = SessionController(["alpha", "beta", "gamma"])
    assert s.current_word == "alpha"
    assert s.position == 1
    assert s.total == 3
    assert s.is_first is True
    assert s.is_last is False


def test_next_advances_position():
    s = SessionController(["alpha", "beta", "gamma"])
    advanced = s.next()
    assert advanced is True
    assert s.current_word == "beta"
    assert s.position == 2


def test_next_returns_false_at_last_word():
    s = SessionController(["alpha", "beta"])
    s.next()  # now at "beta", the last word
    assert s.is_last is True
    advanced = s.next()
    assert advanced is False
    assert s.current_word == "beta"  # unchanged


def test_prev_moves_back():
    s = SessionController(["alpha", "beta", "gamma"])
    s.next()
    s.next()
    moved = s.prev()
    assert moved is True
    assert s.current_word == "beta"


def test_prev_returns_false_at_first_word():
    s = SessionController(["alpha", "beta"])
    assert s.is_first is True
    moved = s.prev()
    assert moved is False
    assert s.current_word == "alpha"  # unchanged


def test_restart_resets_to_first_word():
    s = SessionController(["alpha", "beta", "gamma"])
    s.next()
    s.next()
    s.restart()
    assert s.current_word == "alpha"
    assert s.position == 1
    assert s.is_first is True


def test_progress_ratio_at_start_and_end():
    s = SessionController(["alpha", "beta", "gamma", "delta"])
    assert s.progress_ratio() == pytest.approx(0.25)
    s.next()
    s.next()
    s.next()
    assert s.is_last is True
    assert s.progress_ratio() == pytest.approx(1.0)


def test_single_word_session_is_both_first_and_last():
    s = SessionController(["only"])
    assert s.is_first is True
    assert s.is_last is True
    assert s.next() is False
    assert s.prev() is False


def test_full_walkthrough_of_a_session():
    words = ["one", "two", "three"]
    s = SessionController(words)
    seen = [s.current_word]
    while s.next():
        seen.append(s.current_word)
    assert seen == words
