import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','lectic_project.settings')

import django
django.setup()
from lectic.models import Quiz
from lectic.models import Question

def populate():

    geog_questions = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is the capital of Italy?", "answer": "Rome"},
        {"question": "What is the capital of Germany?", "answer": "Berlin"}]
    
    hist_questions = [
        {"question": "When was the Battle of Hastings?", "answer": "1066"},
        {"question": "How many wives did Henry VIII have?", "answer": "6"},
        {"question": "When was the Great Fire of London?", "answer": "1666"}]

    quizzes = [{"name": "Geography", "questions": geog_questions},
            {"name": "History", "questions": hist_questions}]
    
    for qz in quizzes:
        print (qz["name"])
        # print (qz["questions"])
        thisquiz = add_quiz(qz["name"])
        for q in qz["questions"]:
            print (q["question"])
            print (q["answer"])
            add_question(q["question"], q["answer"], thisquiz)

def add_quiz(name):
    qz = Quiz.objects.get_or_create(name=name)[0]
    qz.save()
    return qz

def add_question(question, answer, quiz):
    q = Question.objects.get_or_create(question=question,quiz=quiz)[0]
    q.answer=answer
    q.save()
    return q

if __name__ == '__main__':
    print("Populating Lectic script...")
    populate()
