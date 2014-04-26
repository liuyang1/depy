rootpath = "../.."
import sys
sys.path.append(rootpath)
from collections import namedtuple

import base
import plot

MdlDep = namedtuple("MdlDep", ["name", "asname", "super"])


def analysisImport(txt):
    def raiseError():
        ex = "unkown IMPORT deps \"%s\"" % (line)
        raise Exception(ex)
    lines = txt.split("\n")
    deps = []
    for line in lines:
        words = line.strip().split()
        ndep = []
        if len(words) == 0:
            continue
        elif words[0] == "import":
            if len(words) == 2:
# import ABC,DEF
                mdls = words[1].split(",")
                ndep = [MdlDep(mdl, mdl, "") for mdl in mdls]
            elif len(words) == 4 and words[2] == "as":
# import ABC as DEF
                ndep.append(MdlDep(words[1], words[3], ""))
            else:
                raiseError()
        elif words[0] == "from":
            if len(words) == 4 and words[2] == "import":
                if words[3] == "*":
# from ABC import *
                    ndep.append(MdlDep(words[1], words[1], ""))
                else:
# from ABC import DEF
                    ndep.append(MdlDep(words[3], words[3], words[1]))
            elif len(words) == 6 and words[2] == "import" and words[4] == "as":
# from ABC import DEF as G
                ndep.append(MdlDep(words[3], words[5], words[1]))
            else:
                raiseError()
        deps.extend(ndep)
    return deps


def analysisFile(filename):
    try:
        txt = base.loadFile(filename)
        return analysisImport(txt)
    except IOError:
        return []


def analysisRootFile(filename, d={}):
    import os
    path, fn = os.path.split(filename)
    prefix = fn.split(".")[0]
    try:
        txt = base.loadFile(filename)
        importdeps = analysisImport(txt)
    except IOError:
        importdeps = []
    d[prefix] = importdeps
    expandlist = [dep.name for dep in importdeps]
    for fn in expandlist:
        fn = "%s/%s.py" % (path, fn)
        if fn in d:
            continue
        ret = analysisRootFile(fn, d)
        d.update(ret)
    return d


def removeBasicDeps(deps):
    deps = {k: v for k, v in deps.iteritems() if len(v) != 0}
    new = {}
    for k, v in deps.iteritems():
        nv = [i for i in v if i.name in deps.keys()]
        new[k] = nv
    return new

if __name__ == "__main__":
    deps = analysisRootFile("/home/liuy/git/gx/pusher/src/pusher.py")
    deps = removeBasicDeps(deps)
    plot.outputGraphviz(deps, filename="rm.vz")
