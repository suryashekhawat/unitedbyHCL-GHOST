import pyaudio
import wave
import json
import random
from watson_developer_cloud import ConversationV1
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import SpeechToTextV1
import watson_developer_cloud
from os.path import join, dirname
import sounddevice as sd
import scipy.io.wavfile as wav


conversation = ConversationV1(
    username='bf88d713-573e-4fdf-b540-ecebf711c6b7',
    password='yxuWVHVPrP5v',
    version='2017-04-21')
workspace_id = '68e5659a-6135-4a80-962b-53e924eb4a66'





text_to_speech = TextToSpeechV1(
    username='5e0974fc-ad30-4920-aaa8-0e58c88360e5',
    password='euCZrCqMHBGI',
    x_watson_learning_opt_out=True)  # Optional flag

#print(json.dumps(text_to_speech.voices(), indent=2))



speech_to_text = SpeechToTextV1(
    username='a11ce326-bb7f-49b3-82ff-4deb9446fa81',
    password='WqhlKVSHBf28',
    x_watson_learning_opt_out=False
)
print(json.dumps(speech_to_text.models(), indent=2))

print(json.dumps(speech_to_text.get_model('en-US_BroadbandModel'), indent=2))

discovery = watson_developer_cloud.DiscoveryV1(
    '2016-11-07',
    username='bd1143e9-4e6a-46c1-b4de-9a0fd149fc6f',
    password='jk7QURk8o7sm')

environments = discovery.get_environments()
print(json.dumps(environments, indent=2))
ghost_environments = [x for x in environments['environments'] if
                     x['name'] == 'byod']
ghost_environment_id = ghost_environments[0]['environment_id']
print(json.dumps(ghost_environment_id, indent=2))

collections = discovery.list_collections(ghost_environment_id)
ghost_collections = [x for x in collections['collections']]
print(json.dumps(collections, indent=2))

configurations = discovery.list_configurations(
    environment_id=ghost_environment_id)
print(json.dumps(configurations, indent=2))


#fs=44100
#duration = 5  # seconds
#myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
#print "Recording Audio"
#sd.wait()
#print "Audio recording complete , Play Audio"
#sd.play(myrecording, fs)
#sd.wait()
#print "Play Audio Complete"

#print(json.dumps(speech_to_text.recognize(
#        myrecording, content_type='audio/wav', timestamps=True,
#        word_confidence=True),
#        indent=2))

def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 6
    WAVE_OUTPUT_FILENAME = "record.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def storetxt(content):
    txtfilename = 'playerdoc\\'+str(random.randint(1,10000)*5) + content[:5] + '.html'
    text_file = open(txtfilename, "w")
    text_file.write('<!DOCTYPE html><html><head><title>'+txtfilename+'</title></head><body><p>'+content+'<p></body></html>')
    text_file.close()
    
print 'say something'
while True: 
#    record()
    txt_input = raw_input() 
    storetxt(txt_input)    
    query_options = {'query': txt_input}
    query_results = discovery.query(ghost_environment_id,
                                ghost_collections[0]['collection_id'],
                                query_options)
    print(json.dumps(query_results, indent=2))
    response = conversation.message(workspace_id=workspace_id, message_input={'text': txt_input})
#    print(json.dumps(response, indent=2))
    print 'Ghost :' + response["output"]["text"][0]






























#record()

#storetxt('you are doing good surya keep it up')













    



