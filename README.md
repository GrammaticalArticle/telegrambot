# telegrambot

# Movie Telegram Bot

A Telegram bot built with **Python** and **aiogram 3.x**. This bot acts as a personal assistant, allowing you to manage, search, and rate your favorite movies through a sleek interface.

## 🚀 Features

*   **Interactive List:** Browse your movie collection using dynamic `InlineKeyboard` buttons.
*   **Deep Search:** Find specific titles using the built-in search functionality.
*   **Genre Filtering:** Organize and find movies based on their genre.
*   **Movie Management:** 
    *   Add new movies with a step-by-step FSM (Finite State Machine) wizard.
    *   Edit existing movie descriptions.
    *   Update ratings (1-10) on the fly.
*   **Detailed View:** View posters, cast lists, and ratings in one clean message.

## 🛠 Tech Stack


| Technology | Purpose |
| :--- | :--- |
| **Python** | Core Programming Language |
| **Aiogram 3.x** | Telegram Bot API Framework |
| **Pydantic** | Data Validation & Modeling |
| **JSON** | Lightweight Data Storage |

## 📁 Project Structure

*   `bot.py` — Main entry point and message handlers.
*   `commands.py` — Bot command definitions and menu setup.
*   `config.py` — Sensitive configuration (API Token).
*   `data.py` — JSON database interaction (CRUD logic).
*   `data.json` — The database file where movie records are kept.
*   `keyboards.py` — Custom keyboard layouts and callback logic.
*   `models.py` — Data schemas using Pydantic.

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com
   cd movie-bot
   ```

2. **Install requirements**
   ```bash
   pip install aiogram pydantic
   ```

3. **Setup Token**
   Edit `config.py` and add your bot token:
   ```python
   BOT_TOKEN = "123456789:ABCDEF..."
   ```

4. **Run the Bot**
   ```bash
   python bot.py
   ```

## 🎮 Commands


| Command | Description |
| :--- | :--- |
| `/start` | Welcome message |
| `/films` | Show all movies |
| `/create_film` | Add a new entry |
| `/search_movie` | Search by title |
| `/filter_movies` | Filter by genre |
| `/edit_movie` | Change description |
| `/rate_movie` | Update rating |

---
*Developed by **Tymofii Zeniuk***
