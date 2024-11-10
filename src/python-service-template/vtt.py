from flask import Flask, jsonify, requests
from pydub import AudioSegment
import SpeechRecognition as sr
import io

app = Flask(__name__)

@app.route("/voice_to_text",methods=["POST"])

def voice_to_text():
    ab = request.data  # input audio data comes in the form of bytes from API; ab stands for audio bytes
    if (ab):
        audio_segment = AudioSegment.from_file(io.BytesIO(ab), format = "wav") # convert raw data to .wav format
        
        # break audio segment so that it's compatible with SpeechRecognition Software

        raw_audio_data = audio_segment.raw_data
        frame_rate = audio_segment.frame_rate
        sample_width = audio_segment.sample_width

        # combine to convert to speechrecognition audio data object to work with

        audio_for_text = sr.AudioData(raw_audio_data, frame_rate, sample_width)

        try:
            text_from_audio = recognizer.recognize_google(audio_for_text)
        except sr.UnknownValueError:
            text_from_audio = "Audio is not clear."

        return jsonify({"resp":text_from_audio})
    return jsonify({"error":"Input not received."})
    

        


    





