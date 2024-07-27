import allure
import requests


class ApiSchedule:
    """Класс предоставляет методы для работы с сервером приложения"""

    def __init__(self, url: str, token: str) -> None:
        """
        Инициализация обьекта

        args:
        url - адрес сайта.
        token - токен авторизации.
        """
        self.url = url
        self.token = token
        self.headers = {}
        self.headers["Cookie"] = self.token

    @allure.step(
            "api.Получение расписание преподавателя, \
            в диопазоне дат от {start} до {end}"
            )
    def get_events(self, start: str, end: str):
        """
        Получение расписания преподавателя.

        args:
        start - дата и время начала списка событий.
        Формат YYYY-MM-DDThh:mm:ss.sssZ.

        end - дата и время окончания списка событий.
        Формат YYYY-MM-DDThh:mm:ss.sssZ.
        """
        body = {
            "from": start,
            "till": end
        }
        resp = requests.post(
            self.url + '/events', json=body, headers=self.headers
        )
        return resp

    @allure.step(
            "api. Добавление личного события, \
                 со списком данных {description}"
            )
    def add_event(self, description: dict):
        """
        Создание личного события.

        args:
        description - словарь с данными личного события.

        {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "",
        "title": "Событие такое",
        "startAt": "2024-07-15T09:30:00+07:00",
        "endAt": "2024-07-15T10:00:00+07:00"
        }
        """
        resp = requests.post(
            self.url + '/createPersonal',
            json=description, headers=self.headers
        )
        return resp

    @allure.step(
            "api. Изменение личного события, \
                со списком данных {description}"
            )
    def update_event(self, description: dict):
        """
        Изменение существующего события.

        args:
        description - словарь с данными личного события.

        {
        "backgroundColor": "#F4F5F6",
        "color": "#43B658",
        "description":"Изменения в описании",
        "title": "Тестовое событие",
        "startAt": "2024-07-15T09:30:00+07:00",
        "endAt": "2024-07-15T10:00:00+07:00",
        "id": event_id,
        "oldStartAt": old_start
        }
        """
        resp = requests.post(
            self.url + '/updatePersonal',
            json=description, headers=self.headers
        )
        return resp

    @allure.step("api. Добавление урока, со списком данных {description}")
    def add_class(self, description: dict):
        """
        Создание урока.

        args:
        description - словарь с данными урока.
        {
        "educationServiceId": EDUCATION_ID,
        "type": "single",
        "startAt": startAt
        }
        """
        resp = requests.post(
            self.url + '/createClass',
            json=description, headers=self.headers
        )
        return resp

    @allure.step(
            "api. Удаление личного события, по идентификатору \
                {id} и началу события {startAt}"
            )
    def del_event(self, id: str, startAt: str):
        """
        Удаление события.

        args:
        id - идентификатор события.
        startAt - время начала события.
        """
        body = {
            "id": id,
            "startAt": startAt
        }
        resp = requests.post(
            self.url + '/removePersonal', json=body, headers=self.headers
        )
        return resp

    @allure.step(
            "api. Удаление урока, по переданым данным {class_id}, \
                {initiator}, {reason}, {comment}"
        )
    def del_class(
            self, class_id: str,
            initiator: str = 'teacher',
            reason: int = 6,
            comment: str = "null"
            ):
        """
        Удаление урока.

        args:
        class_id - идентификатор урока.
        initiator - инициатор удаления урока.
        reason - вариант причины отмены урока.
        comment - комментарий.
        """
        body = {
            "virtualClassId": class_id,
            "initiator": initiator,
            "reason": reason,
            "comment": comment
        }
        resp = requests.post(
            self.url + '/cancelClass', json=body, headers=self.headers
        )
        return resp
