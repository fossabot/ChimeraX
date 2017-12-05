# vim: set expandtab shiftwidth=4 softtabstop=4:

from chimerax.core.toolshed import BundleAPI


class _MyAPI(BundleAPI):

    api_version = 1

    @staticmethod
    def start_tool(session, bi, ti):
        if ti.name == "ViewDockX":
            from .tool import ViewDockTool
            return ViewDockTool(session, ti.name)
        else:
            raise ValueError("trying to start unknown tool: %s" % ti.name)

    @staticmethod
    def register_command(bi, ci, logger):
        if ci.name == "viewdockx":
            from . import cmd
            func = cmd.viewdock
            desc = cmd.viewdock_desc
        else:
            raise ValueError("trying to register unknown command: %s" % ci.name)
        if desc.synopsis is None:
            desc.synopsis = ci.synopsis
        from chimerax.core.commands import register
        register(ci.name, desc, func)

    @staticmethod
    def open_file(session, stream, file_name, auto_style=True):
        from .io import open_mol2
        return open_mol2(session, stream, file_name, auto_style)


bundle_api = _MyAPI()