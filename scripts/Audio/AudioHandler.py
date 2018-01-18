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
    # Microphone stream config.
    CHUNK = 1024  # CHUNKS of bytes to read each time from mic
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    THRESHOLD = 2500  # The threshold intensity that defines silence
                    # and noise signal (an int. lower than THRESHOLD is silence).

    SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                    # only silence is recorded. When this time passes the
                    # recording finishes and the file is delivered.

    PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                    # is detected, how much of previously recorded audio is
                    # prepended. This helps to prevent chopping the beggining
                    # of the phrase.

    def __init__(self):
        return 

    def audio_int(self, num_samples=50):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the 20% largest intensities recorded.
        """

        print("Getting intensity values from mic.")
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
        print(" Finished ")
        print(" Average audio intensity is " + r)
        stream.close()
        p.terminate()
        return r

    def listen_for_speech(self, threshold=THRESHOLD):
        """
        Listens to Microphone, extracts phrases from it and sends it to 
        Google's TTS service and returns response. a "phrase" is sound 
        surrounded by silence (according to threshold). num_phrases controls
        how many phrases to process before finishing the listening process 
        (-1 for infinite). 
        """

        #Open stream
        p = pyaudio.PyAudio()

        stream = p.open(format=AudioHandler.FORMAT,
                        channels=AudioHandler.CHANNELS,
                        rate=AudioHandler.RATE,
                        input=True,
                        frames_per_buffer=AudioHandler.CHUNK)

        print("* Listening mic. ")
        audio2send = []
        cur_data = ''  # current chunk  of audio data
        rel = AudioHandler.RATE/AudioHandler.CHUNK
        slid_win = deque(maxlen=int(AudioHandler.SILENCE_LIMIT * rel))
        #Prepend audio from 0.5 seconds before noise was detected
        prev_audio = deque(maxlen=int(AudioHandler.PREV_AUDIO * rel))
        started = False
        response = []
        n = 1

        while (n > 0):
            cur_data = stream.read(AudioHandler.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            #print slid_win[-1]
            if(sum([x > AudioHandler.THRESHOLD for x in slid_win]) > 0):
                if(not started):
                    print("Starting record of phrase")
                    started = True
                audio2send.append(cur_data)
            elif (started is True):
                print("Finished")
                # The limit was reached, finish capture and deliver.
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                # Send file to Google and get response
                
                stream.close()
                p.terminate()
                return filename
            else:
                prev_audio.append(cur_data)

    def save_speech(self, data, p):
        """ Saves mic data to temporary WAV file. Returns filename of saved 
            file """

        filename = 'output_'+str(int(time.time()))
        # writes data to WAV file
        data = b''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)  # TODO make this value a function parameter?
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    def process_input(self, filename):
        texto = Reconocimiento().llamar_api(filename)

        if(texto is not None):
            if(texto.startswith("Nuevo tweet")):
                texto = texto.replace('Nuevo tweet', '', 1)
                Twitter().enviar_tweet(texto = texto.strip().capitalize())
            elif(texto.startswith("Dime el tiempo en")):
                texto = Tiempo_api().textoClima(texto.replace('Dime el tiempo en', '', 1).strip().replace('.',''))
                print(texto)
                filename = Sintetizador().sintetizar(texto)
                self.play_wav(filename, True)
        else:
            print("Error")

    def play_wav(self, filename, delete=False):
        f = wave.open(filename + '.wav',"rb")  
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output=True)
        data = f.readframes(AudioHandler.CHUNK)  

        #play stream  
        while data:  
            stream.write(data)  
            data = f.readframes(AudioHandler.CHUNK)  

        #stop stream  
        stream.stop_stream()  
        stream.close()  

        #close PyAudio  
        p.terminate()  
        f.close()

        if(delete):
            os.remove(filename + '.wav')
        