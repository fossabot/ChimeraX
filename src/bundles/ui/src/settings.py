# vim: set expandtab shiftwidth=4 softtabstop=4:

# === UCSF ChimeraX Copyright ===
# Copyright 2016 Regents of the University of California.
# All rights reserved.  This software provided pursuant to a
# license agreement containing restrictions on its disclosure,
# duplication and use.  For details see:
# http://www.rbvi.ucsf.edu/chimerax/docs/licensing.html
# This notice must be embedded in or attached to all copies,
# including partial copies, of the software or any revisions
# or derivations thereof.
# === UCSF ChimeraX Copyright ===

from chimerax.core.settings import Settings

class UI_Settings(Settings):

    EXPLICIT_SAVE = {
        'auto_float_tools': False,
        'autostart': [
            'Log', 'Model Panel', 'Command Line Interface',
            'Toolbar',
        ],
        'default_tool_window_side': "right",
        'favorites': [],
        'initial_window_size': ("last used", None),
        'tool_positions': {'toolbars': {}, 'windows': {}},
        'undockable': [
            'Help Viewer',
        ],
    }

    AUTO_SAVE = {
        'last_window_size': None,
        'show_splash_screen': True,
    }

def register_settings_options(session):
    from .options import BooleanOption
    settings = session.ui.settings
    opt = BooleanOption('Show splash screen', settings.show_splash_screen, None,
                        attr_name='show_splash_screen', settings=settings,
                        balloon='Whether to show the splash screen when ChimeraX starts')
    session.ui.main_window.add_settings_option("Startup", opt)
