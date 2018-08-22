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

def distance(session, atoms, *, color=None, dashes=None,
        decimal_places=None, radius=None, symbol=None):
    '''
    Show/report distance between two atoms.
    '''
    grp = session.pb_manager.get_group("distances", create=False)
    from chimerax.core.core_settings import settings
    if not grp:
        # create group and add to DistMonitor
        grp = session.pb_manager.get_group("distances")
        if color is not None:
            grp.color = color.uint8x4()
        else:
            grp.color = settings.distance_color.uint8x4()
        if radius is not None:
            grp.radius = radius
        else:
            grp.radius = settings.distance_radius
        grp.dashes = settings.distance_dashes
        session.models.add([grp])
        session.pb_dist_monitor.add_group(grp)
    a1, a2 = atoms
    for pb in grp.pseudobonds:
        pa1, pa2 = pb.atoms
        if (pa1 == a1 and pa2 == a2) or (pa1 == a2 and pa2 == a1):
            from chimerax.core.errors import UserError
            raise UserError("Distance already exists;"
                " modify distance properties with 'distance style'")
    pb = grp.new_pseudobond(a1, a2)

    if color is not None:
        pb.color = color.uint8x4()
    if dashes is not None:
        grp.dashes = dashes
    if radius is not None:
        pb.radius = radius
    if decimal_places is not None or symbol is not None:
        if decimal_places is not None:
            session.pb_dist_monitor.decimal_places = decimal_places
        if symbol is not None:
            session.pb_dist_monitor.show_units = symbol

    session.logger.info(("Distance between %s and %s: " + session.pb_dist_monitor.distance_format)
        % (a1, a2.string(relative_to=a1), pb.length))

def distance_save(session, save_file_name):
    from chimerax.core.io import open_filename
    save_file = open_filename(save_file_name, 'w')
    from chimerax.atomic import Structure
    for model in session.models:
        if not isinstance(model, Structure):
            continue
        print("Model", model.id_string, "is", model.name, file=save_file)

    print("\nDistance information:", file=save_file)
    grp = session.pb_manager.get_group("distances", create=False)
    if grp:
        pbs = list(grp.pseudobonds)
        pbs.sort(key=lambda pb: pb.length)
        fmt = "%s <-> %s:  " + session.pb_dist_monitor.distance_format
        for pb in pbs:
            a1, a2 = pb.atoms
            d_string = fmt % (a1, a2.string(relative_to=a1), pb.length)
            # drop angstrom symbol...
            if not d_string[-1].isdigit():
                d_string = d_string[:-1]
            print(d_string, file=save_file)
    if save_file_name != save_file:
        # Wasn't a stream that was passed in...
        save_file.close()

def distance_style(session, pbonds, *, color=None, dashes=None,
        decimal_places=None, radius=None, symbol=None, set_defaults=False):
    '''
    Modify appearance of existing distance(s).
    '''
    grp = session.pb_manager.get_group("distances", create=False)
    if pbonds is not None:
        pbs = [pb for pb in pbonds if pb.name == "distances"]
    elif grp:
        pbs = grp.pseudobonds
    else:
        pbs = []
    from chimerax.core.core_settings import settings
    if color is not None:
        for pb in pbs:
            pb.color = color.uint8x4()
        if grp:
            from chimerax.label.label3d import labels_model, PseudobondLabel
            lm = labels_model(grp, create=False)
            if lm:
                lm.add_labels(pbs, PseudobondLabel, session.main_view,
                    settings={ 'color': color.uint8x4() })
        if set_defaults and settings.distance_color != color:
            settings.distance_color = color
            session.triggers.activate_trigger("distance color changed", color)

    if dashes is not None:
        if not grp:
            grp = session.pb_manager.get_group("distances", create=True)
        grp.dashes = dashes
        if set_defaults and settings.distance_dashes != dashes:
            settings.distance_dashes = dashes
            session.triggers.activate_trigger("distance dashes changed", dashes)

    if decimal_places is not None:
        session.pb_dist_monitor.decimal_places = decimal_places

    if radius is not None:
        for pb in pbs:
            pb.radius = radius
        if settings.distance_radius != radius:
            settings.distance_radius = radius
            session.triggers.activate_trigger("distance radius changed", radius)

    if symbol is not None:
        session.pb_dist_monitor.show_units = symbol

def xdistance(session, pbonds=None):
    pbg = session.pb_manager.get_group("distances", create=False)
    if not pbg:
        return
    dist_pbonds = pbonds.with_group(pbg) if pbonds != None else None
    if pbonds == None or len(dist_pbonds) == pbg.num_pseudobonds:
        session.models.close([pbg])
        return
    for pb in dist_pbonds:
        pbg.delete_pseudobond(pb)

def register_command(logger):
    from chimerax.core.commands import CmdDesc, register, AnnotationError, \
        Or, EmptyArg, ColorArg, NonNegativeIntArg, FloatArg, BoolArg, SaveFileNameArg
    from chimerax.atomic import AtomsArg, PseudobondsArg
    # eventually this will handle more than just atoms, but for now...
    class AtomPairArg(AtomsArg):
        name = "an atom-pair specifier"

        @classmethod
        def parse(cls, text, session):
            atoms, text, rest = super().parse(text, session)
            if len(atoms) != 2:
                raise AnnotationError("Expected two atoms to be specified (%d specified)"
                    % len(atoms))
            return atoms, text, rest
    d_desc = CmdDesc(
        required = [('atoms', AtomPairArg)],
        keyword = [('color', ColorArg), ('dashes', NonNegativeIntArg), ('radius', FloatArg),
            ('decimal_places', NonNegativeIntArg), ('symbol', BoolArg)],
        synopsis = 'show/report distance')
    register('distance', d_desc, distance, logger=logger)
    xd_desc = CmdDesc(
        required = [('pbonds', Or(PseudobondsArg,EmptyArg))],
        synopsis = 'remove distance monitors')
    register('~distance', xd_desc, xdistance, logger=logger)
    df_desc = CmdDesc(
        required = [('pbonds', Or(PseudobondsArg,EmptyArg))],
        keyword = [('color', ColorArg), ('dashes', NonNegativeIntArg), ('radius', FloatArg),
            ('decimal_places', NonNegativeIntArg), ('symbol', BoolArg), ('set_defaults', BoolArg)],
        synopsis = 'set distance display properties')
    register('distance style', df_desc, distance_style, logger=logger)
    ds_desc = CmdDesc(
        required = [('save_file_name', SaveFileNameArg)],
        synopsis = 'save distance information')
    register('distance save', ds_desc, distance_save, logger=logger)
