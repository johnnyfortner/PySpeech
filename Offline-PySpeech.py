import os
import threading
import asyncio
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pygame
import edge_tts
import uuid
import tempfile

OUTPUT_FILE = os.path.join(tempfile.gettempdir(), f"speech_{uuid.uuid4().hex}.mp3")

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline PySpeech")
        self.root.geometry("640x580")
        self.root.minsize(500, 580)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Correct binding here

        self.is_playing = False
        self.is_paused = False
        self.play_lock = threading.Lock()

        # Text input with border using a Labelframe
        self.text_frame = ttk.LabelFrame(root, text="Welcome", bootstyle="success")
        self.text_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        self.text_frame_title = ttk.Label(self.text_frame, text="Enter the text that you would like spoken below:", font=("Segoe UI", 12), bootstyle="success")
        self.text_frame_title.pack(anchor="nw", padx=10, pady=5)


        self.text_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)
        self.text_input = tk.Text(self.text_frame, height=8, wrap="word", relief="groove", bd=5, font=("Segoe UI", 16))
        self.text_input.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Voice selection
        self.voice_label = ttk.Label(root, text="Voice:", font=("Segoe UI", 12, "bold"))
        self.voice_label.pack(pady=(5, 0))
        self.voice_var = tk.StringVar(value="en-US-GuyNeural")
        self.voice_combo = ttk.Combobox(
            root,
            textvariable=self.voice_var,
            values=[
                "en-US-AriaNeural",   # US Female 1
                "en-US-JennyNeural",  # US Female 2
                "en-US-GuyNeural",    # US Male 1
                "en-GB-LibbyNeural",  # UK Female 1
                "en-GB-SoniaNeural",  # UK Female 2
                "en-GB-RyanNeural",   # UK Male 1
                "en-GB-ThomasNeural", # UK Male 2
            ],
            font=("Segoe UI", 12),
            bootstyle="active"
        )
        self.voice_combo.pack(pady=(0, 10))

        # Controls Frame (horizontal layout)
        self.controls_frame = ttk.Frame(root)
        self.controls_frame.pack(pady=10)

        self.speak_button = ttk.Button(self.controls_frame, text="Speak", command=self.on_speak, bootstyle="success")
        self.speak_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(self.controls_frame, text="Pause", command=self.on_pause, state="disabled", bootstyle="warning")
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(self.controls_frame, text="Stop", command=self.on_stop, state="disabled", bootstyle="danger")
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Initialize pygame mixer
        pygame.mixer.init()

    def on_speak(self):
        if self.is_playing:
            self.stop_playback()
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input needed", "Please enter some text to speak.")
            return
        voice = self.voice_var.get()
        threading.Thread(target=self.speak_and_play, args=(text, voice), daemon=True).start()

    def on_pause(self):
        with self.play_lock:
            if not self.is_playing:
                return
            if not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.pause_button.config(text="Resume")
            else:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.pause_button.config(text="Pause")

    def on_stop(self):
        self.stop_playback()

    def stop_playback(self):
        with self.play_lock:
            if self.is_playing or self.is_paused:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.unload()
                except Exception:
                    pass
                self.is_playing = False
                self.is_paused = False
                self.pause_button.config(text="Pause", state="disabled")
                self.stop_button.config(state="disabled")
                self.speak_button.config(state="normal")
            if os.path.exists(OUTPUT_FILE):
                try:
                    os.remove(OUTPUT_FILE)
                except Exception as e:
                    print(f"Error deleting {OUTPUT_FILE}: {e}")

    async def save_speech(self, text, voice):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(OUTPUT_FILE)

    def speak_and_play(self, text, voice):
        self.root.after(0, lambda: self.speak_button.config(state="disabled"))
        self.root.after(0, lambda: self.pause_button.config(state="normal"))
        self.root.after(0, lambda: self.stop_button.config(state="normal"))

        try:
            asyncio.run(self.save_speech(text, voice))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"TTS generation failed:\n{e}"))
            self.root.after(0, self.stop_playback)
            return

        with self.play_lock:
            self.is_playing = True
            self.is_paused = False
            self.root.after(0, lambda: self.pause_button.config(text="Pause"))

        try:
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Playback Error", f"Cannot play audio:\n{e}"))
            self.stop_playback()
            return

        while pygame.mixer.music.get_busy():
            if not self.is_paused:
                pygame.time.Clock().tick(100)

        with self.play_lock:
            if not self.is_paused:  # Only stop playback if it really ended
                self.is_playing = False
                self.root.after(0, lambda: self.pause_button.config(state="disabled"))
                self.root.after(0, lambda: self.stop_button.config(state="disabled"))
                self.root.after(0, lambda: self.speak_button.config(state="normal"))

                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                except Exception:
                    pass

                if os.path.exists(OUTPUT_FILE):
                    try:
                        os.remove(OUTPUT_FILE)
                    except Exception as e:
                        print(f"Error deleting {OUTPUT_FILE}: {e}")

    def on_close(self):
        self.stop_playback()
        pygame.mixer.quit()
        if os.path.exists(OUTPUT_FILE):
            try:
                os.remove(OUTPUT_FILE)
            except Exception as e:
                print(f"Error deleting {OUTPUT_FILE} on close: {e}")
        self.root.destroy()

if __name__ == "__main__":
    app = ttk.Window(themename="cyborg")  # Choose theme
    TTSApp(app)
    app.mainloop()
