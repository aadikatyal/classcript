# classcript

## Inspiration

Many of my peers complained of having trouble taking efficient notes and retaining information during online classes in the past year during the COVID-19 pandemic, especially during long lectures. I decided to tackle this problem by developing a digital solution.

## What it does

classcript is an in-person/virtual classroom tool that accepts audio files and transcribes them to text. classcript also accepts video files, converts them to individual images, and extracts text from them. Users can save these transcriptions to their library and edit them. Students can easily search through their audio and video lectures, as they have been converted to searchable transcriptions.

Students can also download any of their library transcriptions as PDFs, providing them with printable notes ready for next class! classcript can also convert lecture notes to different languages - perfect for foreign students struggling with English. Finally, students can share their lecture notes with other classmates via email.

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
