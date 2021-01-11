from flask import send_from_directory,Flask,make_response,jsonify,Response,render_template,request
import os

import librosa
import numpy as np
import uuid

TMP_FOLDER = "static/temp/"

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.secret_key='secretkey'

@app.route('/')
def home():
	return render_template('home.html')

def get_timestamp_str(raw_seconds):
	# Prepare time stamp for vtt standard

	raw_seconds = round(raw_seconds, 3)
	seconds = raw_seconds%60
	minutes=(raw_seconds/60)%60
	minutes = int(minutes)
	hours = (raw_seconds/(60*60))%24
	hours = int(hours)

	return f'{hours:02d}:{minutes:02d}:{seconds:0>6.3f}'


@app.route('/process-notes',methods=["POST"])
def process_notes():
	
	# inputs
	raw_music_file = request.files['file']

	# signal processing
	y, sr = librosa.load( raw_music_file )
	music_duration = librosa.get_duration(y=y, sr=sr)


	f0, voiced_flag, voiced_probs = librosa.pyin(
										y, sr=sr, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7')
									)
	# To remove "nan" from `f0`
	f0[ voiced_flag==False ] = 1.0
	music_notes = np.asarray( librosa.hz_to_note(f0) )
	# Add dashes for no note detection
	music_notes[ voiced_flag==False ] = "--"
	music_notes = music_notes.tolist()

	# Writing VTT file
	time_gap = music_duration/len(music_notes)
	start_time = 0

	vtt_filename = f'{TMP_FOLDER}{uuid.uuid4().hex}.vtt'
	with open(vtt_filename,'w+',encoding='utf8') as file:
		
		# Add this tag at beginning
		file.write("WEBVTT")
		for note in music_notes:
			end_time = start_time+time_gap

			start_timestr = get_timestamp_str( start_time )
			end_timestr = get_timestamp_str( end_time )
			time_caption = f'\n\n{start_timestr} --> {end_timestr}\n{note}'
			file.write(time_caption)

			start_time = end_time

	return jsonify({
		'notesCaptionFile': vtt_filename
		})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)