"""
Tkinter GUI for Speak Easy Trainer.

This module is intentionally thin: all word data lives in words.py and all
navigation logic lives in session.py. The GUI just renders state and wires
up button callbacks. Keeping it this way is what lets the logic be pytest-
tested without ever creating a Tk window.
"""

import tkinter as tk
from tkinter import ttk

from .words import CATEGORIES, build_session_words
from .session import SessionController


class SpeakEasyTrainerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Speak Easy Trainer")
        self.root.geometry("560x420+100+100")
        self.root.minsize(480, 380)
        self.root.configure(bg="#1e2a38")

        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(300, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()

        self.controller: SessionController | None = None
        self.category_key: str | None = None
        self.auto_playing = False
        self.after_id = None

        self.shuffle_var = tk.BooleanVar(value=True)
        self.delay_var = tk.DoubleVar(value=2.0)

        self._build_menu_screen()

    # ---------------- Menu screen ----------------

    def _build_menu_screen(self):
        self._clear_root()

        container = tk.Frame(self.root, bg="#1e2a38")
        container.pack(expand=True, fill="both", padx=30, pady=30)

        title = tk.Label(
            container, text="Speak Easy Trainer",
            font=("Helvetica", 22, "bold"), fg="#ffffff", bg="#1e2a38"
        )
        title.pack(pady=(0, 4))

        subtitle = tk.Label(
            container, text="Pick a category to start your drill",
            font=("Helvetica", 11), fg="#9fb3c8", bg="#1e2a38"
        )
        subtitle.pack(pady=(0, 20))

        btn_frame = tk.Frame(container, bg="#1e2a38")
        btn_frame.pack(fill="both", expand=True)

        for name in CATEGORIES:
            b = tk.Button(
                btn_frame, text=name, font=("Helvetica", 12),
                bg="#2f4157", fg="white", activebackground="#3d5573",
                activeforeground="white", relief="flat", bd=0,
                height=2, command=lambda n=name: self._start_session(n)
            )
            b.pack(fill="x", pady=4)

        options_frame = tk.Frame(container, bg="#1e2a38")
        options_frame.pack(fill="x", pady=(16, 0))

        shuffle_check = tk.Checkbutton(
            options_frame, text="Shuffle order", variable=self.shuffle_var,
            font=("Helvetica", 10), fg="#cfe0ee", bg="#1e2a38",
            selectcolor="#2f4157", activebackground="#1e2a38",
            activeforeground="#cfe0ee"
        )
        shuffle_check.pack(side="left")

        exit_btn = tk.Button(
            options_frame, text="Exit", font=("Helvetica", 10),
            bg="#4a2f36", fg="white", relief="flat",
            command=self.root.destroy
        )
        exit_btn.pack(side="right")

    # ---------------- Practice screen ----------------

    def _start_session(self, category_key: str):
        self.category_key = category_key
        words = build_session_words(category_key, self.shuffle_var.get())
        self.controller = SessionController(words)
        self.auto_playing = False
        self._build_practice_screen()
        self._render_current_word()

    def _build_practice_screen(self):
        self._clear_root()

        header = tk.Frame(self.root, bg="#1e2a38")
        header.pack(fill="x", padx=20, pady=(16, 0))

        back_btn = tk.Button(
            header, text="< Back to menu", font=("Helvetica", 9),
            bg="#1e2a38", fg="#9fb3c8", relief="flat", bd=0,
            command=self._back_to_menu
        )
        back_btn.pack(side="left")

        self.category_label = tk.Label(
            header, text=self.category_key, font=("Helvetica", 10, "bold"),
            fg="#9fb3c8", bg="#1e2a38"
        )
        self.category_label.pack(side="right")

        center = tk.Frame(self.root, bg="#1e2a38")
        center.pack(expand=True, fill="both")

        self.progress_label = tk.Label(
            center, text="", font=("Helvetica", 11),
            fg="#7fa8c9", bg="#1e2a38"
        )
        self.progress_label.pack(pady=(10, 0))

        self.word_label = tk.Label(
            center, text="", font=("Helvetica", 34, "bold"),
            fg="#ffffff", bg="#1e2a38", wraplength=480
        )
        self.word_label.pack(expand=True)

        self.progress_bar = ttk.Progressbar(
            center, orient="horizontal", mode="determinate", length=440
        )
        self.progress_bar.pack(pady=(0, 20))

        controls = tk.Frame(self.root, bg="#1e2a38")
        controls.pack(fill="x", padx=20, pady=(0, 12))

        prev_btn = tk.Button(
            controls, text="<< Prev", font=("Helvetica", 11),
            bg="#2f4157", fg="white", relief="flat", width=8,
            command=self._prev_word
        )
        prev_btn.grid(row=0, column=0, padx=4)

        self.play_pause_btn = tk.Button(
            controls, text="Auto-Play", font=("Helvetica", 11, "bold"),
            bg="#2f7a4f", fg="white", relief="flat", width=12,
            command=self._toggle_autoplay
        )
        self.play_pause_btn.grid(row=0, column=1, padx=4)

        next_btn = tk.Button(
            controls, text="Next >>", font=("Helvetica", 11),
            bg="#2f4157", fg="white", relief="flat", width=8,
            command=self._next_word
        )
        next_btn.grid(row=0, column=2, padx=4)

        restart_btn = tk.Button(
            controls, text="Restart", font=("Helvetica", 11),
            bg="#4a3d2f", fg="white", relief="flat", width=8,
            command=self._restart_session
        )
        restart_btn.grid(row=0, column=3, padx=4)

        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)
        controls.grid_columnconfigure(2, weight=1)
        controls.grid_columnconfigure(3, weight=1)

        pace_frame = tk.Frame(self.root, bg="#1e2a38")
        pace_frame.pack(fill="x", padx=20, pady=(0, 16))

        tk.Label(
            pace_frame, text="Pace (seconds per word):",
            font=("Helvetica", 9), fg="#9fb3c8", bg="#1e2a38"
        ).pack(side="left")

        pace_scale = tk.Scale(
            pace_frame, from_=1.0, to=4.0, resolution=0.5,
            orient="horizontal", variable=self.delay_var,
            bg="#1e2a38", fg="#cfe0ee", troughcolor="#2f4157",
            highlightthickness=0, length=200
        )
        pace_scale.pack(side="left", padx=8)

    def _render_current_word(self):
        c = self.controller
        self.word_label.config(text=c.current_word)
        self.progress_label.config(text=f"Word {c.position} of {c.total}")
        self.progress_bar["maximum"] = c.total
        self.progress_bar["value"] = c.position

    def _next_word(self):
        if self.controller.next():
            self._render_current_word()
        else:
            self._stop_autoplay()
            self.word_label.config(text="Done! Nice work.")

    def _prev_word(self):
        if self.controller.prev():
            self._render_current_word()

    def _restart_session(self):
        self._stop_autoplay()
        words = build_session_words(self.category_key, self.shuffle_var.get())
        self.controller = SessionController(words)
        self._render_current_word()

    def _toggle_autoplay(self):
        if self.auto_playing:
            self._stop_autoplay()
        else:
            self._start_autoplay()

    def _start_autoplay(self):
        self.auto_playing = True
        self.play_pause_btn.config(text="Pause", bg="#7a4f2f")
        self._autoplay_tick()

    def _stop_autoplay(self):
        self.auto_playing = False
        self.play_pause_btn.config(text="Auto-Play", bg="#2f7a4f")
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def _autoplay_tick(self):
        if not self.auto_playing:
            return
        if self.controller.is_last:
            self._stop_autoplay()
            self.word_label.config(text="Done! Nice work.")
            return
        self._next_word()
        delay_ms = int(self.delay_var.get() * 1000)
        self.after_id = self.root.after(delay_ms, self._autoplay_tick)

    def _back_to_menu(self):
        self._stop_autoplay()
        self._build_menu_screen()

    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
