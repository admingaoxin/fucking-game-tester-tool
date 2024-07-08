from pathlib import Path

path = Path(r"F:\AutoWeb\Tesla_front\src\router\modules")
code = Path(r"F:\AutoWeb\Tesla_front\src\router\modules\exception.ts").read_text(encoding="utf-8")
print(code)
sort = 15
for name, title, icon in [
    ("project", "项目管理", "AppleOutlined"),
    ("case_api", "接口测试", "DingdingOutlined"),
    ("case_ui", "UI测试", "YoutubeOutlined"),
    ("suite", "测试套件", "SkypeOutlined"),
    ("account", "个人中心", "FacebookOutlined"),
    ("system", "系统设置", "SlackSquareOutlined"),
]:
    sort += 1
    new_path = path / f"houchen_{name}.ts"
    print(new_path)
    new_code = (code.replace("exception", f"{name}")  # 路径
                .replace("Exception", name.title())  # 路由的名字
                .replace("异常页面", title)  # 显示名字
                .replace("sort: 3", f"sort: {sort}")  # 排序
                .replace("ExclamationCircleOutlined", icon)  # 图标
                )
    new_path.write_text(new_code, encoding="utf-8")
