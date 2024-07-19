import requests

class ApiSchedule:

# Инициализация
    def __init__(self, url, token) -> None:
        self.url = url
        self.token = token
        self.headers = {}
        self.headers["Cookie"] = self.token
       

# Получение расписания преподавателя
    def get_events(self, start, end):
        body = {
            "from": start,
            "till": end
        }
        resp = requests.post(
            self.url + '/events', json=body, headers=self.headers
        )
        return resp

#  Создание личного события
    def add_event(self, description):
        resp = requests.post(
            self.url + '/createPersonal',
            json=description, headers=self.headers
        )
        return resp
    
# Изменение существующего события
    def update_event(self, description):
        resp = requests.post(
            self.url + '/updatePersonal',
            json=description, headers=self.headers
        )
        return resp
     
# Создание урока
    def add_class(self, description):
        resp = requests.post(
            self.url + '/createClass',
            json=description, headers=self.headers
        )
        return resp
    
# Удаление события
    def del_event(self, id, startAt):
        body = {
            "id": id,
            "startAt": startAt
        }
        resp = requests.post(
            self.url + '/removePersonal', json=body, headers=self.headers
        )
        return resp
    
# Удаление урока
    def del_class(
            self, class_id, initiator='teacher', reason=6, comment="null"
        ):
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
