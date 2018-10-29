def simple_random(img_bin):
    import random
    import numpy as np
    maxis = []
    minis = []
    li = img_bin.tolist()
    re_bin = np.array(li)
    print(li)
    # for tensor in range(len(img_bin)-1):
    #     maxis.append(img_bin[tensor].argmax)
    #     minis.append(img_bin[tensor].argmin)
    # # for tensor in range(len(img_bin)):
    # #     img_bin[tensor] = random.random(img_bin[tensor])
    # # print(img_bin[0])
    # # print(type(img_bin))
    # print(maxis)
    # print(minis)

def ancestral_scale_random(img_bin):
    pass

def ancestral_scale_random_v2(img_bin):
    pass

def swap(img_bin):
    pass