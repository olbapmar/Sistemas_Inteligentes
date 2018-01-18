import http.client
import urllib.parse
import json



class Tiempo_api:
    api_key = "d2d0ade56c57389b60485410a176c228"

    def textoClima(self, nombre):
        conn = http.client.HTTPConnection("api.openweathermap.org")
        params = urllib.parse.urlencode({
            "q": nombre,
            "lang": "ES",
            "units": "metric",
            "appid": Tiempo_api.api_key
        })

        conn.request("GET", "/data/2.5/weather/?" + params)
        response = conn.getresponse()

        if(response.status == 200):
            try:
                respuesta = json.loads(response.read().decode('utf-8'))
                return "El tiempo en " + nombre + " es: " + respuesta["weather"][0]["description"] + ", con una temperatura de " + str(respuesta["main"]["temp"]).partition(".")[0] + " grados"
            except KeyError:
                pass

        return None