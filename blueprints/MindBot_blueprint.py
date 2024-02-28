from flask import Blueprint, render_template, request
from diagnosis import get_diagnosis  # Assuming this function is correctly implemented
import random
import csv

MindBot_blueprint = Blueprint('MindBot', __name__, template_folder='templates')

questions = []
pinned_question = "سوف اسألك اسئلة تشخيصيه هل أنت مستعد؟"
pinned_question_asked = False

# Load questions from CSV file
with open('diagnosis.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    questions = [row[0] for row in reader]

# Shuffle questions and select only 10 random questions
random.shuffle(questions)
questions = questions[:10]

chat_history = []
current_question_index = 0
error_message = ""


@MindBot_blueprint.route('/', methods=['GET', 'POST'])
def MindBot():
    global current_question_index, chat_history, pinned_question_asked, error_message
    if request.method == 'POST':
        answer = request.form.get('answer', '').strip().lower()
        if answer in ["نعم", "لا"]:
            chat_history.append({"type": "answer", "text": answer})
            current_question_index += 1
        else:
            error_message = "الرجاء الإجابة بـ 'نعم' أو 'لا' فقط."
            return render_template('MindBot.html', chat_history=chat_history, show_input=True, error_message=error_message, current_question_index=current_question_index)

    if not pinned_question_asked:
        chat_history.append({"type": "question", "text": pinned_question})
        pinned_question_asked = True
        return render_template('MindBot.html', chat_history=chat_history, show_input=True, error_message="", current_question_index=current_question_index)

    if current_question_index < len(questions):
        chat_history.append({"type": "question", "text": questions[current_question_index]})
        return render_template('MindBot.html', chat_history=chat_history, show_input=True, error_message="", current_question_index=current_question_index)
    
    yes_count = sum(1 for chat in chat_history if chat["text"] == "نعم")
    diagnosis = get_diagnosis(yes_count)
    return render_template('MindBot.html', chat_history=chat_history, show_input=False, yes_count=yes_count, no_count=(current_question_index - yes_count), diagnosis=diagnosis)
