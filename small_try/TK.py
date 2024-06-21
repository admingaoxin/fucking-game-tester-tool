import tkinter as tk
from tkinter import ttk
import pandas as pd
import difflib

def compare_tables():
    file1 = entry1.get()
    file2 = entry2.get()

    df1 = pd.read_excel(file1, engine='openpyxl')
    df2 = pd.read_excel(file2, engine='openpyxl')

    diff = difflib.unified_diff(df1.to_string().splitlines(), df2.to_string().splitlines())
    diff_list = list(diff)
    diff_str = '\n'.join(diff_list)

    text.delete(1.0, tk.END)
    text.insert(tk.END, diff_str)

def main():
    root = tk.Tk()
    root.title("表格比对工具")

    label1 = tk.Label(root, text="文件1:")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(root)
    entry1.grid(row=0, column=1)

    label2 = tk.Label(root, text="文件2:")
    label2.grid(row=1, column=0)

    entry2 = tk.Entry(root)
    entry2.grid(row=1, column=1)

    compare_button = tk.Button(root, text="比对", command=compare_tables)
    compare_button.grid(row=2, column=0, columnspan=2)

    text = tk.Text(root, height=10, width=50)
    text.grid(row=3, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()