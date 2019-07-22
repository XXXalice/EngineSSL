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
        'n_random': lambda x: ef.normal_random(x),
        'mizutama': lambda x: ef.mizutama(x),
    }
    try:
        effected = e_dict[mode](img_bin)
        print(effected.shape)
        img_name = make_imgname(mode=mode)
    except Exception as e:
        sys.stderr.write(str(e)+'\n')
        exit(0)
    save_img(path=os.path.join('noise_test', img_name), x=effected)
    return True

def make_imgname(mode):
    tag = np.random.randint(0, 9999)
    name = '{}_{:04}.png'.format(mode, tag)
    return name

def main():
    img_path = './noise_test/test.png'
    parser = argparse.ArgumentParser(description='noise_tester')
    parser.add_argument('-i', '--img', help='img path.')
    parser.add_argument('-m', '--mode', help='noise algorithm')
    args = parser.parse_args()
    if args.img != None:
        img_path = args.img
    img = load_img(img_path, color_mode='grayscale', target_size=(100, 100))
    img_bin = img_to_array(img)
    result = make_noise(img_bin=img_bin, mode=args.mode)
    if result:
        print('succsessed.')





if __name__ == '__main__':
    main()