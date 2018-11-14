import sys
import os
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