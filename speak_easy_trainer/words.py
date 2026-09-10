"""
Word data and session-building logic for Speak Easy Trainer.

This module has NO dependency on tkinter or any GUI toolkit, so it can be
unit tested directly with pytest.
"""

import random

P_WORDS = [
    "population", "opportunity", "personality", "participate", "preparation",
    "professional", "popularity", "presentation", "perspective", "potential",
    "properly", "apparently", "particular", "positively", "comparison",
    "proposal", "principle", "participant", "purposeful", "productivity",
    "perpendicular", "appropriate", "capacity", "temporary", "transparency",
]

F_WORDS = [
    "foundation", "fascination", "familiarity", "fabricate", "formation",
    "fictional", "federation", "flexibility", "fortunately", "philosophy",
    "photography", "fundamental", "facilitate", "favorable", "ferociously",
    "financially", "forgiveness", "fortunate", "functionality", "familiarize",
    "definitely", "reference", "fantasy", "faithfully", "formidable",
]

B_WORDS = [
    "beautiful", "ability", "probability", "responsibility", "celebration",
    "bacteria", "obligation", "basically", "absolutely", "benefit",
    "combination", "observation", "biography", "obesity", "bibliography",
    "babysitter", "rebellion", "probable", "contribution", "bureaucracy",
    "abundant", "debatable", "inhibition", "establishment", "celebrity",
]

V_WORDS = [
    "vocabulary", "availability", "university", "variety", "environment",
    "vulnerable", "eventually", "individual", "volunteer", "investigate",
    "conversation", "advantage", "relevant", "innovative", "vibration",
    "violation", "inevitable", "cultivate", "activity", "negative",
    "valuable", "vocalist", "adventure", "violently", "victory",
]

GENERAL_WORDS = [
    "technology", "dictionary", "calculator", "temperature", "laboratory",
    "curiosity", "generation", "imagination", "determination", "communication",
    "organization", "examination", "registration", "graduation", "hesitation",
    "explanation", "situation", "limitation", "motivation", "dedication",
    "education", "information", "documentation", "qualification", "recommendation",
    "congratulations", "entertainment", "requirement", "achievement", "development",
    "management", "government", "announcement", "agreement", "involvement",
    "improvement", "investment", "attachment", "equipment", "instrument",
    "category", "territory", "inventory", "accessory", "anniversary",
    "necessary", "secretary", "customary", "imaginary", "auditorium",
]

# Single-sound categories are just word lists.
# Paired categories are built from two equal-length lists so that word[i]
# in list A is the intended contrast partner of word[i] in list B.
CATEGORIES = {
    "P words": {"type": "single", "words": P_WORDS},
    "F words": {"type": "single", "words": F_WORDS},
    "B words": {"type": "single", "words": B_WORDS},
    "V words": {"type": "single", "words": V_WORDS},
    "P/F pairs": {"type": "pair", "a": P_WORDS, "b": F_WORDS},
    "B/V pairs": {"type": "pair", "a": B_WORDS, "b": V_WORDS},
    "General words": {"type": "single", "words": GENERAL_WORDS},
}


def build_session_words(
    category_key: str,
    shuffle: bool = True,
    rng: random.Random | None = None,
) -> list[str]:
    """Return the ordered word sequence for a practice session.

    For 'pair' categories, each contrast pair (e.g. population/foundation)
    always stays adjacent - only the ORDER of pairs is shuffled, never the
    words within a pair. This preserves the contrastive drilling purpose.

    Args:
        category_key: One of the keys in CATEGORIES.
        shuffle: Whether to randomize order.
        rng: Optional random.Random instance for deterministic testing.
             Defaults to the global `random` module.

    Raises:
        KeyError: If category_key is not a valid category.
    """
    if category_key not in CATEGORIES:
        raise KeyError(
            f"Unknown category '{category_key}'. "
            f"Valid categories: {list(CATEGORIES)}"
        )

    rng = rng if rng is not None else random
    cat = CATEGORIES[category_key]

    if cat["type"] == "single":
        words = list(cat["words"])
        if shuffle:
            words = rng.sample(words, len(words))
        return words

    # type == "pair"
    a_list, b_list = cat["a"], cat["b"]
    indices = list(range(len(a_list)))
    if shuffle:
        rng.shuffle(indices)
    sequence = []
    for i in indices:
        sequence.append(a_list[i])
        sequence.append(b_list[i])
    return sequence
