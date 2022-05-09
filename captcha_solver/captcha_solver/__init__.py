from threading import Lock
from typing import Optional, Dict

from captcha_solver.lib.schema import PictureToSolve

_pictures_to_solve_map: Dict[str, PictureToSolve] = {}
_solved_pictures_map: Dict[str, PictureToSolve] = {}

_lock_to_solve_list = Lock()
_lock_solved_list = Lock()


def append_to_pictures_list(*, picture: PictureToSolve) -> None:
    global _lock_to_solve_list
    global _pictures_to_solve_map

    _lock_to_solve_list.acquire()

    _pictures_to_solve_map[picture.id] = picture

    _lock_to_solve_list.release()


def get_picture_by_id(*, picture_id: str) -> Optional[PictureToSolve]:
    global _lock_to_solve_list
    global _pictures_to_solve_map

    _lock_to_solve_list.acquire()

    picture = _pictures_to_solve_map.get(picture_id)

    _lock_to_solve_list.release()

    return picture


def get_next_from_pictures_list() -> Optional[PictureToSolve]:
    global _lock_to_solve_list
    global _pictures_to_solve_map

    _lock_to_solve_list.acquire()

    if len(_pictures_to_solve_map) == 0:
        _lock_to_solve_list.release()
        return None

    picture_key = list(_pictures_to_solve_map.keys())[0]
    picture = _pictures_to_solve_map.pop(picture_key)

    _lock_to_solve_list.release()

    return picture


def add_solved_picture(*, picture: PictureToSolve) -> None:
    global _lock_solved_list
    global _solved_pictures_map

    _lock_solved_list.acquire()

    _solved_pictures_map[picture.id] = picture

    _lock_solved_list.release()


def get_solved_picture(*, picture_id: str) -> Optional[PictureToSolve]:
    global _lock_solved_list
    global _solved_pictures_map

    _lock_solved_list.acquire()

    picture = _solved_pictures_map.get(picture_id)

    _lock_solved_list.release()

    return picture
