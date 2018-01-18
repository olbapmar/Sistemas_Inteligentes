import http.client
import json
import os

class Reconocimiento:
        apiKey = "528e03982d034cb184c0bc1d12c4d310"

        RECOGNITION_MODE = "interactive"
        LANGUAGE_TAG = "es-ES"
        OUTPUT_FORMAT = "simple"

        dir = "speech.platform.bing.com" 
        dir2 = "/speech/recognition/" + RECOGNITION_MODE + "/cognitiveservices/v1?language=" + LANGUAGE_TAG + "&format=" + OUTPUT_FORMAT

        headers = {"Ocp-Apim-Subscription-Key": apiKey,
                "Content-type": "audio/wav; codec=audio/pcm; samplerate=16000"}


        def llamar_api(self, filename):
                fin = open(filename, "rb")
                data = fin.read()

                conn = http.client.HTTPSConnection(Reconocimiento.dir)

                conn.request("POST", Reconocimiento.dir2, headers=Reconocimiento.headers, body=data)

                response = conn.getresponse()
                print(response.status, response.reason)

                data = response.read()
                json_data = json.loads(data.decode('utf-8'))
                fin.close()
                os.remove(filename)
                try:
                        texto = json_data['DisplayText']
                        print(texto)
                        return texto
                except KeyError:
                        return None

                

