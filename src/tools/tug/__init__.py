# vim: set expandtab ts=4 sw=4:

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

class _TugAPI(BundleAPI):

    @staticmethod
    def initialize(session, bundle_info):
        """Register steered md mouse mode."""
        if not session.ui.is_gui:
            return
        from . import tugatoms
        tugatoms.register_mousemode(session)

bundle_api = _TugAPI()
