from GetQuestions import Explorer
from tkinter import *
import customtkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import threading

class MainWindow:
    def __init__(self):
        self.setWindow()

    def setWindow(self):
        customtkinter.set_appearance_mode('System')
        self.app = customtkinter.CTk()
        self.app.title('Obtener preguntas')
        window_height = 200
        window_width = 400

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        bodyapp = customtkinter.CTkFrame(master=self.app)
        bodyapp.pack(padx=10, pady=(10, 20), fill='both', expand=True)
        bodyapp.columnconfigure(0, weight=1)
        bodyapp.columnconfigure(1, weight=1)
        bodyapp.columnconfigure(2, weight=1)
        bodyapp.columnconfigure(3, weight=1)
        self.user = customtkinter.StringVar(value='Usuario')
        user = customtkinter.CTkEntry(master=bodyapp,
                                            width=200,
                                            textvariable=self.user,
                                            placeholder_text='Usuario',
                                            justify='center')
        user.pack(fill='x')

        self.pswd = customtkinter.StringVar(value='Contraseña')
        pswd = customtkinter.CTkEntry(master=bodyapp,
                                      width=200,
                                      textvariable=self.pswd,
                                      placeholder_text='Contraseña',
                                      justify='center')
        pswd.pack(fill='x')

        self.course = customtkinter.StringVar(value='Curso URL')
        course = customtkinter.CTkEntry(master=bodyapp,
                                      width=200,
                                      textvariable=self.course,
                                      placeholder_text='Curso URL',
                                      justify='center',)
        course.pack(fill='x')


        button = customtkinter.CTkButton(master=bodyapp, text='Iniciar', command=self.cmd)
        button.pack(pady=(10,  0), fill='x')
        self.app.mainloop()

    def cmd(self):
        if self.user.get() != 'Usuario' and self.pswd.get() != 'Contraseña' and self.course.get() != 'Curso URL':
            threading.Thread(target=Explorer, args=(self.user.get(), self.pswd.get(), self.course.get())).start()

if __name__ == '__main__':
    main = MainWindow()