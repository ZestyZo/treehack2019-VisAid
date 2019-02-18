#this script uses the soundHound Houndify API and google Cloud Vision API to 
#   prove a conecpt to help visually impared poeple

import sys
import json
import cv2
import io
import os
from gtts import gTTS
from google.cloud import vision
from matplotlib import pyplot as plt
import houndify

CLIENT_ID = sys.argv[1]
CLIENT_KEY = sys.argv[2]
BUFFER_SIZE = 512

def takePhoto(): #uses mac camera to take a photo
    video_capture = cv2.VideoCapture(0)

    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    out = cv2.VideoWriter('output.jpg',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    while(video_capture.isOpened()):
        ret, frame = video_capture.read()
        if ret == True:
            out.write(frame)
            cv2.imshow('Frame', frame)
            break
            if cv2.waitKey(0):
                break
        else: 
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()


def faceDetection(path):  # uses google cloud vision api to detect number of faces in photo
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
        
    print(len(faces))
    if len(faces) ==1 :
        spokenText = "There is one person in the room"
    elif len(faces) == 0:
        spokenText = "There are no faces detected in the frame"
    else:
        spokenText = "There are" + str(len(faces)) + "people in the room"; 
    language = 'en'
    myobj = gTTS(text=spokenText, lang=language, slow=False)
    myobj.save("audio.mp3")
    os.system("afplay audio.mp3")
    os.remove("audio.mp3")

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if len(texts) != 0:
        spokenText = "It says" + str(texts[0].description)
        print('\n"{}"'.format(texts[0].description))
    else:
        spokenText= "No text detected"
    
    language = 'en'
    myobj = gTTS(text=spokenText, lang=language, slow=False)
    myobj.save("audio.mp3")
    os.system("afplay audio.mp3")
    os.remove("audio.mp3")




class MyListener(houndify.HoundListener):

  def onPartialTranscript(self, transcript):
    print("")
    #print "Partial transcript: " + transcript
  def onFinalResponse(self, response):

    audioMessage=str(response['AllResults'][0]['FormattedTranscription'])
    #print("Final response: " + audioMessage)
    roomList = ["many", "people", "faces", "person", "room"]
    readList = ["say", "sign", "read", "does this"]

    #print(audioMessage)
    if any(k in audioMessage.split(' ') for k in roomList): 
        faceDetection("./output.jpg") #finding how many people are in a photo
    elif any(j in audioMessage.split(' ') for j in readList):
        detect_text("./output.jpg") #finding what a sign says in a picture

    print("program done")

    # print "Final response: " + str(response['AllResults'][0]['FormattedTranscription'])
  def onError(self, err):
    print("Error: " + str(err))


client = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "test_user")
client.setLocation(37.388309, -121.973968)
takePhoto()
client.start(MyListener())

while True:
  samples = sys.stdin.buffer.read(BUFFER_SIZE)
  if len(samples) == 0: 
      break
  if client.fill(samples): 
      break
  
client.finish()
