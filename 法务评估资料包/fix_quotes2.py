
# -*- coding: utf-8 -*-
import re

# 先还原被错误替换的函数默认参数（把「xxx」还原回"xxx"只在函数定义行）
with open('generate_docs.py', encoding='utf-8') as f:
    src = f.read()

# 还原函数参数默认值行里的「」回双引号（这些都是ASCII字符串）
# 这些是在 def 行或者是函数调用时的 name_cn=... name_en=... 等参数默认值
# 策略：把「宋体」「黑体」「Times New Roman」「Arial」等还原
restore = [
    ('\u300c宋体\u300d', '"宋体"'),
    ('\u300c黑体\u300d', '"黑体"'),
    ('\u300cTimes New Roman\u300d', '"Times New Roman"'),
    ('\u300cArial\u300d', '"Arial"'),
]
for old, new in restore:
    src = src.replace(old, new)

# 现在把剩余的「」（应该只在字符串内容里出现）保留
with open('generate_docs.py', 'w', encoding='utf-8') as f:
    f.write(src)

import ast
try:
    ast.parse(src)
    print('syntax OK')
except SyntaxError as e:
    print(f'line {e.lineno}: {e.msg}')
    print('text:', repr(e.text))
