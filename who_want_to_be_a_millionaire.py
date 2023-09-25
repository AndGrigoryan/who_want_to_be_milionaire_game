#!/usr/bin/env python3

from random import randrange, shuffle


def select_random_questions_id(questions, question_cnt):
    indexes_list = []
    while len(indexes_list) < question_cnt:
        num = randrange(len(questions))
        if num not in indexes_list:
            indexes_list.append(num)
    return indexes_list


def get_questions_ls(path):
    questions = []
    with open(path, 'r') as f:
        for line in f:
            questions.append(line.strip())
    return questions


def create_qa_dict(indexes_ls, questions):   #create questions and answers dict
    tmp = []
    for i in indexes_list:
        tmp.append(questions[i])
    questions = {}
    for item in tmp:
        q, a = item.split("?")
        questions[q] = a

    return questions


def display_question(q, a):
    variants = a.split(" ")
    correct = " ".join(variants[0].split("_"))
    print("\n", q + "?\n")
    shuffle(variants)
    variants_dict = {}
    for i in range(len(variants)):
        variants_dict[chr(ord('A') + i)] = " ".join(variants[i].split("_"))
    
    for k, v in variants_dict.items():
        print(k + ".", v, end=" ")
    print()
    return correct, variants_dict


def check_answ(cnt, mx_questions, variants_dict, correct):
    answ = input("\nPlease enter your answer(A, B, C or D): ").upper()
    while answ == "" or answ not in "ABCD":
        print("\nInvalid answer")
        answ = input("\nPlease enter your answer(A, B, C or D): ").upper()
    if correct == variants_dict[answ]:
        cnt += 1
        print("\nCorrect. You have %d/%d" %(cnt, mx_questions))
    else:
        print("\nNope. The correct answer was " + correct)
    return cnt


def play(indexes_list, questions_dict):
    cnt = 0
    print("Welcome to the game 'Who wants to be a millionaire'\n")
    for q, a in questions_dict.items():
        correct, variants_dict = display_question(q, a)
        cnt = check_answ(cnt, mx_questions, variants_dict, correct)
    print("End of the game. You got %d/%d" %(cnt, mx_questions))


questions_ls = get_questions_ls("questions_capitals.txt")

mx_questions = 10

indexes_list = select_random_questions_id(questions_ls, mx_questions)

questions_dict = create_qa_dict(indexes_list, questions_ls)

play(indexes_list, questions_dict)

