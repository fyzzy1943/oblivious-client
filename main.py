from helper import conf
from urllib import request
import json, os, re

base_url = conf.main('base_url')
base_img_url = conf.main('base_img_url')
re_img = re.compile(r'\{IMG:(\S+)}')

for section in conf.all():
    serial = conf.get(section, 'serial')
    local_path = conf.get(section, 'local_path')
    folder_prefix = conf.get(section, 'folder_prefix')
    title_folder = conf.get(section, 'title_folder')
    update_number = conf.get(section, 'update_number')

    with request.urlopen(base_url+serial+'/'+update_number) as f:
        data = f.read()
        # print('Status:', f.status, f.reason)
        # print('Data:', data.decode('utf-8'))
        articles = json.loads(data.decode('utf-8'), encoding='utf-8')
        for index in range(int(update_number)):
            # 当前操作路径
            current_path = os.path.join(local_path, folder_prefix+str(index+1))
            current_img_path = os.path.join(current_path, 'img', 'pic')
            # 删除所有图片
            for file in [x for x in os.listdir(current_img_path) if x != 'line.jpg']:
                os.remove(os.path.join(current_img_path, file))

            ar = articles[index]

            text = ar['article']
            # 下载并处理图片
            for image in re_img.finditer(ar['article']):
                url = base_img_url+image.group(1)
                with request.urlopen(url) as img:
                    with open(os.path.join(os.path.curdir, 'temp', image.group(1)), 'wb') as tmp:
                        tmp.write(img.read())

                print(image.group(0))
                print(image.group(1))

            ar['article'] = ar['article'].replace('\\r\\n', '\n')

            L =[]
            L.append(r'<?xml version="1.0" encoding="utf-8"?>')
            L.append(r'<Mypage stageW="960" stageH="1192" slip="0" doubleClick="0" effect="1" filter="0" btn="all_btns.swf" idBar="all_dots.swf">')
            L.append(r'  <pages pW="960" pH="1192" img="img/001.jpg">')
            L.append(r'    <article aW="780" aH="1000" aColor="0x000000" aSize="20"><![CDATA[<p align="center"><font size="28" color="#C1272D"><B>'+ar['title']+'</B></font></p><img src="img/pic/line.jpg" hspace="0"><p align="center"><font size="16" color="#000000">  '+ar['date']+'</font></p>')
            L.append(ar['article'])
            L.append(r']]></article>')
            L.append(r'  </pages>')
            L.append(r'</Mypage>')
            article = '\n'.join(L)

            path = os.path.join(current_path, 'pages.xml')
            with open(path, 'w', encoding='utf-8') as file:
                file.write(article)
            # print(article)

os.system('pause')
