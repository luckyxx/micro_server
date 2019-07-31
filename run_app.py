import atexit
# 导入http server
from wgsi_server.wgsi_server import MhttpServer
from kanado import Kanado, render_template
from blog.blog import Blog

if __name__ == '__main__':
    app=Kanado(__name__)

    blogs = []
    b1 = Blog(1, 'hello1', 'zhangsan')
    b2 = Blog(2, 'hello2', 'lisi')
    blogs.append(b1)
    blogs.append(b2)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/blogs')
    def list_notes():
        return render_template('list_blogs.html',blogs = blogs)

    @app.route('/blog/<id>')
    def query_note(id):
        blog = None
        # 到数据库查询博文详情
        for blg in blogs:
            if blg.id == int(id):
                blog = blg
        # 渲染博文详情页面
        return render_template('query_blog.html', blog=blog)
    host = '127.0.0.1'
    port = 8889
    server=MhttpServer(host,port,app)
    atexit.register(server.server_close)
    print('running http://{}:{}'.format(host, port))
    server.serve_forever()


