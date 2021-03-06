![akiba_translation](https://socialify.git.ci/Akegarasu/akiba_translation/image?description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fs3.ax1x.com%2F2021%2F02%2F25%2FyvLBJe.png&owner=1&pulls=1&stargazers=1&theme=Light)
# akiba_translation

基于selenium的一个新式烤推机！高效，方便，快捷的进行翻译推特进行嵌字

**支持多种类型的推特**

- 单条推特

- 带转发的推特

- 多条回复连续烤制


**提供了方便快捷的webapi**

- 提交任务
- 检查任务

**Celery异步任务队列**

- 并发性能高

若有发现 bug 、以及建议欢迎在 issue 中提问，也欢迎 pr

### 食用方法

### 第一步：部署

部署文档：[deploy.md](https://github.com/Akegarasu/akiba_translation/blob/main/docs/deploy.md)

### 第二步：添加你的烤推模板

当然，你也可以选择不添加，程序会直接使用内置的模板

在`templates`文件夹下，新建一个文件夹。

文件夹名称会作为**模板名称**

在该文件夹下添加两个文件，分别是`index.html`与`icon.png`，分别是烤推的模板 html 和烤推的图标（PNG格式）

其中，有两个魔术变量

- `{KT_IMG}` 会被替换为烤推标识的base64
- `{T}` 会被替换为烤推文本

**以下是旧版添加模板方法，现已过时，但仍然可用**

部署好后修改utils/template.py中的内容，在`TEMP`中加入你的模板
每一个模板都是一个`dict`，需要有`html`、`icon_b64`两个字段。
其中，有两个魔术变量

- `{KT_IMG}` 会被替换为烤推标识的base64
- `{T}` 会被替换为烤推文本

本项目已经提供了一个名为`akiba_temp`的模板，可以参考该模板进行修改。
```python3
"akiba_temp": {
    "html": '''你的烤推html模板（插入模板）''',
    "icon_b64":  "烤推标识的图片base64"   
}
```

### 第三步：进行烤制

以下是 webapi 提供的接口

- 提交烤推任务

终结点：`http://example.com/api/auto`  方式：`POST` 

需要添加 `headers`：`Content-Type: application/json`

POST 的内容如下所示

```
{
        "template_name": "模板名称",
        "link": "推文链接",
        "text": {
            "tweet": "推特的烤制内容",
            "retweet": "回复推的烤制内容" # 仅在 type 为 retweet 时需要该字段
        },
        "type": "烤推类型" # single，retweet，reply三种
}
```

返回值：

```
{'task_id': task_id}
```



- 查询烤制任务

  终结点：`http://example.com/api/get_task=<string:task_id> `方式：`GET` 

  

### 目前进度

- [ ] 基础烤推功能
    - [x] 基础单挑推特烤制
    - [x] 转发烤制
    - [X] 回复烤制
        - [X] 单条回复
        - [X] 多条回复
    - [ ] 转发怎么还带着回复这什么破玩意
- [ ] 烤推bot端


2020.1.5更新：我回来了 不鸽了（bushi）