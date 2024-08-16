import xlrd
from util import glb


class readXlsUtil ():
    def __init__(self, xlsPath, sheetName):
        self.data = xlrd.open_workbook (xlsPath)
        self.sheetList = self.data.sheet_names ()
        self.table = self.data.sheet_by_name (sheetName)
        # 读取第一行数据作为key值
        self.keys = self.table.row_values (0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols

    # 获取用例数据
    def dict_data(self, case_type):
        if self.rowNum <= 1:
            print ("总行数小于1")
        else:
            r = []

        # 查找 case_type 列的索引
        try:
            case_type_index = self.keys.index ('case_type')
        except ValueError:
            print ("未找到列头 'case_type'")
            return []

        for i in range (1, self.rowNum):  # 从第二行开始读取数据
            s = {}
            values = self.table.row_values (i)
            s['rowNum'] = i + 2
            # 去除空白并将 case_type 转换为字符串进行比较
            case_type_value = values[case_type_index]
            if int(case_type_value) == int(case_type):
                for x in range(self.colNum):
                    s[self.keys[x].strip()] = str(values[x]).strip ()
                r.append(s)
            else:
                print(case_type)
                print (f"行 {i + 1} 被跳过，case_type 不匹配: {case_type_value}")

        return r

    # 获取用例名称
    def dict_name(self, caseData):
        caseNames = []
        for i in caseData:
            caseNames.append (i['caseName'])
            print ("caseData:", caseData)
            print ("caseNames:", caseNames)
        return caseNames


if __name__ == "__main__":
    filepath =r'D:\try-pytest\data\case.xlsx'
    sheetName = 'Sheet1'
    data = readXlsUtil (filepath, sheetName)
    case_data = data.dict_data (1)
    caseNames = data.dict_name (case_data)
    print (caseNames)