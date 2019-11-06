#!/usr/local/var/pyenv/versions/anaconda3-5.2.0/envs/ml/bin/python
import sys
import argparse
import pprint
from crawler import system as crawler_api
from ml import system as ml_api
from ml.data_handling import system as data_api
from etc import system_metadata as opt
from common_handler.hyper_handler import get_static_labels
from etc import wordart
from pred_app import pred_app


def main():
    if len(sys.argv) <= 1:
        print(opt.help)
        sys.exit(0)
    parser = argparse.ArgumentParser(description='engine ssl')
    parser.add_argument('-t', '--target', help='target name.')
    parser.add_argument('-nt', '--nottarget', help='not target name.', nargs='*')
    parser.add_argument('-tr', '--train', help='train status.')
    parser.add_argument('-r', '--reuse', help='Launch the app on an existing model.', nargs='*')
    parser.add_argument('-f', '--font', help='起動時のフォント')
    p_args = parser.parse_args()

    font = p_args.font if p_args.font != None else 'slant'
    wordart.print_logo(font)

    if p_args.reuse == None:
        img_folpath = []
        target_folpath = []
        #ターゲット画像収集用APIをインスタンス化
        c = crawler_api.Clawler([p_args.target])
        c.delete_datas_dir()
        c.crawl()
        img_folpath.append(c.save_img(rtn_folpath=True))
        target_folpath.append(c.save_img(rtn_folpath=True))
        # es = True if p_args.train is 'True' or p_args.train is 'true' else False

        #ターゲットではない画像収集用APIをインスタンス化
        if p_args.nottarget != None:
            for nt in p_args.nottarget:
                not_c = crawler_api.Clawler([nt])
                not_c.crawl()
                img_folpath.append(not_c.save_img(rtn_folpath=True))

        # 対立画像を作る
        target_label = str(p_args.target)
        image_tanks = list(map(lambda path: path.split('/')[-1], img_folpath))
        nt_image_tanks = list(map(lambda path: path.split('/')[-1], target_folpath))
        # print(image_tanks)
        data = data_api.DataHandling(target_label=target_label ,image_tanks=image_tanks)
        noise = data.oppo_kernel(target_dir=nt_image_tanks ,image_tanks=image_tanks)
        labels = noise.make_noise()
        labels.insert(0, str(p_args.target))
        #ここまで
        targets, not_targets = data.read_dirs(target_label=target_label)
        # print('target_image_path')
        # pprint.pprint(targets)
        # print('not_target_image_path')
        # pprint.pprint(not_targets)
        x_train, y_train, x_test, y_test = data.get_builtup_data(targets=targets, not_targets=not_targets, color_mode='grayscale')
        print('num: x_train:', len(x_train), ' x_test:', len(x_test), 'y_train:', len(y_train), 'y_test:', len(y_test))
        ml = ml_api.MachineLearning()
        datas = (x_train, y_train, x_test, y_test)
        model = ml.build_model(num_classes=len(y_train[0]))
        model_name = ml.train(model=model, datas=datas, name=p_args.target, es=p_args.train)
    else:
        labels = get_static_labels()
        labels.insert(0, str(p_args.reuse[0]))
        model_name = p_args.reuse[0] + '.h5'

    app = pred_app.PredApp(labels)
    app.debug = True
    app.run(model_name=model_name)

def print_model_arch(model):
    model.summary()

if __name__ == '__main__':
    main()