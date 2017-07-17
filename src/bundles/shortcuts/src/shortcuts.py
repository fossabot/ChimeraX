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

def register_shortcuts(keyboard_shortcuts):
    '''Register the standard keyboard shortcuts.'''

    ks = keyboard_shortcuts
    scuts, catcols = standard_shortcuts(ks.session)
    for sc in scuts:
        ks.add_shortcut(sc)

    ks.category_columns = catcols

    return ks

def standard_shortcuts(session):

    # Shortcut documentation categories
    mapcat = 'Map Display'
    molcat = 'Molecule Display'
    surfcat = 'Surfaces'
    gcat = 'General Controls'
    ocat = 'Open, Save, Close'
    catcols = ((ocat,mapcat,surfcat), (molcat,), (gcat,))

    maparg = {'each_map':True}
    molarg = {'each_molecule':True}
    atomsarg = {'atoms_arg': True}
    surfarg = {'each_surface':True}
    viewarg = {'view_arg':True}
    mmarg = {'mouse_modes_arg':True}
    noarg = {}
    sesarg = {'session_arg':True}

    fmenu = 'File'
    smenu = 'Scene'
    mmenu = 'Map'
    mlmenu = 'Molecule'
    sfmenu = 'Surface'
    pmenu = 'Panes'
    msmenu = 'Mouse'
    dmenu = 'Device'
    hmenu = 'Help'
    s = session

    sep = True  # Add menu separator after entry.
#    from ..files import opensave
#    from .. import ui
    shortcuts = [
        # Sessions
#        ('op', ui.show_open_file_dialog, 'Open file', ocat, sesarg, fmenu),
#        ('rf', show_file_history, 'Show recent files', ocat, sesarg, fmenu),
#        ('Sv', opensave.save_session, 'Save session', ocat, sesarg, fmenu),
#        ('sv', ui.save_session_dialog, 'Save session as...', ocat, sesarg, fmenu),
#        ('si', lambda s: opensave.save_image(None,s), 'Save image', ocat, sesarg, fmenu),
        ('Ca', 'close', 'Close all models', ocat, noarg, fmenu),
        ('Qt', 'quit', 'Quit', ocat, noarg, fmenu),

        # Scene
        ('va', 'view', 'View all', gcat, noarg, smenu),
        ('dv', 'view orient true', 'Default orientation', gcat, noarg, smenu),
#        ('Sp', save_position, 'Save position, restore it with pp', gcat, sesarg, smenu),
#        ('pp', restore_position, 'Restore previous position saved with Sp', gcat, sesarg, smenu, sep),

#        ('dA', display_all_positions, 'Display all copies', gcat, sesarg, smenu),
        ('dm', 'show selModels models', 'Display selected models', ocat, noarg, smenu),
        ('hm', 'hide selModels models', 'Hide selected models', ocat, noarg, smenu),
        ('Ds', 'close sel', 'Delete selected models', ocat, noarg, smenu, sep),
        ('cs', 'select clear', 'Clear selection', gcat, noarg, smenu),

        ('bk', 'set bg black', 'Black background', gcat, noarg, smenu),
        ('wb', 'set bg white', 'White background', gcat, noarg, smenu),
        ('gb', 'set bg gray', 'Gray background', gcat, noarg, smenu, sep),

        ('dq', depth_cue, 'Toggle depth cue', gcat, viewarg, smenu),
        ('bl', motion_blur, 'Toggle motion blur', gcat, viewarg, smenu, sep),

        ('sh', toggle_shadows, 'Toggle shadows', gcat, sesarg, smenu),
        ('se', toggle_silhouettes, 'Toggle silhouette edges', gcat, sesarg, smenu),
        ('la', 'lighting soft', 'Ambient lighting', gcat, noarg, mlmenu),
        ('lf', 'lighting full', 'Full lighting', gcat, noarg, mlmenu),
        ('ls', 'lighting simple', 'Simple lighting', gcat, noarg, mlmenu),
        ('lF', 'lighting flat', 'Flat lighting', gcat, noarg, mlmenu),

        ('sx', save_image, 'Save snapshot', gcat, sesarg, mlmenu),
        ('vd', save_spin_movie, 'Record spin movie', gcat, sesarg, mlmenu),
#        ('Mo', mono_mode, 'Set mono camera mode', gcat, viewarg, smenu),
#        ('So', stereo_mode, 'Set sequential stereo mode', gcat, viewarg, smenu, sep),

#        ('uh', undisplay_half, 'Undisplay z > 0', gcat, sesarg, smenu),
        ('rt', show_framerate, 'Show framerate', gcat, sesarg, smenu),
        ('nt', show_triangle_count, 'Show scene triangle count', gcat, sesarg, smenu),

        # Maps
        ('sM', 'volume selMaps show', 'Show map', mapcat, noarg, mmenu),
        ('hM', 'volume selMaps hide', 'Hide map', mapcat, noarg, mmenu),
        ('ft', fit_molecule_in_map, 'Fit molecule in map', mapcat, sesarg, mmenu),
        ('fT', fit_map_in_map, 'Fit map in map', mapcat, sesarg, mmenu),
        ('fs', fit_subtract, 'Fit molecule in map subtracting other molecules', mapcat, sesarg, mmenu),
        ('sb', subtract_maps, 'Subtract map from map', mapcat, sesarg, mmenu),
        ('gf', smooth_map, 'Smooth map', mapcat, sesarg, mmenu),
        ('fr', 'volume selMaps step 1', 'Show map at full resolution', mapcat, noarg, mmenu),
        ('ob', toggle_outline_box, 'Toggle outline box', mapcat, maparg, mmenu, sep),

        ('fl', 'volume selMaps style surface', 'Show map or surface in filled style', mapcat, noarg, mmenu),
        ('me', 'volume selMaps style mesh', 'Show map or surface as mesh', mapcat, noarg, mmenu),
        ('gs', 'volume selMaps style solid', 'Show map as grayscale', mapcat, noarg, mmenu, sep),

        ('s1', 'volume selMaps step 1', 'Show map at step 1', mapcat, noarg, mmenu, sep),
        ('s2', 'volume selMaps step 2', 'Show map at step 2', mapcat, noarg, mmenu, sep),
        ('s4', 'volume selMaps step 4', 'Show map at step 4', mapcat, noarg, mmenu, sep),

        ('pl', show_one_plane, 'Show one plane', mapcat, maparg, mmenu),
        ('pa', show_all_planes, 'Show all planes', mapcat, maparg, mmenu),
        ('o3', toggle_orthoplanes, 'Show 3 orthogonal planes', mapcat, maparg, mmenu),
        ('bx', toggle_box_faces, 'Show box faces', mapcat, maparg, mmenu),
        ('mc', mark_map_surface_center, 'Mark map surface center', mapcat, maparg, mmenu),

        # Molecules
        ('da', 'show selAtoms', 'Show atoms', molcat, noarg, mlmenu),
        ('ha', 'hide selAtoms', 'Hide atoms', molcat, noarg, mlmenu, sep),

        ('bs', 'style selAtoms ball', 'Display atoms in ball and stick', molcat, noarg, mlmenu),
        ('sp', 'style selAtoms sphere', 'Display atoms in sphere style', molcat, noarg, mlmenu),
        ('st', 'style selAtoms stick', 'Display atoms in stick style', molcat, noarg, mlmenu, sep),

        ('rb', 'show selAtoms ribbon', 'Display ribbon', molcat, noarg, mlmenu),
        ('hr', 'hide selAtoms ribbon', 'Undisplay ribbon', molcat, noarg, mlmenu),
#        ('r+', fatter_ribbons, 'Thicker ribbons', molcat, molarg, mlmenu),
#        ('r-', thinner_ribbons, 'Thinner ribbons', molcat, molarg, mlmenu, sep),

#        ('la', show_ligands, 'Show ligand atoms', molcat, molarg, mlmenu),
        ('sw', 'show solvent', 'Show water atoms', molcat, noarg, mlmenu),
        ('hw', 'hide solvent', 'Hide water atoms', molcat, noarg, mlmenu, sep),

        ('db', 'show selAtoms bonds', 'Display bonds', molcat, noarg, mlmenu),
        ('hb', 'hide selAtoms bonds', 'Hide bonds', molcat, noarg, mlmenu),

        ('Hb', 'color selAtoms halfbond true', 'Half bond coloring', molcat, noarg, mlmenu),
        ('Sb', 'color selAtoms halfbond false', 'Single color bonds', molcat, noarg, mlmenu),

#        ('c1', color_one_color, 'Color molecule one color', molcat, molarg, mlmenu),
        ('cc', 'color selAtoms bychain', 'Color chains', molcat, noarg, mlmenu, sep),
        ('ce', 'color selAtoms byhet', 'Color non-carbon atoms by element', molcat, noarg, mlmenu),
        ('rc', 'color selAtoms random', 'Random color atoms and residues', molcat, noarg, mlmenu),
        ('bf', color_by_bfactor, 'Color by bfactor', molcat, atomsarg, mlmenu),

        ('ms', 'show selAtoms surface', 'Show molecular surface', molcat, noarg, mlmenu),
        ('sa', 'sasa selAtoms', 'Compute solvent accesible surface area', molcat, noarg, mlmenu, sep),

        ('xm', lambda m,s=s: minimize_crosslinks(m,s), 'Minimize link lengths', molcat, atomsarg, mlmenu),

#        ('bu', lambda m,s=s: show_biological_unit(m,s), 'Show biological unit', molcat, molarg, mlmenu),
#        ('au', lambda m,s=s: show_asymmetric_unit(m,s), 'Show asymmetric unit', molcat, molarg, mlmenu),

#        ('mb', lambda m,s=s: molecule_bonds(m,s), 'Compute molecule bonds using templates', molcat, molarg),

        # Surfaces
        ('ds', display_surface, 'Display surface', surfcat, sesarg, sfmenu),
        ('hs', 'hide selAtoms surface', 'Hide surface', surfcat, noarg, sfmenu),
# TODO: hs used to also hide non-molecular surfaces.
#        ('hs', hide_surface, 'Hide surface', surfcat, sesarg, sfmenu),
# TODO: Show filled and mesh used to work on surfaces, now only maps.
        ('sf', show_filled, 'Show map or surface in filled style', mapcat, sesarg, mmenu),
        ('sm', show_mesh, 'Show surface as mesh', mapcat, sesarg, mmenu),
        ('sd', show_dots, 'Show surface as dots', mapcat, sesarg, mmenu),
        ('tt', toggle_surface_transparency, 'Toggle surface transparency', surfcat, sesarg, sfmenu),
        ('t5', show_surface_transparent, 'Make surface transparent', surfcat, sesarg, sfmenu),
        ('t0', show_surface_opaque, 'Make surface opaque', surfcat, sesarg, sfmenu),

        # Pane
#        ('mp', ui.show_model_panel, 'Show model panel', ocat, sesarg, pmenu),
#        ('lg', show_log, 'Show command log', gcat, sesarg, pmenu),
#        ('gr', show_graphics_window, 'Show graphics window', gcat, sesarg, pmenu),
#        ('sc', show_scenes, 'Show scene thumbnails', gcat, sesarg, pmenu),
#        ('ch', show_command_history, 'Show command history', gcat, sesarg, pmenu),
        ('cl', command_line, 'Enter command', gcat, sesarg),

        # Mouse
        ('zm', enable_zoom_mouse_mode, 'Zoom mouse mode', gcat, mmarg, msmenu),
        ('mv', enable_move_mouse_mode, 'Movement mouse mode', gcat, mmarg, msmenu),
        ('mS', enable_move_selected_mouse_mode, 'Move selected mouse mode', gcat, mmarg, msmenu),
        ('mP', enable_move_planes_mouse_mode, 'Move planes mouse mode', mapcat, mmarg, msmenu),
        ('ct', enable_contour_mouse_mode, 'Adjust contour level mouse mode', mapcat, mmarg, msmenu),
        ('mk', enable_marker_mouse_mode, 'Place marker mouse mode', mapcat, mmarg, msmenu),
        ('mC', enable_mark_center_mouse_mode, 'Mark center mouse mode', mapcat, mmarg, msmenu),
        ('vs', enable_map_series_mouse_mode, 'Map series mouse mode', mapcat, mmarg, msmenu),
#        ('sl', selection_mouse_mode, 'Select models mouse mode', gcat, sesarg),

        # Devices
        ('sn', toggle_space_navigator, 'Toggle use of space navigator', gcat, sesarg, dmenu),
        ('nf', toggle_space_navigator_fly_mode, 'Toggle space navigator fly mode', gcat, sesarg, dmenu, sep),
#        ('nc', space_navigator_collisions, 'Toggle space navigator collision avoidance', gcat, sesarg),

        ('oc', start_oculus, 'Start Oculus Rift stereo', gcat, sesarg, dmenu),
#        ('om', oculus_move, 'Move Oculus window to primary display', gcat, sesarg, dmenu),

#        ('lp', toggle_leap, 'Toggle leap motion input device', gcat, sesarg, dmenu),
#        ('lP', leap_position_mode, 'Enable leap motion position mode', gcat, sesarg),
#        ('lx', leap_chopsticks_mode, 'Enable leap motion chopstick mode', gcat, sesarg),
#        ('lv', leap_velocity_mode, 'Enable leap motion velocity mode', gcat, sesarg),
#        ('lf', leap_focus, 'Check if app has leap focus', gcat, sesarg),
#        ('lq', leap_quit, 'Quit using leap motion input device', gcat, sesarg),

        # Help
#        ('mn', show_manual, 'Show manual', gcat, sesarg, hmenu),
#        ('ks', list_keyboard_shortcuts, 'List keyboard shortcuts', gcat, sesarg, hmenu),
        ]

#    from ..molecule.blastpdb import blast_shortcuts
#    shortcuts.extend(blast_shortcuts())

    scuts = []
    for sc in shortcuts:
        k,f,d,cat,argskw = sc[:5]
        menu = sc[5] if len(sc) >= 6 else None
        sep = sc[6] if len(sc) >= 7 else False
        sc = Shortcut(k, f, s, d, category = cat, menu = menu, menu_separator = sep, **argskw)
        scuts.append(sc)

    return scuts, catcols

class Shortcut:

    def __init__(self, key_seq, func, session, description = '', key_name = None, category = None,
                 menu = None, menu_separator = False, each_map = False, each_molecule = False,
                 each_surface = False, atoms_arg = False, view_arg = False, mouse_modes_arg = False,
                 session_arg = False):
        '''
        A keyboard shortcut is a key sequence and function to call when
        that key sequence is entered.  The function can be a string in which case
        it is a user command.  Shortcuts are put in categories and have
        textual descriptions for automatically creating documentation.  A shortcut
        function can take no arguments or it can take a map, molecule, surface or
        view argument.
        '''
        self.key_seq = key_seq
        self.key_name = key_seq if key_name is None else key_name
        self.func = func		# Python function or string command
        self.description = description
        self.category = category
        self.menu = menu
        self.menu_separator = menu_separator

        self.each_map = each_map
        self.each_molecule = each_molecule
        self.each_surface = each_surface
        self.atoms_arg = atoms_arg
        self.view_arg = view_arg
        self.mouse_modes_arg = mouse_modes_arg
        self.session_arg = session_arg
        
    def run(self, session):
        f = self.func
        s = session

        self.log(s.logger)

        # User command string
        if isinstance(f, str):
            from chimerax.core import commands
            commands.run(s, f)
            return

        # Python function
        if self.atoms_arg:
            f(shortcut_atoms(s))
        elif self.each_map:
            for m in shortcut_maps(s):
                f(m)
        elif self.each_molecule:
            for m in shortcut_molecules(s):
                f(m)
        elif self.each_surface:
            for m in shortcut_surfaces(s):
                f(m)
        elif self.view_arg:
            v = s.main_view
            f(v)
        elif self.mouse_modes_arg:
            m = s.ui.mouse_modes
            f(m)
        elif self.session_arg:
            f(s)
        else:
            f()

    def log(self, logger):
        smsg = '%s - %s' % (self.key_name, self.description)
        logger.status(smsg)

class Keyboard_Shortcuts:
    '''
    Maintain a list of multi-key keyboard shortcuts and run them in response to key presses.
    '''
    def __init__(self, session):

        # Keyboard shortcuts
        self.shortcuts = {}
        self.keys = ''
        self.session = session
        self._enabled = False

    def add_shortcut(self, sc):
        self.shortcuts[sc.key_seq] = sc

    def enable_shortcuts(self):
        if not self._enabled:
            ui = self.session.ui
            ui.register_for_keystrokes(self)
            # TODO: Don't get key strokes if command line has focus
            ui.main_window.graphics_window.widget.setFocus()
            self._enabled = True

    def disable_shortcuts(self):
        if self._enabled:
            s = self.session
            s.ui.deregister_for_keystrokes(self)
            self._enabled = False

    def forwarded_keystroke(self, event):
        self.key_pressed(event)
      
    def key_pressed(self, event):
        k = event.key()
        from PyQt5.QtCore import Qt
        if k == Qt.Key_Escape:
            self.disable_shortcuts()
            return
        elif k == Qt.Key_Up:        # Up arrow
            self.session.selection.promote()
        elif k == Qt.Key_Down:        # Down arrow
            self.session.selection.demote()

        self.keys += event.text()
        self.try_shortcut()

    def try_shortcut(self, keys = None):

        if not keys is None:
            self.keys = keys
        k = self.keys
        s = self.shortcuts
        if k in s:
          keys = self.keys
          self.keys = ''
          self.run_shortcut(keys)
          return True

        is_prefix = False
        for ks in s.keys():
            if ks.startswith(k):
                is_prefix = True
                break
        msg = self.keys if is_prefix else '%s - unknown shortcut' % self.keys
        if not is_prefix:
            self.keys = ''

        self.session.logger.status(msg)
        return not is_prefix

    def run_shortcut(self, keys):
        sc = self.shortcuts.get(keys)
        if sc is not None:
            sc.run(self.session)

def register_selectors(logger):
    from chimerax.core.commands import register_selector
    register_selector("selAtoms", _sel_atoms_selector, logger)
    register_selector("selMaps", _sel_maps_selector, logger)
    register_selector("selModels", _sel_models_selector, logger)

# Selected atoms, or if none selected then all atoms.
def _sel_atoms_selector(session, models, results):
    atoms = shortcut_atoms(session)
    for m in atoms.unique_structures:
        results.add_model(m)
    results.add_atoms(atoms)

# Selected maps, or if none selected then displayed maps.
def _sel_maps_selector(session, models, results):
    for m in shortcut_maps(session):
        results.add_model(m)

# Selected models, or if none selected then all models.
def _sel_models_selector(session, models, results):
    for m in shortcut_models(session):
        results.add_model(m)

def shortcut_models(session, mclass = None, undisplayed = True, at_least = None):
    sel = session.selection.models()
    mlist = [m for m in sel
             if (mclass is None or isinstance(m,mclass))
             and (undisplayed or m.display)]
    if len(mlist) == 0:
        mlist = [m for m in session.models.list()
                 if (mclass is None or isinstance(m,mclass)) and (undisplayed or m.display)]
    elif at_least is not None and len(mlist) < at_least:
        # Include unselected models too if at_least option given.
        mlist += [m for m in session.models.list()
                  if m not in sel and
                  (mclass is None or isinstance(m,mclass)) and
                  (undisplayed or m.display)]
    return mlist

def shortcut_maps(session, undisplayed = True, at_least = None):
    from chimerax.core.map import Volume
    return shortcut_models(session, Volume, undisplayed=undisplayed, at_least=at_least)

def shortcut_molecules(session):
    from chimerax.core.atomic import AtomicStructure
    return shortcut_models(session, AtomicStructure, undisplayed = False)

def shortcut_atoms(session):
    matoms = []
    sel = session.selection
    atoms_list = sel.items('atoms')
    from chimerax.core.atomic import concatenate, Atoms
    if atoms_list:
        atoms = concatenate(atoms_list)
    elif sel.empty():
        # Nothing selected, so operate on all atoms
        from chimerax.core.atomic import all_atoms
        atoms = all_atoms(session)
    else:
        atoms = Atoms()
    return atoms

def shortcut_surfaces(session):
    sel = session.selection
    models = [m for m in session.models.list() if m.display] if sel.empty() else sel.models()
    # Avoid group nodes by only taking non-empty models.
    surfs = [m for m in models if not m.empty_drawing()]
    # TODO: Need a Surface base class.
    return surfs

def shortcut_surfaces_and_maps(session):
    sel = session.selection
    models = [m for m in session.models.list() if m.display] if sel.empty() else sel.models()
    # Avoid group nodes by only taking non-empty models.
    from chimerax.core.map import Volume
    sm = [m for m in models if isinstance(m,Volume) or not m.empty_drawing()]
    return sm

def show_mesh(session):
    for m in shortcut_surfaces(session):
        m.display_style = m.Mesh

def show_filled(session):
    for m in shortcut_surfaces(session):
        m.display_style = m.Solid

def show_dots(session):
    for m in shortcut_surfaces(session):
        m.display_style = m.Dot

def show_grayscale(m):
  m.set_representation('solid')
  m.show()

def toggle_outline_box(m):
  ro = m.rendering_options
  ro.show_outline_box = not ro.show_outline_box
  m.show()

def show_one_plane(m):
  ijk_step = (1,1,1)
  ijk_min, ijk_max = [list(b) for b in m.region[:2]]
  ijk_min[2] = ijk_max[2] = (ijk_min[2] + ijk_max[2])//2
  m.set_parameters(orthoplanes_shown = (False, False, False),
                   box_faces = False)
  m.new_region(ijk_min, ijk_max, ijk_step, adjust_step = False)
  m.show('solid')
        
def show_all_planes(m):
  ijk_min = (0,0,0)
  ijk_max = tuple(s-1 for s in m.data.size)
  m.new_region(ijk_min, ijk_max)

def toggle_orthoplanes(m):
  s = False in m.rendering_options.orthoplanes_shown
  p = tuple(s//2 for s in m.data.size)
  m.set_parameters(orthoplanes_shown = (s,s,s),
                   orthoplane_positions = p,
                   color_mode = 'l8' if s else 'auto8',
                   box_faces = False)
  m.show('solid')

def toggle_box_faces(m):
  s = not m.rendering_options.box_faces
  m.set_parameters(box_faces = s,
                   color_mode = 'l8' if s else 'auto8',
                   orthoplanes_shown = (False, False, False))
  m.show('solid')

def mark_map_surface_center(m):
    from chimerax.core import markers
    markers.mark_map_center(m)

def enable_move_planes_mouse_mode(mouse_modes, button = 'right'):
    m = mouse_modes
    from chimerax.core.map import PlanesMouseMode
    m.bind_mouse_mode(button, PlanesMouseMode(m.session))

def enable_contour_mouse_mode(mouse_modes, button = 'right'):
    m = mouse_modes
    from chimerax.core.map import ContourLevelMouseMode
    m.bind_mouse_mode(button, ContourLevelMouseMode(m.session))

def enable_marker_mouse_mode(mouse_modes, button = 'right'):
    m = mouse_modes
    from chimerax.core import markers
    m.bind_mouse_mode(button, markers.MarkerMouseMode(m.session))

def enable_mark_center_mouse_mode(mouse_modes, button = 'right'):
    m = mouse_modes
    from chimerax.core import markers
    m.bind_mouse_mode(button, markers.MarkCenterMouseMode(m.session))

def enable_map_series_mouse_mode(mouse_modes, button = 'right'):
    m = mouse_modes
    from chimerax.core.map import series
    m.bind_mouse_mode(button, series.PlaySeriesMouseMode(m.session))

def enable_move_selected_mouse_mode(mouse_modes):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode('left', ui.RotateSelectedMouseMode(m.session))
    m.bind_mouse_mode('middle', ui.TranslateSelectedMouseMode(m.session))

def enable_translate_selected_mouse_mode(mouse_modes, button = 'right'):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode(button, ui.TranslateSelectedMouseMode(m.session))

def enable_rotate_selected_mouse_mode(mouse_modes, button = 'right'):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode(button, ui.RotateSelectedMouseMode(m.session))

def enable_move_mouse_mode(mouse_modes):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode('left', ui.RotateMouseMode(m.session))
    m.bind_mouse_mode('middle', ui.TranslateMouseMode(m.session))

def enable_select_mouse_mode(mouse_modes, button = 'right'):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode(button, ui.SelectMouseMode(m.session))

def enable_rotate_mouse_mode(mouse_modes, button = 'right'):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode(button, ui.RotateMouseMode(m.session))

def enable_translate_mouse_mode(mouse_modes, button = 'right'):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode(button, ui.TranslateMouseMode(m.session))

def enable_zoom_mouse_mode(mouse_modes, button = 'right'):
    from chimerax.core import ui
    m = mouse_modes
    m.bind_mouse_mode(button, ui.ZoomMouseMode(m.session))

def fit_molecule_in_map(session):
    mols, maps = shortcut_molecules(session), shortcut_maps(session)
    log = session.logger
    if len(mols) != 1 or len(maps) != 1:
        log.status('Fit molecule in map requires one '
                   'displayed or selected molecule (got %d) and map (got %d).'
                   % (len(mols), len(maps)))
        return

    mol, map = mols[0], maps[0]
    points = mol.atoms.coords
    point_weights = None        # Equal weight for each atom
    data_array = map.full_matrix()
    xyz_to_ijk_transform = map.data.xyz_to_ijk_transform * map.position.inverse() * mol.position
    from chimerax.core.map import fit
    move_tf, stats = fit.locate_maximum(points, point_weights, data_array, xyz_to_ijk_transform)
    mol.position = mol.position * move_tf

    msg = ('Fit %s in %s, %d steps, shift %.3g, rotation %.3g degrees, average map value %.4g'
           % (mol.name, map.name, stats['steps'], stats['shift'], stats['angle'], stats['average map value']))
    log.status(msg)
    from chimerax.core.map.fit import fitmap
    log.info(fitmap.atom_fit_message(mols, map, stats))

def fit_subtract(session):
    models = session.models.list()
    from chimerax.core.map import Volume
    maps = [m for m in models if isinstance(m, Volume) and m.any_part_selected()]
    if len(maps) == 0:
        maps = [m for m in models if isinstance(m, Volume) and m.display]
    molfit = [m for m in shortcut_molecules(session) if m.display]
    mfitset = set(molfit)
    from chimerax.core.atomic import AtomicStructure
    molsub = [m for m in models
              if isinstance(m, AtomicStructure) and m.display and not m in mfitset]
    print ('fs', len(maps), len(molfit), len(molsub))
    log = session.logger
    if len(maps) != 1:
        log.status('Fit subtract requires one displayed or selected map.')
        return
    if len(molfit) == 0:
        log.status('Fit subtract requires at least one displayed or selected molecule.')
        return

    v = maps[0]
    res = 3*min(v.data.step)
    from chimerax.core.map.fit.fitmap import simulated_map
    mfit = [simulated_map(m.atoms, res, session) for m in molfit]
    msub = [simulated_map(m.atoms, res, session) for m in molsub]
    from chimerax.core.map.fit.fitcmd import fit_sequence
    fit_sequence(mfit, v, msub, resolution = res, sequence = len(mfit), log = log)
    print ('fit seq')

def fit_map_in_map(session):
    maps = shortcut_maps(session, undisplayed = False, at_least = 2)
    if len(maps) != 2:
        log = session.logger
        log.status('Fit map in map requires two displayed or selected maps (got %d).'
                   % len(maps))
        return

    map1, map2 = maps
    from chimerax.core.commands import run
    run(session, 'fit #%s in #%s' % (map1.id_string(), map2.id_string()))

def subtract_maps(session):
    maps = shortcut_maps(session, undisplayed = False, at_least = 2)
    if len(maps) != 2:
        log = session.logger
        log.status('Subtract maps requires two displayed or selected maps (got %d).'
                   % len(maps))
        return

    map1, map2 = maps
    from chimerax.core.commands import run
    run(session, 'vop subtract #%s #%s minrms' % (map1.id_string(), map2.id_string()))

def smooth_map(session):
    maps = shortcut_maps(session, undisplayed = False)
    if len(maps) != 1:
        log = session.logger
        log.status('Smooth map requires one displayed or selected map (got %d).'
                   % len(maps))
        return

    map = maps[0]
    sdev = 3*max(map.data.step)
    from chimerax.core.commands import run
    run(session, 'vop gaussian #%s sdev %.3g' % (map.id_string(), sdev))

def show_biological_unit(m, session):

    if hasattr(m, 'pdb_text'):
        from chimerax.core.atomic import biomt
        places = biomt.pdb_biomt_matrices(m.pdb_text)
        print (m.path, 'biomt', len(places))
        if places:
            m.positions = places

def show_asymmetric_unit(m, session):

    if len(m.positions) > 1:
        from chimerax.core.geometry import Places
        m.positions = Places([m.positions[0]])

def display_surface(session):
    surfs = shortcut_surfaces(session)
    if len(surfs) == 0 or session.selection.empty():
        surfs = [m for m in session.models.list() if not m.empty_drawing()]
    for m in surfs:
        sp = m.selected_positions
        if sp is None or sp.sum() == len(sp):
            m.display = True
        else:
            dp = m.display_positions
            if dp is None:
                m.display_positions = sp
            else:
                from numpy import logical_or
                m.display_positions = logical_or(dp,sp)

def hide_surface(session):
    for m in shortcut_surfaces(session):
        sp = m.selected_positions
        if sp is None or sp.sum() == len(sp):
            m.display = False
        else:
            dp = m.display_positions
            from numpy import logical_and, logical_not
            if dp is None:
                m.display_positions = logical_not(sp)
            else:
                m.display_positions = logical_and(dp,logical_not(sp))

def toggle_surface_transparency(session):
    from chimerax.core.map import Volume
    from chimerax.core.graphics import Drawing
    for m in shortcut_surfaces_and_maps(session):
        if isinstance(m, Volume):
            m.surface_colors = tuple((r,g,b,(0.5 if a == 1 else 1)) for r,g,b,a in m.surface_colors)
            m.show()
        else:
            for d in m.all_drawings():
                c = d.colors
                opaque = (c[:,3] == 255)
                c[:,3] = 255                # Make transparent opaque
                c[opaque,3] = 128           # and opaque transparent.
                d.colors = c

def show_surface_transparent(session, alpha = 0.5):
    from chimerax.core.map import Volume
    from chimerax.core.graphics import Drawing
    a = int(255*alpha)
    for m in shortcut_surfaces_and_maps(session):
        if not m.display:
            continue
        if isinstance(m, Volume):
            m.surface_colors = tuple((r,g,b,alpha) for r,g,b,a in m.surface_colors)
            m.show()
        elif isinstance(m, Drawing):
            for d in m.all_drawings():
                c = d.colors
                c[:,3] = a
                d.colors = c
                if not d.vertex_colors is None:
                    vcolors = d.vertex_colors
                    vcolors[:,3] = a
                    d.vertex_colors = vcolors.copy()

def show_surface_opaque(session):
    show_surface_transparent(session, alpha = 1)

def toggle_shadows(session):
    lp = session.main_view.lighting
    cmd = 'light shadow %s' % ('false' if lp.shadows else 'true')
    if lp.key_light_intensity == 0 and not lp.shadows:
        cmd += ' intensity 0.5'		# Make sure shadow is visible.
    from chimerax.core.commands import run
    run(session, cmd)

def toggle_silhouettes(session):
    v = session.main_view
    from chimerax.core.commands import run
    run(session, 'set silhouettes %s' % ('false' if v.silhouettes else 'true'))

def depth_cue(viewer):
    viewer.depth_cue = not viewer.depth_cue
    
def selection_mouse_mode(session):
    mm = session.mouse_modes
    mm.mouse_modes.bind_mouse_mode('right', mm.mouse_select)

def command_line(session):
    session.keyboard_shortcuts.disable_shortcuts()
    from chimerax.cmd_line.tool import CommandLine
    c = session.tools.find_by_class(CommandLine)
    if c:
        c[0].set_focus()

def color_by_bfactor(atoms):
    from time import time
    t0 = time()
    for a in atoms:
        b = a.bfactor
        f = min(1.0, b/50)
#        a.radius = 1+f
        a.color = (max(128,int((1-f)*255)),128,max(128,int(f*255)),255)
    t1 = time()
    print ('set colors by b-factors for %d atoms in %.3f seconds, %.0f atoms/sec'
           % (len(atoms), t1-t0, len(atoms)/(t1-t0)))

def color_one_color(m):
    m.single_color()

def fatter_ribbons(m):
    m.set_ribbon_radius(2*m.ribbon_radius)
def thinner_ribbons(m):
    m.set_ribbon_radius(0.5*m.ribbon_radius)
def show_ligands(m):
    m.show_ligand_atoms()
def molecule_bonds(m, session):
    if m.bonds is None:
        from chimerax.core.atomic import connect
        m.bonds, missing = connect.molecule_bonds(m, session)
        msg = 'Created %d bonds for %s using templates' % (len(m.bonds), m.name)
        log = session.logger
        log.status(msg)
        log.info(msg)
        if missing:
            log.info('Missing %d templates: %s' % (len(missing), ', '.join(missing)))

def list_keyboard_shortcuts(session):
    m = session.main_window
    if m.showing_text() and m.text_id == 'keyboard shortcuts':
        m.show_graphics()
    else:
        t = shortcut_descriptions(session.keyboard_shortcuts, html = True)
        m.show_text(t, html = True, id = "keyboard shortcuts")

def shortcut_descriptions(ks, html = False):
  ksc = {}
  for k, sc in ks.shortcuts.items():
    ksc.setdefault(sc.category,[]).append((sc.key_name,sc.description))
  cats = list(ksc.keys())
  cats.sort()
  for cat in cats:
    ksc[cat].sort(key = lambda a: str.lower(a[0]))
  if html:
    cols = ks.category_columns
    lines = ['<html>', '<body>']
    # Multi-column table
    lines.extend(['<table style="background-color:lightgray;">'
                  '<tr><th align=left colspan=%d><h1>Keyboard Shortcuts</h1>' % len(cols),
                  '<tr>']),
    for colcats in cols:
      lines.append('<td>')
      for cat in colcats:
        lines.extend(['<table>', '<tr><th colspan=2 align=left>%s' % cat])
        lines.extend(['<tr><td width=40>%s<td>%s' % (n,d) for n,d in ksc[cat]])
        lines.append('</table>')
    lines.append('</table>') # Multi-column table
  else:
    lines = ['Keyboard shortcuts']
    for cat in cats:
      lines.extend(['', cat])
      lines.extend(['%s - %s' % (n,d) for n,d in ksc[cat]])
  descrip = '\n'.join(lines)
  return descrip

def show_graphics_window(session):
    m = session.main_window
    m.show_graphics()
    m.show_back_forward_buttons(False)

def show_log(session):
  session.log.show()

def show_manual(session):
  m = session.main_window
  if m.showing_text() and m.text_id == 'manual':
    m.show_graphics()
    m.show_back_forward_buttons(False)
  else:
    from os.path import join, dirname
    path = join(dirname(dirname(__file__)), 'docs', 'index.html')
    url = 'file:/%s' % path
    m.show_text(url = url, open_links = True, id = 'manual')

def show_file_history(session):
    session.file_history.show_thumbnails()

def show_command_history(session):
    session.commands.history.show_command_history()

def show_scenes(session):
    session.scenes.show_thumbnails(toggle = True)

def show_framerate(session):
    def report_rate(fps, log=session.logger):
        msg = '%.1f frames/sec' % fps
        log.status(msg)
        log.info(msg)
    session.main_view.report_framerate(report_rate)

def show_triangle_count(session):
    models = session.models.list()
    from chimerax.core.atomic import AtomicStructure
    mols = [m for m in models if isinstance(m, AtomicStructure)]

    na = nt = 0
    for m in mols:
        ad = m._atoms_drawing
        if m.display and ad:
            dp = ad.display_positions
            if dp is not None:
                nma = dp.sum()
                na += nma
                if ad:
                    nt += nma * len(ad.triangles)

    n = len(models)
    nat = sum([m.number_of_triangles(displayed_only = True) for m in mols])

    msg = '%d models, %d atoms, %d atom triangles, all triangles %d' % (n, na, nt, nat)
    log = session.logger
    log.status(msg)
    log.info(msg)

def toggle_leap(session):
    from chimerax.core.devices import c2leap
    c2leap.toggle_leap(session)

def leap_chopsticks_mode(session):
    from chimerax.core.devices import c2leap
    c2leap.leap_mode('chopsticks', session)

def leap_position_mode(session):
    from chimerax.core.devices import c2leap
    c2leap.leap_mode('position', session)

def leap_velocity_mode(session):
    from chimerax.core.devices import c2leap
    c2leap.leap_mode('velocity', session)

def leap_focus(session):
    from chimerax.core.devices import c2leap
    c2leap.report_leap_focus(session)

def leap_quit(session):
    from chimerax.core.devices import c2leap
    c2leap.quit_leap(session)

def motion_blur(viewer):
    from chimerax.core.graphics import MotionBlur
    mb = [o for o in viewer.overlays() if isinstance(o, MotionBlur)]
    if mb:
        viewer.remove_overlays(mb)
    else:
        MotionBlur(viewer)

def mono_mode(viewer):
    from chimerax.core import graphics
    viewer.camera.mode = graphics.mono_camera_mode
def stereo_mode(viewer):
    from chimerax.core import graphics
    viewer.camera.mode = graphics.stereo_camera_mode

def start_oculus(session):
    from chimerax.core.devices import oculus
    if session.main_view.camera.name() == 'oculus':
        oculus.stop_oculus(session)
    else:
        oculus.start_oculus(session)
def oculus_move(session):
    oc = session.oculus
    if oc:
        if hasattr(oc, 'on_primary') and oc.on_primary:
            oc.oculus_full_screen()
            oc.on_primary = False
        else:
            oc.window.move_window_to_primary_screen()
            oc.on_primary = True

def toggle_space_navigator(session):
    from chimerax.core.devices import spacenavigator
    spacenavigator.toggle_space_navigator(session)

def toggle_space_navigator_fly_mode(session):
    from chimerax.core.devices import spacenavigator
    spacenavigator.toggle_fly_mode(session)

def space_navigator_collisions(session):
    from chimerax.core.devices import spacenavigator
    spacenavigator.avoid_collisions(session)

def undisplay_half(session):
    for m in session.models_list():
        undisplay_half_model(m)

def undisplay_half_model(m):
    if not m.empty_drawing():
        mp = m.positions
        va = m.vertices
        c = 0.5*(va.min(axis=0) + va.max(axis=0))
        if len(mp) == 1:
            if (mp[0]*c)[2] > 0:
                m.display = False
        else:
            from numpy import array, bool
            pmask = array([(pl*c)[2] <= 0 for pl in mp], bool)
            m.display_positions = pmask
            print('uh', m.name, pmask.sum())
    for c in m.child_drawings():
        undisplay_half_model(c)

def display_all_positions(session):
    for m in session.model_list():
        for c in m.all_drawings():
            if c.display:
                c.display_positions = None

def save_position(session):
    c = session.view.camera
    session._saved_camera_view = c.position

def restore_position(session):
    if hasattr(session, '_saved_camera_view'):
        c = session.view.camera
        c.position = session._saved_camera_view

def minimize_crosslinks(atoms, session):
    from chimerax.core.crosslinks import crosslink
    crosslink(session, minimize = atoms.unique_structures, frames = 30)

def save_image(session, basepath = '~/Desktop/image', suffix = '.png'):
    from chimerax.core.commands import run
    run(session, 'save %s supersample 3' % unused_file_name(basepath, suffix))

def save_spin_movie(session, basepath = '~/Desktop/movie', suffix = '.mp4'):
    cmd = 'movie record ; turn y 2 180 ; wait 180 ; movie encode %s' % unused_file_name(basepath, suffix)
    from chimerax.core.commands import run
    run(session, cmd)
    
def unused_file_name(basepath, suffix):
    '''
    Return path which is basepath plus a positive integer plus the file suffix
    such that the integer is greater than any other file that has this form.
    '''
    from os.path import dirname, basename, expanduser
    dir = expanduser(dirname(basepath))
    from os import listdir
    files = listdir(dir)
    bname = basename(basepath)
    nums = []
    for f in files:
        if f.startswith(bname) and f.endswith(suffix):
            try:
                nums.append(int(f[len(bname):len(f)-len(suffix)]))
            except:
                pass
    n = max(nums, default = 0) + 1
    path = '%s%d%s' % (basepath, n, suffix)
    return path
    
def keyboard_shortcuts(session):
    ks = getattr(session, 'keyboard_shortcuts', None)
    if ks is None:
        session.keyboard_shortcuts = ks = Keyboard_Shortcuts(session)
        register_shortcuts(ks)
    return ks

def ks(session, shortcut = None):
    '''
    Enable keyboard shortcuts.  Keys typed in the graphics window will be interpreted as shortcuts.

    Parameters
    ----------
    shortcut : string
      Keyboard shortcut to execute.  If no shortcut is specified switch to shortcut input mode.
    '''
    ks = keyboard_shortcuts(session)
    if shortcut is None:
        ks.enable_shortcuts()
    else:
        ks.try_shortcut(shortcut)

def register_shortcut_command(logger):
    from chimerax.core.commands import CmdDesc, StringArg, register
    desc = CmdDesc(optional = [('shortcut', StringArg)],
                   synopsis = 'Run keyboard a shortcut')
    register('ks', desc, ks, logger=logger)