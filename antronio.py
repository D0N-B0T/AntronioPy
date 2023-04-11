# antronio_session.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Sesion:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.logged_in = self.login(username, password)

    def extract_csrf_token(self, html):
        soup = BeautifulSoup(html, "html.parser")
        csrf_token = soup.find("input", {"name": "_xfToken"})["value"]
        return csrf_token

    def login(self, username, password):
        url_login = "https://www.antronio.cl/login/login"
        response = self.session.get(url_login)
        cookies = response.cookies
        login_page = response.text
        login_csrf_token = self.extract_csrf_token(login_page)
        login_data = {
            "login": username,
            "password": password,
            "_xfToken": login_csrf_token, 
            "cookie_check": "1",
            "register": "0"
        }
        response = self.session.post(url_login, data=login_data, cookies=cookies)
        return response.url != url_login


    def get_thread_images(self, thread_url):
            response = self.session.get(thread_url)
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.find_all("div", {"class": "message"})
            images = []
            emoji_url_base = "https://www.antronio.cl/styles/elantro/"

            for post in posts:
                    post_content = post.find("div", {"class": "message-content"})
                    if post_content:  # Asegúrate de que post_content no sea None
                        for img in post_content.find_all("img"):
                            if img.has_attr("src"):
                                image_url = urljoin(thread_url, img["src"])
                                if not image_url.startswith(emoji_url_base):
                                    username = post.find("a", {"class": "username"}).text.strip()
                                    message_id = post["id"]
                                    message_link = f"{thread_url}#{message_id}"
                                    images.append({"url": image_url, "user": username, "link": message_link})

            return images
