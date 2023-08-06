import speech_recognition as sr
import moviepy.editor as mp
import os


# Function to convert
# Pass in the path to the file
def extracte(file_name):                     
    r=sr.Recognizer()
    clip=mp.VideoFileClip(file_name)
    conv_file="audio"
    clip.audio.write_audiofile("audio.wav")
    with sr.AudioFile("audio.wav") as file:
        audio_data=r.record(file)
        text=r.recognize_google(audio_data)
        return text
    

def extracter(file_name):
    answer=extracte(file_name)
    os.remove("audio.wav")
    return answer
