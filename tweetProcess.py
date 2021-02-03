from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import re
from PIL import Image

from config import PROXY
from utils.template import RETWEET_TEMP
from utils.twemoji import EMOJI_HTML, TWEET_EMOJI_JS


class Processor:
    def __init__(self, cfg):
        self.options = webdriver.ChromeOptions()
        self.link: str = cfg['link']
        self.type: str = cfg['type']
        self.html_template: str = cfg['template']['html']
        self.icon_b64: str = cfg['template']['icon_b64']
        self.text: dict = cfg['text']

        self.init_argument()
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.init_webdriver()

    def init_argument(self):
        argument_list = [
            '--headless',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
        ]
        if PROXY:
            argument_list.append(f'--proxy-server={PROXY}')

        for arg in argument_list:
            self.options.add_argument(arg)

    def init_webdriver(self):
        self.driver.delete_all_cookies()

    def process_tweet(self) -> str:
        img_name = ""
        self.driver.get(self.link)
        WebDriverWait(self.driver, 60, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))
        try:
            if self.type == "single":
                img_name = self.process_tweet_single()
            if self.type == "retweet":
                self.process_tweet_retweet()
                img_name = self.process_tweet_single()
            if self.type == "reply":
                img_name = self.process_tweet_reply()
        except Exception as e:
            print(repr(e))

        self.driver.close()
        return img_name

    def save_screenshot(self) -> str:
        """
        :return: 截图名称
        """
        # modify tweet
        self.driver.set_window_size(640, self.driver.execute_script('''
        return document.querySelector("section").getBoundingClientRect().bottom'''))
        self.modify_tweet()
        # save and clip tweet image
        clip_info = self.driver.execute_script('''
        return document.querySelector("article .css-1dbjc4n .r-vpgt9t").getBoundingClientRect();''')
        self.driver.save_screenshot(
            f'cache_image.png')
        img = Image.open('cache_image.png')
        crop = img.crop((0, 0, 640, int(clip_info['bottom'] + 14)))
        img_name = f'{str(int(time.time()))}_a.png'
        crop.save("./imgs/" + img_name)
        return img_name

    def process_tweet_single(self):
        # process template
        text_ok = self.process_text(self.text["tweet"])
        template = self.html_template.replace("{T}", text_ok)
        if "KT_IMG" in template:
            template = template.replace("{KT_IMG}", self.icon_b64)
        # execute js
        print("execute tweet_single js")
        self.driver.execute_script(f'''
            document.querySelector(".css-1dbjc4n.r-156q2ks").innerHTML += `{template}`''')
        img_name = self.save_screenshot()
        return img_name

    def process_tweet_retweet(self):
        selector = '''document.querySelector("#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1gm7m50.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div.css-1dbjc4n.r-1bs4hfb.r-1867qdf.r-rs99b7.r-1loqt21.r-dap0kf.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg > div > div.css-1dbjc4n.r-15d164r.r-vlx1xi > div.css-901oao.r-18jsvk2.r-1tl8opc.r-a023e6.r-16dba41.r-ad9z0x.r-1g94qm0.r-bcqeeo.r-bnwqim.r-qvutc0")'''
        text_ok = self.process_text(self.text["retweet"])
        template = RETWEET_TEMP.replace("{T}", text_ok)
        if "KT_IMG" in template:
            template = template.replace("{KT_IMG}", self.icon_b64)
        self.driver.execute_script(
            f'''{selector}.innerHTML += `{template}`''')

    def process_tweet_reply(self):
        assert isinstance(self.text["tweet"], list)
        for i in range(len(self.text["tweet"])):
            if i == len(self.text["tweet"]) - 1:
                tweet_sele = 3
            else:
                tweet_sele = 4

            src = self.text["tweet"][i]
            text_ok = self.process_text(src)
            template = RETWEET_TEMP.replace("{T}", text_ok)
            if "KT_IMG" in template:
                template = template.replace("{KT_IMG}", self.icon_b64)
            self.driver.execute_script(
                f'''
                let nodes = [...document.querySelectorAll("article")];
                nodes[{i}].querySelectorAll('[dir="auto"]')[{tweet_sele}].innerHTML += `{template}`;''')

        img_name = self.save_screenshot()
        return img_name

    def process_emoji(self, src):
        js = TWEET_EMOJI_JS.replace("{EMOJI_HTML}", src)
        emoji_parsed_html = self.driver.execute_script(js)
        emoji_list = re.findall(
            '''src="https://twemoji.maxcdn.com/v/13.0.1/72x72/(.*?).png"/>''',
            emoji_parsed_html)
        print(emoji_list)
        for eve in emoji_list:
            emoji_parsed_html = re.sub('''<img class="emoji" draggable="false" .*?"/>''',
                                       EMOJI_HTML.replace("{EMOJI}", eve), emoji_parsed_html, count=1)
        emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]')
        text_emoji_clear = emoji_pattern.sub('', emoji_parsed_html)
        return text_emoji_clear

    def process_text(self, src):
        if "\r\n" in src:
            return self.process_emoji(src.replace("\r\n", "<br>"))
        elif "\n" in src and "\\n" not in src:
            return self.process_emoji(src.replace("\n", "<br>"))
        else:
            return self.process_emoji(src)

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
    pass