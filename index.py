from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = "MyVerySecretKey123"

ENV = "dev"
createctr = 0


if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Alohamora@localhost/quizzard"
else:
    app.debug = False
    # Do app.config

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class questions(db.Model):
    __tablename__ = "questions"
    quizid = db.Column(db.Integer(), primary_key=True)
    questionid = db.Column(db.Integer(), unique=False)
    question = db.Column(db.String(200), unique=False)
    option1 = db.Column(db.String(200), unique=False)
    option2 = db.Column(db.String(200), unique=False)
    option3 = db.Column(db.String(200), unique=False)
    option4 = db.Column(db.String(200), unique=False)
    correct_option = db.Column(db.Integer(), unique=False)

    def __init__(self, quizid, questionid, question, option1, option2, option3, option4, correct_option):
        self.quizid = quizid
        self.questionid = questionid
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.correct_option = correct_option


class quizes(db.Model):
    __tablename__ = "quizes"
    quizid = db.Column(db.Integer(), primary_key=True, unique=True)
    maxquestionno = db.Column(db.Integer(), unique=False)

    def __init__(self, quizid, maxquestionno):
        self.quizid = quizid
        self.maxquestionno = maxquestionno


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/createquiz", methods=["POST", "GET"])
def createquiz():
    return render_template("createquiz.html")


@app.route("/playquiz", methods=["POST", "GET"])
def playquiz():
    return render_template("playquiz.html")


@app.route("/create", methods=["POST","GET"])
def create():
    # Database storing stuff
    if request.method == "POST":
        quizid = request.form.get("quizid")
        questionid = request.form.get("questionid")
        question = request.form.get("question")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        option1correct = request.form.get("option1correct")
        option2correct = request.form.get("option2correct")
        option3correct = request.form.get("option3correct")
        option4correct = request.form.get("option4correct")
        correct_option = ""
        if option1correct:
            correct_option = "1"
        elif option2correct:
            correct_option = "2"
        elif option3correct:
            correct_option = "3"
        elif option4correct:
            correct_option = "4"
        print(questionid)
        print(quizid)
        if quizid == None or quizid == "":
            maxquizid = db.session.query(db.func.max(questions.quizid)).first()
            print(maxquizid)
            print(maxquizid[0])
            if maxquizid[0] == None:
                quizid = 100000
            else:
                quizid = maxquizid[0] + 1
        if questionid == None or questionid == "":
            maxquesid = db.session.query(db.func.max(questions.questionid)).filter(questions.quizid == quizid).first()
            print(maxquesid[0])
            if maxquesid[0] == None:
                questionid = 1
            else:
                questionid = maxquesid[0] + 1
            print(questionid)
        else:
            intquestionid= int(questionid)
            intquestionid += 1
            questionid = str(intquestionid)
        if db.session.query(questions).filter(questions.quizid == quizid).count() == 0:
            data = questions(quizid, questionid, question, option1, option2, option3, option4, correct_option)
            db.session.add(data)
            db.session.commit()
       
    return render_template("createquiz.html", quizid = quizid, questionid = questionid)


app.route("/quizmade", methods=["POST", "GET"])
def quizmade():

    return render_template("quizmade.html", quizid=quizid)

if __name__ == "__main__":
    app.run()
