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

from chimerax.core.toolshed import BundleAPI

class _DistUIBundleAPI(BundleAPI):

    @staticmethod
    def initialize(session, bundle_info):
        """Install distance mouse mode"""
        if session.ui.is_gui:
            mm = session.ui.mouse_modes
            from .mouse_dist import DistMouseMode
            mm.add_mode(DistMouseMode(session))

bundle_api = _DistUIBundleAPI()
