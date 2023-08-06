#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

import pytest  # noqa

from qary.clibot import CLIBot
from qary.skills.base import BotReply

__author__ = "SEE AUTHORS.md"
__copyright__ = "Hobson Lane"
__license__ = "The Hippocratic License, see LICENSE.txt (MIT + Do no Harm)"


def test_clibot_default():
    clibot = CLIBot()
    assert callable(clibot.reply)
    assert isinstance(clibot.reply('Hi'), BotReply)
    assert isinstance(clibot.reply('Hi').text, str)
    assert isinstance(clibot.reply('Hi')[1], str)


def test_clibot_eliza():
    clibot = CLIBot(skill_module_names='eliza')
    assert callable(clibot.reply)
    assert isinstance(clibot.reply('Hi'), BotReply)
    assert isinstance(clibot.reply('Hi').text, str)
    assert isinstance(clibot.reply('Hi')[1], str)


def test_clibot_glossary():
    clibot = CLIBot(skill_module_names='glossary')
    assert callable(clibot.reply)
    assert isinstance(clibot.reply('Hi'), BotReply)
    assert isinstance(clibot.reply('Hi').text, str)
    assert isinstance(clibot.reply('Hi')[1], str)
