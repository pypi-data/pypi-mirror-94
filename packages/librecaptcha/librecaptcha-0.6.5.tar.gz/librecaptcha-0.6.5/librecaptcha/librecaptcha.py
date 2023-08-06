# Copyright (C) 2017, 2019 taylor.fish <contact@taylor.fish>
#
# This file is part of librecaptcha.
#
# librecaptcha is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# librecaptcha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with librecaptcha.  If not, see <http://www.gnu.org/licenses/>.

from . import cli
from .errors import GtkImportError, UserError
from .recaptcha import ReCaptcha

__version__ = "0.6.5"


def _get_gui():
    try:
        from . import gui
    except GtkImportError as e:
        raise UserError(
            "Error: Could not load the GUI. Is PyGObject installed?\n"
            "Try (re)installing librecaptcha[gtk] with pip.\n"
            "For more details, add the --debug option.",
        ) from e
    return gui


def has_gui():
    try:
        from . import gui  # noqa: F401
    except GtkImportError:
        return False
    return True


def get_token(api_key, site_url, user_agent, *, gui=False, debug=False):
    rc = ReCaptcha(api_key, site_url, user_agent, debug=debug)
    ui = (_get_gui().Gui if gui else cli.Cli)(rc)
    uvtoken = None

    def callback(token):
        nonlocal uvtoken
        uvtoken = token
    ui.run(callback)
    return uvtoken
