from flask import Flask, jsonify, request
import requests
from pydub import AudioSegment
import speech_recognition as sr
import io
import language_tool_python

app = Flask(__name__)

speech_recog = sr.Recognizer() # initialize speech recognition
grammar_check = language_tool_python.LanguageTool("en-US") # for grammar check and inserting correct punctuation
# AudioSegment.ffmpeg = "C:\Users\gurle\Downloads\ffmpeg-2024-11-06-git-4047b887fc-full_build\ffmpeg-2024-11-06-git-4047b887fc-full_build\bin\ffmpeg.exe"
#C:\Users\prana\Downloads\ffmpeg-2024-11-11-git-96d45c3b21-full_build\ffmpeg-2024-11-11-git-96d45c3b21-full_build\bin
# AudioSegment.ffmpeg = "C:\\Users\\prana\\Downloads\\ffmpeg-2024-11-11-git-96d45c3b21-full_build\\ffmpeg-2024-11-11-git-96d45c3b21-full_build\\bin\\ffmpeg.exe"

@app.route("/voice_to_text",methods=["POST"])
def voice_to_text():
    ab = request.data  # input audio data comes in the form of bytes from API; ab stands for audio bytes
    ab = request.files['file']
    if (ab):
        file = ab.read()

        audio_segment = AudioSegment.from_file(io.BytesIO(file)) # convert raw data to .wav format
        
        audio_segment.export("test.wav", format="wav")
        # break audio segment so that it's compatible with SpeechRecognition Software

        raw_audio_data = audio_segment.raw_data
        frame_rate = audio_segment.frame_rate
        sample_width = audio_segment.sample_width

        # combine to convert to speechrecognition audio data object to work with

        audio_for_text = sr.AudioData(raw_audio_data, frame_rate, sample_width)

        try:
            text_from_audio = speech_recog.recognize_google(audio_for_text)
            Accurate_text = grammar_check.correct(text_from_audio) # correct grammar

        except sr.UnknownValueError:
            Accurate_text = "Audio is not clear."

        return jsonify({"resp": Accurate_text}) # final output
    
    return jsonify({"error":"Input not received."})
    
if __name__ == "__main__":
    app.run(debug=True)
