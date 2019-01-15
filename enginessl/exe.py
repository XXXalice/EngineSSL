from crawler import system
from etc import system_metadata as opt
import sys


if len(sys.argv) <= 1:
    print(opt.help)
    exit()


c = system.Clawler(sys.argv[1:])
c.crawl()
c.save_img()