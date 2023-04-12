import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import pickle



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
    
    
    
    def get_forum_threads(self, forum_url):
        response = self.session.get(forum_url)
        soup = BeautifulSoup(response.text, "html.parser")
        threads = soup.find_all("div", {"class": "structItem-title"})
        return [thread.find("a").text for thread in threads]
    
    
    def check_for_new_threads(self, forum_url):
        response = self.session.get(forum_url)
        soup = BeautifulSoup(response.text, "html.parser")
        threads = soup.find_all("div", {"class": "structItem-title"})
        current_titles = [thread.find("a").text for thread in threads]

        conn = sqlite3.connect("threads.db")
        cursor = conn.cursor()
        self.create_threads_table(cursor)

        old_titles = self.get_thread_titles(cursor)

        new_titles = set(current_titles) - set(old_titles)

        if new_titles:
            for title in new_titles:
                self.insert_thread(cursor, title)
            conn.commit()
            print("Nuevos temas:")
            print(new_titles)
        else:
            print("No hay nuevos temas")
        conn.close()

    def create_threads_table(self, cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS threads (title TEXT PRIMARY KEY)")

    def insert_thread(self, cursor, title):
        cursor.execute("INSERT INTO threads (title) VALUES (?)", (title,))

    def get_thread_titles(self, cursor):
        cursor.execute("SELECT title FROM threads")
        return [row[0] for row in cursor.fetchall()]
