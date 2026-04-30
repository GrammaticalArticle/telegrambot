from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

FILMS_COMMAND = Command('films')
START_COMMAND = Command('start')
FILM_CREATE_COMMAND = Command("create_film")
SEARCH_MOVIE_COMMAND = Command("search_movie")
FILTER_MOVIES_COMMAND = Command("filter_movies")
EDIT_MOVIE_COMMAND = Command("edit_movie")
RATE_MOVIE_COMMAND = Command("rate_movie")

BOT_COMMANDS = [
   BotCommand(command="films", description="Перегляд списку фільмів"),
   BotCommand(command="start", description="Почати розмову"),
   BotCommand(command="create_film", description="Додати новий фільм"),
   BotCommand(command="search_movie", description="Пошук фільму за назвою"),
   BotCommand(command="filter_movies", description="Фільтрація за жанром"),
   BotCommand(command="edit_movie", description="Редагувати опис фільму"),
   BotCommand(command="rate_movie", description="Оцінити фільм")
]
