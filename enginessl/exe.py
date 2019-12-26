#!/usr/local/var/pyenv/versions/anaconda3-5.2.0/envs/ml/bin/python
import sys
import argparse
import time
from crawler import system as crawler_api
from ml import system as ml_api
from ml.data_handling import system as data_api
from etc import system_metadata as opt
from common_handler.hyper_handler import get_static_labels
from etc import wordart
from pred_app import pred_app

class BuildTime:
    """
    時間測定用
    """
    def __init__(self):
        pass

    def start(self):
        self.start_time = time.time()

    def end(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time


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

    # 実行時間測定
    ti = BuildTime()
    ti.start()


    font = p_args.font if p_args.font != None else 'slant'
    wordart.print_logo(font)

    if p_args.reuse == None:
        img_folpath = []
        target_folpath = []
        #ターゲット画像収集用APIをインスタンス化
        c = crawler_api.Clawler([p_args.target])
        c.delete_datas_dir()
        c.crawl()
        c.write_crawl_stat()
        img_folpath.append(c.save_img(rtn_folpath=True))
        target_folpath.append(c.save_img(rtn_folpath=True))

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
        data = data_api.DataHandling(target_label=target_label ,image_tanks=image_tanks)
        noise = data.oppo_kernel(target_dir=nt_image_tanks ,image_tanks=image_tanks)
        labels = noise.make_noise()
        labels.insert(0, str(p_args.target))
        targets, not_targets = data.read_dirs(target_label=target_label)
        x_train, y_train, x_test, y_test = data.get_builtup_data(targets=targets, not_targets=not_targets, color_mode='grayscale')
        print('num: x_train:', len(x_train), ' x_test:', len(x_test), 'y_train:', len(y_train), 'y_test:', len(y_test))
        ml = ml_api.MachineLearning()
        datas = (x_train, y_train, x_test, y_test)
        model = ml.build_model(num_classes=len(y_train[0]))
        model_name = ml.train(model=model, datas=datas, name=p_args.target, es=p_args.train)
        ml.draw_graph(model_name=model_name)
        bias = ml.bias
    else:
        c = crawler_api.Clawler([p_args.reuse])
        num = c.read_crawl_stat(p_args.reuse)
        labels = get_static_labels()
        labels.insert(0, str(p_args.reuse))
        model_name = p_args.reuse + '.h5'
        bias = num

    # 経過時間
    elapsed_time = ti.end()
    print('elapsed_time: {}'.format(elapsed_time))

    app = pred_app.PredApp(labels, bias=bias)
    app.debug = True
    app.run(model_name=model_name)

def print_model_arch(model):
    model.summary()

if __name__ == '__main__':
    main()