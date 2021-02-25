![akiba_translation](https://socialify.git.ci/Akegarasu/akiba_translation/image?description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fs3.ax1x.com%2F2021%2F02%2F25%2FyvLBJe.png&owner=1&pulls=1&stargazers=1&theme=Light)
# akiba_translation

基于selenium的一个新式烤推机  

~~鸽到放假（bushi）~~  

### 食用方法

部署文档：[deploy.md](https://github.com/Akegarasu/akiba_translation/blob/main/docs/deploy.md)

部署好后修改utils/template.py中的内容，在`TEMP`中加入你的模板
每一个模板都是一个`dict`，需要有`html`、`icon_b64`两个字段。
其中，有两个魔术字符

- `{KT_IMG}` 会被替换为烤推标识的base64
- `{T}` 会被替换为烤推文本

本项目已经提供了一个名为`akiba_temp`的模板，可以参考该模板进行修改。
```python3
"akiba_temp": {
    "html": '''你的烤推html模板（插入模板）''',
    "icon_b64":  "烤推标识的图片base64"   
}
```

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