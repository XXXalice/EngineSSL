import sys
import os

from crawler import system as crawler_api
from ml import system as ml_api
from etc import system_metadata as opt
import sys


# if len(sys.argv) <= 1:
#     print(opt.help)
#     exit()
#
#
# c = crawler_api.Clawler(sys.argv[1:])
# c.crawl()
# c.save_img()

def main():
    Ml = ml_api.MachineLearning()
    datas = Ml.get_datas()
    model = Ml.build_model()
    model.summary()
    Ml.train_model(model=model, datas=datas)

if __name__ == '__main__':
    main()