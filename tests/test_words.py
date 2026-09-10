import random

import pytest

from speak_easy_trainer.words import (
    CATEGORIES,
    P_WORDS,
    F_WORDS,
    B_WORDS,
    V_WORDS,
    GENERAL_WORDS,
    build_session_words,
)


# ---------------- Data integrity ----------------

@pytest.mark.parametrize("word_list", [P_WORDS, F_WORDS, B_WORDS, V_WORDS])
def test_sound_lists_have_25_words(word_list):
    assert len(word_list) == 25


def test_general_words_has_50_words():
    assert len(GENERAL_WORDS) == 50


@pytest.mark.parametrize(
    "word_list",
    [P_WORDS, F_WORDS, B_WORDS, V_WORDS, GENERAL_WORDS],
)
def test_no_duplicate_words_within_a_list(word_list):
    assert len(word_list) == len(set(word_list))


def test_pair_categories_have_equal_length_lists():
    for key in ("P/F pairs", "B/V pairs"):
        cat = CATEGORIES[key]
        assert len(cat["a"]) == len(cat["b"])


# ---------------- build_session_words: single categories ----------------

def test_single_category_returns_all_words_unshuffled():
    words = build_session_words("P words", shuffle=False)
    assert words == P_WORDS


def test_single_category_shuffle_preserves_word_set():
    rng = random.Random(42)
    words = build_session_words("General words", shuffle=True, rng=rng)
    assert sorted(words) == sorted(GENERAL_WORDS)
    assert len(words) == len(GENERAL_WORDS)


def test_single_category_shuffle_is_deterministic_with_seeded_rng():
    words_a = build_session_words("P words", shuffle=True, rng=random.Random(7))
    words_b = build_session_words("P words", shuffle=True, rng=random.Random(7))
    assert words_a == words_b


# ---------------- build_session_words: pair categories ----------------

def test_pair_category_length_is_double_the_source_lists():
    words = build_session_words("P/F pairs", shuffle=False)
    assert len(words) == len(P_WORDS) + len(F_WORDS)


def test_pair_category_keeps_pairs_adjacent_unshuffled():
    words = build_session_words("P/F pairs", shuffle=False)
    # word[0]/word[1] must be the P/F contrast pair, and so on down the list.
    for i, (p, f) in enumerate(zip(P_WORDS, F_WORDS)):
        assert words[i * 2] == p
        assert words[i * 2 + 1] == f


def test_pair_category_keeps_pairs_adjacent_when_shuffled():
    rng = random.Random(3)
    words = build_session_words("P/F pairs", shuffle=True, rng=rng)
    # Regardless of shuffle, every even/odd position pair must still be a
    # valid P/F contrast pair (i.e. found at the same index in the source lists).
    for i in range(0, len(words), 2):
        p_word, f_word = words[i], words[i + 1]
        assert p_word in P_WORDS
        assert f_word in F_WORDS
        assert P_WORDS.index(p_word) == F_WORDS.index(f_word)


def test_bv_pairs_also_stay_adjacent_when_shuffled():
    rng = random.Random(11)
    words = build_session_words("B/V pairs", shuffle=True, rng=rng)
    for i in range(0, len(words), 2):
        b_word, v_word = words[i], words[i + 1]
        assert B_WORDS.index(b_word) == V_WORDS.index(v_word)


# ---------------- Error handling ----------------

def test_unknown_category_raises_keyerror():
    with pytest.raises(KeyError):
        build_session_words("Nonexistent category")
