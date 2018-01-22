# Proyecto de Sistemas Inteligentes: Sistema de Ayuda al Conductor

## Universidad de La Laguna, 2018

### Autores:
* Pablo Pastor Martín  
* Isaac Aimán Salas 

Este es el repositorio del proyecto final de la asignatura de Sistemas Inteligentes de los alumnos citados. 

El objetivo del proyecto es crear un sistema que ayude al conductor mediante la detección de señales de trafico y semáforos en la escena, así como un sistema que le brinde servicios mediante la voz.

### Modo de Uso:
**Usamos Python3**

Recomendamos iniciar todos los scripts desde la raíz del repositorio, aunque esto es **necesario** en el caso del de audio. Para iniciar éste último usar:

```
python ./scripts/Audio/Ventana.py
```

Para el caso de las señales:
```
cd scripts/Videos/
python ./main.py ruta_al_video
```

Para el caso de los semáforos:
```
python ./scripts/Videos/semaforos/main_semaforos.py ruta_al_video
```

En [este enlace](https://drive.google.com/open?id=1m4wjfbkHHHabnGZWm464FRfb_P_XgJJb) se encuentran vídeos con, como su nombre indica, videos con señales y semáforos.

**Requerimientos**

* OpenCV para python, con los contrib incluidos
* Tweepy
* PyAudio
