# classcript

## Inspiration

Many of my peers complained of having trouble taking efficient notes and retaining information during online classes in the past year during the COVID-19 pandemic, especially during long lectures. I decided to tackle this problem by developing a digital solution.

## What it does

classcript is an in-person/virtual classroom tool that accepts audio files and transcribes them to text. classcript also accepts video files, converts them to individual images, and extracts text from them. Users can save these transcriptions to their library and edit them. Students can easily search through their audio and video lectures, as they have been converted to searchable transcriptions.

Students can also download any of their library transcriptions as PDFs, providing them with printable notes ready for next class! classcript can also convert lecture notes to different languages - perfect for foreign students struggling with English. Finally, students can share their lecture notes with other classmates via email.

## Dependencies Utilized:
- Python
- Flask
- SQLAlchemy
- Google Web Speech API
- OpenCV API
- NumPy
- Google Translate API
- FFmpeg multimedia framework
- smtplib (email)
- BeautifulSoup parser
- HTML, CSS/Bootstrap
- JavaScript

## Challenges we ran into
- Long download times for command-line tools, including FFmpeg to convert audio files to .wav formats.
- Using the starttls email protocol command in SMTP to create secure connection

## Accomplishments that we're proud of
- Allowing users to upload all types of audio formats, as the API only allows .wav files
- Ability to capture multiple frames from uploaded video and convert each frame to an image (OpenCV)
- Making transcripts available in multiple languages

What we learned

- Learned various concepts of the HTTP protocol:
-- Allowable methods (GET & POST) and how to configure them in Flask
- How to code multipart form uploads for audio and video files

## What's next for classcript
- Automatically tag lectures with the subject (identify based on transcript)
- Implement a full-text indexing to search through all transcripts
