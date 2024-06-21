from DataLoader import DataLoader
import json

xl=DataLoader('新山东司法厅题库.xlsx')
data=xl.to_dicts()
with open('data.json',mode='w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False)
print('ok....')