from thread import Settings
import xlrd
import os

def open_excel(file_path):
    try:
        excel = xlrd.open_workbook(file_path)
        return excel
    except Exception as e:
        print("打开Excel错误！")
 
def verify_table(table):
    """
    验证sheet是否有效
    :param table:
    :param sheet_name:
    :return:
    """
    if table.nrows < 5 or table.ncols < 2:
        return False
    clientstr = "".join(table.cell_value(2, 0)).lower()
    serverstr = "".join(table.cell_value(4, 0)).lower()
    if 'client' not in clientstr:
        return False
    if 'server' not in serverstr:
        return False
    return True
 
def parse_excel(file_path, fieldnames, side):
    """
    解析Excel表格内容
    :return:value_dict
    """
    os.chdir(Settings.setting["dist"])
    excel = open_excel(file_path)
    sheet_names = excel.sheet_names()
    value_dict = {}
    for sheet in sheet_names:
        table = excel.sheet_by_name(sheet)
        if not table:
            print("table为空")
            continue
        if not verify_table(table):
            continue
        client_key = {}
        data_type = {}
        server_key = {}
        for col in range(1, table.ncols):
            client_key[col] = table.cell_value(2, col)
            data_type[col] = table.cell_value(3, col)
            server_key[col] = table.cell_value(4, col)
        key = 0
        if "," in fieldnames:
            fieldname = str(fieldnames).split(",")
            for fieldname in fieldname:
                if side in ["client", "client_and_server"]:
                    key = [k for k, v in client_key.items() if v == fieldname]
                elif side == "server":
                    key = [k for k, v in server_key.items() if v == fieldname]
                for row in range(5, table.nrows):
                    id = table.cell_value(row, 1)
                    if id == "":
                        continue
                    value = table.cell_value(row, int("".join([str(x)for x in key])))
                    key_tuple = (sheet, row, int("".join([str(x)for x in key])))
                    if value == "":
                        continue
                    value_dict[key_tuple] = value
        else:
            fieldname = fieldnames
            if side in ["client" , "client_and_server"]:
                key = [k for k, v in client_key.items() if v == fieldname]
            elif side == "server":
                key = [k for k, v in server_key.items() if v == fieldname]
            for row in range(5, table.nrows):
                id = table.cell_value(row, 1)
                if id == "":
                    continue
                value = table.cell_value(row, int("".join([str(x)for x in key])))
                key_tuple = (sheet, row, int("".join([str(x)for x in key])))
                if value == "":
                    continue
                value_dict[key_tuple] = value
    # print("value_dict",value_dict)
    return value_dict