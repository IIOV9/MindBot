from flask import Flask, render_template, request, redirect
from diagnosis import get_diagnosis  # Importing the get_diagnosis function
import random
import csv

app = Flask(__name__)

questions = []
pinned_question = "سوف اسألك اسئلة تشخيصيه هل أنت مستعد؟"  # The pinned question
pinned_question_asked = False  # Flag to track if the pinned question has been asked

with open('diagnosis.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    all_questions = [row[0] for row in reader]  # Extract all questions
    questions = [question.strip('[]') for question in all_questions]  # Remove square brackets
    # Randomly select 10 questions initially
    random_questions = random.sample(questions, 10)

chat_history = []
current_question_index = 0
error_message = ""  # متغير جديد لتخزين رسالة الخطأ 

@app.route('/', methods=['GET', 'POST'])
def home():
    global pinned_question_asked
    if request.method == 'POST':
        # Check if the pinned question is answered with 'yes'
        answer = request.form.get('answer', '').lower()
        if answer == "نعم":
            # Reset chat history and current question index
            global chat_history, current_question_index
            chat_history = [{"type": "question", "text": pinned_question}]
            current_question_index = 0
            pinned_question_asked = True
            return redirect('/MindBot')
    return render_template('HomePage.html')

@app.route('/MindBot', methods=['GET', 'POST'])
def mindbot():
    global current_question_index, chat_history, pinned_question_asked
    if request.method == 'POST':
        answer = request.form.get('answer', '').lower()
        if answer in ["نعم", "لا"]:
            chat_history.append({"type": "answer", "text": answer})
            current_question_index += 1
        else:
            return render_template('MindBot.html', chat_history=chat_history, show_input=True, error_message="الرجاء الإجابة بـ 'نعم' أو 'لا' فقط.", current_question_index=current_question_index)

    # If the pinned question has not been asked yet
    if not pinned_question_asked:
        chat_history.append({"type": "question", "text": pinned_question})
        pinned_question_asked = True
        return render_template('MindBot.html', chat_history=chat_history, show_input=True, error_message="", current_question_index=current_question_index)

    # Proceed with the diagnosis process if there are more questions
    if current_question_index < len(questions):
        chat_history.append({"type": "question", "text": questions[current_question_index]})
        return render_template('MindBot.html', chat_history=chat_history, show_input=True, error_message="", current_question_index=current_question_index)
    
    yes_count = sum(1 for chat in chat_history if chat["text"] == "نعم")
    diagnosis = get_diagnosis(yes_count)
    return render_template('MindBot.html', chat_history=chat_history, show_input=False, yes_count=yes_count, no_count=(current_question_index - yes_count), diagnosis=diagnosis)

if __name__ == '__main__':
    app.run(debug=True)
