def compute_morph(mols, log, method = 'corkscrew', rate = 'linear', frames = 20, cartesian = False):
        motion = MolecularMotion(mols[0], method = method, rate = rate, frames = frames)
        from .interpolate import residue_interpolators
        res_interp = residue_interpolators(motion.trajectory().residues, cartesian)
        for i, mol in enumerate(mols[1:]):
                log.status("Computing interpolation %d\n" % (i+1))
                motion.interpolate(mol, res_interp)
        traj = motion.trajectory()
        return traj

ht = it = 0
class MolecularMotion:

        def __init__(self, m, method = "corkscrew", rate = "linear", frames = 20):
                """
                Compute a trajectory that starting from molecule m conformation.
                Subsequent calls to interpolate must supply molecules
                that have the exact same set of atoms as 'm'.
                Currently support keyword options are:

                        method                string, default "corkscrew"
                                        Use interpolation method 'method'.
                                        Known methods are "corkscrew",
                                        "independent" and "linear".
                        rate                string, default "linear"
                                        Interpolate frames so that the
                                        trajectory motion appears to be
                                        "rate": either "linear" (constant
                                        motion throughout) or "sinusoidal"
                                        (fast in middle, slow at ends).
                        frames                integer, default 20
                                        Number of intermediate frames to
                                        generate in trajectory
                """

                # Make a copy of the molecule to hold the computed trajectory
                from .util import copyMolecule
                tmol, atomMapMol, residueMapMol = copyMolecule(m)
                tmol.name = "Morph - %s" % m.name
                self.mol = tmol

                self.method = method
                self.rate = rate
                self.frames = frames

        def interpolate(self, m, res_interp):
                """Interpolate to new conformation 'm'."""

                #
                # Find matching set of residues.  First try for
                # one-to-one residue match, and, if that fails,
                # then finding a common set of residues.
                #
                from . import segment
                sm = self.mol
                from time import time
                t0 = time()
                try:
                        results = segment.segmentHingeExact(sm, m)
                except ValueError:
                        results = segment.segmentHingeApproximate(sm, m)
                t1 = time()
                global ht
                ht += t1-t0
                segments, atomMap, unusedResidues, unusedAtoms = results
                from chimerax.core.atomic import Residues, Atoms
                res_groups = [Residues(r0) for r0,r1 in segments]
                unusedResidues.delete()
                unusedAtoms.delete()

                if sm.deleted:
                        from chimerax.core.errors import UserError
                        raise UserError('No atoms matched')
                #
                # Interpolate between current conformation in trajectory
                # and new conformation
                #
                t0 = time()
                # Make coordinate set arrays for starting and final coordinates
                nc = sm.coordset_size
                matoms = sm.atoms
                maindices = matoms.coord_indices
                from numpy import float64, empty
                coords0 = empty((nc,3), float64)
                coords0[maindices] = matoms.coords
                coords1 = empty((nc,3), float64)
                # Convert to trajectory local coordinates.
                xform = sm.scene_position.inverse() * m.scene_position
                coords1[maindices] = xform * Atoms([atomMap[a] for a in matoms]).coords
                from .interpolate import interpolate
                coordsets = interpolate(coords0, coords1, res_groups, res_interp,
                                        self.method, self.rate, self.frames,
                                        sm.session.logger)
                base_id = max(sm.coordset_ids) + 1
                for i, cs in enumerate(coordsets):
                        sm.add_coordset(base_id + i, cs)
                sm.active_coordset_id = base_id + i
                t1 = time()
                global it
                it += t1-t0

        def trajectory(self):
                return self.mol