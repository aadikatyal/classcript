from flask import Flask, render_template, request, redirect, make_response
import speech_recognition as sr
from textblob import TextBlob
import textwrap
from flask_mail import Mail, Message

import smtplib

from os import path
from pydub import AudioSegment

import cv2
import numpy as np
import os

from PIL import Image
import pytesseract
import pandas as pd

from werkzeug.utils import secure_filename

from flask_mail import Mail, Message

from googletrans import Translator, constants
from pprint import pprint

from flask import (
    render_template,
    redirect, request,
    flash, session,
    jsonify, current_app, url_for
)

from utils.forms import (
    LoginForm, SignUpForm,
    AddNoteForm, EmailForm, AddNoteFormVideo
)
from core import core
from app import api
from flask_restful import reqparse, Resource
from utils.decorators import login_required
from flask import Markup
import utils.functions as functions
import markdown
import textwrap
parser = reqparse.RequestParser()
from fpdf import FPDF

app = Flask(__name__)
UPLOAD_FOLDER  = '/Users/aadikatyal/sound-class/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@core.route('/')
def home_page():
    session['user_count'] = functions.get_user_count()
    try:
        if session['username']:
            notes = functions.get_data_using_user_id(session['id'])
            return render_template('profile.html', username=session['username'], notes=notes)
        return render_template('homepage.html')
    except (KeyError, ValueError):
        return render_template('homepage.html')


@core.route('/profile/')
@login_required
def profile():
    if request.method == 'GET':
        notes = functions.get_data_using_user_id(session['id'])
        return render_template(
            'profile.html',
            username=session['username'],
            notes=notes
        )

@core.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        user_id = functions.check_user_exists(username, password)
        if user_id:
            session['username'] = username
            session['id'] = user_id
            functions.store_last_login(session['id'])
            return redirect('/profile/')
        else:
            flash('Username/Password Incorrect!')
    return render_template('login.html', form=form)


@core.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        email = request.form['email']
        check = functions.check_username(username)
        if check:
            flash('Username already taken!')
        else:
            functions.signup_user(username, password, email)
            session['username'] = username
            user_id = functions.check_user_exists(username, password)
            session['id'] = user_id
            return redirect('/profile/')
    return render_template('signup.html', form=form)


@core.route("/logout/")
def logout():
    session['username'] = None
    session['id'] = None
    return login()


@core.route("/email/send/<id>/", methods=["POST"])
def email(id):
    form = EmailForm()
    notes = functions.get_data_using_id(id)

    translation = ""
    email = ""

    if form.validate_on_submit():
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        email = request.form['email']
        translation = request.form['translation']
        server.login("aadikatyal21@gmail.com", "Google0621!!")
        message = 'Subject: {}\n\n{}'.format(f"New classcript message from {session['username']}!", translation)
        server.sendmail("aadikatyal21@gmail.com", email, message.encode("utf8"))
    return render_template("view_note.html", notes=notes, translation=translation, username=session['username'], form=form)

@core.route("/language/<id>/<lang>/")
def language(id, lang):
    notes = functions.get_data_using_id(id)
    form = EmailForm()

    transcript = ""
    
    for note in notes:
        transcript = note[5]

    translator = Translator()

    translation = translator.translate(transcript, dest=lang)

    language = ""

    if lang == 'en':
        language = "English"
    elif lang == 'es':
        language = "Spanish"
    elif lang == 'de':
        language = "German"
    elif lang == 'fr':
        language = "French"

    return render_template("view_note.html", translation=f"{language}: {translation.text}", notes=notes, username=session['username'], form=form)

@core.route("/notes/add/", methods=['GET', 'POST'])
@login_required
def add_note():
    form = AddNoteForm()

    if form.validate_on_submit():
        note_title = request.form['note_title']
        note_markdown = form.note.data
        note = Markup(markdown.markdown(note_markdown))
        
        transcript = ""

        file = request.files["file"]

        if file not in request.files:
            redirect(request.url)

        if file.filename == "":
            redirect(request.url)

        if file:
            if "mp3" in file.filename:
                src = file
                dst = "test.wav"

                sound = AudioSegment.from_mp3(src)
                sound.export(dst, format="wav")
                file = dst

            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)

            with audioFile as source:
                data = recognizer.record(source)

            transcript = recognizer.recognize_google(data, key=None)
        
        functions.add_note(note_title, note, transcript, session['id'])
        return redirect('/profile/')
    return render_template('add_note.html', form=form, username=session['username'])

@core.route("/notes/<id>/")
@login_required
def view_note(id):
    form = EmailForm()
    notes = functions.get_data_using_id(id)
    return render_template('view_note.html', notes=notes, username=session['username'], form=form)

@core.route("/notes/pdf/<id>/<translation>")
@login_required
def pdf(id, translation):
    pdf = FPDF()

    title = ""
    transcript = ""

    notes = functions.get_data_using_id(id)
    
    for note in notes:
        title = note[3]
        transcript = translation

    pdf.add_page()
    pdf.set_font("Times", size = 15)

    my_wrap = textwrap.TextWrapper(width = 40)
    wrap_list = my_wrap.wrap(text=transcript)

    text = ""

    for txt in wrap_list:
        text += txt + "\n"

    print(f"PIZZA: {text}")

    pdf.cell(200, 10, txt = title, ln = 1, align = 'C')
    pdf.cell(200, 10, txt = text, ln = 2, align = 'C')
    #pdf.multi_cell(float, float, txt = text, border = 0, align = 'C', fill = True)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={title}.pdf'
    return response


@core.route("/notes/edit/<note_id>/", methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    form = AddNoteForm()
    
    if request.method == 'GET':
        data = functions.get_data_using_id(note_id)
        form.note_id.data = note_id
        form.note_title.data = data[0][3]
        form.note.data = data[0][5]
        return render_template('edit_note.html', form=form, username=session['username'], id=note_id)
    elif form.validate_on_submit():
        note_id = form.note_id.data
        note_title = request.form['note_title']
        note_markdown = form.note.data

        note = Markup(markdown.markdown(note_markdown))
        functions.edit_note(note_title, note, note_markdown, note_id=note_id)
        return redirect('/profile/')

@core.route("/notes/delete/<id>/", methods=['GET', 'POST'])
@login_required
def delete_note(id):
    functions.delete_note_using_id(id)
    notes = functions.get_data_using_user_id(session['id'])
    return render_template('profile.html', delete=True, username=session['username'], notes=notes)

@core.route("/notes/add/video/", methods=['GET', 'POST'])
def video(save_rate=100, save_extension=".jpg"):
    form = AddNoteFormVideo()

    if form.validate_on_submit():
        note_title = request.form['note_title']
        note_markdown = form.note.data
        note = Markup(markdown.markdown(note_markdown))

        print("Hello")
        
        transcript = ""

        file = request.files["file"]

        if file not in request.files:
            redirect(request.url)

        if file.filename == "":
            redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(video_path)

        save_dir = os.path.splitext(video_path)[0] + "/"

        cap = cv2.VideoCapture(video_path)
        success, frame = cap.read()
        
        frames_counter = 0
        img_counter = 0
        
        while success:
            success, frame = cap.read()
            if success:
                frames_counter+=1
                if (frames_counter % save_rate != 0):
                    continue
                
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    
                img_path = save_dir + str(img_counter) + save_extension
                img_counter+=1
                
                cv2.imwrite(img_path, frame)
        cap.release()

        t = []
        for root, dirs, filenames in os.walk(save_dir):
            for filename in filenames:
                try:
                    img = Image.open(save_dir+ filename)
                    text = pytesseract.image_to_string(img, lang = 'eng')
                    t.append(text)
                except:
                    continue

        transcript = ""
        for text in t:
            transcript += text + "\n"

        functions.add_note(note_title, note, transcript, session['id'])
        return redirect('/profile/')
    return render_template('add_video.html', form=form, username=session['username'])

@core.route('/background_process/')
def background_process():
    try:
        notes = request.args.get('notes')
        if notes == '':
            return jsonify(result='')
        results = functions.get_search_data(str(notes), session['id'])
        temp = ''
        for result in results:
            temp += "<li><a href='/notes/" + str(result[0]) + "/'>" + f'{notes}' + "</a><br>"
        return jsonify(result=Markup(temp))
    except Exception as e:
        return str(e)

class GetDataUsingUserID(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            username = args['username']
            password = functions.generate_password_hash(args['password'])
            user_id = functions.check_user_exists(username, password)
            if user_id:
                functions.store_last_login(user_id)
                return functions.get_rest_data_using_user_id(user_id)
            else:
                return {'error': 'You cannot access this page, please check username and password'}
        except AttributeError:
            return {'error': 'Please specify username and password'}


api.add_resource(GetDataUsingUserID, '/api/')
parser.add_argument('username')
parser.add_argument('password')