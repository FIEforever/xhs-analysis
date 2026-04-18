
# -*- coding: utf-8 -*-
import re

with open('generate_docs.py', encoding='utf-8') as f:
    lines = f.readlines()

fixed = []
for line in lines:
    # 把 "中文..." 模式（中文字符开头的双引号包裹内容）替换为 「中文...」
    new_line = re.sub(u'"([\u4e00-\u9fff][^"]*?)"', u'\u300c\\1\u300d', line)
    fixed.append(new_line)

with open('generate_docs.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed)
print('done')

import ast
with open('generate_docs.py', encoding='utf-8') as f:
    src = f.read()
try:
    ast.parse(src)
    print('syntax OK')
except SyntaxError as e:
    print(f'line {e.lineno}: {e.msg}')
    print('text:', repr(e.text))
