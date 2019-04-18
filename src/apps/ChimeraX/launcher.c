#include <stdio.h>
#include <Python.h>

#ifdef _WIN32
# define WIN32_LEAN_AND_MEAN
# include <windows.h>
#endif
#include <locale.h>

/*
 * Mimic:
 *
 *	python -I [-X faulthandler] -m ChimeraX_main.py app-args
 */

static wchar_t* extra[] = {
	L"-I",
#if 0
	// TODO: Probably the right thing to do, but needs discussing
	L"-X",
	L"utf8",
#endif
	L"-X",
	L"faulthandler",
	L"-m",
	L"ChimeraX_main",
};
static const int ec = sizeof(extra) / sizeof (extra[0]);

static wchar_t* debug_extra[] = {
	L"-X",
	L"dev",
	L"-X",
	L"importtime",
};
static const int debug_ec = sizeof(debug_extra) / sizeof (debug_extra[0]);

/*
 * Make Nvidia Optimus GPU switching choose high performance graphics.
 * http://developer.download.nvidia.com/devzone/devcenter/gamegraphics/files/OptimusRenderingPolicies.pdf
 */
#ifdef _WIN32
_declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
#endif

static int
app_main(int argc, wchar_t** wargv)
{
	int debug = 0;
	for (int i = 1; i < argc; ++i) {
		if (wcscmp(wargv[i], L"--debug") == 0) {
			debug = 1;
			break;
		}
	}
	int new_argc = argc + ec + debug * debug_ec;
	wchar_t** new_argv = (wchar_t**) malloc((new_argc + 1) * sizeof (wchar_t*));
	if (new_argv == NULL) {
		fprintf(stderr, "out of memory\n");
		return 123;
	}
	int ac = 0;
	new_argv[ac++] = wargv[0];
	if (debug) {
		for (int i = 0; i < debug_ec; ++i)
			new_argv[ac++] = debug_extra[i];
	}
	for (int i = 0; i < ec; ++i)
		new_argv[ac++] = extra[i];
	for (int i = 1; i < argc; ++i)
		new_argv[ac++] = wargv[i];
	assert(ac == new_argc);
	new_argv[ac] = NULL;

	int result = Py_Main(new_argc, new_argv);
	return result;
}

#ifdef _WIN32
int WINAPI
wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPWSTR lpCmdLine,
	int nCmdShow)
{
	return app_main(__argc, __wargv);
}

#else
int
main(int argc, char** argv)
{
	size_t len;
	wchar_t** wargv = (wchar_t**) malloc(argc * sizeof (wchar_t*));
	if (wargv == NULL) {
		fprintf(stderr, "out of memory\n");
		return 120;
	}

	setlocale(LC_ALL, "");
	for (int i = 0; i < argc; ++i) {
		wargv[i] = Py_DecodeLocale(argv[i], &len);
		if (wargv[i] == NULL) {
			fprintf(stderr, "out of memory\n");
			return 121;
		}
	}
	return app_main(argc, wargv);
}
#endif
