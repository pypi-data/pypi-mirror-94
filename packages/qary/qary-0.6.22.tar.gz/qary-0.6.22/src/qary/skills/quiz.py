""" Pattern and template based chatbot dialog engines """
import logging
import os

import yaml
from qary.constants import DATA_DIR
from qary.etl.utils import squash_wikititle as normalize_text

# FIXME: make this a config option
INTERN_QUIZ = os.path.join(DATA_DIR, 'yes_no/intern_quiz.yml')


log = logging.getLogger(__name__)


def load(datafile):
    """Loads a datafile (currently only json) and creates a turns datastructure
    >>> datafile = INTERN_QUIZ
    >>> load(datafile) # doctest: +ELLIPSIS
    [{'state': 'welcome', 'bot': ["I'm...
    """
    with open(datafile, 'r') as infile:
        turns = yaml.load(infile, Loader=yaml.SafeLoader)
    # make lower case all keys in the dictlist
    turns_new = []
    for turn_old in turns:
        turn = {key.lower(): value for key, value in turn_old.items()}
        turn['state'] = turn['state'].lower()  # states also make lower for ease of use
        turns_new.append(turn)
    return turns_new


class Skill:
    r"""Skill for Quiz"""

    def __init__(self, datafile=None):
        """ """
        datafile = datafile or INTERN_QUIZ
        self.turns = load(datafile)
        self.welcome_turn = [turn for turn in self.turns if turn['state'] == 'welcome'].pop()
        self.state = None
        self.current_idx = None
        return

    def reply(self, statement, context=None):
        r"""Except for the welcome state, all other states are mere recordings of the quiz responses

        Examples:
            #TODO
        """
        if self.state in (None, False, 0, '', ''.encode(), '0', 'none', 'None'):
            self.current_idx = 0
            current_turn = self.turns[self.current_idx]
            self.state = current_turn['state']
            response = '\n'.join(current_turn['bot'])
        elif self.state == 'welcome':
            yes_responses = [normalize_text(text) for text in self.welcome_turn['player']]
            if normalize_text(statement) in yes_responses:
                self.current_idx += 1
                current_turn = self.turns[self.current_idx]
                self.state = current_turn['state']
                response = '\n'.join(current_turn['bot'])
            else:
                response = 'Please answer "yes" or "quit" to exit'
        else:
            if self.current_idx < len(self.turns) - 1:
                self.current_idx += 1
                current_turn = self.turns[self.current_idx]
                self.state = current_turn['state']
                response = '\n'.join(current_turn['bot'])
            else:
                response = 'The quiz has been completed. Have a good day'
                self.state = None
        return [(1.0, response)]


# def main():
#     b = Skill()
#     response = b.reply(None)
#     response = b.reply('yes')
#     response = b.reply('Did the cat go missing and have babies and came back?')
#     response = b.reply('Did he think that the lady would recognize her cat among these 8 cats?')

#     return


# if __name__ == '__main__':
#     main()


# def xtest_current():
#     s = Skill()
#     response = s.reply(None)
#     print(response)
#     return
