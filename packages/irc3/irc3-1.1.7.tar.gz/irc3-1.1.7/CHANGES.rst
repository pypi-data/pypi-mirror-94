1.1.7 (2021-02-13)
==================

- Add sqlite storage.

- Escape string that are interpolated into the regular expressions.


1.1.6 (2020-05-13)
==================

- Allow to overrides config values via `os.environ`.


1.1.5 (2020-01-18)
==================

- Allow to use `irc3.rfc.*` as `iotype='out'`

- Use more pop in userlist to avoid bug when a weird event occurs

1.1.4 (2019-11-22)
==================

- Use pop in userlist to avoid bug when a weird event occurs

- Expend filename path in logger plugin

- Force latest venusian version


1.1.3 (2019-08-22)
==================

- Rename async plugin to asynchronious so we can use it with python3.7


1.1.2 (2019-02-28)
==================

- Allow to have more than one `[bot]` section in config file

- IrcString now allow to retrieve username/hostname from mask


1.1.1 (2018-09-22)
==================

- Do not show builtins command in help. Fixed #167


1.1.0 (2018-07-30)
==================

- Backward incompatibility: async is renamed to asynchronous for py37 compat
  (thanks to @JulienPalard)

- Except a KeyError on missing twitter configuration in social plugin

1.0.3 (2018-05-08)
==================

- Add web plugin to allow to POST messages to channel via http

- Add slack plugin

- Avoid bug in userlist when a user parts before join (twitch)

- Drop py33, py34 support

1.0.2 (2017-11-13)
==================

- Add `irc3.__main__` to allow `python -m irc3 config.ini`


1.0.1 (2017-11-11)
==================

- Add `command(error_format=callable)` argument.

- Add ${#} as a shorter alias for ${hash}.

- Bug fix in fifo plugin. We now remove the file first if it's not a pipe.

- Fix some irc3d issues with QUIT and KICK command


1.0.0 (2017-02-05)
==================

- Added storage.getlist()/setlist()

- Improve autocommands


0.9.8 (2017-01-03)
==================

- Command aliases support (#121)

- Add quakenet plugin (#99)

- Allow dash character in command


0.9.7 (2016-12-07)
==================

- Added ``bot.async_cmds.topic()``

- Use shlex to parse command args by default


0.9.6 (2016-10-24)
==================

- Fixed #118: ssl context.check_hostname must be False when using CERT_NONE


0.9.5 (2016-10-15)
==================

- ``.privmsg(nowait=True)`` now really don't wait

- clean up some old py2/3 compat code

0.9.4 (2016-09-15)
==================

- Added SASL Auth support

0.9.3 (2016-05-31)
==================

- New release due to release problem (broken pypi)


0.9.2 (2016-05-31)
==================

- Fixed flood_burst sending one extra line (#92)

0.9.1 (2016-05-22)
==================

- Added autojoin_delay option. Handle reload in autojoin plugin.

- Added flood_rate_delay option.

- Added --help and --version CLI options.

- Fixed #91 bug with command arguments and spaces

0.9.0 (2016-04-20)
==================

- WARNING: we do no longer support python2. python3.3+ is required.

- WARNING: realname is now username and userinfo is now realname in config

- Introduce some plugins: fifo, shell_commands, pager

- Add ``flood_burst`` and ``flood_rate`` options. Queue outgoing messages in a
  single queue handle by ``send_line('...', nowait=False)``.

- ``bot.async`` is now aliased to ``bot.async_cmds`` to be able to use ``await``

0.8.9 (2016-02-23)
==================

- use re.escape to escape command char


0.8.8 (2016-01-27)
==================

- logger plugin now take care of unicode


0.8.7 (2016-01-16)
==================

- fixed 76: split large messages using textwrap.wrap(). This will avoid RevQ
  exceeded.


0.8.6 (2016-01-07)
==================

- fix DCC stuff for python3.5

- added DCC examples at https://github.com/gawel/irc3/tree/master/examples


0.8.5 (2015-12-22)
==================

-  ${hash} is now replaced by # in config files. This allow to set real channel
   names.


0.8.4 (2015-11-29)
==================

- added basic support for IRCv3.2 tags

- fixed #78: plugin can be old style classes

- fixed #75: Ensure we send the PING and PONG data as trailing

- fixed #71: need to pass host and ip to dcc


0.8.3 (2015-11-04)
==================

- fix wheel metadata

- public command was not public if you're using a guard


0.8.2 (2015-11-01)
==================

- Added !help nonexistant error message

- Allow to hide commands from !help

- Don't reject commands with trailing spaces

- Allow to use coroutine guards

- Make commands case insensitive

- Add basic casefolding plugin

- Prevent keyerror when setting keys that don't exist in cache.

0.8.1 (2015-05-14)
==================

-  Fixes bug in userlist plugin `#59 <https://github.com/gawel/irc3/pull/59>`_

-  Strip out self.context.config.cmd from !help arg. Allow to use !help !cmd
   `#57 <https://github.com/gawel/irc3/pull/57>`_


0.8.0 (2015-04-19)
==================

- Added dcc send/get/chat implementation

- Improved storage: can now test the existence of a key

- irc.plugins.storage: `db['foo']` now will raise a `KeyError` if the key does
  not exist to match dictionary behaviour. This will **break** existing
  implementations that make use of this.

- irc.plugins.storage now supports `db.get(key)`  that will return either `None`
  or the value of an optional `default` argument.

- irc3.plugins.feeds is now full async


0.7.1 (2015-02-26)
==================

- Storage plugin documentation

- Support python 3.4.1 again


0.7.0 (2015-02-24)
==================

- the cron plugin now require
  `aiocron <https://pypi.python.org/pypi/aiocron/>`_

- Add `irc3.plugins.async`; Allow to `yield from bot.async.whois('gawel')`

- commands and events can now be coroutines


0.6.0 (2015-02-15)
==================

- Allow to reload modules/plugins

- Add storage plugin

- Fixed #34 Avoid newline injection.


0.5.3 (2014-12-09)
==================

- Bugfix release. Fixed #27 and #30


0.5.2 (2014-11-16)
==================

- Basic irc3d server

- Modules reorganisation

- Add S3 logger


0.5.1 (2014-07-21)
==================

- Fixed #13: venusian 1.0 compat

- Add antiflood option for the command plugin

- commands accept unicode


0.5.0 (2014-06-01)
==================

- Added ``bot.kick()`` and ``bot.mode()``

- Rewrite ctcp plugin so we can ignore flood requests

- Trigger ``{plugin}.server_ready()`` at the end of MOTD

- Fixed #9: The ``command`` plugin uses ``cmd``, not ``cmdchar``.

- Fixed #10. Store server config. Use STATUSMSG config if any in ``userlist``

- ``userlist`` plugin now also store user modes per channel.

- Rename ``add_event`` to ``attach_events`` and added ``detach_events``. This
  allow to add/remove events on the fly.

- The autojoin plugin now detach motd related events after triggering one of
  them.

- Fix compatibility with trollius 0.3


0.4.10 (2014-05-21)
===================

- Fixed #5: autojoin on no motd

- allow to show date/times in console log


0.4.9 (2014-05-08)
==================

- Allow to trigger event on output with ``event(iotype='out')``

- Add a channel logger plugin

- autojoins is now a separate plugin

- userlist plugin take care of kicks

- social plugin is now officially supported and tested


0.4.7 (2014-04-03)
==================

- IrcString use unicode with py2


0.4.6 (2014-03-11)
==================

- Bug fix. The cron need a loop sooner as possible.


0.4.5 (2014-02-25)
==================

- Bug fix. An event was run twice if more than one where using the same regexp


0.4.4 (2014-02-15)
==================

- Add cron plugin

- Improve the command plugin. Fix some security issue.

- Add ``--help-page`` option to generate commands help pages


0.4.3 (2014-01-10)
==================

- Fix a bug on connection_lost.

- Send realname in USER command instead of nickname


0.4.2 (2014-01-09)
==================

- python2.7 support.

- add some plugins (ctcp, uptime, feeds, search)

- add some examples/ (twitter, asterisk)

- improve some internals

0.4.1 (2013-12-30)
==================

- Depends on venusian 1.0a8


0.1 (2013-11-30)
================

- Initial release
