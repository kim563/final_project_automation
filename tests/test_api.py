import allure
import pytest
from pages.api_class import ApiSchedule
from dateutil import parser
from config.config import URL_API, TOKEN, EDUCATION_ID


@allure.epic("Тестирование Api")
@allure.severity("blocker")
class ApiTest:
    """Класс предоставляет методы для тестирования API сервера"""

    api = ApiSchedule(URL_API, TOKEN)

    @allure.id("Skyeng-1")
    @allure.story("Получение расписания")
    @allure.feature("READ")
    @allure.title("Получение списка личных событий преподавателя")
    @allure.description(
        "Данный тест проверяет возможность получения личных \
        событий в расписании преподавателей."
    )
    @pytest.mark.api_test
    def test_get_events(self):
        with allure.step(
                "Получение расписание преподователя в \
                заданном диопазоне дат"
                ):
            resp = self.api.get_events(
                "2024-07-15T00:00:00+07:00",
                "2024-07-15T23:59:59+07:00"
                )
        with allure.step("Проверка статус кода"):
            assert resp.status_code == 200
        with allure.step("Проверка наличия файла в ответе"):
            assert resp.headers["Content-Type"] == "application/json"

    @allure.id("Skyeng-2")
    @allure.story("Создание событий")
    @allure.feature("CREATE")
    @allure.title("Добавление личного события в расписание преподавателя.")
    @allure.description(
        "Данный тест проверяет возможность добавления личных событий \
        в расписание преподавателя."
    )
    @pytest.mark.api_test
    def test_add_even(self):
        with allure.step("Создание списка данных для нового события"):
            body = {
                "backgroundColor": "#F4F5F6",
                "color": "#81888D",
                "description": "",
                "title": "Событие такое",
                "startAt": "2024-07-15T09:30:00+07:00",
                "endAt": "2024-07-15T10:00:00+07:00"
            }
        with allure.step("Добавить новое событие"):
            resp = self.api.add_event(body)

        with allure.step("Фильтрация полезных данных из ответа сервера"):
            resp_data = resp.json()["data"]["payload"]["payload"]

        with allure.step("Проверка статус кода"):
            assert resp.status_code == 200

        with allure.step("Проверка соответствия цвета фона события"):
            assert resp_data["backgroundColor"] == body["backgroundColor"]

        with allure.step("Проверка соответствия цвета текста события"):
            assert resp_data["color"] == body["color"]

        with allure.step("Проверка соответствия описания события"):
            assert resp_data["description"] == body["description"]

        with allure.step("Проверка соответствия названия события"):
            assert resp_data["title"] == body["title"]

    @allure.id("Skyeng-3")
    @allure.story("Изменение события")
    @allure.feature("UPDATE")
    @allure.title(
            "Изменение существующего личного события \
            преподавателя по id"
        )
    @allure.description(
        "Данный тест проверяет возможность изменения уже сущесвующих \
        личных событий в расписании преподавателя."
    )
    @pytest.mark.api_test
    def test_update_event(self):
        with allure.step("Создание списка данных для нового события"):
            body = {
                "backgroundColor": "#F4F5F6",
                "color": "#81888D",
                "description": "",
                "title": "Событие такое",
                "startAt": "2024-07-16T09:30:00+07:00",
                "endAt": "2024-07-16T10:00:00+07:00"
            }

        with allure.step("Добавить новое событие"):
            resp = self.api.add_event(body)

        with allure.step("Получение id события из ответа сервера"):
            event_id = resp.json()['data']["payload"]["id"]

        with allure.step(
                "Получение даты и времени начала события из ответа сервера"
                ):
            old_start = resp.json()['data']['startAt']

        with allure.step(
                "Создание нового списка данных для обновления события"
                ):
            new_body = {
                "backgroundColor": "#F4F5F6",
                "color": "#43B658",
                "description": "Изменения в описании",
                "title": "Тестовое событие",
                "startAt": "2024-07-15T09:30:00+07:00",
                "endAt": "2024-07-15T10:00:00+07:00",
                "id": event_id,
                "oldStartAt": old_start
            }

        with allure.step("Обновление события"):
            resp = self.api.update_event(new_body)

        with allure.step(
                "Получение обновленной даты и времени начала события \
                из ответа сервера"
                ):
            startAt_event = resp.json()["data"]["startAt"]

        with allure.step("Фильтрация полезных данных из ответа сервера"):
            resp_data = resp.json()["data"]["payload"]["payload"]

        with allure.step("Проверка статус кода"):
            assert resp.status_code == 200

        with allure.step("Проверка соответствия обновленного цвета события"):
            assert resp_data["color"] == new_body["color"]

        with allure.step(
                "Проверка соответствия обновленного описания события"
                ):
            assert resp_data["description"] == new_body["description"]

        with allure.step(
                "Проверка соответствия обновленного \
                названия события"
                ):
            assert resp_data["title"] == new_body["title"]

        with allure.step("Удаление тестового события"):
            self.api.del_event(event_id, startAt_event)

    @allure.id("Skyeng-4")
    @allure.story("Создание событий")
    @allure.feature("CREATE")
    @allure.title("Совмещение личного события и урока преподавателя")
    @allure.description(
        "Данный тест проверяет возможность совмещения личного \
            события и урока в расписании преподавателя."
    )
    @pytest.mark.api_test
    def test_combine(self):
        with allure.step("Задать время и дату, начало урока и события"):
            startAt = "2024-09-10T12:00:00+07:00"

        with allure.step("Задать время и дату, окончание урока и события"):
            endAt = "2024-09-10T13:30:00+07:00"

        with allure.step("Создание списка данных по уроку"):
            body_class = {
                "educationServiceId": EDUCATION_ID,
                "type": "single",
                "startAt": startAt
            }
        with allure.step("Добавить новый урок"):
            resp_class = self.api.add_class(body_class)

        with allure.step("Получение id урока из ответа сервера"):
            body = resp_class.json()["data"]["class"]["payload"]
            class_id = body["virtualClassId"]

        with allure.step(
                "Получение даты и времени начала урока из ответа сервера"
                ):
            startAt_class = resp_class.json()["data"]["class"]["startAt"]

        with allure.step("Создание списка данных события"):
            body = {
                "backgroundColor": "#F4F5F6",
                "color": "#81888D",
                "description": "",
                "title": "Событие совм",
                "startAt": startAt,
                "endAt": endAt
            }

        with allure.step("Добавить новое событие"):
            resp_event = self.api.add_event(body)

        with allure.step("Получение id события из ответа сервера"):
            event_id = resp_event.json()["data"]["payload"]["id"]

        with allure.step(
                    "Получение даты и времени начала события \
                    из ответа сервера"
                ):
            startAt_event = resp_event.json()["data"]["startAt"]

        with allure.step("Удаление урока"):
            self.api.del_class(class_id)

        with allure.step("Удаление события"):
            self.api.del_event(event_id, startAt_event)

        with allure.step(
                "Преобразование даты и времени из ответов \
                сервера в объекты dateutil для сравнения"
                ):
            startAt_event = parser.parse(startAt_event)
            startAt_class = parser.parse(startAt_class)

        with allure.step("Проверка статус кода при создании урока"):
            assert resp_class.status_code == 200

        with allure.step("Проверка статус кода при создании личного события"):
            assert resp_event.status_code == 200

        with allure.step("Сравнение времени и даты урока и события"):
            assert startAt_class == startAt_event

    @allure.id("Skyeng-5")
    @allure.story("Удаление события")
    @allure.feature("DELETE")
    @allure.title("Удаление существующего личного события")
    @allure.description(
        "Данный тест проверяет возможность удаления личного \
        события в расписании преподавателя."
    )
    @pytest.mark.api_test
    def test_del_event(self):
        with allure.step("Создание списка данных события"):
            body = {
                "backgroundColor": "#F4F5F6",
                "color": "#81888D",
                "description": "",
                "title": "Событие такое",
                "startAt": "2024-07-20T09:30:00+07:00",
                "endAt": "2024-07-20T10:00:00+07:00"
            }
        with allure.step("Добавление события"):
            resp = self.api.add_event(body)

        with allure.step("Проверка статус кода"):
            assert resp.status_code == 200

        with allure.step("Получение id события из ответа сервера"):
            event_id = resp.json()["data"]["payload"]["id"]

        with allure.step(
            "Получение даты и времени начала события из ответа сервера"
        ):
            startAt_event = resp.json()["data"]["startAt"]

        with allure.step("Удаление события"):
            resp = self.api.del_event(event_id, startAt_event)

        with allure.step("Проверка статус кода на удаление события"):
            assert resp.status_code == 200
