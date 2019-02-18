###### treehack2019-VisAid
A tool that allows users to better understand their surroundings using image processing and speech recognition. Utilizing both Google Cloud Vision API and Houndify's Speech-To-Text API, VisAids lets users ask it questions about their environment and will respond with an answer. It does this by leveraging OpenCV to capture images and by using Text-To-Speech to respond to user queries.

#### Make sure you install the following SDKs and packages before running:
    sox
    json
    io
    sys
    os
    gTTS
    OpenCV
    matplotlib
    Houndify Python SDK
    Google Cloud Vision API

#### Authenticate with Google Cloud API prior to running code:
Run this line in terminal: export GOOGLE_APPLICATION_CREDENTIALS=“/home/user/Downloads/[FILE_NAME].json”

#### Run your program with this line of code:
rec -p | sox - -c 1 -r 16000 -t s16 -L - | ./main.py CLIENT ID CLIENT KEY

Replace CLIENT ID and CLIENT KEY with your unique keys on your Houndify Dashboard

This project was built by Lorenzo Melendez, Amanda Huang, Sean Pine, and Shikhar Bakhda
