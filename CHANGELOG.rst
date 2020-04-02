`Unreleased`_
-------------

`0.2.0`_ - 2020-04-02
---------------------

Changed:
~~~~~~~~

* Use latest ``reportlab`` instead of previously fixed v3.5.18
* Local copy of ``rst2pdf`` updated to v0.96 and patched
* Moved onto the Python 3 with no regret

`0.1.2`_ - 2019-05-14
---------------------

Fixed:
~~~~~~

* Set ``reportlab`` version to v3.2.18 due to https://github.com/rst2pdf/rst2pdf/issues/773 and https://github.com/rst2pdf/rst2pdf/issues/772
* Added ``six`` package to the dependencies list
* Windows: Fixed "Permission denied" error while opening temp files
* Windows: Added workaround for Jijnja2 finds template file by absolute path

`0.1.1`_ - 2019-04-19
---------------------

Fixed:
~~~~~~

* YAML loading is safe now (see https://msg.pyyaml.org/load)
* Generated stylesheet JSON files became temporary

`0.1.0`_ - 2019-02-01
---------------------

* Initial version

.. _`Unreleased`: https://github.com/doker-project/doker/compare/v0.2.0...HEAD
.. _`0.2.0`: https://github.com/doker-project/doker/compare/v0.1.2...v0.2.0
.. _`0.1.2`: https://github.com/doker-project/doker/compare/v0.1.1...v0.1.2
.. _`0.1.1`: https://github.com/doker-project/doker/compare/v0.1.0...v0.1.1
.. _`0.1.0`: https://github.com/doker-project/doker/releases/tag/v0.1.0
