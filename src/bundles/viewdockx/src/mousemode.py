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

from chimerax.mouse_modes import MouseMode
class NextDockingMouseMode(MouseMode):

  name = 'next docking'
  icon_file = 'nextdocking.png'

  def __init__(self, session):
    MouseMode.__init__(self, session)

    self._step_pixels = 50
    self._last_xy = None

  def mouse_down(self, event):
    self._last_xy = event.position()
  
  def mouse_drag(self, event):

    x,y = event.position()
    if self._last_xy is None:
      self._last_xy = (x,y)
      return

    lx,ly = self._last_xy
    dx,dy = x - lx, ly - y
    d = dx if abs(dx) > abs(dy) else dy
    if d >= self._step_pixels:
        step = 1
    elif d <= -self._step_pixels:
        step = -1
    else:
        return

    self._last_xy = (x,y)
    self._show_next(step)

  def mouse_up(self, event):
    self._last_xy = None
    
  def wheel(self, event):
    d = event.wheel_value()
    self._show_next(-int(d))

  def _show_next(self, step):
    if not self._viewdockx_running():
        return
    from chimerax.core.commands import run
    if step > 0:
      run(self.session, 'viewdockx down')
    elif step < 0:
      run(self.session, 'viewdockx up')

  def _viewdockx_running(self):
    from .tool import TableTool
    try:
      tool = TableTool.find(name = None)
    except KeyError:
      return False
    return tool is not None

  def vr_motion(self, position, move, delta_z):
    # Virtual reality hand controller motion.
    step = int(round(20*delta_z))
    if step == 0:
      return 'accumulate drag'
    self._show_next(step)

  def vr_thumbstick(self, xyz1, xyz2, step):
    # Virtual reality hand controller thumbstick tilt.
    self._show_next(step)

  # TODO: Add a vr_trackpad() method for use with Vive hand controllers
  #   so up/down can be done by clicking on different parts of the trackpad.
  
# -----------------------------------------------------------------------------
#
def register_mousemode(session):
    mm = session.ui.mouse_modes
    mm.add_mode(NextDockingMouseMode(session))