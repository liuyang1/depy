def outputGraphviz(deps, filename="deps.vz"):
    fp = open(filename, "w")

    def writeline(s=""):
        fp.write(s + "\n")
    writeline("digraph deps{")
    for dep in deps.keys():
        writeline(dep + ";")
    writeline()
    for dep, v in deps.iteritems():
        writeline("%s -> {%s};" % (dep, " ".join([f.name for f in v])))
    writeline("}")
    fp.close()
