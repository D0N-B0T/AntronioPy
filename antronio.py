import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import pickle



class AntronioSession:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies_file = "cookies.pkl"
        self.session = self.login()
        
        
    def login(self):
        url_login = "https://www.antronio.cl/login/login"
        session = requests.Session()
        
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, "rb") as f:
                cookies = pickle.load(f)
                session.cookies.update(cookies)
                
                if not self.is_session_valid(session):
                    print("La sesión ha expirado. Por favor, vuelva a iniciar sesión.")
                    os.remove(self.cookies_file)
                    return None
        else:
            response = session.get(url_login)
            login_csrf_token = self.extract_csrf_token(response.text)

            login_data = {
                "login": self.username,
                "password": self.password,
                "_xfToken": login_csrf_token,
                "cookie_check": "1",
                "register": "0"
            }

            response = session.post(url_login, data=login_data)

            if response.url == url_login:
                    print("Inicio de sesión fallido")
                    return None

            with open(self.cookies_file, "wb") as f:
                pickle.dump(session.cookies, f)

        print("Inicio de sesión exitoso")
        return session
    
    def is_session_valid(self, session):
        response = session.get("https://www.antronio.cl/")
        if response.status_code in (401, 403):
            return False
        return True
    

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
    
    
    
    def check_for_new_threads(self, forum_url):
       if not self.is_session_valid(self.session):
            print("La sesión ha expirado. Por favor, vuelva a iniciar sesión.")
            os.remove(self.cookies_file)
            return
        
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
