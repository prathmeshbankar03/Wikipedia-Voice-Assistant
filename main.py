#Library for Path managing
import os

#PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap

#Google Images Web Scrapping Module
from pygoogle_image import image as pyimage

#Wikipedia Information API Module
import wikipedia

# Python NLP module used for text Processing (Used here for text summarisation)
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Python module for Text to Speech
import pyttsx3
#Text To speech Engine Set up
engine = pyttsx3.init('sapi5')
voice = engine.getProperty("voices")
engine.setProperty("voice", voice[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate',170)
#Text to speech function Created
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#Python Module for Speech Recognition
import speech_recognition as sr
#Creating a Recognizer for speech recognition
speechHandler = sr.Recognizer() 

#Loading the UI from Qt Designer
app = QtWidgets.QApplication([])
window = uic.loadUi("./app.ui")

# Text Summarisation function
def summarization(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence

    return summary


# After clicking the Listen Button This function will call
def listen():
    
    #setting the default mic as source and listening to the topic
    with sr.Microphone() as source:
        print("Listening...⏳")
        speechHandler.adjust_for_ambient_noise(source, duration=0.25)
        audio = speechHandler.listen(source)

        # If audio is not clear or user didnt say anything Except Clause will help here
        try:
            text = speechHandler.recognize_google(audio)
        except:
            speak("Couldn't understand what do you mean.")
            return None

    # Retrieving the information about the topic
    information = wikipedia.summary(text)

    #Web Scrapping the images related to that topic
    pyimage.download(text, limit=5)

    #Setting Up pathway to the images downloaded by Pyimage
    pathway = text.replace(" ", "_")
    pngpath = f"images/{pathway}/{text}_4.png"
    jpegpath = f"images/{pathway}/{text}_4.jpeg"

    if os.path.exists(pngpath):
        pixmap = QtGui.QPixmap(pngpath)
    else:
        pixmap = QtGui.QPixmap(jpegpath)

    # Resize the image
    pixmap_resized = pixmap.scaled(350, 250, QtCore.Qt.KeepAspectRatio)

    # Set the resized image as the background
    window.label_2.setPixmap(pixmap_resized)
    
    #Setting Up the title
    window.textEdit_2.setText(text)

    #setting up the summary of the Information
    window.textEdit.setText(summarization(information))

    # Text to Speech function to be called when speak button is pressed
    def texttospeech():
        speak("According to Wikipedia" + summarization(information))

    window.pushButton_2.clicked.connect(texttospeech)


speak("Hello, Welcome To Wikipedia Voice Assist, How May I Help You ?" )

window.pushButton.clicked.connect(listen)

window.show()
app.exec()