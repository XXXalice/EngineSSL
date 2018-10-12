from crawler import system
import sys

c = system.Clawler(sys.argv[1:])
c.crawl()
c.save_img()