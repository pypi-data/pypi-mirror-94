"""
我是注释行
"""
from wm_test import wangming1137342409

def print_lists2(this_list):
    """
    把多重列表零散化
    :param this_list:11
    :return:
    """
    for lists in this_list:
        if isinstance(lists,list):
            print_lol(lists)
        else:
            print(lists)