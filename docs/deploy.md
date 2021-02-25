# 烤推机部署文档

## Ubuntu 18.04

### 全局依赖

请在root权限下执行。

#### apt安装以下软件包：

* Web服务器 apache2 / nginx / etc.

* unzip

* git

* python3.7 和 python3-pip

* chromium-browser

* fonts-noto 和 fonts-noto-color-emoji

* redis

* npm(可选)
  
  ```bash
  apt install apache2 npm unzip git python3.7 python3-pip chromium-browser fonts-noto fonts-noto-color-emoji redis
  ```


#### npm安装以下软件包：(可选)

* pm2

  ```bash
  npm install pm2 -g
  pm2 startup
  ```



#### 手动安装ChromeDriver：  [ https://chromedriver.chromium.org/downloads ]

  * 通过`chromium-browser --version`查询版本，然后下载相应的二进制文件并赋权放入`/usr/local/bin`中

  * Ubuntu 18.04软件源一般提供的是version 76

    ```bash
    wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    mv chromedriver /usr/local/bin
    ```
    

### 用户空间

请在非root权限的用户下执行。

#### 拉取项目

```bash
git clone https://github.com/Akegarasu/akiba_translation.git
```

#### 安装python依赖

```bash
pip3 install pipenv
cd akiba_translation
python3 -m pipenv run pip install -r requirements.txt
python3 -m pipenv run pip install gunicorn
```

#### 启动主程序
- 在上述部分没有安装npm、pm2的

**重启服务器需要重新执行**
```bash
screen -S api_run
cd akiba_translation
python3 -m pipenv run ./api_run.sh

按下 ctrl+A+d
screen -S cel_run
cd akiba_translation
python3 -m pipenv run ./cel_run.sh
```
- 在上述部分安装好了npm、pm2的
```bash
python3 -m pipenv run pm2 start api_run.sh
python3 -m pipenv run pm2 start cel_run.sh
pm2 save
```

由`pm2 status`查看各进程均为online即可。

如有异常，可用`pm2 logs <id>`来查看各进程的日志输出。

至此，已经配置完成可以开始你的烤推之旅了、但是 **不推荐直接暴露flask的端口**

为此，可以继续执行之后的步骤（你需要有一个域名）

### 配置Web服务
#### nginx

```nginx
server {
    listen 80;
    server_name your_server;
    location ^~ /api/ {
        proxy_pass http://127.0.0.1:9090;
        proxy_redirect off;
        proxy_set_header Host $host:80;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location / {
        root /root/akiba_translation/imgs;
        index index.html;
    }
}
```