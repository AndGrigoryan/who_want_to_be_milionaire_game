#!/usr/bin/env python3

from random import randrange, shuffle
import argparse


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


def create_qa_dict(indexes_list, questions):   #create questions and answers dict
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


def check_answ(score, mx_questions, variants_dict, correct):
    answ = input("\nPlease enter your answer(A, B, C or D): ").upper()
    while answ == "" or answ not in "ABCD":
        print("\nInvalid answer")
        answ = input("\nPlease enter your answer(A, B, C or D): ").upper()
    if correct == variants_dict[answ]:
        score += 1
        print("\nCorrect. You have %d/%d" %(score, mx_questions))
    else:
        print("\nNope. The correct answer was " + correct)
    return score


def play(indexes_list, questions_dict, mx_questions):
    score = 0
    print("\nWelcome to the game 'Who wants to be a millionaire'\n")
    for q, a in questions_dict.items():
        correct, variants_dict = display_question(q, a)
        score = check_answ(score, mx_questions, variants_dict, correct)
    print("End of the game. You got %d/%d" %(score, mx_questions))
    return score


def create_file_if_not_exist(path):
    try:
        with open(path) as f:
            pass
    except FileNotFoundError:
        with open(path, 'w') as f:
            pass


def get_player_list(path):
    try:
        with open(path) as f:
            nicks = [item for item in f.readlines()]
            nicks = [item.split(',')[0] for item in nicks]
            nicks = " ".join(nicks).strip()
    except FileNotFoundError:
        print("Error while opening top_players.txt")
        exit()

    return nicks


def get_player_name():
    while True:
        player_name = input("Please enter your nickname: ")
        if not player_name:
            print("The player name cannot be empty. Try again.")
        else:
            return player_name


def check_and_prompt_for_overwrite(player_name, nicks):
    player_exists = player_name in nicks
    if player_exists:
        overwrite = input(f'A player named {player_name} already exists. Overwrite data? (y/n): ').lower()
        return overwrite == 'y'
    return True


def sort_data(data):
    try:
        data.sort(key=lambda x: int(x.split(',')[1]), reverse=True)
    except Exception as error:
        print(f"Error sorting data: {error}")
    
    return data


def write_player_score(path, player_name, score):
    try:
        with open(path, 'r+') as f:
            data = f.readlines()
            for i, line in enumerate(data):
                if player_name in line:
                    data[i] = f"{player_name},{score}\n"
                    break
            else:
                data.append(f"{player_name},{score}\n")

            data = sort_data(data)

            f.seek(0)

            f.writelines(data)
    except Exception as error:
        print(f"Error writing player score: {error}")


def main():
    parser = argparse.ArgumentParser(description="Get file for questions.")
    parser.add_argument("questions_path", type=str, help="The path to the questions path.")
    parser.add_argument("top_players_path", type=str, help="The path to the top players path.")

    args = parser.parse_args()

    questions_path = args.questions_path

    questions_ls = get_questions_ls(questions_path)
    mx_questions = 10
    
    top_players_path = args.top_players_path
    create_file_if_not_exist(top_players_path)

    nicks = get_player_list(top_players_path)


    while True:
        player_name = get_player_name()
        if check_and_prompt_for_overwrite(player_name, nicks):
            break
        else:
            continue


    indexes_list = select_random_questions_id(questions_ls, mx_questions)
    questions_dict = create_qa_dict(indexes_list, questions_ls)

    score = play(indexes_list, questions_dict, mx_questions)

    write_player_score(top_players_path, player_name, score)


if __name__ == '__main__':
    main()


