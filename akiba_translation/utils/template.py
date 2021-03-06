import base64
import os
from typing import Dict, List, Optional

RETWEET_TEMP = '''<div style="margin:2px 2px"><style type="text/css">.link{color:#1DA1F2}</style><img src="{KT_IMG}" height="25"></div><div style="font-size: 18px;font-family: Microsoft YaHei UI, Microsoft YaHei, sans-serif;width: 544px;word-break: break-word;line-height:1.5; font-weight:400; letter-spacing:0.01em">{T}</div></div>'''
TEMPLATE: dict = {
    "default": {
        "html": '''<div style="margin:5px 10px"><style type="text/css">.link{color:#1DA1F2}</style><div style="color: #1DA1F2">翻译自日文</div></div><div style="margin:1px 5px;font-size: 27px;font-family: Microsoft YaHei UI, Microsoft YaHei, sans-serif;width: 544px;word-break: break-word;line-height:1.5; font-weight:400; letter-spacing:0.01em">{T}</div></div>''',
        "icon_b64": ""
    },
    "default_with_img": {
        "html": '''<div style="margin:5px 10px"><style type="text/css">.link{color:#1DA1F2}</style><img src="{KT_IMG}" height="25"></div><div style="margin:1px 5px;font-size: 27px;font-family: Microsoft YaHei UI, Microsoft YaHei, sans-serif;width: 544px;word-break: break-word;line-height:1.5; font-weight:400; letter-spacing:0.01em">{T}</div></div>''',
        "icon_b64": ""
    }
}


def load_html(path) -> Optional[str]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            temp_html = f.readlines()
        ok = "".join(temp_html).replace("\n", "")
        return ok


def img_to_base64(path) -> Optional[str]:
    if os.path.exists(path):
        with open(path, 'rb') as f:
            image = f.read()
            ok = "data:image/png;base64," + str(base64.b64encode(image), encoding='utf-8')
            return ok


def load_template() -> Dict[str, Dict]:
    global TEMPLATE
    dirs = os.listdir("./templates")
    for i in dirs:
        d = "./templates/" + i
        html = load_html(d + "/index.html")
        icon_b64 = img_to_base64(d + "/icon.png")
        TEMPLATE[i] = {
            "html": html,
            "icon_b64": icon_b64
        }
    return TEMPLATE
