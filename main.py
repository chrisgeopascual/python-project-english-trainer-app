"""
Speak Easy Trainer - entry point.

Run with: python main.py
Requires: Python 3.10+ (standard library only)
"""

import tkinter as tk

from speak_easy_trainer.gui import SpeakEasyTrainerApp


def main():
    print("Starting Speak Easy Trainer...")
    root = tk.Tk()
    SpeakEasyTrainerApp(root)
    print("Window ready. Entering main loop...")
    root.mainloop()
    print("Window closed. Exiting.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        input("Press Enter to close...")
