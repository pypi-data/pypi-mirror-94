Description
==============

Prompt-String-like Print.

<span style="background-color: black; color: green;">[ INFO ]</span><span style="background-color: black; color: white;">   Print statements with a flexible descriptor prefix for better readability.</span>


Documentation
==================

[![Documentation Status](https://readthedocs.org/projects/psprint/badge/?version=latest)](https://psprint.readthedocs.io/?badge=latest)

Source Code
================

[![source](https://github.githubassets.com/favicons/favicon.png)](https://github.com/pradyparanjpe/psprint.git)
[Repository](https://github.com/pradyparanjpe/psprint.git)


What does it do
=====================

```
#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

print()
print("*** WITHOUT PSPRINT ***")
print("An output statement which informs the user")
print("This statement requests the user to act")
print("A debugging output useless to the user")
print()

from psprint import print
print()
print("*** WITH PSPRINT ***")
print("An output statement which informs the user", mark=1)
print("This statement requests the user to act", mark=2)
print("A debugging output useless to the user", mark='bug')
print ()

```

Screenshot:

![screenshot](docs/output.jpg)
