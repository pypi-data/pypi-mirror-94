import tempfile

import pytest  # noqa
import logging
from qary.etl.dialog_parse import DialogTurns

log = logging.getLogger(__name__)


__author__ = "SEE AUTHORS.md"
__copyright__ = "Jose Robins"
__license__ = "The Hippocratic License, see LICENSE.txt (MIT + Do no Harm)"


#######################################################################
# Class-wide tests

def test_parse_lines1_simple():
    """pytest for a simple use case without states  """
    input_turns = ['Bot: Hi', 'Bot: Welcome', 'Player:Rdy', 'Bot:Awesome']
    expected = [
        {'state': None, 'player': [], 'bot': ['Hi', 'Welcome']},
        {'state': None, 'player': ['Rdy'], 'bot': ['Awesome']},
    ]
    dlg = DialogTurns(dialog_file=None)
    actual = dlg.parse_dialog_lines(input_turns)
    assert actual == expected
    return


def test_parse_lines1b_simple_file():  # sourcery skip: move-assign
    """pytest for a simple use case without states    """

    input_turns = [
        '#state: welcome',
        'Bot: Hi',
        'Bot: Welcome',
        'Player:Rdy',
        'Bot:Awesome',
        '#state:play',
        'Player: How many cats',
        'Bot: irrelevant',
    ]
    expected = [
        {'state': 'welcome', 'player': [], 'bot': ['Hi', 'Welcome']},
        {'state': 'welcome', 'player': ['Rdy'], 'bot': ['Awesome']},
        {'state': 'play', 'player': ['How many cats'], 'bot': ['irrelevant']},
    ]
    # with tempfile.TemporaryDirectory() as tmp_dir:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w') as input_file:
        input_file.write('\n'.join(input_turns))

    dlg = DialogTurns(dialog_file=input_file.name)
    actual = dlg.parse_dialog_lines()
    assert actual == expected
    return


def test_parse_lines2_sticky_state():
    """pytest for a use case with states where the state is sticky - i.e state information is
    carried over to subsequent turns till a new state is encountered"""
    input_turns = [
        '#state: welcome',
        'Bot: Hi',
        'Bot: Welcome',
        'Player:Rdy',
        'Bot:Awesome',
        '#state:play',
        'Player: How many cats',
        'Bot: irrelevant',
    ]
    expected = [
        {'state': 'welcome', 'player': [], 'bot': ['Hi', 'Welcome']},
        {'state': 'welcome', 'player': ['Rdy'], 'bot': ['Awesome']},
        {'state': 'play', 'player': ['How many cats'], 'bot': ['irrelevant']},
    ]
    dlg = DialogTurns(dialog_file=None)
    actual = dlg.parse_dialog_lines(input_turns)
    assert actual == expected
    return


def test_parse_lines3_non_sticky_state():
    """pytest for a use case with states where the state is NOT sticky - i.e state information is
    applied to only the turn immediately following the state comment line"""
    input_turns = [
        '#state: welcome',
        'Bot: Hi',
        'Bot: Welcome',
        'Player:Rdy',
        'Bot:Awesome',
        '#state:play',
        'Player: How many cats',
        'Bot: irrelevant',
    ]
    expected = [
        {'state': 'welcome', 'player': [], 'bot': ['Hi', 'Welcome']},
        {'state': None, 'player': ['Rdy'], 'bot': ['Awesome']},
        {'state': 'play', 'player': ['How many cats'], 'bot': ['irrelevant']},
    ]
    dlg = DialogTurns(dialog_file=None, sticky_state=False)
    actual = dlg.parse_dialog_lines(input_turns)
    assert actual == expected
    return


def test_format_json():
    """pytest for converting the dialog to json format    """
    import tempfile

    input_turns = ['Bot: Hi', 'Bot: Welcome', 'Player:Rdy', 'Bot:Awesome']
    expected = (
        '[{"state": null, "player": [], "bot": ["Hi", "Welcome"]}, '
        '{"state": null, "player": ["Rdy"], "bot": ["Awesome"]}]'
    )
    dlg = DialogTurns(dialog_file=None)
    dlg.parse_dialog_lines(input_turns)
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = f'{tmp_dir}/turns.json'
        actual = dlg.convert_turns_format(turns_format='json', save_filepath=filepath)
    # TODO: Read back the file and ensure the contents are valid
    assert actual == expected
    return


def test_format_json_file_ext():
    """pytest for converting the dialog to json format with the save_filepath indicating the
    format"""
    import tempfile

    input_turns = ['Bot: Hi', 'Bot: Welcome', 'Player:Rdy', 'Bot:Awesome']
    expected = (
        '[{"state": null, "player": [], "bot": ["Hi", "Welcome"]}, '
        '{"state": null, "player": ["Rdy"], "bot": ["Awesome"]}]'
    )
    dlg = DialogTurns(dialog_file=None)
    dlg.parse_dialog_lines(input_turns)
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = f'{tmp_dir}/turns.json'
        actual = dlg.convert_turns_format(save_filepath=filepath)
    # TODO: Read back the file and ensure the contents are valid
    assert actual == expected
    return


def test_format_csv():
    """pytest for converting the dialog to csv format    """
    import tempfile

    input_turns = ['Bot: Hi', 'Bot: Welcome', 'Player:Rdy', 'Bot:Awesome']
    expected = 'state,player,bot\n,[],"[\'Hi\', \'Welcome\']"\n,[\'Rdy\'],[\'Awesome\']\n'
    dlg = DialogTurns(dialog_file=None)
    dlg.parse_dialog_lines(input_turns)
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = f'{tmp_dir}/turns.csv'
        actual = dlg.convert_turns_format(turns_format='csv', save_filepath=filepath)
    # TODO: Read back the file and ensure the contents are valid
    assert actual.replace('\r', '') == expected  # normalize end of lines to just newlines
    return


def test_format_csv_file_ext():
    """pytest for converting the dialog to csv format with the save_filepath indicating the
    format"""
    import tempfile

    input_turns = ['Bot: Hi', 'Bot: Welcome', 'Player:Rdy', 'Bot:Awesome']
    expected = 'state,player,bot\n,[],"[\'Hi\', \'Welcome\']"\n,[\'Rdy\'],[\'Awesome\']\n'
    dlg = DialogTurns(dialog_file=None)
    dlg.parse_dialog_lines(input_turns)
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = f'{tmp_dir}/turns.csv'
        actual = dlg.convert_turns_format(save_filepath=filepath)
    # TODO: Read back the file and ensure the contents are valid
    assert actual.replace('\r', '') == expected  # normalize end of lines to just newlines
    return


def test_format_yaml():
    """pytest for converting the dialog to a yaml format    """
    import tempfile

    input_turns = ['Bot: Hi', 'Bot: Welcome', 'Player:Rdy', 'Bot:Awesome']
    expected = (
        '- bot:\n  - Hi\n  - Welcome\n  player: []\n  state: null\n- bot:\n  - Awesome\n  '
        'player:\n  - Rdy\n  state: null\n'
    )
    dlg = DialogTurns(dialog_file=None)
    dlg.parse_dialog_lines(input_turns)
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = f'{tmp_dir}/turns.yaml'
        actual = dlg.convert_turns_format(turns_format='yaml', save_filepath=filepath)
    # TODO: Read back the file and ensure the contents are valid
    assert actual.replace('\r', '') == expected  # normalize end of lines to just newlines
    return


def test_format_yaml_file_ext():
    """pytest for converting the dialog to yaml format with the save_filepath indicating the
    format"""

    import tempfile

    input_turns = ['Bot: Hi', 'Bot: Welcome', 'Player:Rdy', 'Bot:Awesome']
    expected = (
        '- bot:\n  - Hi\n  - Welcome\n  player: []\n  state: null\n- bot:\n  - Awesome\n  '
        'player:\n  - Rdy\n  state: null\n'
    )
    dlg = DialogTurns(dialog_file=None)
    dlg.parse_dialog_lines(input_turns)
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = f'{tmp_dir}/turns.yaml'
        actual = dlg.convert_turns_format(save_filepath=filepath)
    # TODO: Read back the file and ensure the contents are valid
    assert actual.replace('\r', '') == expected  # normalize end of lines to just newlines
    return

# Class-wide tests
#######################################################################

########################################################
# Corner case tests


def test_parse_comment_line_with_non_comment_data():
    """Test method response to a string which does not start with a '#'    """
    expected = {}
    dlg = DialogTurns(dialog_file=None)
    actual = dlg._parse_comment_line('state: welcome')
    assert actual == expected
    return


def test_parse_comment_line_with_plain_comments():
    """Test method response to a string which does not start with a '#'    """
    expected = {}
    dlg = DialogTurns(dialog_file=None)
    actual = dlg._parse_comment_line('# Indicates welcome state')
    assert actual == expected
    return


def test_parse_comment_line_with_non_state_meta():
    """Test method response to a string which has meta info other than state    """
    input_lines = ['# future_use: yes']
    expected = []
    dlg = DialogTurns(dialog_file=None)
    actual = dlg.parse_dialog_lines(input_lines)
    assert actual == expected
    return


def test_parse_lines_first_state_is_null():
    """pytest for a use case  where the first turn does not have a state"""
    input_turns = [
        '# First line is not a state',
        'Bot: Hi',
        'Bot: Welcome',
        '#state: welcome',
        'Player:Rdy',
        'Bot:Awesome',
        '#state:play',
        'Player: How many cats',
        'Bot: irrelevant',
    ]
    expected = [
        {'state': None, 'player': [], 'bot': ['Hi', 'Welcome']},
        {'state': 'welcome', 'player': ['Rdy'], 'bot': ['Awesome']},
        {'state': 'play', 'player': ['How many cats'], 'bot': ['irrelevant']},
    ]
    dlg = DialogTurns(dialog_file=None)
    actual = dlg.parse_dialog_lines(input_turns)
    assert actual == expected
    return

# Corner case tests
########################################################

########################################################
# TODO: Add tests to give coverage of various branch conditions in test_dialog_parse.py
