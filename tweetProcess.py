from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import re
from PIL import Image
from template import RETWEET_TEMP
from twemoji import EMOJI_HTML, twemoji_js


class Processor:
    def __init__(self, cfg):
        self.ops = webdriver.ChromeOptions()
        self.proxy = cfg['proxy']
        self.link = cfg['link']
        self.type = cfg['type']
        self.template = cfg['template']
        self.icon_b64 = cfg['icon_b64']
        self.text: dict = cfg['text']

        self.init_argument()
        self.driver = webdriver.Chrome(chrome_options=self.ops)
        self.init_webdriver()

    def init_argument(self):
        argument_list = [
            '--headless',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            f'--proxy-server={self.proxy}'
        ]
        for arg in argument_list:
            self.ops.add_argument(arg)

    def init_webdriver(self):
        self.driver.delete_all_cookies()

    def process_tweet(self):
        img_name = ""
        self.driver.get(self.link)
        WebDriverWait(self.driver, 60, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))
        if self.type == "single":
            try:
                img_name = self.process_tweet_single()
            except:
                print("err")
                self.driver.close()
        if self.type == "retweet":
            try:
                self.process_tweet_retweet()
                img_name = self.process_tweet_single()
            except:
                print("err")
                self.driver.close()
        if self.type == "reply":
            self.reply_times: str

        self.driver.close()
        return img_name

    def process_tweet_single(self):
        # process template
        text_emoji_parsed = self.process_emoji(self.text["tweet"])
        template = self.template.replace("{T}", text_emoji_parsed)
        if "KT_IMG" in template:
            template = template.replace("{KT_IMG}", self.icon_b64)
        # execute js
        ajs = '''document.querySelector(".css-1dbjc4n.r-156q2ks").innerHTML = document.querySelector(".css-1dbjc4n.r-156q2ks").innerHTML + `{HTML}` ''' \
            .replace("{HTML}", template)
        print(ajs)
        self.driver.execute_script(ajs)
        # modify tweet
        self.driver.set_window_size(640, self.driver.execute_script('''
        return document.querySelector("section").getBoundingClientRect().bottom
        '''))
        self.modify_tweet()
        # save and clip tweet image
        clip_info = self.driver.execute_script('''
        return document.querySelector("article .css-1dbjc4n .r-vpgt9t").getBoundingClientRect();
        ''')
        self.driver.save_screenshot(
            f'cache_image.png')
        img = Image.open('cache_image.png')
        crop = img.crop((0, 0, 640, int(clip_info['bottom'] + 12)))
        img_name = f'{str(int(time.time()))}_a.png'
        crop.save(img_name)
        return img_name

    def process_tweet_retweet(self):
        q_selector = '''document.querySelector("#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1gm7m50.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div.css-1dbjc4n.r-1bs4hfb.r-1867qdf.r-rs99b7.r-1loqt21.r-dap0kf.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg > div > div.css-1dbjc4n.r-15d164r.r-vlx1xi > div.css-901oao.r-18jsvk2.r-1tl8opc.r-a023e6.r-16dba41.r-ad9z0x.r-1g94qm0.r-bcqeeo.r-bnwqim.r-qvutc0")'''
        text_emoji_parsed = self.process_emoji(self.text["retweet"])
        template = RETWEET_TEMP.replace("{T}", text_emoji_parsed)
        if "KT_IMG" in template:
            template = template.replace("{KT_IMG}", self.icon_b64)
        ajs = f'''{q_selector}.innerHTML = {q_selector}.innerHTML + `{template}`'''
        print(ajs)
        self.driver.execute_script(ajs)

    def process_emoji(self, src):
        ajs = twemoji_js.replace("{EMOJI_HTML}", src)
        emoji_parsed_html = self.driver.execute_script(ajs)
        emoji_list = re.findall(
            '''<img class="emoji" draggable="false" alt=".*" src="https://twemoji.maxcdn.com/v/13.0.1/72x72/(.+?).png"/>''',
            emoji_parsed_html)
        for eve in emoji_list:
            src = src + EMOJI_HTML.replace("{EMOJI}", eve)
        emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]')
        text_emoji_clear = emoji_pattern.sub('', src)
        return text_emoji_clear

    def modify_tweet(self):
        while self.driver.execute_script(
                '''
                let top=0;
                try{
                    top=document.body.parentElement.scrollTop;
                    document.body.scrollIntoView();
                }catch{}
                return top;
                '''
        ) > 0:
            # logger.info("scroll_sleep")
            time.sleep(0.5)
        self.driver.execute_script('''try{
            new_element = document.createElement("style");
            new_element.innerHTML =("*{transition:none!important}");
            document.body.appendChild(new_element);
            document.body.style.overflow="hidden";
            document.body.scrollIntoView();
            document.querySelector("div[data-testid=primaryColumn]").style.maxWidth="640px";
            document.querySelector("div[data-testid=primaryColumn]").style.border="0";
            document.querySelectorAll("article div[role=group]").forEach(o=>o.remove());
            function shakeTree(node){
                for (let e of node.parentElement.children){if(e!==node)e.remove()};
                if(node.id!=="react-root")shakeTree(node.parentElement);
            }
            document.querySelector("html").style.overflow="hidden";
            document.querySelectorAll("div[data-testid=caret]").forEach(o=>o.style.visibility="hidden");
            shakeTree(document.querySelector('section[aria-labelledby=accessible-list-0]'));
            document.body.scrollIntoView();
            }catch{}''')

        self.driver.set_window_size(640, 2000)
        # time.sleep(3)
        self.driver.execute_script('''try{
                    document.body.scrollIntoView();
                    }catch{}''')


if __name__ == "__main__":
    # noinspection PyDictCreation
    c = {
        "proxy": "socks5://127.0.0.1:10808",
        "icon_b64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAAoCAIAAABfMzs3AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAFyGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDIgNzkuMTY0NDYwLCAyMDIwLzA1LzEyLTE2OjA0OjE3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMiAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIwLTEyLTA3VDE5OjQ2OjU3KzA4OjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDIwLTEyLTA3VDE5OjQ2OjU3KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMC0xMi0wN1QxOTo0Njo1NyswODowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo0NGUwODE1YS0xODY2LTM2NDYtODc2YS1iOWY5YjczMjI2NjkiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo5YzA4OTcyOC1iYmZlLWViNDEtOGEwYy00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",
        "template": '''<div style="margin:5px 10px"><style type="text/css">.link{color:#1DA1F2}</style><img src="{KT_IMG}" height="35"></div><div style="margin:1px 5px;font-size: 27px;width: 544px;word-break: break-word;">{T}</div></div>''',
        "link": "https://twitter.com/murasakishionch/status/1343955238563139586",
        "text": {
            "tweet": "新年快乐🍑",
            "retweet": "happy new year🍑"
        },
        "type": "retweet"
    }
    c['link'] = "https://twitter.com/houshoumarine/status/1346429093319827456"
    driver_init_time = time.time()
    print("driver启动：" + str(driver_init_time))
    p = Processor(c)
    process_init_time = time.time()
    print("process启动：" + str(process_init_time))
    name = p.process_tweet()
    process_ok_time = time.time()
    print("process完成：" + str(process_ok_time))
    print(f"driver启动耗时：{process_init_time - driver_init_time}")
    print(f"process完成耗时：{process_ok_time - process_init_time}")
