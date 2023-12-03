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
        name = request.form.get("name")+" "+request.form.get("surname")
        db.add_user(name, request.form.get("username"), request.form.get("password"))
        return redirect("login")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = db.get_user_login(request.form.get("username"))
        if user:
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect("/")
            else:
                return redirect("/login")
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def main_page():
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        risks = db.get_all_risks()
        return render_template('index.html', risks=risks, titles=titles)


@app.route('/moje')
def my_page():
    user = db.get_user(current_user.id)
    risks = db.get_risks_by_owner(user.name)
    return render_template('mine.html', titles=titles, risks=risks)


@app.route('/<int:idn>', methods=["GET", "POST"])
def risk_page(idn):
    if request.form.get('remove_risk') == "yes":
        db.remove_risk(idn)
        return redirect("/moje")
    risk_data = db.get_risk(idn)
    data = []
    for i in range(len(titles)):
        try:
            data.append([titles[i], risk_data[i]])
        except IndexError:
            data.append([titles[i], ""])

    return render_template("risk.html", idn=idn, data=data)


@app.route('/nowe', methods=["GET", "POST"])
def new_risk():
    if request.method == "POST":
        db.add_risk(current_user.id, request.form.get('category'), request.form.get('impact'),
                    request.form.get('proximity'), request.form.get('response'), request.form.get('status'),
                    str(request.form.get('contact')), request.form.get('description'))
        return redirect("/moje")
    return render_template('new_risk.html')


if __name__ == '__main__':
    app.run()
