FROM python:3.8
RUN mkdir /mdblog && mkdir mdblog/data && mkdir mdblog/config
COPY config.toml /mdblog/config
RUN pip3 install sanic toml fire jinja2  --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple && pip3 install mdblog -U
WORKDIR /
CMD ["mdblog","run","--config","/mdblog/config/config.toml"]