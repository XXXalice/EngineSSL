def simple_random(img_bin):
    import numpy as np
    scale = img_bin.shape[0]
    re_bin = np.random.permutation(np.ravel(img_bin)).reshape(scale, scale, -1)
    return re_bin

def ancestral_scale_random(img_bin):
    pass

def ancestral_scale_random_v2(img_bin):
    pass

def swap(img_bin):
    pass

def use_gradcam(img_bin):
    pass

def mizutama(img_bin, max=25):
    import cv2
    import numpy as np
    scale = img_bin.shape
    mizutama_num = np.random.randint(3, max)
    for i in range(mizutama_num):
        cv2.ellipse(img_bin,
                    ((np.random.randint(0, scale[0]), np.random.randint(0, scale[0])),
                    (np.random.randint(0, scale[0]), np.random.randint(0, scale[0])),
                    np.random.randint(0, 180)),
                    (np.random.randint(0, 255)),
                    np.random.randint(1, 10),
                    cv2.LINE_8
                    )
    return img_bin

def discontinuous_random(img_bin, max=25):
    import cv2
    import numpy as np
    scale = img_bin.shape
    rect_num = np.random.randint(5, max)
    region = lambda :np.random.randint(0, scale[0])
    for i in range(rect_num):
        cv2.rectangle(img_bin,
                      pt1=(region(), region()),
                      pt2=(region(), region()),
                      color=(0, 0, 0),
                      thickness=np.random.randint(1,10),
                      lineType=cv2.LINE_8
                      )
    return img_bin


def slice(img_bin, size=40):
    import numpy as np
    scale = 100
    div_size = size
    while True:
        if scale % div_size == 0:
            break
        else:
            div_size -= 1
            if div_size == 1:
                break
    re_bin = np.random.permutation(img_bin.reshape(div_size, -1, 1)).reshape(scale, scale, -1)
    return re_bin
