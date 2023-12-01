from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, current_user

import db

titles = ["Id", "Właściciel", "Data Zarejestrowania", "Kategoria", "Przewidywany Wpływ",
              "Prawdopodobieństwo Wystąpienia", "Kategoria Odpowiedzi", "Status", "Nr Kontaktowy", "Opis"]


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def loader_user(idn):
    return db.get_user(idn)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db.add_user(request.form.get("name")+" "+request.form.get("surname"), request.form.get("username"), request.form.get("password"))
        return redirect("login")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = db.get_user_login(request.form.get("username"))
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect("/")
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def main_page():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        risks = db.get_all_risks()
        return render_template('index.html', risks=risks, titles=titles)


@app.route('/home')
def home_page():
    risks = db.get_all_risks()
    return render_template('index.html', risks=risks, titles=titles)


@app.route('/moje')
def my_page():
    user = db.get_user(current_user.id)
    risks = db.get_risks_by_owner(user.name)
    return render_template('moje.html', name=user.name, titles=titles, risks=risks)


@app.route('/<int:idn>')
def risk_page(idn):
    risk_data = db.get_risk(idn)
    data = []
    for i in range(len(titles)):
        data.append([titles[i], risk_data[i]])

    return render_template("ryzyko.html", idn=idn, data=data)


if __name__ == '__main__':
    app.run()
