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

# -----------------------------------------------------------------------------
# Implementation of "volume" command.
#
def register_volume_command(logger):

    from chimerax.core.commands import CmdDesc, register
    from chimerax.core.commands import BoolArg, IntArg, StringArg, FloatArg, FloatsArg, NoArg, ListOf, EnumOf, Int3Arg, ColorArg, CenterArg, AxisArg, CoordSysArg, RepeatOf, Or
    from chimerax.atomic import SymmetryArg
    from .mapargs import MapsArg, MapRegionArg, MapStepArg, Float1or3Arg, Int1or3Arg
    from .colortables import appearance_names

    from .volume import Rendering_Options
    ro = Rendering_Options()

    volume_desc = CmdDesc(
        optional = [('volumes', MapsArg)],
        keyword = [
               ('style', EnumOf(('surface', 'mesh', 'image', 'solid'))),
               ('show', NoArg),
               ('hide', NoArg),
               ('toggle', NoArg),
               ('level', RepeatOf(FloatsArg)),
               ('rms_level', RepeatOf(FloatsArg)),
               ('sd_level', RepeatOf(FloatsArg)),
               ('enclose_volume', FloatsArg),
               ('fast_enclose_volume', FloatsArg),
               ('color', RepeatOf(ColorArg)),
               ('brightness', FloatArg),
               ('transparency', FloatArg),
               ('appearance', EnumOf(appearance_names())),
               ('step', MapStepArg),
               ('region', MapRegionArg),
               ('name_region', StringArg),
               ('expand_single_plane', BoolArg),
               ('origin', Float1or3Arg),
               ('origin_index', Float1or3Arg),
               ('voxel_size', Float1or3Arg),
               ('planes', PlanesArg),
               ('dump_header', BoolArg),
               ('pickable', BoolArg),
# Symmetry assignment.
               ('symmetry', SymmetryArg),
               ('center', CenterArg),
               ('center_index', Float1or3Arg),
               ('axis', AxisArg),
               ('coordinate_system', CoordSysArg),
# Global options.
               ('data_cache_size', FloatArg),
               ('show_on_open', BoolArg),
               ('voxel_limit_for_open', FloatArg),
               ('show_plane', BoolArg),
               ('voxel_limit_for_plane', FloatArg),
# Rendering options.
               ('show_outline_box', BoolArg),
               ('outline_box_rgb', ColorArg),
#               ('outline_box_linewidth', FloatArg),
               ('limit_voxel_count', BoolArg),
               ('voxel_limit', FloatArg),
               ('color_mode', EnumOf(ro.color_modes)),
               ('colormap_on_gpu', BoolArg),
               ('colormap_size', IntArg),
               ('blend_on_gpu', BoolArg),
               ('projection_mode', EnumOf(ro.projection_modes)),
               ('plane_spacing', Or(EnumOf(('min', 'max', 'mean')), FloatArg)),
               ('full_region_on_gpu', BoolArg),
               ('bt_correction', BoolArg),
               ('minimal_texture_memory', BoolArg),
               ('maximum_intensity_projection', BoolArg),
               ('linear_interpolation', BoolArg),
               ('dim_transparency', BoolArg),
               ('dim_transparent_voxels', BoolArg),
#               ('line_thickness', FloatArg),
               ('smooth_lines', BoolArg),
               ('mesh_lighting', BoolArg),
               ('two_sided_lighting', BoolArg),
               ('flip_normals', BoolArg),
               ('subdivide_surface', BoolArg),
               ('subdivision_levels', IntArg),
               ('surface_smoothing', BoolArg),
               ('smoothing_iterations', IntArg),
               ('smoothing_factor', FloatArg),
               ('square_mesh', BoolArg),
               ('cap_faces', BoolArg),
               ('box_faces', BoolArg),
               ('orthoplanes', EnumOf(('xyz', 'xy', 'xz', 'yz', 'off'))),
               ('position_planes', Int3Arg),
        ],
        synopsis = 'set volume model parameters, display style and colors')
    register('volume', volume_desc, volume, logger=logger)

    vsettings_desc = CmdDesc(optional = [('volumes', MapsArg)],
                             synopsis = 'report volume display settings')
    register('volume settings', vsettings_desc, volume_settings, logger=logger)

    # Register volume subcommands for filtering operations.
    from . import filter
    filter.register_volume_filtering_subcommands(logger)
    
# -----------------------------------------------------------------------------
#
def volume(session,
           volumes = None,
           style = None,
           show = None,
           hide = None,
           toggle = None,
           level = None,
           rms_level = None,
           sd_level = None,
           enclose_volume = None,
           fast_enclose_volume = None,
           color = None,
           brightness = None,
           transparency = None,
           appearance = None,
           step = None,
           region = None,
           name_region = None,
           expand_single_plane = None,
           origin = None,
           origin_index = None,
           voxel_size = None,
           planes = None,
           dump_header = None,
           pickable = None,
# Symmetry assignment.
           symmetry = None,
           center = None,
           center_index = None,
           axis = None,
           coordinate_system = None,
# Global options.
           data_cache_size = None,
           show_on_open = None,
           voxel_limit_for_open = None,
           show_plane = None,
           voxel_limit_for_plane = None,
# Rendering options.
           show_outline_box = None,
           outline_box_rgb = None,
           outline_box_linewidth = None,
           limit_voxel_count = None,          # auto-adjust step size
           voxel_limit = None,               # Mvoxels
           color_mode = None,                # image rendering pixel formats
           colormap_on_gpu = None,           # image colormapping on gpu or cpu
           colormap_size = None,             # image colormapping
           blend_on_gpu = None,		     # image blending on gpu or cpu
           projection_mode = None,           # auto, 2d-xyz, 2d-x, 2d-y, 2d-z, 3d
           plane_spacing = None,	     # min, max, or numeric value
           full_region_on_gpu = None,	     # for fast cropping with image rendering
           bt_correction = None,             # brightness and transparency
           minimal_texture_memory = None,
           maximum_intensity_projection = None,
           linear_interpolation = None,
           dim_transparency = None,          # for surfaces
           dim_transparent_voxels = None,     # for image rendering
           line_thickness = None,
           smooth_lines = None,
           mesh_lighting = None,
           two_sided_lighting = None,
           flip_normals = None,
           subdivide_surface = None,
           subdivision_levels = None,
           surface_smoothing = None,
           smoothing_iterations = None,
           smoothing_factor = None,
           square_mesh = None,
           cap_faces = None,
           box_faces = None,
           orthoplanes = None,
           position_planes = None,
           ):
    '''
    Control the display of density maps.

    Parameters
    ----------
    volumes : list of maps
    style : "surface", "mesh", or "image"
    show : bool
    hide : bool
    toggle : bool
    level : sequence of 1 or 2 floats
      In image style 2 floats are used the first being a density level and second 0-1 brightness value.
    enclose_volume : float
    fast_enclose_volume : float
    color : Color
    brightness : float
    transparency : float
    step : sequence of 3 integers
    region : sequence of 6 integers
      3 minimum grid indices and 3 maximum grid indices for x,y,z axes.
    name_region : string
    expand_single_plane : bool
    origin : sequence of 3 floats
    origin_index : sequence of 3 floats
    voxel_size : sequence of 3 floats
    planes : tuple of (axis, start, end, increment, depth), last 3 are optional

    ------------------------------------------------------------------------------------------------
    Symmetry assignment options
    ------------------------------------------------------------------------------------------------

    symmetry : string
    center : string
      Parsed as 3 comma-separated floats, or an atom specifier
    center_index : sequence of 3 floats
    axis : sequence of 3 floats
    coordinate_system : Place
      Coordinate system for axis and center symmetry options

    ------------------------------------------------------------------------------------------------
    Global options
    ------------------------------------------------------------------------------------------------

    data_cache_size : float
      In Mbytes
    show_on_open : bool
    voxel_limit_for_open : float
    show_plane : bool
    voxel_limit_for_plane : float

    ------------------------------------------------------------------------------------------------
    Rendering options
    ------------------------------------------------------------------------------------------------

    show_outline_box : bool
    outline_box_rgb : Color
    outline_box_linewidth : float
    limit_voxel_count : bool
      Auto-adjust step size.
    voxel_limit : float (Mvoxels)
    color_mode : string
      Image rendering pixel formats: 'auto4', 'auto8', 'auto12', 'auto16',
      'opaque4', 'opaque8', 'opaque12', 'opaque16', 'rgba4', 'rgba8', 'rgba12', 'rgba16',
      'rgb4', 'rgb8', 'rgb12', 'rgb16', 'la4', 'la8', 'la12', 'la16', 'l4', 'l8', 'l12', 'l16'
    colormap_on_gpu : bool
      Whether colormapping is done on gpu or cpu for image rendering.
    colormap_size : integer
      Size of colormap to use for image rendering.
    blend_on_gpu : bool
      Whether image blending is done on gpu or cpu.
    projection_mode : string
      One of 'auto', '2d-xyz', '2d-x', '2d-y', '2d-z', '3d'
    plane_spacing : "min", "max", "mean" or float
      Spacing between planes when using 3d projection mode.  "min", "max", "mean" use
      minimum, maximum or average grid spacing along x,y,z axes.
    full_region_on_gpu : bool
      Whether to cache data on GPU for fast cropping.
    bt_correction : bool
      Brightness and transparency view angle correction for image rendering mode.
    minimal_texture_memory : bool
      Reduce graphics memory use for image rendering at the expense of rendering speed.
    maximum_intensity_projection : bool
    linear_interpolation : bool
      Interpolate gray levels in image style rendering.
    dim_transparency : bool
      Makes transparent surfaces dimmer
    dim_transparent_voxels : bool
      For image rendering.
    line_thickness : float
    smooth_lines : bool
    mesh_lighting : bool
    two_sided_lighting : bool
    flip_normals : bool
    subdivide_surface : bool
    subdivision_levels : integer
    surface_smoothing : bool
    smoothing_iterations : integer
    smoothing_factor : float
    square_mesh : bool
    cap_faces : bool
    box_faces : bool
    orthoplanes : One of 'xyz', 'xy', 'xz', 'yz', 'off'
    position_planes : sequence of 3 integers
      Intersection grid point of orthoplanes display
    '''
    if volumes is None:
        from . import Volume
        vlist = session.models.list(type = Volume)
    else:
        vlist = volumes

    if style == 'solid':
        style = 'image'	# Rename solid to image.

    # Special defaults
    if box_faces:
        defaults = (('style', 'image'), ('color_mode', 'opaque8'),
                    ('show_outline_box', True), ('expand_single_plane', True),
                    ('orthoplanes', 'off'))
    elif not orthoplanes is None and orthoplanes != 'off':
        defaults = (('style', 'image'), ('color_mode', 'opaque8'),
                    ('show_outline_box', True), ('expand_single_plane', True))
    elif not box_faces is None or not orthoplanes is None:
        defaults = (('color_mode', 'auto8'),)
    else:
        defaults = ()
    loc = locals()
    for opt, value in defaults:
        if loc[opt] is None:
            loc[opt] = value

    # Adjust global settings.
    gopt = ('data_cache_size', 'show_on_open', 'voxel_limit_for_open',
            'show_plane', 'voxel_limit_for_plane')
    if volumes is None:
        gopt += ('pickable',)
    gsettings = dict((n,loc[n]) for n in gopt if not loc[n] is None)
    if gsettings:
        apply_global_settings(session, gsettings)

    if len(gsettings) == 0 and len(vlist) == 0:
        from chimerax.core import errors
        raise errors.UserError('No volumes specified%s' %
                            (' by "%s"' % volumes if volumes else ''))

    # Apply volume settings.
    dopt = ('style', 'show', 'hide', 'toggle', 'level', 'rms_level', 'sd_level',
            'enclose_volume', 'fast_enclose_volume',
            'color', 'brightness', 'transparency', 'appearance',
            'step', 'region', 'name_region', 'expand_single_plane', 'origin',
            'origin_index', 'voxel_size', 'planes',
            'symmetry', 'center', 'center_index', 'axis', 'coordinate_system', 'dump_header', 'pickable')
    dsettings = dict((n,loc[n]) for n in dopt if not loc[n] is None)
    ropt = (
        'show_outline_box', 'outline_box_rgb', 'outline_box_linewidth',
        'limit_voxel_count', 'voxel_limit', 'color_mode', 'colormap_on_gpu', 'colormap_size',
        'blend_on_gpu', 'projection_mode', 'plane_spacing', 'full_region_on_gpu',
        'bt_correction', 'minimal_texture_memory', 'maximum_intensity_projection',
        'linear_interpolation', 'dim_transparency', 'dim_transparent_voxels',
        'line_thickness', 'smooth_lines', 'mesh_lighting',
        'two_sided_lighting', 'flip_normals', 'subdivide_surface',
        'subdivision_levels', 'surface_smoothing', 'smoothing_iterations',
        'smoothing_factor', 'square_mesh', 'cap_faces', 'box_faces')
    rsettings = dict((n,loc[n]) for n in ropt if not loc[n] is None)
    if not orthoplanes is None:
        rsettings['orthoplanes_shown'] = ('x' in orthoplanes,
                                         'y' in orthoplanes,
                                         'z' in orthoplanes)
    if not position_planes is None:
        rsettings['orthoplane_positions'] = position_planes
    if outline_box_rgb:
        rsettings['outline_box_rgb'] = tuple(outline_box_rgb.rgba[:3])

    for v in vlist:
        apply_volume_options(v, dsettings, rsettings, session)

# -----------------------------------------------------------------------------
#
def apply_global_settings(session, gsettings):

    from .volume import default_settings
    default_settings(session).update(gsettings)

    if 'data_cache_size' in gsettings:
        from .volume import data_cache
        dc = data_cache(session)
        dc.resize(gsettings['data_cache_size'] * (2**20))

    if 'pickable' in gsettings:
        from . import maps_pickable
        maps_pickable(session, gsettings['pickable'])
    
# -----------------------------------------------------------------------------
#
def apply_volume_options(v, doptions, roptions, session):

    if 'style' in doptions:
        v.set_display_style(doptions['style'])

    kw = level_and_color_settings(v, doptions)
    kw.update(roptions)
    if kw:
        v.set_parameters(**kw)

    if 'enclose_volume' in doptions:
        levels = [v.surface_level_for_enclosed_volume(ev) for ev in doptions['enclose_volume']]
        v.set_parameters(surface_levels = levels)
    elif 'fast_enclose_volume' in doptions:
        levels = [v.surface_level_for_enclosed_volume(ev, rank_method = True)
                  for ev in doptions['fast_enclose_volume']]
        v.set_parameters(surface_levels = levels)

    if 'region' in doptions or 'step' in doptions:
        r = v.subregion(doptions.get('step', None),
                        doptions.get('region', None))
    else:
        r = None
    if not r is None:
        ijk_min, ijk_max, ijk_step = r
        v.new_region(ijk_min, ijk_max, ijk_step,
                     adjust_step = not 'step' in doptions)
    if doptions.get('expand_single_plane', False):
        v.expand_single_plane()

    if 'name_region' in doptions:
        name = doptions['name_region']
        if r is None:
            r = v.region
        if r:
            v.region_list.add_named_region(name, r[0], r[1])

    if 'planes' in doptions:
        from . import volume
        volume.cycle_through_planes(v, session, *doptions['planes'])

    d = v.data
    if 'origin_index' in doptions:
        index_origin = doptions['origin_index']
        xyz_origin = [-a*b for a,b in zip(index_origin, d.step)]
        d.set_origin(xyz_origin)
    elif 'origin' in doptions:
        origin = doptions['origin']
        d.set_origin(origin)

    if 'voxel_size' in doptions:
        vsize = doptions['voxel_size']
        if min(vsize) <= 0:
            from chimerax.core import errors
            raise errors.UserError('Voxel size must positive, got %g,%g,%g'
                                % tuple(vsize))
        # Preserve index origin.
        origin = [(a/b)*c for a,b,c in zip(d.origin, d.step, vsize)]
        d.set_origin(origin)
        d.set_step(vsize)

    if 'symmetry' in doptions:
        csys = doptions.get('coordinate_system', v.position)
        if 'center_index' in doptions:
            c = v.data.ijk_to_xyz(doptions['center_index'])
            if 'coordinate_system' in doptions:
                c = csys.inverse() * (v.position * c)
            from chimerax.core.commands import Center
            center = Center(c)
        else:
            center = doptions.get('center')
        ops = doptions['symmetry'].positions(center, doptions.get('axis'), csys)
        d.symmetries = ops.transform_coordinates(v.position)

    if 'show' in doptions:
        v.display = True
    elif 'hide' in doptions:
        v.display = False
    elif 'toggle' in doptions:
        v.display = not v.display

    # TODO: Volume should note when it needs update
    v._drawings_need_update()

    if 'dump_header' in doptions and doptions['dump_header']:
        show_file_header(v.data, session.logger)

    if 'pickable' in doptions:
        v.pickable = doptions['pickable']


# TODO:
#  Allow quoted color names.
#  Could allow region name "full" or "back".
#  Could allow voxel_size or origin to be "original".
   
# -----------------------------------------------------------------------------
#
def level_and_color_settings(v, options):

    kw = {}

    levels = options.get('level', [])
    rms_levels = options.get('rms_level', [])
    sd_levels = options.get('sd_level', [])
    if rms_levels or sd_levels:
        mean, sd, rms = v.mean_sd_rms()
        if rms_levels:
            for lvl in rms_levels:
                lvl[0] *= rms
            levels.extend(rms_levels)
        if sd_levels:
            for lvl in sd_levels:
                lvl[0] *= sd
            levels.extend(sd_levels)

    colors = options.get('color', [])

    # Allow 0 or 1 colors and 0 or more levels, or number colors matching
    # number of levels.
    if len(colors) > 1 and len(colors) != len(levels):
        from chimerax.core import errors
        raise errors.UserError('Number of colors (%d) does not match number of levels (%d)'
                            % (len(colors), len(levels)))

    if 'style' in options:
        style = options['style']
        if style == 'mesh':
            style = 'surface'
    elif v.surface_shown:
        style = 'surface'
    elif v.image_shown:
        style = 'image'
    else:
        style = 'surface'

    if style in ('surface', 'mesh'):
        for l in levels:
            if len(l) != 1:
                from chimerax.core.errors import UserError
                raise UserError('Surface level must be a single value')
        levels = [l[0] for l in levels]
    elif style == 'image':
        for l in levels:
            if len(l) != 2:
                from chimerax.core.errors import UserError
                raise UserError('Image level must be <data-value,brightness-level>')

    if levels:
        kw[style+'_levels'] = levels

    if len(colors) == 1:
        if levels:
            clist = [colors[0].rgba]*len(levels)
        else:
            nlev = len(v.image_levels if style == 'image' else [s.level for s in v.surfaces])
            clist = [colors[0].rgba]*nlev
        kw[style+'_colors'] = clist
    elif len(colors) > 1:
        kw[style+'_colors'] = [c.rgba for c in colors]

    if len(levels) == 0 and len(colors) == 1:
        kw['default_rgba'] = colors[0].rgba

    if 'brightness' in options:
        kw[style+'_brightness_factor'] = options['brightness']

    if 'transparency' in options:
        if style == 'surface':
            kw['transparency_factor'] = options['transparency']
        else:
            kw['transparency_depth'] = options['transparency']

    if 'appearance' in options:
        from . import colortables
        akw = colortables.appearance_settings(options['appearance'], v)
        kw.update(akw)
                              
    return kw

# -----------------------------------------------------------------------------
# Arguments are axis,pstart,pend,pstep,pdepth.
#
def planes_arg(planes, session):

    axis, param = (planes.split(',',1) + [''])[:2]
    from chimerax.core.commands.parse import enum_arg, floats_arg
    p = [enum_arg(axis, session, ('x','y','z'))] + floats_arg(param, session)
    if len(p) < 2 or len(p) > 5:
        from chimerax.core import errors
        raise errors.UserError('planes argument must have 2 to 5 comma-separated values: axis,pstart[[[,pend],pstep],pdepth.], got "%s"' % planes)
    return p

# -----------------------------------------------------------------------------
# Find maps among models and all descendants.
#
def all_maps(models):
    maps = []
    from .volume import Volume
    from chimerax.core.models import Model
    for m in models:
        if isinstance(m, Volume):
            maps.append(m)
        if isinstance(m, Model):
            maps.extend(all_maps(m.child_drawings()))
    return maps
    
# -----------------------------------------------------------------------------
#
from chimerax.core.commands import Annotation
class PlanesArg(Annotation):
    '''
    Parse planes argument to volume command axis,start,end,increment,depth.
    axis can be x, y, or z, and the other values are integers with the last 3
    being optional.
    '''
    name = 'planes x|y|z[,<start>[,<end>[,<increment>[,<depth>]]]]'

    @staticmethod
    def parse(text, session):
        from chimerax.core.commands import next_token, AnnotationError
        token, text, rest = next_token(text)
        fields = token.split(',')
        if fields[0] not in ('x', 'y', 'z'):
            raise AnnotationError('Planes argument first field must be x, y, or z, got "%s"' % fields[0])
        try:
            values = [int(f) for f in fields[1:]]
        except:
            raise AnnotationError('Planes arguments after axis must be integers')
        result = tuple([fields[0]] + values)
        return result, text, rest
    
# -----------------------------------------------------------------------------
#
def show_file_header(d, log):
    if hasattr(d, 'file_header') and isinstance(d.file_header, dict):
        h = d.file_header
        klist = list(h.keys())
        klist.sort()
        msg = ('File header for %s\n' % d.path +
               '\n'.join(('%s = %s' % (k, str(h[k]))) for k in klist))
    else:
        msg = 'No header info for %s' % d.name
        log.status(msg)
    log.info(msg + '\n')
    
# -----------------------------------------------------------------------------
#
def volume_settings(session, volumes = None):
    if volumes is None:
        from . import Volume
        volumes = session.models.list(type = Volume)
    msg = '\n\n'.join(volume_settings_text(v) for v in volumes)
    session.logger.info(msg)
    
# -----------------------------------------------------------------------------
#
def volume_settings_text(v):
    lines = ['Settings for map %s' % v.name,
             'grid size = %d %d %d' % tuple(v.data.size),
             'region = %d %d %d' % tuple(v.region[0]) + ' to %d %d %d' % tuple(v.region[1]),
             'step = %d %d %d' % tuple(v.region[2]),
             'voxel size = %.3g %.3g %.3g' % tuple(v.data.step),
             'surface levels = ' + ','.join('%.5g' % s.level for s in v.surfaces),
             'surface brightness = %.5g' % v.surface_brightness_factor,
             'surface transparency factor = %.5g' % v.transparency_factor,
             'image levels = ' + ' '.join('%.5g,%.5g' % tuple(sl) for sl in v.image_levels),
             'image brightness factor = %.5g' % v.image_brightness_factor,
             'image transparency depth = %.5g' % v.transparency_depth,
             ]
    ro = v.rendering_options
    from .volume import default_settings
    ds = default_settings(v.session)
    attrs = list(ds.rendering_option_names())
    attrs.sort()
    for attr in attrs:
        value = getattr(ro, attr)
        lines.append('%s = %s' % (camel_case(attr), value))
    return '\n'.join(lines)
    
# -----------------------------------------------------------------------------
#
def camel_case(string):
    if '_' not in string:
        return string
    cc = []
    up = False
    for c in string:
        if c == '_':
            up = True
        else:
            cc.append(c.upper() if up else c)
            up = False
    return ''.join(cc)

