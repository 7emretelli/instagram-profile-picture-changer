import os
import requests
import getpass
import json
import io
import time

enc = 'your enc_password'
X_SECOND = 30 ## Changing picture for per X seconds
BASE_URL = "https://www.instagram.com/"
LOGIN_URL = BASE_URL + "accounts/login/ajax/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; ) Gecko/20100101 Firefox/65.0"
CHANGE_URL = "https://www.instagram.com/accounts/web_change_profile_picture/"
CHNAGE_DATA = {"Content-Disposition": "form-data", "name": "profile_pic",
               "filename": "profilepic.jpg", "Content-Type": "image/jpeg"}
headers = {
    "Host": "www.instagram.com",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.instagram.com/accounts/edit/",
    "X-IG-App-ID": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Connection": "keep-alive",
}
session = requests.Session()
session.headers = {'user-agent': USER_AGENT, 'Referer': BASE_URL}


def login():
    USERNAME = str(input('Username > '))
    resp = session.get(BASE_URL)
    session.headers.update({'X-CSRFToken': resp.cookies['csrftoken']})
    login_data = {'username': USERNAME, 'enc_password': enc}
    login_resp = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
    if login_resp.json()['authenticated']:
        print("Login successful")
    else:
        print("Login failed!")
        login()
    # print(login.json())
    session.headers.update({'X-CSRFToken': login_resp.cookies['csrftoken']})


def save():
    with open('cookies.txt', 'w+') as f:
        json.dump(session.cookies.get_dict(), f)
    with open('headers.txt', 'w+') as f:
        json.dump(session.headers, f)


def load():
    with open('cookies.txt', 'r') as f:
        session.cookies.update(json.load(f))
    with open('headers.txt', 'r') as f:
        session.headers = json.load(f)


def change():
    session.headers.update(headers)
    try:
        print("wow"+str(i))
        with open("./data/yourimagename"+str(i)+".png", "rb") as resp: ##change here
            f = resp.read()
        p_pic = bytes(f)
        p_pic_s = len(f)
        session.headers.update({'Content-Length': str(p_pic_s)})
        files = {'profile_pic': p_pic}
        r = session.post(CHANGE_URL, files=files, data=CHNAGE_DATA)
        if r.json()['changed_profile']:
            print("Profile picture changed!")
        else:
            print("Something went wrong")
        time.sleep(X_SECOND)
    except Exception as e:
        print(e)
        pass
        time.sleep(10)


if __name__ == "__main__":
    i = 0
    try:
        load()
    except:
        login()
        save()
    while True:
        if i == 12: ## How many pictures you have in Data folder
            i = 0
        i += 1
        change()
