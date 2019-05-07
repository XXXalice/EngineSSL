import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array, load_img, array_to_img
img_path = './check_imgs/001.png'

pilobj_fromimg = Image.open(img_path)
pilobj_fromimg_alt = load_img(img_path, target_size=(100, 100), grayscale=True)
# pilobj_fromimg_alt.show()
print(type(pilobj_fromimg), type(pilobj_fromimg_alt))
nda = [img_to_array(pilobj) for pilobj in [pilobj_fromimg, pilobj_fromimg_alt]]

for i in nda:
    print(i.shape)

augmantated_img = np.ravel(np.float32(nda[1]) / 255)
print(augmantated_img.shape)
img_bin = augmantated_img.reshape(100, 100, 1)
img = array_to_img(img_bin)
print(type(img))
img.show()