import os
import logging
from qary.skills.quiz import Skill
from qary.etl.utils import squash_wikititle as normalize_text

log = logging.getLogger(__name__)


__author__ = "SEE AUTHORS.md"
__copyright__ = "Jose Robins"
__license__ = "The Hippocratic License, see LICENSE.txt (MIT + Do no Harm)"
from qary.constants import DATA_DIR


class TestQuiz:
    """Tests to verify the yes_no.py module """

    DATA_FILE = os.path.join(DATA_DIR, 'testsets/dialog/intern_quiz.yml')

    def setup_class(self):
        pass

    def test1_welcome_state(self):
        """Tests the very first turn which puts the bot into welcome state """
        skill = Skill(datafile=self.DATA_FILE)
        str_expected = (
            'I\'m going to ask you a few questions about python to set a baseline on your python knowledge.'
            'This way you can see how much you learn over time.'
            'So don\'t worry if you don\'t know the answers, you will soon!'
            'Ready?'
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

    def test2_quiz_start_reponse_state(self):
        """Tests the 2nd turn to ensure that the player's affirmative response is accepted  """
        skill = Skill(datafile=self.DATA_FILE)
        str_start_expected = 'Rate your \'python\''
        str_start_expected = normalize_text(str_start_expected)
        player_reply = 'yes'
        state_expected = 'q0'
        skill.reply(None)
        responses_actual = skill.reply(player_reply)
        str_actual = responses_actual[0][1]
        str_actual = normalize_text(str_actual)
        substr_pos = str_actual.find(str_start_expected)
        assert substr_pos == 0
        assert skill.state == state_expected
        return

    def test3_quiz_part_way_reponse_state(self):
        """Tests the 3nd turn to ensure that things are chugging along smoothly  """
        skill = Skill(datafile=self.DATA_FILE)
        str_start_expected = 'Name one of your'
        str_start_expected = normalize_text(str_start_expected)
        player_replies = [None, 'yes', 'dummy']
        state_expected = 'q1'
        for reply in player_replies:
            responses_actual = skill.reply(reply)
        # noinspection PyUnboundLocalVariable
        str_actual = responses_actual[0][1]
        str_actual = normalize_text(str_actual)
        substr_pos = str_actual.find(str_start_expected)
        assert substr_pos == 0
        assert skill.state == state_expected
        return

    def test4_quiz_finish(self):
        """Tests the end of the quiz to ensure that there is a deterministic end to the world as
        we know it"""
        skill = Skill(datafile=self.DATA_FILE)
        str_start_expected = 'The quiz has been completed'
        str_start_expected = normalize_text(str_start_expected)
        player_replies = [None, 'yes']
        player_replies.extend(['foo'] * 9)
        state_expected = None
        for reply in player_replies:
            responses_actual = skill.reply(reply)
        # noinspection PyUnboundLocalVariable
        str_actual = responses_actual[0][1]
        str_actual = normalize_text(str_actual)
        substr_pos = str_actual.find(str_start_expected)
        assert substr_pos == 0
        assert skill.state == state_expected
        return
