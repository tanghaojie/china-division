# 数据来源  2020年12月中华人民共和国县以上行政区划代码  http://www.mca.gov.cn/article/sj/xzqh/2020/20201201.html
# 因为 三沙市（460300）的 西沙区、南沙区 暂时没有行政区划代码，故移除

import json
from json import encoder
result = []
with open('xzqh.txt', 'r', encoding='utf-8') as f:
    for line in f:
        [code, name] = line.split()
        # 省，直辖市
        if code.endswith('0000'):
            result.append({
                'code': code,
                'value': name,
                'label': name,
                'children': []
            })
        # 地级市
        elif code.endswith('00'):
            province = next(
                (item
                 for item in result if item['code'].startswith(code[0:2])),
                None)
            if province:
                province['children'].append({
                    'code': code,
                    'value': name,
                    'label': name,
                    'children': []
                })
        # 区县
        else:
            province = next(
                (item
                 for item in result if item['code'].startswith(code[0:2])),
                None)
            if province:
                chis = province['children']
                city = next((i for i in chis if i['code'].startswith(code[0:4])
                             and i['code'].endswith('00')), None)
                # 属于地级市
                if city:
                    city['children'].append({
                        'code': code,
                        'value': name,
                        'label': name,
                        'children': []
                    })
                # 属于直辖市
                else:
                    province['children'].append({
                        'code': code,
                        'value': name,
                        'label': name,
                        'children': []
                    })

with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, sort_keys=False, indent=2)
