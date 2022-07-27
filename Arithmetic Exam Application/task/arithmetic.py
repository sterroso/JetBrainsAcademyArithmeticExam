# write your code here
from random import seed, randint
from typing import List

IntList = List[int]


class Task:
    LEVELS = {
        1: {
            'name': 'Easy',
            'description': 'simple operations with numbers 2-9',
            'min_int': 2,
            'max_int': 9,
            'funcs': ['sum', 'diff', 'mult'],
        },
        2: {
            'name': 'Medium',
            'description': 'integral squares 11-29',
            'min_int': 11,
            'max_int': 29,
            'funcs': ['int_square']
        }
    }

    OPERATOR_MAP = {
        'sum': '+',
        'diff': '-',
        'mult': '*',
        'int_div': '\u00F7',
        'int_square': '\u00B2',
    }

    '''
    Initialises a Problem instance with a specific level of
    difficulty.
    '''

    def __init__(self, level: int):
        if level in Task.LEVELS.keys():
            self.level = level
        else:
            self.level = 1
        # Generates a pair of random integers
        self.integers = Task.generate_random_integers(self.level)
        # Chooses a random function
        self.func = Task.generate_random_func(self.level)
        # Matches the chosen function with its corresponding character.
        self.operator = Task.OPERATOR_MAP[self.func]

    @staticmethod
    def sum(__x: int, __y: int) -> int:
        return __x + __y

    @staticmethod
    def diff(__x: int, __y: int) -> int:
        return __x - __y

    @staticmethod
    def mult(__x: int, __y: int) -> int:
        return int(__x * __y)

    @staticmethod
    def int_div(__x: int, __y: int) -> int:
        return int(__x // __y)

    @staticmethod
    def int_square(__x: int) -> int:
        return int(__x ** 2)

    @staticmethod
    def generate_random_integers(level: int) -> IntList:
        if level in Task.LEVELS.keys():
            seed()
            min_int = Task.LEVELS[level]['min_int']
            max_int = Task.LEVELS[level]['max_int']
            return [randint(min_int, max_int), randint(min_int, max_int)]

        raise ValueError('No integer were found for problem difficulty level {}.'.format(level))

    @staticmethod
    def generate_random_func(level) -> str:
        if level in Task.LEVELS.keys():
            seed()
            min_int = 0
            max_int = len(Task.LEVELS[level]['funcs']) - 1
            index = randint(min_int, max_int)
            return Task.LEVELS[level]['funcs'][index]

        raise ValueError('No operators were found for problem difficulty level {}.'.format(level))

    def get_result(self) -> int:
        if self.integers and self.func:
            if self.func == 'sum':
                return Task.sum(self.integers[0], self.integers[1])
            elif self.func == 'diff':
                return Task.diff(self.integers[0], self.integers[1])
            elif self.func == 'mult':
                return Task.mult(self.integers[0], self.integers[1])
            elif self.func == 'int_div':
                return Task.int_div(self.integers[0], self.integers[1])
            elif self.func == 'int_square':
                return Task.int_square(self.integers[0])
            else:
                raise ValueError('No solution could be found for operator {}.'.format(self.operator))

    def __str__(self):
        if self.operator == Task.OPERATOR_MAP['int_square']:
            return '{}'.format(self.integers[0])
        else:
            return '{} {} {}'.format(self.integers[0], self.operator, self.integers[1])


def is_valid_level(_in: str) -> bool:
    if len(_in) == 0:
        return False

    try:
        val = int(_in)
    except ValueError:
        return False
    else:
        return val in Task.LEVELS.keys()


def is_valid_answer(_in: str) -> bool:
    if len(_in) == 0:
        return False

    try:
        val = int(_in)
    except ValueError:
        return False
    else:
        return True


if __name__ == "__main__":
    # Ask for level until correct input is given
    level = 0

    while level not in (1, 2):
        print('Which level do you want? Enter a number:')
        for i in Task.LEVELS.keys():
            print('{} - {}'.format(i, Task.LEVELS[i]['description']))

        chosen_level = input().strip()

        if is_valid_level(chosen_level):
            task_level = int(chosen_level)
            correct_answers = 0
            for _ in range(5):
                task = Task(task_level)
                user_answer = ''
                while not is_valid_answer(user_answer):
                    print(task)
                    user_answer = input().strip()
                    if is_valid_answer(user_answer):
                        task_answer = int(user_answer)
                        if task_answer == task.get_result():
                            correct_answers += 1
                            print('Right!')
                        else:
                            print('Wrong!')
                    else:
                        print('Wrong format! Try again.')

            user_mark = '{}/5'.format(correct_answers)
            print('Your mark is {}. Would you like to save the result? Enter yes or no.'.format(user_mark))

            will_save = input().strip()

            if will_save in ('yes', 'YES', 'y', 'Yes'):
                try:
                    print('What is your name?')
                    user_name = input().strip()
                    with open('results.txt', 'a+') as f_out:
                        f_out.write('{}: {} in level {} ({})\n'.format(user_name, user_mark, task_level, Task.LEVELS[task_level]['description']))

                    print('The results are saved in "results.txt".')

                except (FileExistsError, FileNotFoundError, IOError):
                    print('Unexpected IO Error found.')

            break

        else:
            print('Incorrect format.')
