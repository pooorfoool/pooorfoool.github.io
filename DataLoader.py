from python_calamine import load_workbook
'''
依赖python_calamine
使用：
d=DataLoader('test.xls')
d.rows #行数组
d.cols #列数组
d.to_dicts() #字典数组
d.to_pairs(key_col_index=0,value_col_index=3) #键值对
'''
class DataLoader:
    def __init__(self,path,sheet=0):
        self.raw_data=None
        self.data=None
        self.read_excel(path,sheet) 
    @property
    def rows(self):
        '''
        返回由行组成的list
        其中每行都是一个list
        格式：[[A1,B1,...],[A2,B2,...],...]
        '''
        return self.data
    @property
    def cols(self):
        '''
        返回由列组成的list
        其中每列都是一个list
        格式：[[A1,A2,...],[B1,B2,...],...]
        '''
        #行list转列list
        tdata=[list(t) for t in zip(*self.data)]
        return tdata
    def to_dicts(self,head_row_index=0):
        '''
        返回由行组成的list
        其中每列都是一个dict,某行做key,其余行做value
        格式：[{A1:A2,B1:B2,...},{A1:A3,B1:B3,...},...]
        '''
        keys=self.data[head_row_index]
        start_row=head_row_index+1
        tdata=[dict(zip(keys,values)) for values in self.data[start_row:]]
        return tdata
    def to_pairs(self,key_col_index=0,value_col_index=1):
        '''
        返回由两列组成的dict
        其中1列做key,1行做value,同一行组成 key:value
        格式：{A1:B1,A2:B2,...}
        '''
        tcols=self.cols
        tdata=dict(zip(tcols[key_col_index],tcols[value_col_index]))
        return tdata

    def read_excel(self,path,sheet=0):
        '''
        sheet可以是表序号(从0开始),也可以是表名(str)
        '''
        workbook=load_workbook(path)
        if type(sheet)==int:
            worksheet=workbook.get_sheet_by_index(sheet)
        else:
            assert sheet in workbook.sheet_names,f"{path} 中无表 {sheet}"
            worksheet=workbook.get_sheet_by_name(sheet)
        self.raw_data=worksheet.to_python()
        #修正int
        self.data=[[self.fix_number(i) for i in row] for row in self.raw_data]
        
    def fix_number(self,number):
        '''
        将float型的整数(例如：2.0)修正为int(结果：2)
        '''
        if isinstance(number,float) and number.is_integer():
            result=int(number)
        else:
            result=number
        return result
    