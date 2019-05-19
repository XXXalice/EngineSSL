#!/usr/local/var/pyenv/versions/anaconda3-5.2.0/envs/ml/bin/python
import sys
from crawler import system as crawler_api
from ml import system as ml_api
from ml.data_handling import system as data_api
from etc import system_metadata as opt
from etc import wordart
from pred_app import auto_startup, pred_app


def main():
    wordart.print_logo('big')
    if len(sys.argv) <= 1:
        print(opt.help)
        exit()
    c = crawler_api.Clawler(sys.argv[1:])
    c.crawl()
    c.save_img()
    #対立画像を作る
    data = data_api.DataHandling()
    ml = ml_api.MachineLearning()
    preprocessed_datas = ml.get_preprocessed_data()
    model = ml.build_model()
    print_model_arch(model)
    made_model_name = ml.train_model(model=model, datas=preprocessed_datas, save_name=sys.argv[1:])
    app = pred_app.PredApp(sys.argv[1:], 'not_{}'.format(sys.argv[1:]))
    app.run(made_model_name)

def print_model_arch(model):
    model.summary()


if __name__ == '__main__':
    main()