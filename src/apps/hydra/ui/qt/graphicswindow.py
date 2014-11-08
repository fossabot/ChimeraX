from .qt import QtCore, QtGui, QtOpenGL, QtWidgets
from ...graphics import View

class Graphics_Window(View, QtGui.QWindow):
    '''
    A graphics window displays the 3-dimensional models.
    Routines that involve the window toolkit or event processing are handled by this class
    while routines that depend only on OpenGL are in the View base class.
    '''
    def __init__(self, session, parent=None):

        QtGui.QWindow.__init__(self)
        self.widget = w = QtWidgets.QWidget.createWindowContainer(self, parent)
        self.setSurfaceType(QtGui.QSurface.OpenGLSurface)       # QWindow will be rendered with OpenGL
#        w.setFocusPolicy(QtCore.Qt.ClickFocus)
        w.setFocusPolicy(QtCore.Qt.NoFocus)

        window_size = (w.width(), w.height())		# pixels
        View.__init__(self, session, window_size)

        self.set_stereo_eye_separation()

        self.opengl_context = None

        self.timer = None			# Redraw timer
        self.redraw_interval = 10               # milliseconds
        # TODO: Redraw interval is set fast enough for 75 Hz oculus rift.
        self.minimum_event_processing_ratio = 0.1   # Event processing time as a fraction of time since start of last drawing
        self.last_redraw_start_time = 0
        self.last_redraw_finish_time = 0

        from . import mousemodes
        self.mouse_modes = mousemodes.Mouse_Modes(self)
        self.enable_trackpad_events()

    def set_stereo_eye_separation(self, eye_spacing_millimeters = 61.0):
        # Set stereo eye spacing parameter based on physical screen size
        s = self.screen()
        ssize = s.physicalSize().width()        # millimeters
        psize = s.size().width()                # pixels
        self.camera.eye_separation_pixels = psize * (eye_spacing_millimeters / ssize)

    def enable_trackpad_events(self):
        # TODO: Qt 5.1 has touch events disabled on Mac
        #        w.setAttribute(QtCore.Qt.WA_AcceptTouchEvents)
        # Qt 5.2 has touch events disabled because it slows down scrolling.  Reenable them.
        import sys
        if sys.platform == 'darwin':
            from ... import mac_os_cpp
            mac_os_cpp.accept_touch_events(int(self.winId()))

    # QWindow method
    def resizeEvent(self, e):
        s = e.size()
        w, h = s.width(), s.height()
#
# TODO: On Mac retina display event window size is half of opengl window size.
#    Can scale width/height here, but also need mouse event positions to be scaled by 2x.
#    Not sure how to detect when app moves between non-retina and retina displays.
#    QWindow has a screenChanged signal but I did not get it in tests with Qt 5.2.
#    Also did not get moveEvent().  May need to get these on top level window?
#
#        r = self.devicePixelRatio()    # 2 on retina display, 1 on non-retina
#        w,h = int(r*w), int(r*h)
#
        self.window_size = w, h
        if not self.opengl_context is None:
            self.resize(w,h)

    # QWindow method
    def exposeEvent(self, event):
        if self.isExposed():
            self.draw_graphics()

    # QWindow method
    def keyPressEvent(self, event):

        # TODO: This window should never get key events since we set widget.setFocusPolicy(NoFocus)
        # but it gets them anyways on Mac in Qt 5.2 if the graphics window is clicked.
        # So we pass them back to the main window.
        self.session.main_window.event(event)
        
    def create_opengl_context(self, stereo = False):

        f = self.pixel_format(stereo)
        self.setFormat(f)
        self.create()

        self.opengl_context = c = QtGui.QOpenGLContext(self)
        c.setFormat(f)
        if not c.create():
            raise SystemError('Failed creating QOpenGLContext')
        c.makeCurrent(self)

        # Write a log message indicating OpenGL version
        s = self.session
        f = c.format()
        stereo = 'stereo' if f.stereo() else 'no stereo'
        s.show_info('OpenGL version %s, %s' % (self.opengl_version(), stereo))

        return c

    def pixel_format(self, stereo = False):

        f = QtGui.QSurfaceFormat()
        f.setMajorVersion(3)
        f.setMinorVersion(3)
        f.setDepthBufferSize(24);
        f.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        f.setStereo(stereo)
        return f

    def enable_opengl_stereo(self, enable):

        supported = self.opengl_context.format().stereo()
        if not enable or supported:
            return True

        msg = 'Stereo mode is not supported by OpenGL driver'
        s = self.session
        s.show_status(msg)
        s.show_info(msg)
        return False

    def make_opengl_context_current(self):
        c = self.opengl_context
        if c is None:
            self.opengl_context = c = self.create_opengl_context()
            self.start_update_timer()
        c.makeCurrent(self)

    def swap_opengl_buffers(self):
        self.opengl_context.swapBuffers(self)

    def start_update_timer(self):
        if self.timer is None:
            self.timer = t = QtCore.QTimer(self)
            t.timeout.connect(self.redraw_timer_callback)
            t.start(self.redraw_interval)

    def redraw_timer_callback(self):
        import time
        t = time.perf_counter()
        dur = t - self.last_redraw_start_time
        if t >= self.last_redraw_finish_time + self.minimum_event_processing_ratio * dur:
            # Redraw only if enough time has elapsed since last frame to process some events.
            # This keeps the user interface responsive even during slow rendering.
            self.last_redraw_start_time = t
            self.update_graphics()
            self.last_redraw_finish_time = time.perf_counter()

    def update_graphics(self):
        if self.isExposed():
            if not self.redraw():
                self.mouse_modes.mouse_pause_tracking()

class Secondary_Graphics_Window(QtGui.QWindow):
    '''
    A top level graphics window separate for the main window for example to render to Oculus Rift headset.
    It has its own opengl context that shares state with the main graphics window context.
    '''
    def __init__(self, title, session):

        self.session = session
        QtGui.QWindow.__init__(self)
        # Use main window as a parent so this window is closed if main window gets closed.
        parent = session.main_window
        self.widget = w = QtWidgets.QWidget.createWindowContainer(self, parent, QtCore.Qt.Window)
        self.setSurfaceType(QtGui.QSurface.OpenGLSurface)       # QWindow will be rendered with OpenGL
        w.setWindowTitle(title)
        w.show()

        shared_context = session.view.opengl_context
        self.opengl_context = self.create_opengl_context(shared_context)

    def close(self):
        self.opengl_context.deleteLater()
        self.opengl_context = None
        self.widget.close()
        self.widget = None
        
    def create_opengl_context(self, shared_context):

        f = self.pixel_format()
        self.setFormat(f)
        self.create()

        c = QtGui.QOpenGLContext(self)
        if not shared_context is None:
            c.setShareContext(shared_context)
        c.setFormat(f)
        if not c.create():
            raise SystemError('Failed creating QOpenGLContext')
        c.makeCurrent(self)
        return c

    def pixel_format(self, stereo = False):

        f = QtGui.QSurfaceFormat()
        f.setMajorVersion(3)
        f.setMinorVersion(3)
        f.setDepthBufferSize(24);
        f.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        f.setStereo(stereo)
        return f

    def make_opengl_context_current(self):
        c = self.opengl_context
        if c is None:
            self.opengl_context = c = self.create_opengl_context()
        c.makeCurrent(self)

    def swap_opengl_buffers(self):
        self.opengl_context.swapBuffers(self)

    def full_screen(self, width, height):
        d = self.session.application.desktop()
        ow = self.widget
        for s in range(d.screenCount()):
            g = d.screenGeometry(s)
            if g.width() == width and g.height() == height:
                ow.move(g.left(), g.top())
                break
        ow.resize(width,height)
        ow.showFullScreen()

    def move_window_to_primary_screen(self):
        d = self.session.application.desktop()
        s = d.primaryScreen()
        g = d.screenGeometry(s)
        ow = self.widget
        ow.showNormal()     # Exit full screen mode.  
        x,y = (g.width() - ow.width())//2, (g.height() - ow.height())//2
        def move_window(ow=ow, x=x, y=y):
            ow.move(x, y)
        # TODO: On Mac OS 10.9 going out of full-screen takes a second during which
        #   moving the window to the primary display does nothing.
        from ...ui.qt.qt import QtCore
        QtCore.QTimer.singleShot(1500, move_window)
