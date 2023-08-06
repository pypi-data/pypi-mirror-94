import random

from psychometric_tests.shared.misc_funcs import save_csv


def create_1digit_summing_ques():
    ques = []
    while len(ques) < 100:
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)

        if num1 + num2 < 10:
            ques.append(['{} + {}'.format(num1, num2), str(num1 + num2)])

    save_csv('stimulus/sum_1digit_ans.csv', data=ques)


def create_summing_ques():
    ques = []
    while len(ques) < 100:
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)

        ques.append(['{} + {}'.format(num1, num2), str(num1 + num2)])

    save_csv('stimulus/sum.csv', data=ques)


if __name__ == '__main__':
    create_summing_ques()
    create_1digit_summing_ques()
