"""
我是注释行
"""
def print_lists1(this_list):
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