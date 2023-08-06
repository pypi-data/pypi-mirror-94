import sys

from t64 import T64ImageReader


with T64ImageReader(sys.argv[1]) as t:
    print([e.name for e in t.entries])
    with open(sys.argv[3], 'wb') as fileh:
        e = t.entry(sys.argv[2].encode())
        fileh.write(e.contents())
