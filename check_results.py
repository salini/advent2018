
modules = ["day%02d" % (idx+1) for idx in range(25)]

for m in modules:
    exec("import %s"% m)

if __name__ == '__main__':
    for m in modules:
        print "===== %s ====="%m
        eval(m).check()

