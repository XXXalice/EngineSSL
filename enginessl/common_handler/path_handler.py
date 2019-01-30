import sys
import os
import glob
sys.path.append(os.pardir)

ABSOLUTE_APP_NAME = 'enginessl'

def get_abspath(target):
    current = os.getcwd()
    all_fold_li = current.split('/')
    li_reversed = all_fold_li[::-1]
    fold_li, alt_fold_li = split_front_absapp(li_reversed)
    fold_li = [os.path.abspath(apppath) for apppath in fold_li]
    target_abspath = recursive_search(target, fold_li)
    return target_abspath

def get_user_env(root_envs):
    pass

def recursive_search(target, search_li):
    for search in search_li:
        print(search, 'check.')
        if search == target:
            print('hit')
            pass

def split_front_absapp(li):
    try:
        print(li.index(ABSOLUTE_APP_NAME))
        return li[:li.index(ABSOLUTE_APP_NAME)+1], li[li.index(ABSOLUTE_APP_NAME)+1:]
    except:
        print('target error.')
        exit()

def get_path(locate, axis, target):
    parts = []
    for folder in locate.split('/')[::-1]:
        parts.insert(0, folder)
        if folder == axis:
            break
    abspath = []
    abspath.append(locate.split(parts[0])[0]+parts[0])
    search_items = os.listdir(abspath[0])
    if '.DS_Store' in search_items:
        search_items.remove('.DS_Store')
    search_items_handled = ['/' + item for item in search_items]
    # print(search_items_handled)

    def __fetch(folder_path):
        """
        :param folder_path: 掘る対象
        :return: folder_path内のパス list
        """
        return os.listdir(folder_path)

    for item in search_items_handled:
        fullpath = abspath[0] + item
        # while len(os.listdir(fullpath)) != 0:
        #     abspath.append(fullpath)
        new_path = __fetch(fullpath)
        abspath.extend(new_path)
        print(abspath)
        try:
            new_path_items = ['/' + item for item in new_path.split('/')[-1] if '.' not in item]
            search_items_handled.extend(new_path_items)
            print(search_items_handled)
        except:
            break

def get_path_with_glob(locate, axis, target):
    try:
        dir_list = os.listdir(path=glob.glob(str(locate).split(axis)[0] + '**/{}'.format(target), recursive=True)[0])
        return dir_list
    except:
        file = glob.glob(str(locate).split(axis)[0] + '**/{}'.format(target), recursive=True)[0]
        return file

# def get_abspath_with_glob(locate, target):
#     print(locate)
#     try:
#         dir_list = os.listdir(path=glob.glob(str(locate) + '/**/{}'.format(target), recursive=True)[0])
#         return dir_list
#     except:
#         file = glob.glob(str(locate) + '/**/{}'.format(target), recursive=True)[0]
#         return file