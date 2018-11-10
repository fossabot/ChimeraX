// vi: set expandtab shiftwidth=4 softtabstop=4:

/*
 * === UCSF ChimeraX Copyright ===
 * Copyright 2016 Regents of the University of California.
 * All rights reserved.  This software provided pursuant to a
 * license agreement containing restrictions on its disclosure,
 * duplication and use.  For details see:
 * http://www.rbvi.ucsf.edu/chimerax/docs/licensing.html
 * This notice must be embedded in or attached to all copies,
 * including partial copies, of the software or any revisions
 * or derivations thereof.
 * === UCSF ChimeraX Copyright ===
 */

#ifdef __linux__
#include <GL/glx.h>			// Use CGLSetParameter
#endif

#include <arrays/pythonarray.h>		// use parse_uint8_n_array()

// ----------------------------------------------------------------------------
//
static bool set_linux_swap_interval(int sync)
{
#ifdef GLX_SGI_swap_control
   PFNGLXSWAPINTERVALSGIPROC glx_swap_interval_sgi =
          reinterpret_cast<PFNGLXSWAPINTERVALSGIPROC> (glXGetProcAddress(
                  reinterpret_cast<GLubyte const *>("glXSwapIntervalSGI")));
  if (glx_swap_interval_sgi && glx_swap_interval_sgi(sync) == 0)
    return true;
#endif

#ifdef GLX_MESA_swap_control
   PFNGLXSWAPINTERVALMESAPROC glx_swap_interval_mesa =
          reinterpret_cast<PFNGLXSWAPINTERVALMESAPROC> (glXGetProcAddress(
                  reinterpret_cast<GLubyte const *>("glXSwapIntervalMESA")));
  if (glx_swap_interval_mesa && glx_swap_interval_mesa(sync) == 0)
    return true;
#endif

  return false;
}

// ----------------------------------------------------------------------------
//
extern "C" PyObject *
set_linux_swap_interval(PyObject *, PyObject *args, PyObject *keywds)
{
  int sync;
  const char *kwlist[] = {"sync", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keywds, const_cast<char *>("i"),
				   (char **)kwlist,
				   &sync))
    return NULL;

  bool success = set_linux_swap_interval(sync);
  return python_bool(success);
}
