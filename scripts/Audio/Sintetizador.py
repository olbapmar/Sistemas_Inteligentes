#! /usr/bin/env python3

# -*- coding: utf-8 -*-

###
#Copyright (c) Microsoft Corporation
#All rights reserved. 
#MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ""Software""), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###
import http.client
from xml.etree import ElementTree
import time
#Note: The way to get api key:
#Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
#Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0

class Sintetizador:
    apiKey = "528e03982d034cb184c0bc1d12c4d310"

    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}

    #AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    def access_token(self):
        # Connect to server to get the Access Token
        print ("Connect to server to get the Access Token")
        conn = http.client.HTTPSConnection(Sintetizador.AccessTokenHost)
        conn.request("POST", Sintetizador.path, Sintetizador.params, Sintetizador.headers)
        response = conn.getresponse()
        print(response.status, response.reason)

        data = response.read()
        conn.close()

        accesstoken = data.decode("UTF-8")
        return accesstoken

    def sintetizar(self, texto):
        accesstoken = self.access_token()

        body = ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice = ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'es-ES')
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (es-ES, Laura, Apollo)')
        voice.text = texto

        headers = {"Content-type": "application/ssml+xml", 
                    "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm", 
                    "Authorization": "Bearer " + accesstoken,
                    "User-Agent": "Proyecto de Sistemas"}
                    
        #Connect to server to synthesize the wave
        print ("\nConnect to server to synthesize the wave")
        conn = http.client.HTTPSConnection("speech.platform.bing.com")
        conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
        response = conn.getresponse()
        print(response.status, response.reason)

        data = response.read()
        conn.close()

        filename = "voz_" + str(int(time.time()))
        fout = open(filename + '.wav', 'wb')
        fout.write(data)
        fout.close()

        return filename