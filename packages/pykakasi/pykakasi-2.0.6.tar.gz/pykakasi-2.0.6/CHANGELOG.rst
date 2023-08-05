==================
PyKakasi ChangeLog
==================

All notable changes to this project will be documented in this file.

Unreleased_
===========

Added
-----

Changed
-------

Fixed
-----

Deprecated
----------

Removed
-------

Security
--------

v2.0.6_ (7, Feb. 2021)
======================

Fixed
-----

* Hiragana for Age countersa(#116,#117)


v2.0.5_ (5, Feb. 2021)
======================

Changed
-------

* CLI: use argparse for option parse(#113)

Fixed
-----

* Handle 思った、言った、行った properly.(#114)
* CI: fix coveralls error

Deprecated
----------

* CI: drop travis-ci test and badge


v2.0.4_ (26, Nov. 2020)
=======================

Fixed
-----

* CLI: Fix -v and -h option crash on python 3.7 and before (#108).

v2.0.3_ (25, Nov. 2020)
=======================

Fixed
-----

* CLI: Fix -v and -h option crash (#108).


v2.0.2_ (23, Jul. 2020)
=======================

Fixed
-----

* Fix convert() to handle Katakana correctly.(#103)


v2.0.1_ (23, Jul. 2020)
=======================

Changed
-------

* Update setup.py, setup.cfg, tox.ini(#102)


Fixed
-----

* Fix convert() misses last part of a text (#99, #100)
* Fix CI, coverage, and coveralls configurations(#101)


v2.0.0_ (31, May. 2020)
=======================

Changed
-------

* Update test formatting.

v2.0.0b1_ (9, May. 2020)
========================

Changed
-------

* Update test.


v2.0.0a6_ (30, Mar. 2020)
=========================

Added
-----

* Understand more kanji variations.

Fixed
-----

* Fix IVS handling to return correct word length to consume.


v2.0.0a5_ (23, Mar. 2020)
=========================

Changed
-------

* Recognize UNICODE standard Ideographic Variation Selector(IVS) and transiliterate when used.(#97)


v2.0.0a4_ (20, Mar. 2020)
==========================

Added
-----

* Add type hinting.

Changed
-------

* Refactoring dictionary generation classes.
* call super() from wakati.__init__()
* test: detection whether tox or raw pytest by TOX_ENV environment variable.
  When raw pytest, generate dictionaries as fixture.
  Previous versions uses --runenv option for pytest.

Fixed
-----

* NewAPI: fix return value when empty input string.


`v2.0.0a3`_ (18, Mar. 2020)
===========================

Changed
-------

* Update test cases.

Fixed
-----

* Add guard for unknown symbol code point which lead NoneType error. 


`v2.0.0a2`_ (16, Mar. 2020)
===========================

Added
-----

* NewAPI: support kunrei and passport roman conversion rule.

Changed
-------

* CI: test by github actions

Fixed
-----

* Support an extended kana(#77)
  (U0001b150-U0001b152, U0001b164-U0001b167)

`v2.0.0a1`_ (14, Mar. 2020)
===========================

Added
-----

* Structured interface of Kakasi class.(#21)

Changed
-------

* Github workflows for packaging and release.(#91)

Fixed
-----

* fix data kakasidict.utf8: “本蓮沼”

Deprecated
----------

* Drop python 2.7 support.


`v1.2`_ (26, Sep, 2019)
=======================

Fixed
-----

* Fix out-of-index error when kana-dash is placed on first of same character group.(#85)

`v1.1`_ (16, Sep, 2019)
=======================

`v1.1b2`_ (14, Sep, 2019)
=========================

Fixed
-----

* Fix Long symble issue(#58) (thanks @northernbird and @ta9ya)


`v1.1b1`_ (6, Sep, 2019)
========================

Added
-----
* Add conversions: kya, kyu, kyo

Changed
-------
* Rewording README document

`v1.1a1`_ (8, Jul, 2019)
========================

Changed
-------

* pytest: now run on project root without tox, by generating
  dictionary as a test fixture.
* tox: run tox test with installed dictionary instead of
  a generated fixture.
* Optimize kana conversion function.
* Move kakasidict.py to src and conftest.py to tests

Fixed
-----

* Version naming follows PEP386.
* Sometimes fails to insert space after punctuation(#79).
* Special case in kana-roman passport conversion such as 'etchu' etc.



.. _Unreleased: https://github.com/miurahr/pykakasi/compare/v2.0.6...HEAD
.. _v2.0.6: https://github.com/miurahr/pykakasi/compare/v2.0.5...v2.0.6
.. _v2.0.5: https://github.com/miurahr/pykakasi/compare/v2.0.4...v2.0.5
.. _v2.0.4: https://github.com/miurahr/pykakasi/compare/v2.0.3...v2.0.4
.. _v2.0.3: https://github.com/miurahr/pykakasi/compare/v2.0.2...v2.0.3
.. _v2.0.2: https://github.com/miurahr/pykakasi/compare/v2.0.1...v2.0.2
.. _v2.0.1: https://github.com/miurahr/pykakasi/compare/v2.0.0...v2.0.1
.. _v2.0.0: https://github.com/miurahr/pykakasi/compare/v2.0.0b1...v2.0.0
.. _v2.0.0b1: https://github.com/miurahr/pykakasi/compare/v2.0.0a6...v2.0.0b1
.. _v2.0.0a6: https://github.com/miurahr/pykakasi/compare/v2.0.0a5...v2.0.0a6
.. _v2.0.0a5: https://github.com/miurahr/pykakasi/compare/v2.0.0a4...v2.0.0a5
.. _v2.0.0a4: https://github.com/miurahr/pykakasi/compare/v2.0.0a3...v2.0.0a4
.. _v2.0.0a3: https://github.com/miurahr/pykakasi/compare/v2.0.0a2...v2.0.0a3
.. _v2.0.0a2: https://github.com/miurahr/pykakasi/compare/v2.0.0a1...v2.0.0a2
.. _v2.0.0a1: https://github.com/miurahr/pykakasi/compare/v1.2...v2.0.0a1
.. _v1.2: https://github.com/miurahr/pykakasi/compare/v1.1...v1.2
.. _v1.1: https://github.com/miurahr/pykakasi/compare/v1.1b2...v1.1
.. _v1.1b2: https://github.com/miurahr/pykakasi/compare/v1.1b1...v1.1b2
.. _v1.1b1: https://github.com/miurahr/pykakasi/compare/v1.1a1...v1.1b1
.. _v1.1a1: https://github.com/miurahr/pykakasi/compare/v1.0c2...v1.1a1
