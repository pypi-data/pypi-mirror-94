import os
import tempfile

import pytest  # noqa
import logging
from qary.skills.yes_no import Skill
from qary.etl.utils import squash_wikititle as normalize_text

log = logging.getLogger(__name__)


__author__ = "SEE AUTHORS.md"
__copyright__ = "Jose Robins"
__license__ = "The Hippocratic License, see LICENSE.txt (MIT + Do no Harm)"
from qary.constants import DATA_DIR


class TestYesNo:
    """Tests to verify the yes_no.py module """

    DATA_FILE_MULTIPLE_CATS = os.path.join(
        DATA_DIR, 'testsets/dialog/yes_no_multiple_cats_problem.txt'
    )

    def setup_class(self):
        pass

    def test1_welcome_state(self):
        """Tests the very first turn which puts the bot into welcome state """
        skill = Skill(datafile=self.DATA_FILE_MULTIPLE_CATS)
        str_expected = (
            'A woman went on vacation and asked a friend to look after her cat. A week later, 8 grown cats were living in the apartment.\n'
            'Let\'s see how fast you can solve this mystery by asking me questions. The fewer questions you ask the better player you are.\n'
            'Remember: I can only answer with "yes" or "no". Or, sometimes. with "irrelevant".'
            '\nLet\'s play! Ready?'
        )
        str_expected = normalize_text(str_expected)
        responses_expected = [(1.0, str_expected)]
        state_expected = 'welcome'
        responses_actual = skill.reply(None)
        str_actual = responses_actual[0][1]
        str_actual = normalize_text(str_actual)
        responses_actual = [(responses_actual[0][0], str_actual)]
        assert responses_actual == responses_expected
        assert skill.state == state_expected

    def test2_play_state(self):
        """Tests the second turn where the bot will go into the play state"""
        skill = Skill(datafile=self.DATA_FILE_MULTIPLE_CATS)
        str_expected = [
            'Great! Ask me your first question.',
            'Remember: each question should bring you closer to solving the puzzle.',
        ]
        str_expected = ''.join(str_expected)
        str_expected = normalize_text(str_expected)
        responses_expected = [(1.0, str_expected)]
        state_expected = 'play'
        skill.reply(None)
        responses_actual = skill.reply('Yes')
        str_actual = responses_actual[0][1]
        str_actual = normalize_text(str_actual)
        responses_actual = [(responses_actual[0][0], str_actual)]
        assert responses_actual == responses_expected
        assert skill.state == state_expected

    def test3_play_state(self):
        """Tests other play turns """
        skill = Skill(datafile=self.DATA_FILE_MULTIPLE_CATS)
        str_player1 = 'Yes'
        str_player2 = 'Did the cat go missing and have babies and came back?'
        str_expected = [
            'It appears that your question consists of multiple questions.',
            'Can you break that question up into different questions?',
        ]
        str_expected = ''.join(str_expected)
        str_expected = normalize_text(str_expected)
        responses_expected = [(1.0, str_expected)]
        state_expected = 'play'
        skill.reply(None)
        skill.reply(str_player1)
        responses_actual = skill.reply(str_player2)
        str_actual = responses_actual[0][1]
        str_actual = normalize_text(str_actual)
        responses_actual = [(responses_actual[0][0], str_actual)]
        assert responses_actual == responses_expected
        assert skill.state == state_expected

    def test4_final_state(self):
        """Tests  the final play """
        skill = Skill(datafile=self.DATA_FILE_MULTIPLE_CATS)
        str_player1 = 'Yes'
        str_player2 = 'Did he think that the lady would recognize her cat among these 8 cats?'
        str_expected = [
            'Yes.',
            'Kudos! You solved it!',
            'The next day this cat ran away, and the friend had to start looking for it.',
            'Since he did not know the cat very well, he had to keep all the similar cats that he had seen and wait for the friend who was supposed to identify the right pet.',
            'You solved this puzzle with 22 questions.',
            'You\'re in top 30% of the "8 cats" puzzle conquerors!',
            'Most of the players used more ' 'than 22 questions to solve this puzzle!',
            'Keep training your lateral thinking and deductive logic skills!',
            'I have tons of puzzles for you.',
            'Type "m" if you\'d like to crack another one.',
        ]
        str_expected = ''.join(str_expected)
        str_expected = normalize_text(str_expected)
        responses_expected = [(1.0, str_expected)]
        state_expected = None
        skill.reply(None)
        skill.reply(str_player1)
        responses_actual = skill.reply(str_player2)
        str_actual = responses_actual[0][1]
        str_actual = normalize_text(str_actual)
        responses_actual = [(responses_actual[0][0], str_actual)]
        assert responses_actual == responses_expected
        assert skill.state == state_expected
