import os
from jinja2 import Environment,FileSystemLoader
def render_template(template_name_or_list,**context):
    path='{}\\blog\\templates\\'.format(os.getcwd())  # os.getcwd 返回 当前工作路径
    #  创建一个加载器
    print(path)
    loader = FileSystemLoader(path)

    # 用加载器创建一个环境, 有了它才能读取模板文件
    env = Environment(loader=loader)

    # 调用 get_template() 方法加载模板并返回
    template = env.get_template(template_name_or_list)
    print()
    html = template.render(**context)
    # print(html)
    return html
# print(render_template('index.html'))



