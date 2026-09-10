# Speak Easy Trainer

A desktop articulation/pronunciation practice app.

## Project structure

```
speak_easy_trainer_project/
├── main.py                       # Entry point - run this to launch the app
├── speak_easy_trainer/
│   ├── __init__.py
│   ├── words.py                  # Word lists + session-building logic (no GUI dependency)
│   ├── session.py                # Navigation state machine (no GUI dependency)
│   └── gui.py                    # Tkinter GUI - thin layer over words.py + session.py
├── tests/
│   ├── test_words.py             # Tests for word data and pairing logic
│   └── test_session.py           # Tests for next/prev/restart navigation
├── pyproject.toml                # pytest config
└── requirements-dev.txt          # pytest (only needed to run tests, not the app)
```

The logic that matters most to get right (word pairing, session navigation)
lives in plain Python modules with zero GUI dependency, so it can be
unit tested directly. `gui.py` only renders state and wires up buttons -
it doesn't contain logic worth testing on its own.

## Running the app

```
python main.py
```

No third-party dependencies needed - tkinter ships with Python on Windows/Mac,
and on Linux you may need `sudo apt install python3-tk`.

## Running the tests

```
pip install -r requirements-dev.txt
pytest
```

or with more detail:

```
pytest -v
```

## Adding new word categories

Add your lists to `speak_easy_trainer/words.py` and register them in the
`CATEGORIES` dict at the top of that file - the GUI menu will pick them up
automatically, no other changes needed.
