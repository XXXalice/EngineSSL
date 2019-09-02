#!/usr/local/var/pyenv/versions/anaconda3-5.2.0/envs/ml/bin/python
import sys
import argparse
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
        sys.exit(0)
    parser = argparse.ArgumentParser(description='engine ssl')
    parser.add_argument('-t', '--target', help='target name.')
    parser.add_argument('-nt', '--nottarget', help='not target name.', nargs='*')
    parser.add_argument('-tr', '--train', help='train status.', nargs='*')
    p_args = parser.parse_args()

    img_folpath = []
    #ターゲット画像収集用APIをインスタンス化
    c = crawler_api.Clawler([p_args.target])
    c.delete_datas_dir()
    c.crawl()
    img_folpath.append(c.save_img(rtn_folpath=True))

    #ターゲットではない画像収集用APIをインスタンス化
    if p_args.nottarget != None:
        c.crawl(multiple=len(p_args.nottarget) + 1)
        img_folpath.append(c.save_img(rtn_folpath=True))
        for nt in p_args.nottarget:
            not_c = crawler_api.Clawler([nt])
            not_c.crawl()
            img_folpath.append(not_c.save_img(rtn_folpath=True))

    ''' TODO:
        クローラーapiの改善 done
        ・フォルダ名return done
        ・tqdm done
        ・nottarget枚数の自動推定（各ラベルごとに同じくらいの枚数になるようにする）
        それに伴う学習apiの改善
        ・フォルダ名を指定して教師化
        ・self-training
        ・ファインチューニング
    '''
    # 対立画像を作る
    target_label = str(p_args.target)
    image_tanks = list(map(lambda path: path.split('/')[-1], img_folpath))
    data = data_api.DataHandling(target_label=target_label ,image_tanks=image_tanks)
    noise = data.oppo_kernel(image_tanks=image_tanks)
    noise.make_noise()
    targets, not_targets = data.read_dirs(datas_dir=data.data_handling.datas_dir, target_label=target_label)
    x_train, x_test, y_train, y_test = data.get_builtup_data(targets=targets, not_targets=not_targets, flatten=False, color_mode='grayscale')
    print(len(x_train), len(x_test), len(y_train), len(y_test))
    print(y_train)
    print(y_test)
    #ここまでok
    ml = ml_api.MachineLearning()
    model = ml.build_model()
    datas = (x_train, x_test, y_train, y_test)
    es = True if p_args.train is 'True' or p_args.train is 'true' else False
    made_model_name = ml.train_model(model=model, datas=datas, save_name=image_tanks[0], es=es)
    app = pred_app.PredApp(image_tanks[0], 'not_{}'.format(image_tanks[0]))
    app.debug = True
    app.run(made_model_name)

def print_model_arch(model):
    model.summary()

if __name__ == '__main__':
    main()