import requests
from bs4 import BeautifulSoup

class AntronioSession:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = self.login()

    def login(self):
        url_login = "https://www.antronio.cl/login/login"
        session = requests.Session()

        response = session.get(url_login)
        cookies = response.cookies
        login_page = response.text
        login_csrf_token = self.extract_csrf_token(login_page)

        login_data = {
            "login": self.username,
            "password": self.password,
            "_xfToken": login_csrf_token,
            "cookie_check": "1",
            "register": "0"
        }

        response = session.post(url_login, data=login_data, cookies=cookies)

        if response.url != url_login:
            print("Inicio de sesión exitoso")
            return session
        else:
            print("Inicio de sesión fallido")
            return None

    def extract_csrf_token(self, html):
        soup = BeautifulSoup(html, "html.parser")
        csrf_token = soup.find("input", {"name": "_xfToken"})["value"]
        return csrf_token

    def post_on_profile(self, message):
        url_profile = "https://www.antronio.cl/members/el-antro-ai.585142/"
        csrf_token = self.extract_csrf_token(self.session.get(url_profile).text)

        post_data = {
            "_xfToken": csrf_token,
            "message_html": f"<p>{message}</p>",
            "last_date": "",
            "last_known_date": "",
            "load_extra": "1",
            "_xfRequestUri": url_profile,
            "_xfWithData": "1",
            "_xfResponseType": "json"
        }

        response = self.session.post(url_profile + "post", data=post_data)

        return response

