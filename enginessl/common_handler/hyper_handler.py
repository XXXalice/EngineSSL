import inspect
import os

def get_static_labels():
    here = "/".join(inspect.stack()[0][1].split('/')[:-2])
    img_crust = os.path.join(here, 'data', 'img')
    items = sorted([item.split('_')[1] for item in os.listdir(img_crust) if str(item).startswith('n_')])
    return items
