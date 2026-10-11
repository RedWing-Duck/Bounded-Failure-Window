"""Run a figure script with Matplotlib's Figure.savefig wrapped, recording each saved figure's plotted arrays and text
elements (Task 15 checks C5 and C7: the figure objects are inspected, not the image).
Usage (as a module): capture(script_path, out_pickle, setup=callable or None, source=str or None)"""
import os
import pickle
import runpy
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.figure as mfig  # noqa: E402
import numpy as np  # noqa: E402


def _arrays(fig):
    out = []
    for ax in fig.axes:
        for ln in ax.get_lines():
            out.append(("line", np.asarray(ln.get_xydata(), dtype=float)))
        for c in ax.collections:
            off = np.asarray(c.get_offsets(), dtype=float)
            if off.size:
                out.append(("offsets", off))
            arr = c.get_array()
            if arr is not None:
                out.append(("array", np.asarray(arr, dtype=float)))
            for p in c.get_paths()[:5000]:
                out.append(("path", np.asarray(p.vertices, dtype=float)))
        for im in ax.images:
            out.append(("image", np.asarray(im.get_array(), dtype=float)))
        for pt in ax.patches:
            out.append(("patch", np.asarray(pt.get_path().vertices, dtype=float)))
    return out


def _texts(fig):
    fig.canvas.draw()
    t = []
    if fig._suptitle is not None:
        t.append(("suptitle", fig._suptitle.get_text()))
    t += [("figtext", x.get_text()) for x in fig.texts]
    for ax in fig.axes:
        for loc in ("left", "center", "right"):
            t.append(("title", ax.get_title(loc=loc)))
        t += [("xlabel", ax.get_xlabel()), ("ylabel", ax.get_ylabel())]
        t += [("xtick", x.get_text()) for x in ax.get_xticklabels()] + [("ytick", x.get_text()) for x in ax.get_yticklabels()]
        leg = ax.get_legend()
        if leg is not None:
            t += [("legend", x.get_text()) for x in leg.get_texts()]
            if leg.get_title():
                t.append(("legend title", leg.get_title().get_text()))
        t += [("text", x.get_text()) for x in ax.texts]
    return [(k, v) for k, v in t if v]


def capture(script, out_pickle, setup=None, source=None, cwd=None):
    rec = {}
    orig = mfig.Figure.savefig

    def wrapped(self, fname, *a, **k):
        name = os.path.splitext(os.path.basename(str(fname)))[0]
        if name not in rec:
            rec[name] = {"arrays": _arrays(self), "texts": _texts(self)}
        return orig(self, fname, *a, **k)
    mfig.Figure.savefig = wrapped
    old_cwd, old_path = os.getcwd(), list(sys.path)
    try:
        d = cwd or os.path.dirname(os.path.abspath(script))
        os.chdir(d)
        sys.path.insert(0, d)
        if setup:
            setup()
        if source is None:
            runpy.run_path(script, run_name="__main__")
        else:
            exec(compile(source, script, "exec"), {"__name__": "__main__", "__file__": script})
    finally:
        mfig.Figure.savefig = orig
        os.chdir(old_cwd)
        sys.path[:] = old_path
    with open(out_pickle, "wb") as fh:
        pickle.dump(rec, fh)
    return rec
