from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

admin_password = "0209"

def load_user_data():
    try:
        with open('user_data.txt', 'r') as f:
            lines = f.readlines()
            names = []
            usernames = []
            for line in lines:
                name, username = line.strip().split(',')
                names.append(name)
                usernames.append(username)
            return names, usernames
    except FileNotFoundError:
        return [], []

def save_user_data(names, usernames):
    with open('user_data.txt', 'w') as f:
        for name, username in zip(names, usernames):
            f.write(f"{name},{username}\n")

def get_user_data(names, usernames):
    data = []
    for i in range(len(names)):
        try:
            url = f"https://solved.ac/profile/{usernames[i]}"
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml")
            userInfo = soup.find('a', attrs={"class": "css-1ipvd2a"})
            scoreSection = soup.find('div', attrs={"class": "css-1midmz7"})
            tier = scoreSection.find('span').get_text()
            ac_rating = int(scoreSection.find('b').find('span').get_text().replace(',', ''))  # 정수로 변환 및 쉼표 제거
            solved_count = int(userInfo.find('b').get_text().replace(',', ''))  # 정수로 변환 및 쉼표 제거
            data.append((names[i], usernames[i], tier, ac_rating, solved_count))
        except Exception as e:
            data.append((names[i], usernames[i], "Tier", 0, 0))
    data.sort(key=lambda x: x[3], reverse=True)
    return data

@app.route('/')
def home():
    names, usernames = load_user_data()
    data = get_user_data(names, usernames)
    return render_template('index.html', data=data)

@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin', methods=['POST'])
def admin():
    password = request.form['password']
    if password == admin_password:
        names, usernames = load_user_data()
        data = get_user_data(names, usernames)
        return render_template('admin.html', data=data)
    else:
        return "비밀번호가 잘못되었습니다.", 403

@app.route('/admin/update', methods=['POST'])
def admin_update():
    names = request.form.getlist('names')
    usernames = request.form.getlist('usernames')
    save_user_data(names, usernames)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
