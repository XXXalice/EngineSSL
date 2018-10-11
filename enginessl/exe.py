import crawler as cr
import os
import sys

clawler = cr.Clawler()
if len(sys.argv) == 2:
    clawler.crawl(keyword=sys.argv[1], num='')
elif len(sys.argv == 3):
    clawler.crawl(keyword=sys.argv[2], num=sys.argv[3])
else:
    print("error.")
    exit()