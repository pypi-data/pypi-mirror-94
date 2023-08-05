#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Prompt String-like Print
'''

import os
import sys
import typing
import pathlib
from .printer import PrintSpace


# Initiate default print function
def init_print(custom: str = None) -> PrintSpace:
    '''
    Initiate ps-print function with default marks
    and marks read from various psprintrc configurarion files:

    Args:
        custom: custom configuration file location

    '''
    # psprintrc file locations
    user_home = pathlib.Path(os.environ.get("HOME"))
    config = user_home.joinpath(".config")  # default
    rc_locations = {
        'root': pathlib.Path("/etc/psprint/style.yml"),
        'user': user_home.joinpath("." + "psprintrc"),  # bad habit
        'config': pathlib.Path(
            os.environ.get("XDG_CONFIG_HOME", str(config))
        ).joinpath("psprint", "style.yml"),  # good habit
        'local': pathlib.Path('.').resolve().joinpath("." + "psprintrc"),
        'custom': None,
    }

    if custom is not None:
        rc_locations['custom'] = pathlib.Path(custom)

    default_config = os.path.join(os.path.dirname(__file__), "style.yml")
    default_print = PrintSpace(config=default_config)

    for loc in ('root', 'user', 'config', 'local', 'custom'):
        # DONT: loc from tuple, not keys(), deliberately to ascertain order
        if rc_locations[loc] is not None and rc_locations[loc].exists():
            default_print.set_opts(rc_locations[loc])

    if 'idlelib.run' in sys.modules or not sys.stdout.isatty():
        # Running inside idle
        default_print.switches['bland'] = True
    return default_print



DEFAULT_PRINT = init_print()
'''
PrintSpace object created by reading defaults from various
psprintrc and psprint/style.yml files

'''

print = DEFAULT_PRINT.psprint
'''
psprint function for imports

'''


__all__ = ['DEFAULT_PRINT', 'print']


__version__ = "21.2.6"
