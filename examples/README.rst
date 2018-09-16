Examples
========

In order to test the example enter to the correspondent directory and run::

  doker --pdf <project-name>

Minimal
-------

* Description: Generating the minimal PDF document
* Project file: `minimal.yaml <minimal/minimal.yaml>`__
* reStructuredText source file: `main.rst <minimal/main.rst>`__
* Output: `minimal.pdf <minimal/minimal.pdf>`__

Styled
-------

* Description: Generating the PDF document using stylesheet
* Project file: `styled.yaml <styled/styled.yaml>`__
* reStructuredText source file: `main.rst <styled/main.rst>`__
* Stylesheet file: `stylesheet.yaml <styled/stylesheet.yaml>`__
* Output: `styled.pdf <styled/styled.pdf>`__

Cover
-----

* Description: Generating the PDF document with cover page
* Project file: `cover.yaml <cover/cover.yaml>`__
* reStructuredText source file: `main.rst <cover/main.rst>`__
* Cover file: `cover.rst <cover/cover.rst>`__
* Stylesheet file: `stylesheet.yaml <cover/stylesheet.yaml>`__
* Output: `cover.pdf <cover/cover.pdf>`__

Fonts
-----

* Description: Generating the PDF document with custom fonts
* Project file: `fonts.yaml <fonts/fonts.yaml>`__
* reStructuredText source file: `main.rst <fonts/main.rst>`__
* Fonts install script: `install-fonts.sh <fonts/install-fonts.sh>`__
* Stylesheet file: `stylesheet.yaml <fonts/stylesheet.yaml>`__
* Output: `fonts.pdf <fonts/fonts.pdf>`__

TOC
---

* Description: Generating the PDF document with table of contents
* Project file: `toc.yaml <toc/toc.yaml>`__
* reStructuredText source file: `main.rst <toc/main.rst>`__
* Stylesheet file: `stylesheet.yaml <toc/stylesheet.yaml>`__
* Output: `toc.pdf <toc/toc.pdf>`__
