#
# 'register_command' is called by the toolshed on start up
#
def register_command(command_name, tool_info):
    from . import label
    label.register_title_command()
