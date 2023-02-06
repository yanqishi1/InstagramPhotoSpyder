from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import base64
import random
import os
js = """
        _fetch = function(i,src){
          return fetch(src).then(function(response) {
            if(!response.ok) throw new Error("No image in the response");
            var headers = response.headers;
            var ct = headers.get('Content-Type');
            var contentType = 'image/png';
            if(ct !== null){
              contentType = ct.split(';')[0];
            }

            return response.blob().then(function(blob){
              return {
                'blob': blob,
                'mime': contentType,
                'i':i,
              };
            });
          });
        };

        _read = function(response){
          return new Promise(function(resolve, reject){
            var blob = new Blob([response.blob], {type : response.mime});
            var reader = new FileReader();
            reader.onload = function(e){
              resolve({'data':e.target.result, 'i':response.i});
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
          });
        };

        _replace = function(){
            for (var i = 0, len = q.length; i < len; i++) {imgs[q[i].item].src = q[i].data;}
        }

        var q = [];
        var imgs = document.querySelectorAll('img');
        for (var i = 0, len = imgs.length; i < len; i++) {
                _fetch(i,imgs[i].src).then(_read).then(function(data){
            q.push({
              'data': data.data,
              'item': data.i,
            });
          });
            }
        setTimeout(_replace, 1000 );
        """

def download(driver, url, name):
    try:
        driver.get(url)
        driver.execute_script(js)
        sleep(2)
        s = BeautifulSoup(driver.page_source, "html.parser")
        imgs = s.findAll("img")
        imgsrc = imgs[0].get("src")
        suffix = imgsrc.split(';')[0][11:]
        with open(name +"."+suffix, 'wb') as f:
            f.write(base64.b64decode(imgsrc.split(',')[1]))
    except:
        print("Download Error")

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/accounts/login/?next=%2Fsamalive%2F&source=desktop_nav&hl=zh-cn")
    # login
    x = 'n'
    while x!='y':
        x = input("Please input y if you login in ins account:")
    target_url = "https://www.instagram.com/withluke/?hl=zh-cn"
    # target_url = input("Please input instagram url:")
    driver.get(target_url)
    folder = "./imgs/withluke/"
    if os.path.exists(folder) is False:
        os.makedirs(folder)
    sleep(5)

    img_urls = set()
    original_top = 0
    while True:
        driver.execute_script("window.scrollTo(0, 100000);")
        sleep(5 + random.random())  # 停顿一下
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        print(check_height, original_top)
        if check_height == original_top:  # 判断滑动后距顶部的距离与滑动前距顶部的距离
            break
        original_top = check_height
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        img_tags = soup.findAll("img")
        for tag in img_tags:
            if tag.get("alt") is not None  and tag.get("alt").endswith("头像"):
                continue

            if tag.get("src") is not None:
                url = tag.get("src")
                img_urls.add(url)
                print(url[:21])
        print(len(img_urls))

    cnt = 1
    for url in img_urls:
        ty = url[:21]
        if ty.endswith("base64"):
            suffix = url.split(';')[0][11:]
            with open(folder + str(cnt) + "." + suffix, 'wb') as f:
                f.write(base64.b64decode(url.split(',')[1]))
        else:
            download(driver,url,folder+str(cnt))
        cnt+=1

