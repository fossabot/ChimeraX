# vim: set expandtab shiftwidth=4 softtabstop=4:
from .place import Place, Places, identity, rotation, vector_rotation, translation, scale
from .place import product, orthonormal_frame, interpolate_rotation
from .vector import interpolate_points, inner_product, normalize_vector, ray_segment
from .bounds import sphere_bounds, union_bounds, Bounds, point_bounds
from .bounds import copies_bounding_box, copy_tree_bounds, clip_bounds
from ._geometry import natural_cubic_spline
from ._geometry import sphere_axes_bounds, spheres_in_bounds, bounds_overlap
from ._geometry import find_closest_points
from ._geometry import closest_sphere_intercept, closest_cylinder_intercept, closest_triangle_intercept
from ._geometry import segment_intercepts_spheres
from .align import align_points
