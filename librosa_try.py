# import librosa
# import numpy as np

# y, sr = librosa.load('piano_sample.wav')
# print(y)
# f0,b,a = librosa.pyin( y, sr=sr, frame_length=4096, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
# print( len(f0) )
# f0[np.isnan(f0)] = 1.0
# notes = librosa.hz_to_note(f0)
# print( notes )

raw_seconds=input("Enter time in milliseconds ")
raw_seconds = round( float(raw_seconds), 3)
seconds = raw_seconds%60
minutes=(raw_seconds/60)%60
minutes = int(minutes)
hours = (raw_seconds/(60*60))%24
hours = int(hours)

print('Num: {:0.1f}'.format(raw_seconds))
