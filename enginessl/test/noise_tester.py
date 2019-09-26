import inspect
import argparse
import os
import sys
import numpy as np
REL_HIERARCHY = 2
toplevel_path = os.path.join('/'.join(os.path.abspath(__file__).split('/')[:-REL_HIERARCHY]))
sys.path.append(os.path.join(toplevel_path, 'ml', 'data_handling'))
import effect_func as ef
from keras.preprocessing.image import load_img, img_to_array, array_to_img, save_img


def make_noise(img_bin, mode):
    e_dict = {
        's_random': lambda x: ef.simple_random(x),
        # 'n_random': lambda x: ef.normal_random(x),
        'mizutama': lambda x: ef.mizutama(x),
        'rect': lambda x: ef.discontinuous_random(x),
        'slice': lambda x: ef.slice(x),
    }
    try:
        effected = e_dict[mode](img_bin)
        print(effected.shape)
        img_name = make_imgname(mode=mode)
    except Exception as e:
        sys.stderr.write(str(e)+'\n')
        raise e
    save_img(path=os.path.join('noise_test', img_name), x=effected)
    return True

def make_imgname(mode):
    tag = np.random.randint(0, 9999)
    name = '{}_{:04}.png'.format(mode, tag)
    return name

def delete_file(item):
    wild = True if item == '.' else False
    import shutil
    del_target = os.path.join('noise_test') if wild else os.path.join('noise_test', item)
    try:
        shutil.rmtree(path=del_target)
        if wild:
            os.makedirs(del_target)
    except Exception as err:
        sys.stderr.write(str(err)+'\n')
        return False
    return True

def main():
    img_path = './noise_test/001.png'
    parser = argparse.ArgumentParser(description='noise_tester')
    parser.add_argument('-i', '--img', help='img path.')
    parser.add_argument('-m', '--mode', help='noise algorithm')
    parser.add_argument('-d', '--delete', help='[CAUTION] delete experimental product in ./noise_test/')
    args = parser.parse_args()
    if args.delete != None:
        del_result = delete_file(args.delete)
        message = 'succsessed rm {}'.format(args.delete) if del_result else 'faild rm. try again.'
        print(message)
        exit(0)
    if args.img != None:
        img_path = args.img
    img = load_img(img_path, color_mode='grayscale', target_size=(100, 100))
    img_bin = img_to_array(img)
    result = make_noise(img_bin=img_bin, mode=args.mode)
    if result:
        print('succsessed.')


if __name__ == '__main__':
    main()