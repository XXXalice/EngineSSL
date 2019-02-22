from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import os
import numpy as np
import sys
import glob

src_dir = './src'

flags = {
    'rm_flag':False,
    'show_flag':False
}

def main():
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    img_dir = os.listdir(src_dir)
    if '.DS_Store' in img_dir:
        img_dir.remove('.DS_Store')
    suisui_img = [os.path.join(src_dir, fname) for fname in img_dir]

    img = image.load_img(suisui_img[0], color_mode='grayscale')

    #npa変換(row, col, channel)
    x = image.img_to_array(img)

    #to four dim tensor (sample, row, col, channel)
    img_tensor = np.expand_dims(x, axis=0)

    img_generate(data_generator=datagen, img_tensor=img_tensor, img_name='test_suisui')

def img_generate(data_generator, img_tensor, img_name):

    temp_dir = os.path.join(src_dir, 'augmentations')
    if flags['rm_flag'] == True:
        remove_olddir(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    g = data_generator.flow(
        x=img_tensor,
        batch_size=img_tensor.shape[0],
        save_to_dir=temp_dir,
        save_format='png',
        save_prefix='img',

    )
    for i in range(4):
        batch = g.next()
    if flags['show_flag'] == True:
        show_madeimg(temp_dir, img_name)
    else:
        return

def remove_olddir(temp_dir):
    for i in glob.glob(os.path.join(temp_dir, '*.png')):
        os.remove(i)

def show_madeimg(temp_dir, img_name):
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gspc
    imgs = glob.glob(os.path.join(temp_dir, '*.png'))
    fig = plt.figure()
    gs = gspc.GridSpec(2,2)
    gs.update(wspace=0.1, hspace=0.1)
    for i in range(4):
        img = image.load_img(imgs[i])
        plt.subplot(gs[i])
        plt.imshow(img, aspect='auto')
        plt.axis('off')
    plt.savefig(os.path.join(temp_dir ,img_name+'.png'))

if __name__ == '__main__':
    if '-rm' in sys.argv:
        flags['rm_flag'] = True
    if '-sh' in sys.argv:
        flags['show_flag'] = True
    main()