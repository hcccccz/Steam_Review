
#删掉 "average achievements"
#修改 “price“
#算出推出日期
#算出评论数量
#算出好评率
#增加语言支持

import json

def remove_key(dict_ob,key):
    if key in dict_ob:
        del dict_ob[key]
    return dict_ob

with open("before_clean.json", "r") as file:
    before = json.loads(file.read())
    before = remove_key(before,"average achievements")
