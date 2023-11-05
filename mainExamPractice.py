import time
import tkinter
import tkinter.messagebox
import customtkinter
import json
import webbrowser
from win32api import GetMonitorInfo, MonitorFromPoint
#import pyttsx3

class ExamPracticeApp:
    def __init__(self):
        with open('questions.txt') as f:
            self.questionList = json.load(f)
        self.qPos = 319
        self.score = 0
        self.selectedOption = []
        self.available = True
        self.resizing = False
        self.sizeValues = []
        self.sizePos = 0
        self.countRepWidth = 0
        #self.voice = pyttsx3.init()
        self.setWindow()

    def setWindow(self):
        self.app = customtkinter.CTk()
        customtkinter.set_appearance_mode('System')
        self.app.title("Práctica de exámen")
        #self.app.resizable(False, False)  # This code helps to disable windows from resizing
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")
        #print("The work area size is {}x{}.".format(work_area[2], work_area[3]))
        #self.app.maxsize(work_area[2], work_area[3])
        window_width = work_area[2]
        window_height = work_area[3]

        self.app.geometry("{}x{}+-9+-1".format(window_width, window_height-238))
        #self.app.rowconfigure(0, weight=1)
        self.app.rowconfigure(1, weight=1)
        #self.app.rowconfigure(2, weight=1)
        self.app.columnconfigure(0, weight=1)

        self.QuestionPanel = customtkinter.CTkFrame(master=self.app)
        #self.QuestionPanel.pack(padx=10, pady=(20, 10), fill='x', expand=True, anchor='n')
        self.QuestionPanel.grid(row=0, column=0, padx=10, pady=(20, 10), sticky='nswe')
        self.QuestionPanel.rowconfigure(0, weight=1)

        self.OptionPanel = customtkinter.CTkScrollableFrame(master=self.app)
        #self.OptionPanel.pack(padx=10, pady=(10, 20), fill='both', expand=True)
        self.OptionPanel.grid(row=1, column=0, padx=10, pady=(20, 10), sticky='nsew')
        self.OptionPanel.rowconfigure(0, weight=1)
        self.OptionPanel.columnconfigure(0, weight=1)

        self.controlPanel = customtkinter.CTkFrame(master=self.app)
        #self.controlPanel.pack(padx=10, pady=(10, 20), fill='x', expand=True, ipady=10, anchor='s')
        self.controlPanel.grid(row=2, column=0, padx=10, pady=(20, 10), sticky='nswe')
        self.controlPanel.rowconfigure(0, weight=1)
        self.controlPanel.columnconfigure(0, weight=1)
        self.controlPanel.columnconfigure(1, weight=1)
        self.controlPanel.columnconfigure(2, weight=1)

        self.previousQuestion = customtkinter.CTkButton(master=self.controlPanel, text='Anterior', font=customtkinter.CTkFont(size=25, weight="bold"), anchor="center", command=lambda action='previous': self.controlQ(action))
        self.nextQuestion = customtkinter.CTkButton(master=self.controlPanel, text='Siguiente', font=customtkinter.CTkFont(size=25, weight="bold"), anchor="center", command=lambda action='next': self.controlQ(action))
        self.scoreI = customtkinter.CTkLabel(master=self.controlPanel, text=str(self.score)+'\nAciertos', font=customtkinter.CTkFont(size=30, weight="bold"), anchor="center", justify="center")
        self.previousQuestion.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.scoreI.grid(row=0, column=1,  padx=10, pady=0, sticky='nsew')
        self.nextQuestion.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        self.selectQuestion(self.qPos)
        self.app.bind('<Configure>', lambda e: self.sizeMgmt(self.app))
        self.app.bind('<Left>', lambda e: self.controlQ('previous'))
        self.app.bind('<Right>', lambda e: self.controlQ('next'))
        #self.QuestionPanel.after(50, self.sizeMgmt(self.app))
        self.app.mainloop()

    def sizeMgmt(self, window):
        if window.winfo_width() not in self.sizeValues:
            self.sizeValues.append(window.winfo_width())
        else:
            if self.countRepWidth > 3:
                if len(self.sizeValues) == self.sizePos:
                    if self.resizing != True:
                        self.resizing = True
                        #window.attributes("-alpha", 0.0)
                        self.questionNo.configure(text=self.resizeContent(window, self.questionNo.cget('text').replace('\n', ' '), 14, 1))
                        self.questionLabel.configure(text=self.resizeContent(window, self.questionLabel.cget('text').replace('\n', ' '), 25, 22))
                        #print(self.resizeContent(window, self.questionLabel.cget('text'), 25, 22))
                        self.linkLabel.configure(text=self.resizeContent(window, self.linkLabel.cget('text').replace('\n', ' '), 25, 21))
                        for bttn in self.questionList[self.qPos]['options']:
                            globals()[bttn].configure(text=self.resizeContent(window, globals()[bttn].cget('text').replace('\n', ' '), 20, 18))
                        #window.attributes("-alpha", 1.0)
                        self.sizeValues = []
                        self.sizePos = 0
                        self.countRepWidth = 0
                else:
                    self.sizePos = len(self.sizeValues)
            else:
                self.countRepWidth += 1

    def resizeContent(self, window, text, letterSize, letterSum):
        character_sum = 0
        tex_resized = ''
        split_section = window.winfo_width() // (len(text)*letterSize)
        if split_section < 1:
            for text in text.split():
                character_sum += len(text)*letterSum
                if character_sum < window.winfo_width()-30:
                    tex_resized = tex_resized + ' ' + text
                else:
                    tex_resized = tex_resized + '\n' + text
                    character_sum = 0
            self.resizing = False
            return tex_resized.strip()

        else:
            self.resizing = False
            return text

    def controlQ(self, action):
        self.destroyobject()
        if (self.questionList[self.qPos]['most_voted_answer'] == self.selectedOption and len(self.selectedOption) != 0) \
                or (self.questionList[self.qPos]['page_answer'] == self.selectedOption and len(self.selectedOption) != 0):
            self.score += 1
        self.scoreI.configure(text=str(self.score)+'\nAciertos')
        self.available = True
        self.selectedOption = []
        if action == 'next':
            if self.qPos + 1 >= len(self.questionList):
                self.qPos = 0
            else:
                self.qPos += 1
        else:
            self.qPos -= 1
        self.selectQuestion(self.qPos)

    def checkanswer(self, options):
        if options not in self.selectedOption:
            if len(self.questionList[self.qPos]['most_voted_answer']) != 0:
                if self.available is True:
                    self.selectedOption.append(options)
                    if options in self.questionList[self.qPos]['most_voted_answer']:
                        globals()[options].configure(text_color='#2ECC71')
                    else:
                        globals()[options].configure(text_color='#E74C3C')
                if len(self.selectedOption) >= len(self.questionList[self.qPos]['most_voted_answer']):
                    self.available = False
                    for answer in self.questionList[self.qPos]['most_voted_answer']:
                        if answer not in self.selectedOption:
                            globals()[answer].configure(text_color='#F1C40F')

                    for answer in self.questionList[self.qPos]['page_answer']:
                        globals()[answer].configure(border_color='#00FF00')##00AEFF
            else:
                if self.available is True:
                    self.selectedOption.append(options)
                    if options in self.questionList[self.qPos]['page_answer']:
                        globals()[options].configure(text_color='#2ECC71')
                        globals()[options].configure(border_color='#00FF00')
                    else:
                        globals()[options].configure(text_color='#E74C3C')
                if len(self.selectedOption) >= len(self.questionList[self.qPos]['page_answer']):
                    for answer in self.questionList[self.qPos]['page_answer']:
                        if answer not in self.selectedOption:
                            globals()[answer].configure(text_color='#F1C40F')
                            globals()[answer].configure(border_color='#00FF00')

    def updateStateBttn(self):
        time.sleep(.1)
        if self.nextQuestion.cget('state') == 'normal':
            self.nextQuestion.configure(state='disabled')
            self.previousQuestion.configure(state='disabled')
        else:
            self.nextQuestion.configure(state='normal')
            self.previousQuestion.configure(state='normal')
        time.sleep(.1)

    def destroyobject(self):
        self.questionNo.destroy()
        self.questionLabel.destroy()
        self.linkLabel.destroy()
        self.discussion.destroy()
        for bttn in self.questionList[self.qPos]['options']:
            globals()[bttn].destroy()

    def callback(self, url):
        self.linkLabel.configure(text_color='#8E44AD')
        webbrowser.open_new_tab(url)

    def selectQuestion(self, pos):
        self.questionNo = customtkinter.CTkLabel(master=self.QuestionPanel, text=self.questionList[pos]['questionNo'].replace('\n', ' '), font=customtkinter.CTkFont(size=14, weight="bold"), anchor="w", justify="left")
        self.questionNo.pack(padx=10, anchor='w')
        question = self.resizeContent(self.app, self.questionList[pos]['question'].replace('\n', ' '), 25, 22)
        #print(question)
        self.questionLabel = customtkinter.CTkLabel(master=self.QuestionPanel, text=question, font=customtkinter.CTkFont(size=25, weight="bold"), anchor="center", justify="center")
        self.questionLabel.pack(pady=(0, 10), padx=10)
        self.linkLabel = customtkinter.CTkLabel(master=self.QuestionPanel, text=self.questionList[pos]['current_URL'].replace('\n', ' '), text_color='#3498DB', font=customtkinter.CTkFont(size=14, weight="bold"), anchor="w", justify="left", cursor="hand2")
        self.linkLabel.pack(padx=40, side='left')
        self.discussion = customtkinter.CTkLabel(master=self.QuestionPanel, text='Discusión', text_color='#3498DB',
                                                 font=customtkinter.CTkFont(size=14, weight="bold"), anchor="e",
                                                 justify="left", cursor="hand2")
        self.discussion.pack(pady=(0, 10), padx=40, side='right')
        self.linkLabel.bind("<Button-1>", lambda e: self.callback(self.questionList[pos]['current_URL']))
        self.discussion.bind("<Button-1>", lambda e: self.discWin(self.questionList[pos]['discussion'], question))
        #self.questionLabel.bind('<Configure>', lambda e: self.resizeContent(self.app))
        for index, bttn in enumerate(self.questionList[pos]['options']):
            self.OptionPanel.rowconfigure(index, weight=1)
            globals()[bttn] = customtkinter.CTkButton(master=self.OptionPanel, text=self.resizeContent(self.OptionPanel, str(bttn).strip(), 20, 18), fg_color="transparent", border_width=3, font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center", command=lambda options=bttn: self.checkanswer(options))
            globals()[bttn].pack(anchor='center', padx=20, pady=20, expand=True, fill='both')
        """self.voice.say(self.questionList[pos]['question'])
        self.voice.runAndWait()"""

    def discWin(self, comments, question):
        self.discWindow = customtkinter.CTk()
        customtkinter.set_appearance_mode('System')
        self.discWindow.title("Discusión - comentarios")
        # self.app.maxsize(work_area[2], work_area[3])
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")
        window_width = work_area[2]
        window_height = work_area[3]

        self.discWindow.geometry("{}x{}+-9+-1".format(window_width, window_height - 238))

        #self.discWindow.rowconfigure(0, weight=1)
        self.discWindow.rowconfigure(1, weight=1)
        #self.discWindow.rowconfigure(2, weight=1)
        self.discWindow.columnconfigure(0, weight=1)

        QuestionPanel = customtkinter.CTkFrame(master=self.discWindow)
        QuestionPanel.grid(row=0, column=0, padx=10, pady=(20, 10), sticky='nswe')
        QuestionPanel.rowconfigure(0, weight=1)

        CommentPanel = customtkinter.CTkScrollableFrame(master=self.discWindow)
        #CommentPanel.pack(padx=10, pady=(10, 20), fill='both', expand=True)
        CommentPanel.rowconfigure(0, weight=1)
        CommentPanel.grid(row=1, column=0, padx=10, pady=(20, 10), sticky='nsew')

        self.questionL = customtkinter.CTkLabel(master=QuestionPanel, text=question.replace('\n', ' '),font=customtkinter.CTkFont(size=25, weight="bold"), anchor="center",justify="center", wraplength=window_width-500)
        self.questionL.pack(pady=(0, 10), padx=10)

        self.createComments(comments, CommentPanel, '_')
        self.discWindow.bind('<Configure>', lambda e: self.sizeMgmtDisc())
        self.discWindow.mainloop()

    def sizeMgmtDisc(self):
        self.questionL.configure(wraplength=self.discWindow.winfo_width()-500)

    def createComments(self, comments, CommentPanel, string_variable):
        for index, comment in enumerate(comments):
            globals()['commentFrame' + str(index) + string_variable] = customtkinter.CTkFrame(master=CommentPanel, border_width=5)
            globals()['commentFrame' + str(index) + string_variable].pack(padx=10, pady=20, fill='x', expand=True)

            globals()['commentFrame' + str(index) + string_variable].rowconfigure(0, weight=1)
            globals()['commentFrame' + str(index) + string_variable].rowconfigure(1, weight=1)
            globals()['commentFrame' + str(index) + string_variable].columnconfigure(0, weight=1)

            globals()['headerSection' + str(index) + string_variable] = customtkinter.CTkFrame(master=globals()['commentFrame' + str(index) + string_variable])
            globals()['headerSection' + str(index) + string_variable].pack(padx=10, pady=20, fill='x', expand=True)

            globals()['header' + str(index) + string_variable] = customtkinter.CTkLabel(master=globals()['headerSection' + str(index) + string_variable], text=comment['header'])
            globals()['votes' + str(index) + string_variable] = customtkinter.CTkLabel(master=globals()['headerSection' + str(index) + string_variable], text=comment['votes'])
            globals()['header' + str(index) + string_variable].pack(padx=20, pady=(10, 20), side='left')
            globals()['votes' + str(index) + string_variable].pack(padx=20, pady=(10, 20), side='right')

            globals()['selected_answer' + str(index) + string_variable] = customtkinter.CTkLabel(master=globals()['commentFrame' + str(index) + string_variable], text=comment['selected_answer'], anchor="w", justify="left", font=customtkinter.CTkFont(size=25, weight="bold"))
            globals()['body' + str(index) + string_variable] = customtkinter.CTkLabel(master=globals()['commentFrame' + str(index) + string_variable], text=comment['body'], wraplength=1400, anchor="w", justify="left", font=customtkinter.CTkFont(size=20, weight="bold"))
            #globals()['body' + str(index) + string_variable] = customtkinter.CTkTextbox(master=globals()['commentFrame' + str(index) + string_variable], state='normal', font=customtkinter.CTkFont(size=20, weight="bold"))
            #globals()['body' + str(index) + string_variable].insert("0.0", comment['body'])
            #globals()['body' + str(index) + string_variable].configure(state='disabled')
            globals()['selected_answer' + str(index) + string_variable].pack(padx=20, pady=(10, 20), anchor='w')
            globals()['body' + str(index) + string_variable].pack(padx=20, pady=(10, 20), anchor='w', expand=True, fill='x')

            if len(comment['reply']) != 0:
                self.createComments(comment['reply'], globals()['commentFrame'+str(index)+string_variable], string_variable+'_')

if __name__ == '__main__':
    main = ExamPracticeApp()

