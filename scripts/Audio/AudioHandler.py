import pyaudio
import wave
import audioop
from collections import deque
import os
import time
import math
from Reconocimiento import Reconocimiento
from twitter import Twitter
from tiempo import Tiempo_api
from Sintetizador import Sintetizador


class AudioHandler:
    CHUNK = 1024  
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    THRESHOLD = 2300 

    SILENCE_LIMIT = 1

    PREV_AUDIO = 0.5 

    def __init__(self):
        return 


    def audio_int(self, num_samples=50):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the 20% largest intensities recorded.
        """

        p = pyaudio.PyAudio()

        stream = p.open(format=AudioHandler.FORMAT,
                        channels=AudioHandler.CHANNELS,
                        rate=AudioHandler.RATE,
                        input=True,
                        frames_per_buffer=AudioHandler.CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(AudioHandler.CHUNK), 4))) 
                for x in range(num_samples)] 
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        stream.close()
        p.terminate()
        return r


    def listen_for_speech(self, threshold=THRESHOLD):
        """
        Escucha del micrófono hasta que detecta un sonido, para de grabar cuando se deja de hablar
        """

        p = pyaudio.PyAudio()

        stream = p.open(format=AudioHandler.FORMAT,
                        channels=AudioHandler.CHANNELS,
                        rate=AudioHandler.RATE,
                        input=True,
                        frames_per_buffer=AudioHandler.CHUNK)

        print("Escuchando micrófono")
        audio2send = []
        cur_data = ''  
        rel = AudioHandler.RATE/AudioHandler.CHUNK
        slid_win = deque(maxlen=int(AudioHandler.SILENCE_LIMIT * rel))
        prev_audio = deque(maxlen=int(AudioHandler.PREV_AUDIO * rel))
        started = False
        response = []
        n = 1

        while (n > 0):
            cur_data = stream.read(AudioHandler.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            if(sum([x > AudioHandler.THRESHOLD for x in slid_win]) > 0):
                if(not started):
                    print("Iniciada grabación")
                    started = True
                audio2send.append(cur_data)
            elif (started is True):
                print("Fin de grabación")
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                
                stream.close()
                p.terminate()
                return filename
            else:
                prev_audio.append(cur_data)

    def save_speech(self, data, p):
        """ Guarda los datos en un archivo wav temporal """

        filename = 'output_'+str(int(time.time()))
        data = b''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)  
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    def process_input(self, filename):
        texto = Reconocimiento().llamar_api(filename)
        exito = False
        if(texto is not None):
            if(texto.startswith("Nuevo tweet")):
                texto = texto.replace('Nuevo tweet', '', 1)
                exito = Twitter().enviar_tweet(texto = texto.strip().capitalize())
                if exito:
                    self.play_wav('scripts/Audio/offline/Tweet', False)
            elif(texto.startswith("Dime el tiempo en")):
                texto = Tiempo_api().textoClima(texto.replace('Dime el tiempo en', '', 1).strip().replace('.',''))
                if texto is not None:
                    exito = True
                    print(texto)
                    filename = Sintetizador().sintetizar(texto)
                    self.play_wav(filename, True)
        
        if not exito:
            print("Error")
            self.play_wav('scripts/Audio/offline/Error', False)

    def play_wav(self, filename, delete=False):
        f = wave.open(filename + '.wav',"rb")  
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output=True)
        data = f.readframes(AudioHandler.CHUNK)  

        while data:  
            stream.write(data)  
            data = f.readframes(AudioHandler.CHUNK)  
 
        stream.stop_stream()  
        stream.close()  
 
        p.terminate()  
        f.close()

        if(delete):
            os.remove(filename + '.wav')
        