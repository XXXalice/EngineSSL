from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import os

def main():
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    img_dir = os.listdir('./src')
    if '.DS_Store' in img_dir:
        img_dir.remove('.DS_Store')
    suisui_img = img_dir[0]
    print(suisui_img)

if __name__ == '__main__':
    main()