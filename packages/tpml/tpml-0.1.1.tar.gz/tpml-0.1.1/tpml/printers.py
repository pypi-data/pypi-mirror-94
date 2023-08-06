from typing import Optional


class BColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ORANGEBACK = '\033[43m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def box_print(msg: str, col:Optional[str] = BColours.ENDC):
    """
    Small helper function to print messages to console in a centralised box.
    :param msg: Message to be placed in box
    :type msg: str
    """
    max_len = max(78, len(msg) + 10)
    print('{}'.format('-' * (max_len + 2)))
    print(f'|{col}{msg.center((max_len))}{BColours.ENDC}|')
    print('{}'.format('-' * (max_len + 2)))


def cprint(msg: str, col:Optional[str] =BColours):
    print(f'{col}{msg}{BColours.ENDC}')


def hline():
    print('-' * 80)
