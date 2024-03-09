classcript is a digital tool designed to enhance students' note-taking by transcribing audio and video lectures into editable and searchable text, facilitating easier review and study. It features functionalities such as PDF exports, language translation for foreign students, and the ability to share notes via email

## Dependencies Utilized:
- Python (Flask)
- SQLAlchemy
- Google Web Speech API
- OpenCV API
- NumPy
- Google Translate API
- FFmpeg (multimedia framework)
- smtplib
- BeautifulSoup parser

## How to install on your server

* You can download the zip or clone the project with git.

    `https://github.com/aadikatyal/classcript.git`

* Install `requirement.txt` via terminal:

    `pip install -r /path/to/requirements.txt`

## Running the site

* To enable all development features (including debug mode) you can export the FLASK_ENV environment variable and set it to development before running the server:

    `export FLASK_ENV=development`

* To run the application you can use the **flask** command or python’s -m switch with Flask. Before you can do that you need to tell your terminal the application to work with by exporting the **FLASK_APP** environment variable:

    `export FLASK_APP=application.py`

* To test the web app, execute

    ``` Shell
    $ flask run
        * Running on http://127.0.0.1:5000/
    ```

* Alternatively you can use python -m flask:
    ``` Shell
    $ python -m flask run
        * Running on http://127.0.0.1:5000/
    ```

## Requirements

* Python
* Flask
