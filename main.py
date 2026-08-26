from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/recepcao")
def recepcao():
    return render_template("dashboard_recepcao.html")


@app.route("/administracao")
def administracao():
    return render_template("dashboard_admin.html")


if __name__ == "__main__":
    app.run(debug=True)