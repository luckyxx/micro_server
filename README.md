###StaticHttpServer

>1.  __init__  host(服务器地址)  port(端口号)
>> 初始化、启动服务器
>2. accept  sock (网络链接对象)
>> 等待客户端接入，并且注册已连接的客户端到监听里
>3. write sock (网络链接对象)
>> 组织响应数据包，用socket对象把数据包发送给浏览器，解除监听，关闭当前socket
>4. read  conn
>> 从请求里读物数据，把字节数据交给请求解析类去解析，当前链接对象注册监听
>5. server_close
>> 关闭当前socket对象，关闭监听器对象
>6. server_bind
>> 将我们设置的地址和端口绑定到服务器socket对象上
>7. server_listen
>> 服务端socket对象启动监听
>8. server_socket
>> 调用server_bind() 和server_listen()
>9. server_forever
>> 无限从监听器中取出事件列表，循环事件列表，取出触发每个时间的socket对象，调用注册时指定的函数

## BaseRequest
>1. __init__   request
>>接受request对象，调用_parsed_request函数
>2. _parsed_request
>> 调用 _parsed_header和_parsed_body函数 
>3. _parsed_header
>> 把http协议request对象的头部信息拆分出来，复制到字典对象 
>4. _parsed_body
>>把http 协议request对象body信息解析出来赋值给self.body
>5. method
>>返回http协议request对象的请求类型
>6. url
>>返回http协议request对象的请求地址
>7. protocol
>>返回http协议request对象的请求协议
