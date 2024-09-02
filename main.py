from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

admin_password = "liquid"

def load_user_data():
    try:
        with open('user_data.txt', 'r', encoding='euc-kr') as f:
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
    with open('user_data.txt', 'w', encoding='euc-kr') as f:
        for name, username in zip(names, usernames):
            f.write(f"{name},{username}\n")

def get_tier_name(tier):
    tiers = ["Unranked", "Bronze V", "Bronze IV", "Bronze III", "Bronze II", "Bronze I",
             "Silver V", "Silver IV", "Silver III", "Silver II", "Silver I",
             "Gold V", "Gold IV", "Gold III", "Gold II", "Gold I",
             "Platinum V", "Platinum IV", "Platinum III", "Platinum II", "Platinum I",
             "Diamond V", "Diamond IV", "Diamond III", "Diamond II", "Diamond I",
             "Ruby V", "Ruby IV", "Ruby III", "Ruby II", "Ruby I", "Master"]
    return tiers[tier]

def get_user_data(names, usernames):
    data = []
    for i in range(len(names)):
        try:
            url = f"https://solved.ac/api/v3/user/show?handle={usernames[i]}"
            res = requests.get(url)
            res.raise_for_status()
            user_info = res.json()
            tier = get_tier_name(user_info['tier'])
            ac_rating = user_info['rating']
            solved_count = user_info['solvedCount']
            data.append((names[i], usernames[i], tier, ac_rating, solved_count))
        except Exception as e:
            data.append((names[i], usernames[i], "Unranked", 0, 0))
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
    app.run(debug=True, port=80, host="0.0.0.0")
