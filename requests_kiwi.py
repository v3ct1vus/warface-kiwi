import requests

class RequestsKIWI(object):
    _headers_request = {
        'Accept': "application/json, text/plain, */*",
        'User-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        'Content-Type': "application/json;charset=utf-8",
        'Referer': "https://wf.mail.ru/kiwi",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cache-Control': "no-cache"
        }
    _session = []

    def __init__(self):
        return


    def auth(self, login, password):
        payload = {
            'Domain': 'mail.ru',
            'FakeAuthPage': 'https://wf.mail.ru/auth',
            'Login': login,
            'Page': '',
            'Password': password,
            'Saveauth': '1'
            }
        headers_auth = {
            'Origin': "https://wf.mail.ru",
            'Upgrade-insecure-requests': "1",
            'DNT': "1",
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Referer': "https://wf.mail.ru/kiwi",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cache-Control': "no-cache",
            }
        with requests.Session() as session:
            response = session.post("https://auth.mail.ru/cgi-bin/auth", data = payload, headers = headers_auth)
            self._session = session


    def getChainTasks(self, chain, callback):
        response = self._session.get("https://wf.mail.ru/minigames/bp4/info/tasks", headers = self._headers_request, params = {"chain": chain})
        return self.parser(response.json()['data']['tasks'], callback)


    def getTasks(self, callback):
        chains = ["icebreaker", "pripyat", "anubis", "volcano", "shark"]
        azbuga = []

        for chain in chains:
            chainTasks = self.getChainTasks(chain, callback)
            if chainTasks != None:
                azbuga.append(chainTasks)

        if len(azbuga) == 0: return None
        return azbuga


    def parser(self, tasks, callback):
        azbuga = []
        for taskgroup in tasks.values():
            for task in taskgroup.values():
                task_back = callback(task)
                if task_back != None:
                    azbuga.append(task_back)

        if len(azbuga) == 0: return None
        return azbuga


    def callback_activetask(self, task):
        if task['type'] == 'avatar':
            if task['status'] == 'progress':
                return task
        return None


    def callback_avatartask(self, task):
        if task['type'] == 'avatar':
            return task
        return None


    def taskStart(self, task_id, stars):
        payload = {
            'stars': stars,
            'task_id': task_id,
            }
        headers_task = {
            'accept': "application/json, text/plain, */*",
            'origin': "https://wf.mail.ru",
            'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'referer': "https://wf.mail.ru/kiwi",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            }
        response = self._session.post("https://wf.mail.ru/minigames/bp4/task/start-task", data = payload, headers = headers_task)

        return response.json()

    def taskDone():
        payload = {
            'is_paid': '0',
            'stars': stars,
            'task_id': task_id,
            }
        response = self._session.post("https://wf.mail.ru/minigames/bp4/task/done-task", data = payload, headers = self._headers_request)
        return response.json()
