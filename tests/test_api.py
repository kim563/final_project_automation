from pages.api_class import ApiSchedule
from dateutil import parser
from config.config import URL_API, TOKEN, EDUCATION_ID

api = ApiSchedule(URL_API, TOKEN)

# Тест на получение расписания
def test_get_events():
    resp = api.get_events(
        "2024-07-15T00:00:00+07:00", "2024-07-15T23:59:59+07:00"
    )
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json"

# Создание личного события
def test_add_event():
    body = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "",
        "title": "Событие такое",
        "startAt": "2024-07-15T09:30:00+07:00",
        "endAt": "2024-07-15T10:00:00+07:00"
    }
    resp = api.add_event(body)
    resp_data = resp.json()["data"]["payload"]["payload"]

    assert resp.status_code == 200
    assert resp_data["backgroundColor"] == body["backgroundColor"]
    assert resp_data["color"] == body["color"]
    assert resp_data["description"] == body["description"]
    assert resp_data["title"] == body["title"]

# Изменение существующего события
def test_update_event():
    body = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "",
        "title": "Событие такое",
        "startAt": "2024-07-16T09:30:00+07:00",
        "endAt": "2024-07-16T10:00:00+07:00"
    }
    resp = api.add_event(body)
    event_id = resp.json()['data']["payload"]["id"]
    old_start = resp.json()['data']['startAt']
    
    new_body = {
        "backgroundColor": "#F4F5F6",
        "color": "#43B658",
        "description":"Изменения в описании",
        "title": "Тестовое событие",
        "startAt": "2024-07-15T09:30:00+07:00",
        "endAt": "2024-07-15T10:00:00+07:00",
        "id": event_id,
        "oldStartAt": old_start
    }

    resp = api.update_event(new_body)
    startAt_event = resp.json()["data"]["startAt"]

    resp_data = resp.json()["data"]["payload"]["payload"]


    assert resp.status_code == 200
    assert resp_data["color"] == new_body["color"]
    assert resp_data["description"] == new_body["description"]
    assert resp_data["title"] == new_body["title"]

    api.del_event(event_id, startAt_event)

 # Совмещение личного события и урока
def test_combine():
    startAt = "2024-09-10T12:00:00+07:00"
    endAt = "2024-09-10T13:30:00+07:00"
    body_class = {
        "educationServiceId": EDUCATION_ID,
        "type": "single",
        "startAt": startAt
    }
    resp_class = api.add_class(body_class)

    class_id = resp_class.json()["data"]["class"]["payload"]["virtualClassId"]
    startAt_class = resp_class.json()["data"]["class"]["startAt"]

    body = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "",
        "title": "Событие совм",
        "startAt": startAt,
        "endAt": endAt
    }
    resp_event = api.add_event(body)

    event_id = resp_event.json()["data"]["payload"]["id"]
    startAt_event = resp_event.json()["data"]["startAt"]
   
    api.del_class(class_id)
    api.del_event(event_id, startAt_event)

    startAt_event = parser.parse(startAt_event)
    startAt_class = parser.parse(startAt_class)

    assert resp_class.status_code == 200
    assert resp_event.status_code == 200
    assert startAt_class == startAt_event

# Удаление существующего личного события
def test_del_event():
    body = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "",
        "title": "Событие такое",
        "startAt": "2024-07-20T09:30:00+07:00",
        "endAt": "2024-07-20T10:00:00+07:00"
    }
    resp = api.add_event(body)
    assert resp.status_code == 200

    event_id = resp.json()["data"]["payload"]["id"]
    startAt_event = resp.json()["data"]["startAt"]

    resp = api.del_event(event_id, startAt_event)
    assert resp.status_code == 200
