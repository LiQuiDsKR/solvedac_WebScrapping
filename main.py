from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    names = ["이재형", "정은수", "강민성", "심준현", "이한승", "김용성"]
    usernames = ["littleplayer", "celcy0318", "helpgms", "simjunhyun", "rvsg94486", "yongseongg00"]
    data = []
    for i in range(len(names)):
        url = f"https://solved.ac/profile/{usernames[i]}"
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        userInfo = soup.find('a', attrs={"class": "css-1ipvd2a"})
        scoreSection = soup.find('div', attrs={"class": "css-1midmz7"})
        tier = scoreSection.find('span').get_text()
        ac_rating = scoreSection.find('b').find('span').get_text()
        solved_count = userInfo.find('b').get_text()
        #streak = streakInfo.find('div', attrs={"class": "css-1midmz7"}).find('b').get_text()
        data.append((names[i], usernames[i], tier, ac_rating, solved_count))
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
