import sys
i = 0
for fi in sys.argv[1:]:
    with open (fi, "r") as f:
        for line in f.readlines():
            if line.split() == [] or line.strip().split()[0][0] == "#":
                pass
            else:
                i += 1
    print(i)
