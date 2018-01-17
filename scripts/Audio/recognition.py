import http.client
import json

apiKey = "528e03982d034cb184c0bc1d12c4d310"

RECOGNITION_MODE = "interactive"
LANGUAGE_TAG = "es-ES"
OUTPUT_FORMAT = "simple"

dir = "speech.platform.bing.com" 
dir2 = "/speech/recognition/" + RECOGNITION_MODE + "/cognitiveservices/v1?language=" + LANGUAGE_TAG + "&format=" + OUTPUT_FORMAT

headers = {"Ocp-Apim-Subscription-Key": apiKey,
        "Content-type": "audio/wav; codec=audio/pcm; samplerate=16000"}


fin = open("voz.wav", "rb")
data = fin.read()
#print(len(data))


conn = http.client.HTTPSConnection(dir)

conn.request("POST", dir2, headers = headers, body = data)

response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
print(json.loads(data.decode('utf-8')))