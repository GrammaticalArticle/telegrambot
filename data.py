# Example: https://s.studiobinder.com/wp-content/uploads/2019/06/Movie-Poster-Template-Movie-Credits-StudioBinder.jpg

import json

def get_films(file_path: str = "data.json", film_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        films = json.load(fp)
        if film_id is not None and film_id < len(films):
            return films[film_id]
        return films
    

def add_film(film: dict, file_path: str = "data.json"):
    films = get_films(file_path=file_path)
    films.append(film)
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(films, fp, indent=4, ensure_ascii=False)


def update_film_rating(film_name: str, new_rating: float, file_path: str = "data.json"):
    films = get_films(file_path=file_path)
    for film in films:
        if film['name'].lower() == film_name.lower():
            film['rating'] = new_rating
            break
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(films, fp, indent=4, ensure_ascii=False)
