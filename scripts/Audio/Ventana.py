from tkinter import *
from AudioHandler import AudioHandler


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.init_window()
        self.boton
        self.audio = AudioHandler()

    def init_window(self):
        self.master.title("Audio")

        self.boton = Button(self, text="Iniciar dictado", command=self.iniciar)
        self.boton.place(x=0,y=0)
        self.boton.pack()
        self.pack()
    
    def iniciar(self):
        self.boton['state'] = 'disabled'
        input = self.audio.listen_for_speech()
        self.audio.process_input(input)
        self.boton['state'] = 'normal'


root = Tk()
app = Window(root)
root.mainloop()