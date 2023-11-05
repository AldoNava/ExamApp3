import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
import sys, os
import json
from tkinter import messagebox

class Explorer:
    def __init__(self, user, pswd, course):
        self.user = user
        self.pswd = pswd
        self.course = course
        self.page = 1
        self.waiting = False
        self.questionList = []
        self.login()

    def login(self):
        self.opendriver('https://www.examtopics.com/')
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[1]/ul/li[1]/a').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'etemail').send_keys(self.user)#('abcdef_12323')
        self.driver.find_element(By.ID, 'etpass').send_keys(self.pswd)#('123456')
        self.driver.find_element(By.XPATH, '//*[@id="login-modal"]/div/div/div[2]/div/form/button').click()
        time.sleep(5)
        self.driver.get(self.course + str(self.page) + '/')
        self.manageProcess()

    def manageProcess(self):
        self.working = True
        try:
            while True and self.working is True:
                if self.waiting is False:
                    self.waiting = True
                    self.clickCheckBox()
            self.writeQuestions()

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            #self.driver.quit()

    def opendriver(self, url):
        """ua = UserAgent(os='windows')
        user_agent = ua.random
        print(user_agent)
        options = Options()
        options.add_argument(f'--user-agent={user_agent}')"""
        ser = FirefoxService(r'geckodriver.exe')
        self.driver = webdriver.Firefox(service=ser)
        self.driver.maximize_window()
        self.driver.get(url)

    def nextPage(self, checknextpage):
        if checknextpage == 1:
            self.page += 1
            self.driver.get(self.course + str(self.page)+'/')
            #self.driver.execute_script('document.getElementsByClassName("btn btn-success pull-right")[0].click()')
            self.waiting = False
        else:
            self.working = False
            self.driver.quit()

    def clickCheckBox(self):
        try:
            if self.driver.execute_script('return document.getElementsByClassName("col-12 text-center").length') != 0:
                #self.driver.execute_script('document.getElementsByClassName("g-recaptcha btn btn-primary")[0].click()')
                self.checkStatus()
            else:
                self.checkStatus()
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def checkStatus(self):
        if self.driver.execute_script('return document.getElementsByClassName("card exam-question-card").length') != 0:
            self.checkIfIsLoaded("/html/body/div[1]/header/div[2]/div/div/div/div/nav/ul/li[1]/a")
            self.startProcess()
        else:
            time.sleep(3)
            self.checkStatus()

    def startProcess(self):
        time.sleep(2)
        self.checkIfIsLoaded("/html/body/div[1]/header/div[2]/div/div/div/div/nav/ul/li[1]/a")
        questionNumber = int(self.driver.execute_script('return document.getElementsByClassName("card exam-question-card").length'))
        for x in range(questionNumber):
            questionNo = self.driver.execute_script('return document.getElementsByClassName("card-header text-white bg-primary")['+str(x)+'].outerText')
            question = self.driver.execute_script('return document.getElementsByClassName("card exam-question-card")['+str(x)+'].children[1].children[0].outerText')
            optionNumber = int(self.driver.execute_script('return document.getElementsByClassName("card exam-question-card")['+str(x)+'].children[1].children[1].getElementsByTagName("li").length'))
            options = []
            correct_answers = []
            page_answers = []
            for number in range(optionNumber):
                text_option = self.driver.execute_script('return document.getElementsByClassName("card exam-question-card")['+str(x)+'].children[1].children[1].getElementsByTagName("li")['+str(number)+'].outerText')
                options.append(text_option)
                most_voted = self.driver.execute_script('return document.getElementsByClassName("card exam-question-card")['+str(x)+'].children[1].children[1].getElementsByTagName("li")['+str(number)+'].getElementsByClassName("badge badge-success most-voted-answer-badge").length')
                if most_voted == 1:
                    correct_answers.append(text_option)

            for CA in range(self.driver.execute_script('return document.getElementsByClassName("card exam-question-card")['+str(x)+'].children[1].children[1].getElementsByClassName("multi-choice-item correct-hidden").length')):
                page_answer = self.driver.execute_script('return document.getElementsByClassName("card exam-question-card")[' + str(x) + '].children[1].children[1].getElementsByClassName("multi-choice-item correct-hidden")['+str(CA)+'].outerText')
                page_answers.append(page_answer)

            self.driver.execute_script('document.getElementsByClassName("card exam-question-card")['+str(x)+'].getElementsByClassName("btn btn-secondary question-discussion-button d-print-none")[0].click()')
            self.getDiscussion()
            discData = self.getData()
            self.driver.execute_script('document.getElementsByClassName("modal fade show")[0].getElementsByClassName("close")[0].click()')

            dictionary = {}
            dictionary['questionNo'] = questionNo
            dictionary['question'] = question
            dictionary['options'] = options
            dictionary['most_voted_answer'] = correct_answers
            dictionary['page_answer'] = page_answers
            dictionary['current_URL'] = self.driver.current_url
            dictionary['discussion'] = discData
            self.questionList.append(dictionary)
            time.sleep(.5)

        checknextpage = self.driver.execute_script('return document.getElementsByClassName("btn btn-success pull-right").length')
        self.nextPage(checknextpage)

    def getData(self):
        discussion_List = []
        head_information, selected_answer, text, votes = '', '', '', ''
        for comment in range(
                self.driver.execute_script('return document.getElementsByClassName("media comment-container").length')):
            try:
                head_information = self.driver.execute_script(
                'return document.getElementsByClassName("media comment-container")[' + str(
                    comment) + '].getElementsByClassName("media-body")[0].getElementsByClassName("comment-head")[0].outerText')
            except:
                pass
            try:
                selected_answer = self.driver.execute_script(
                    'return document.getElementsByClassName("media comment-container")[' + str(
                        comment) + '].getElementsByClassName("media-body")[0].getElementsByClassName("comment-body comment-toggled")[0].getElementsByClassName("comment-selected-answers badge badge-warning")[0].outerText')
            except:
                pass
            try:
                text = self.driver.execute_script(
                'return document.getElementsByClassName("media comment-container")[' + str(
                    comment) + '].getElementsByClassName("media-body")[0].getElementsByClassName("comment-body comment-toggled")[0].getElementsByClassName("comment-content")[0].outerText')
            except:
                pass
            try:
                votes = self.driver.execute_script(
                'return document.getElementsByClassName("media comment-container")[' + str(
                    comment) + '].getElementsByClassName("media-body")[0].getElementsByClassName("comment-body comment-toggled")[0].getElementsByClassName("comment-control")[0].outerText')
            except:
                pass
            reply_length = self.driver.execute_script('return document.getElementsByClassName("media comment-container")[' + str(
                    comment) + '].getElementsByClassName("media-body")[0].getElementsByClassName("comment-replies")[0].getElementsByClassName("media comment-container").length')

            if reply_length != 0:
                string = 'return document.getElementsByClassName("media comment-container")[' + str(comment) + '].getElementsByClassName("media-body")[0].getElementsByClassName("comment-replies")[0].getElementsByClassName("media comment-container")'
                repliesH = self.replies(reply_length, string)
            else:
                repliesH = []
            discDict = {}
            discDict['header'] = head_information
            discDict['selected_answer'] = selected_answer
            discDict['body'] = text
            discDict['votes'] = votes
            discDict['reply'] = repliesH
            discussion_List.append(discDict)
            #print(f'mainReply -> {discussion_List}')

        return discussion_List


    def replies(self, reply_length, string):
        replies = []
        reply_header_information, reply_selected_answer, reply_text, reply_votes = '', '', '', ''
        for reply in range(reply_length):
            try:
                reply_header_information = self.driver.execute_script(string+'['+str(reply)+'].getElementsByClassName("comment-head")[0].outerText')
            except:
                pass
            try:
                reply_selected_answer = self.driver.execute_script(string+'['+str(reply)+'].getElementsByClassName("comment-head")[0].getElementsByClassName("comment-selected-answers badge badge-warning")[0].outerText')
            except:
                pass
            try:
                reply_text = self.driver.execute_script(string+'['+str(reply)+'].getElementsByClassName("comment-body comment-toggled")[0].getElementsByClassName("comment-content")[0].outerText')
            except:
                pass
            try:
                reply_votes = self.driver.execute_script(string+'['+str(reply)+'].getElementsByClassName("comment-body comment-toggled")[0].getElementsByClassName("comment-control")[0].outerText')
            except:
                pass

            reply_length = self.driver.execute_script(string+'['+str(reply)+'].getElementsByClassName("comment-replies")[0].getElementsByClassName("media comment-container").length')
            if reply_length != 0:
                repliesH = self.replies(reply_length, string+'['+str(reply)+'].getElementsByClassName("comment-replies")[0].getElementsByClassName("media comment-container")')
            else:
                repliesH = []
            discDict = {}
            discDict['header'] = reply_header_information
            discDict['selected_answer'] = reply_selected_answer
            discDict['body'] = reply_text
            discDict['votes'] = reply_votes
            discDict['reply'] = repliesH
            replies.append(discDict)
            #print(f'replies -> {discDict}')
        return replies

    def getDiscussion(self):
        if self.driver.execute_script('return document.getElementsByClassName("discussion-real-title display-none")[0].getAttribute("style")') == 'display: inline;':
            self.getAllComments()

        else:
            time.sleep(5)
            self.getDiscussion()

    def getAllComments(self):
        try:
            self.driver.execute_script(
                'document.getElementsByClassName("load-more-section d-print-none mb-1")[0].children[0].click()')
            self.checkifIsGone()
        except:
            pass

    def checkifIsGone(self):
        if self.driver.execute_script('return document.getElementsByClassName("load-more-section d-print-none mb-1").length') !=0:
            pass
        else:
            time.sleep(5)
            self.checkifIsGone()

    def writeQuestions(self):
        with open('questions.txt', 'a', encoding='utf-8') as f:
            json.dump(self.questionList, f)
            #f.write(json.dumps(dictionary))
        self.driver.quit()
        messagebox.showinfo('Completado', 'Proceso completado')

    def checkIfIsLoaded(self, xpath):
        try:
            # Wait for the page to load and a specific element to be present
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, 10).until(element_present)

            # If the above line doesn't throw an exception, it means the page is loaded
            print("Page loaded successfully!")

        except Exception as e:
            print("Page took too long to load or encountered an error:", e)
            self.checkIfIsLoaded(xpath)
            time.sleep(3)


if __name__ == '__main__':
    main = Explorer()
    main.login()