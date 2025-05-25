<div align="center">
  <h1>PySpeech</h1>
  <p>Offline text to speech in python</p>

🗣️ Text-to-Speech Voice App

A simple and efficient GUI-based text-to-speech (TTS) utility using Microsoft's Edge TTS, `pygame` for audio playback, and `ttkbootstrap` for a modern tkinter look.

---
</div>
 📦 Installation

### ✅ Install Globally (System-Wide)
```bash
python -m pip install -r requirements.txt
```

### 🧪 Isolated Install via Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

> 💡 It's recommended to use a virtual environment to avoid dependency conflicts with other Python projects.

---

## 🚀 Usage

### Run via Python
```bash
python app.py
```

Or double-click `app.py` if file associations are properly configured on Windows.

---

## 🎯 Functionality

- ✅ Enter text in a modern, styled tkinter GUI
- ✅ Converts entered text to speech using Microsoft Edge TTS (multilingual)
- ✅ Saves audio to a temporary `.mp3` file
- ✅ Plays it back instantly with `pygame`
- ✅ Works offline once dependencies are installed
- ✅ Clean threading ensures GUI stays responsive during TTS generation

---

## 🛠️ Utilities & Dependencies

- [`edge-tts`](https://pypi.org/project/edge-tts/) – Leverages Microsoft’s online speech synthesis
- [`pygame`](https://pypi.org/project/pygame/) – Lightweight audio playback for `.mp3` output
- [`ttkbootstrap`](https://pypi.org/project/ttkbootstrap/) – Modern Bootstrap-inspired GUI styling for tkinter
- `tempfile`, `uuid`, `os`, `asyncio`, `threading`, `tkinter` – Standard Python libraries

---

## 🔧 To Do

- [ ] Add ability to export `.mp3` files to a user-defined location
- [ ] Voice selection previews
- [ ] Custom speaking rate and pitch sliders
- [ ] Support for macOS and Linux platforms

---

## ⚠️ Notes

This app was only tested on **Windows 10/11**.  
Microsoft's built-in TTS options are surprisingly limited and clunky, which is why this tool was hacked together in one morning to solve a real personal need.

---

## 🧼 Cleanup

Temporary `.mp3` files are created in your OS temp directory and may be cleaned up manually if needed (though they’re generally small and disposable).

---

## 📄 License

[MIT License](LICENSE) – Free for personal and commercial use.


---

## 🙌 Credits

Created with Python

> If you like this, ⭐️ the repo.
