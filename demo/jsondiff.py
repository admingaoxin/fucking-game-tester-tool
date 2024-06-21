import tkinter as tk
import json
import difflib


def decode_escapes(s):
    """解码字符串中的Unicode转义序列"""
    return s.encode('latin1').decode('unicode_escape')


def compare_jsons():
    json_str1 = json_entry1.get("1.0", tk.END).strip()
    json_str2 = json_entry2.get("1.0", tk.END).strip()


    try:
        data1 = json.loads(json_str1)
        data2 = json.loads(json_str2)


        json_str1 = json.dumps(data1, indent=4, sort_keys=True)
        json_str2 = json.dumps(data2, indent=4, sort_keys=True)


        diff = difflib.unified_diff(json_str1.splitlines(), json_str2.splitlines(), fromfile='JSON 1', tofile='JSON 2')


        decoded_diff = []
        for line in diff:
            # 解码可能存在的Unicode转义序列，使其在文本框中正确显示
            decoded_line = decode_escapes(line)
            decoded_diff.append(decoded_line)


        output_text.delete(1.0, tk.END)
        for line in decoded_diff:
            output_text.insert(tk.END, line + '\n')


    except json.JSONDecodeError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "输入的不是有效的JSON格式，请检查后重新输入。")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"发生错误：{str(e)}")


# 创建主窗口
root = tk.Tk()
root.title("JSON 数据比较工具")


# JSON数据输入框
json_label1 = tk.Label(root, text="第一个JSON数据:")
json_label1.pack()
json_entry1 = tk.Text(root, height=10, width=40)
json_entry1.pack()


json_label2 = tk.Label(root, text="第二个JSON数据:")
json_label2.pack()
json_entry2 = tk.Text(root, height=10, width=40)
json_entry2.pack()


# 比较按钮
compare_button = tk.Button(root, text="比较", command=compare_jsons)
compare_button.pack()


# 输出结果文本框
output_label = tk.Label(root, text="比较结果:")
output_label.pack()
output_text = tk.Text(root, height=10, width=80)
output_text.pack()


# 运行GUI主循环
root.mainloop()