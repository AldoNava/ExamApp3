import tkinter as tk
from tkinter import messagebox


class ExamPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Practice App")

        self.questions = [
            {
                'question': 'What is the capital of France?',
                'options': ['Paris', 'London', 'Berlin', 'Madrid'],
                'correct_answer': 'Paris'
            },
            {
                'question': 'Which planet is known as the Red Planet?',
                'options': ['Earth', 'Mars', 'Venus', 'Jupiter'],
                'correct_answer': 'Mars'
            }
            # Add more questions here...
        ]

        self.current_question = 0
        self.score = 0
        self.selected_answer = None

        self.question_label = tk.Label(root, text="")
        self.question_label.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(root, text="", command=lambda i=i: self.select_answer(i))
            button.pack(fill='both', expand=True, padx=20, pady=5)
            self.option_buttons.append(button)

        self.confirm_button = tk.Button(root, text="Confirm Answer", command=self.confirm_answer)
        self.confirm_button.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0")
        self.score_label.pack(pady=10)

        self.update_question()

    def update_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data['question'])

            for i, option in enumerate(question_data['options']):
                self.option_buttons[i].config(text=option)

            self.confirm_button.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("Exam Complete", f"Your final score: {self.score}/{len(self.questions)}")
            self.root.destroy()

    def select_answer(self, selected_option):
        self.selected_answer = self.questions[self.current_question]['options'][selected_option]

    def confirm_answer(self):
        correct_answer = self.questions[self.current_question]['correct_answer']
        if self.selected_answer is not None:
            self.option_buttons[self.questions[self.current_question]['options'].index(self.selected_answer)].config(
                bg='white')
            if self.selected_answer == correct_answer:
                self.score += 1
            else:
                self.option_buttons[self.questions[self.current_question]['options'].index(correct_answer)].config(
                    bg='green')

        self.current_question += 1
        self.update_question()


if __name__ == '__main__':
    root = tk.Tk()
    app = ExamPracticeApp(root)
    root.mainloop()
