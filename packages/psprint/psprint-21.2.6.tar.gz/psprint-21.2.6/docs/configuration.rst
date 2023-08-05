Although prefix can be defined on the fly by configuring ``**kwargs``, it
may be slow and should be avoided. Frequently used prefixes
should be declared in a configuration file located at standard
locations. Configuration file is in `yaml <https://yaml.org/spec/>`__
format.

Location of configuration files
-------------------------------

Configuration may be specified in any of the following locations:

Root (UNIX ONLY):
^^^^^^^^^^^^^^^^^

This is inhereted by all users of the system

``/etc/psprint/style.yml``

User (HOME):
^^^^^^^^^^^^

**This is discouraged.** Maintaining configuration files in ``$HOME`` is
a bad practice. Such configuration should be in ``$XDG_CONFIG_HOME``.

``$HOME/.psprintrc``

User (XDG_CONFIG_HOME):
^^^^^^^^^^^^^^^^^^^^^^^

This variable is generally set to ``$HOME/.config`` on unix-like
systems. Even if unset, we will still try the ``$HOME/.config``
directory.

``$XFG_CONFIG_HOME/psprint/style.yml``

Local:
^^^^^^

In the current working directory

``.psprintrc``

Configuration format
--------------------

Sections:
^^^^^^^^^

#. FLAGS

   Following variables may be set as boolean value forms (yes, true,
   false, no).

   - ``short``: Information prefix is short (1 character).
   - ``bland``: Information prefix lacks ansi style (color/gloss).
   - ``disabled``: Behave like python3 native print.
   - ``pad``: Information prefix is fixed length, padded with <space>.
     wherever necessary.
   - ``flush``: This is passed to python's print function.

   Following variables may be set to string values:

   - ``sep``: This is passed to python's native print function.
   - ``end``: This is passed to python's native print function.
   - ``file``: *Discouraged* ``STDOUT`` gets appended to ``file``. This may
     be risky as the file is opened out of context.
   - ``pref_max_len``: Maximum length of prefix

   .. code:: yaml

      FLAGS:
        # short: False
        pad: True
        flush: True
        # sep:
        # end:
        pref_max_len: 7

#. ``custom``

   The string ``custom`` is used as prefix index while calling print
   function.

   Following variables may be set as string names or integers
   (ANSI Terminal colors) [black, red, g, 5, light blue]

   - ``pref_color``: color of information prefix
   - ``pref_bgcol``: background of information prefix
   - ``text_color``: color of information text
   - ``text_bgcol``: background of information text

   Following variables may be set as strings or integers representing gloss
   [dim, b, 2]

   - ``pref_gloss``: brightness of information prefix
   - ``text_gloss``: brightness of information text

   Following variables may be set as str

   - ``pref``: character long information prefix string (long form)
   - ``pref_s``: 1 character information prefix (short form)
     *Remember to quote "" special characters*

   .. code:: yaml

      help:
        pref: HELP
        pref_s: "?"
        pref_color: yellow
        pref_bgcol: black
        pref_style: normal
        text_color: white
        text_style: normal
        text_bgcol: black
