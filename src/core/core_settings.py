# vi: set expandtab shiftwidth=4 softtabstop=4:
"""
preferences: manage preferences
===============================

TODO
"""
from .commands import cli
from .commands import color
from . import configfile
from .settings import Settings
_prefs = None


class _CoreSettings(Settings):

    EXPLICIT_SAVE = {
        'bg_color': configfile.Value(
            color.Color('#000'), color.ColorArg, color.Color.hex_with_alpha),
        'multisample_threshold': configfile.Value(
            0, cli.NonNegativeIntArg, str),
        'silhouette': False,
        # autostart map_series_gui until alternate means of installing
        # trigger is found
        'autostart': ['cmd_line', 'mouse_modes', 'log', 'sideview', 'map_series_gui'],
    }

def init(session):
    global settings
    settings = _CoreSettings(session, "chimera.core")
