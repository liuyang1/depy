def outputGraphviz(deps, filename="deps.vz"):
    fp = open(filename, "w")

    def writeline(s="", offset=""):
        fp.write(offset + s + "\n")
    writeline("digraph deps{")
    offset = "    "
    for dep in deps.keys():
        writeline(dep + ";", offset)
    writeline()
    for dep, v in deps.iteritems():
        if len(v) == 0:
            continue
        writeline("%s -> {%s};" % (dep, " ".join([f.name for f in v])), offset)
    writeline("}")
    fp.close()
