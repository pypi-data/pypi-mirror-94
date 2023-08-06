# -*- coding: utf-8 -*-
from unittest import TestCase
from irc3.utils import IrcString
from irc3.utils import maybedotted
from irc3.utils import split_message
from irc3.utils import parse_config_env
from irc3.utils import slugify
from irc3.testing import ini2config
import irc3.plugins


def test_hash():
    config = ini2config('''
[bot]
autojoins =
    ${hash}irc3
    ${hash}${hash}irc3
    ${#}irc3
''')
    assert config['autojoins'] == ['#irc3', '##irc3', '#irc3']


def test_config_env():
    config = ini2config('''
[bot]
nickname = bot
''', env={'IRC3_BOT_AUTOJOINS': '#irc3 ##irc3'})
    assert config['autojoins'] == ['#irc3', '##irc3']


class TestUtils(TestCase):

    def test_ircstring(self):
        s = IrcString('nick')
        self.assertTrue(s.is_nick)
        self.assertEqual(s.nick, 'nick')
        self.assertEqual(s.host, None)

        s = IrcString('nick!user@host')
        self.assertTrue(s.is_user)
        self.assertTrue(s.is_nick)
        self.assertEqual(s.nick, 'nick')
        self.assertEqual(s.host, 'user@host')
        self.assertEqual(s.username, 'user')
        self.assertEqual(s.hostname, 'host')

        s = IrcString('#chan')
        self.assertTrue(s.is_channel)
        s = IrcString('&chan')
        self.assertTrue(s.is_channel)

        s = IrcString('*')
        self.assertTrue(s.is_server)

    def test_maybedotted(self):
        self.assertTrue(
            maybedotted('irc3.plugins') is irc3.plugins)
        self.assertTrue(
            maybedotted('irc3.utils.IrcString') is IrcString)
        self.assertTrue(
            maybedotted(IrcString) is IrcString)
        self.assertRaises(LookupError, maybedotted, 'irc3.none.none')
        self.assertRaises(LookupError, maybedotted, 'irc3.none')
        self.assertRaises(LookupError, maybedotted, None)
        self.assertRaises(LookupError, maybedotted, '')

    def test_slugify(self):
        assert slugify('a test file .rst') == 'a-test-file.rst'
        assert slugify('a test/../ file .rst') == 'a-test.file.rst'
        assert slugify('C:\\\\a test\../ file .rst') == 'ca-test.file.rst'


class TestConfig(TestCase):

    def test_config_env(self):
        value = parse_config_env({
            'IRC3_BOT_NICKNAME': 'env_nickname',
            'IRC3_BOT_PASSWORD': 'env_password',
        })
        self.assertEqual(value, {
            'bot': {
                'nickname': 'env_nickname',
                'password': 'env_password',
            },
        })


class TestSplit(TestCase):

    def callFTU(self, messages, max_length=10):
        return list(split_message(' '.join(messages), max_length))

    def test_split_message(self):
        messages = ['allo', 'alloallo']
        self.assertEqual(messages, self.callFTU(messages))
        messages = ['allo\t', 'alloallo']
        self.assertEqual([m.strip() for m in messages], self.callFTU(messages))
        messages = ['\x1d \x1f']
        self.assertEqual(messages, self.callFTU(messages))
