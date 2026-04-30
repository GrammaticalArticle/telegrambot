import asyncio
import logging
import sys

from aiogram import types

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN as TOKEN
from data import get_films, add_film, update_film_rating
from keyboards import films_keyboard_markup

from keyboards import films_keyboard_markup, FilmCallback
from aiogram.types import Message, CallbackQuery

from models import Film
from aiogram.types import URLInputFile

from commands import (
   FILMS_COMMAND, 
   START_COMMAND, 
   FILM_CREATE_COMMAND, 
   SEARCH_MOVIE_COMMAND, 
   FILTER_MOVIES_COMMAND, 
   EDIT_MOVIE_COMMAND,
   RATE_MOVIE_COMMAND,
   BOT_COMMANDS
)



dp = Dispatcher()

class MovieStates(StatesGroup):
    search_query = State()
    filter_criteria = State()
    delete_query = State()
    edit_query = State()
    edit_description = State()

class MovieRatingStates(StatesGroup):
    rate_query = State()
    set_rating = State()


@dp.message(SEARCH_MOVIE_COMMAND)
async def search_movie(message: types.Message, state: FSMContext):
    await message.reply("Введіть назву фільму для пошуку:")
    await state.set_state(MovieStates.search_query)

@dp.message(MovieStates.search_query)
async def get_search_query(message: types.Message, state: FSMContext):
    query = message.text.lower()
    results = [film for film in get_films() if query in film['name'].lower()]
    if results:
        for film in results:
            await message.reply(f"Знайдено: {film['name']} - {film['description']}")
    else:
        await message.reply("Фільм не знайдено.")
    
    await state.clear()

@dp.message(FILTER_MOVIES_COMMAND)
async def filter_movies(message: types.Message, state: FSMContext):
    await message.reply("Введіть жанр для фільтрації:")
    await state.set_state(MovieStates.filter_criteria)

@dp.message(MovieStates.filter_criteria)
async def get_filter_criteria(message: types.Message, state: FSMContext):
    criteria = message.text.lower()
    filtered = [film for film in get_films() if criteria in film['genre'].lower()]
    
    if filtered:
        for film in filtered:
            await message.reply(f"Знайдено: {film['name']} - {film['description']}")
    else:
        await message.reply("Фільм не знайдено за цими критеріями.")
    
    await state.clear()

@dp.message(EDIT_MOVIE_COMMAND)
async def edit_movie(message: types.Message, state: FSMContext):
    await message.reply("Введіть назву фільму, який бажаєте редагувати:")
    await state.set_state(MovieStates.edit_query)

@dp.message(MovieStates.edit_query)
async def get_edit_query(message: types.Message, state: FSMContext):
    film_to_edit = message.text.lower()
    all_films = get_films()
    for film in all_films:
        if film_to_edit == film['name'].lower():
            await state.update_data(film_name=film['name'])
            await message.reply("Введіть новий опис фільму:")
            await state.set_state(MovieStates.edit_description)
            return
    await message.reply("Фільм не знайдено.")
    await state.clear()

@dp.message(MovieStates.edit_description)
async def update_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    film_name = data['film_name']
    await message.reply(f"Фільм '{film_name}' оновлено.")
    await state.clear()


@dp.message(START_COMMAND)
async def start(message: Message) -> None:
    await message.answer(
        f"Вітаю, {message.from_user.full_name}!\n"\
        "Я перший бот Python розробника Тимофія Денисович Зенюка."
    )


@dp.message(FILMS_COMMAND)
async def films(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        f"Перелік фільмів. Натисніть на назву фільму для отримання деталей.",
        reply_markup=markup
    )

class FilmForm(StatesGroup):
   name = State()
   description = State()
   rating = State()
   genre = State()
   actors = State()
   poster = State()



@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext) -> None:
   await state.set_state(FilmForm.name)
   await message.answer(
       f"Введіть назву фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )


@dp.message(FilmForm.name)
async def film_name(message: Message, state: FSMContext) -> None:
   await state.update_data(name=message.text)
   await state.set_state(FilmForm.description)
   await message.answer(
       f"Введіть опис фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )


@dp.message(FilmForm.description)
async def film_description(message: Message, state: FSMContext) -> None:
   await state.update_data(description=message.text)
   await state.set_state(FilmForm.rating)
   await message.answer(
       f"Вкажіть рейтинг фільму від 0 до 10.",
       reply_markup=ReplyKeyboardRemove(),
   )


@dp.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
   await state.update_data(rating=float(message.text))
   await state.set_state(FilmForm.genre)
   await message.answer(
       f"Введіть жанр фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )


@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
   await state.update_data(genre=message.text)
   await state.set_state(FilmForm.actors)
   await message.answer(
       text=f"Введіть акторів фільму через роздільник ', '\n"
       + html.bold("Обов'язкова кома та відступ після неї."),
       reply_markup=ReplyKeyboardRemove(),
   )


@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
   await state.update_data(actors=[x for x in message.text.split(", ")])
   await state.set_state(FilmForm.poster)
   await message.answer(
       f"Введіть посилання на постер фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )


@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
   data = await state.update_data(poster=message.text)
   film = Film(**data)
   add_film(film.model_dump())
   await state.clear()
   await message.answer(
       f"Фільм {film.name} успішно додано!",
       reply_markup=ReplyKeyboardRemove(),
   )



@dp.callback_query(FilmCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    film_id = callback_data.id
    film_data = get_films(film_id=film_id)
    film = Film(**film_data)

    text = f"Фільм: {film.name}\n" \
           f"Опис: {film.description}\n" \
           f"Рейтинг: {film.rating}\n" \
           f"Жанр: {film.genre}\n" \
           f"Актори: {', '.join(film.actors)}\n"
   
    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            film.poster,
            filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
        )
    )

@dp.message(RATE_MOVIE_COMMAND)
async def rate_movie(message: Message, state: FSMContext):
    await message.reply("Введіть назву фільму, щоб оцінити:")
    await state.set_state(MovieRatingStates.rate_query)

@dp.message(MovieRatingStates.rate_query)
async def get_rate_query(message: Message, state: FSMContext):
    film_to_rate = message.text.lower()
    all_films = get_films()
    
    found = False
    for film in all_films:
        if film['name'].lower() == film_to_rate:
            await state.update_data(film_name=film['name'])
            await message.reply(f"Знайдено: {film['name']}\nЯку оцінку ставимо (1-10)?")
            await state.set_state(MovieRatingStates.set_rating)
            found = True
            break
            
    if not found:
        await message.reply("Фільм не знайдено.")
        await state.clear()

@dp.message(MovieRatingStates.set_rating)
async def set_rating_done(message: Message, state: FSMContext):
    try:
        new_rating = float(message.text.replace(',', '.'))
        if 1 <= new_rating <= 10:
            data = await state.get_data()
            update_film_rating(data['film_name'], new_rating)
            await message.answer(f"✅ Рейтинг фільму '{data['film_name']}' оновлено до {new_rating}!")
            await state.clear()
        else:
            await message.answer("Будь ласка, введіть число від 1 до 10.")
    except ValueError:
        await message.answer("Це не схоже на число. Спробуйте ще раз.")




@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        user_text = message.text.lower()
        if user_text == "привіт":
            name = message.from_user.first_name
            await message.answer( f"Привіт, {name}! Я готовий шукати фільми 🍿")
        elif user_text == "id":
            await message.answer(f"Тримай свій секретний номер агента кінопрокату:: {message.from_user.id}")
        else:
            await message.answer( "Мої кіно-датчики такого не знають... Може, просто подивимось кіно?")
    except AttributeError:
        await message.answer("Ого, яке фото! Але я поки розумію лише текст. Напиши 'привіт'.")
    except Exception as e:
        await message.answer("Nice try! Щось пішло не так.")


async def main() -> None:
   bot = Bot(
       token=TOKEN,
       default=DefaultBotProperties(
           parse_mode=ParseMode.HTML,
       ),
   )
   await bot.set_my_commands(BOT_COMMANDS)
   await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())