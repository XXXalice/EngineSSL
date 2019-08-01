def simple_random(img_bin):
    import random
    import numpy as np
    # maxis = []
    # minis = []
    # li = img_bin.tolist()
    # li_proto = li[:]
    # random.shuffle(li)
    # print(li)
    # re_bin = np.array(li)
    # for tensor in range(len(img_bin)-1):
    #     maxis.append(img_bin[tensor].argmax())
    #     minis.append(img_bin[tensor].argmin())
    # for tensor in range(len(img_bin)):
    #     img_bin[tensor] = random.random(img_bin[tensor])
    # print(img_bin[0])
    # print(type(img_bin))
    # print(maxis)
    # print(minis)


    re_bin = np.random.permutation(img_bin)
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
    region = np.random.randint(0, scale[0])
    for i in range(rect_num):
        cv2.rectangle(img_bin,
                      pt1=(region, region),
                      pt2=(region, region),
                      color=(0, 0, 0),
                      thickness=np.random.randint(1,10),
                      lineType=cv2.LINE_8
                      )
    return img_bin