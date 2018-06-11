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

def register_command(logger):
    from chimerax.core.commands import CmdDesc, register, StringArg, BoolArg, run
    desc = CmdDesc(required=[('text', StringArg)],
                   optional=[('log', BoolArg),
                             ('downgrade_errors', BoolArg),
                         ],
                   synopsis='indirectly run a command')
    register('run', desc, run, logger=logger)