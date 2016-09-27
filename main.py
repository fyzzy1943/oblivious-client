from helper import conf
from urllib import request, parse
from PIL import Image
import json, os, shutil, re

base_url = conf.main('base_url')
base_img_url = conf.main('base_img_url')
base_title_url = conf.main('base_title_url')
re_img = re.compile(r'<img src="(\S+)">')

print(conf.all())

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

        print('文章获取成功开始更新')

        # 清空标题目录
        for file in os.listdir(os.path.join(local_path, title_folder)):
            os.remove(os.path.join(os.path.join(local_path, title_folder), file))

        print('标题目录已清空')

        for index in range(int(update_number)):
            # 当前操作路径
            current_path = os.path.join(local_path, folder_prefix+str(index+1))
            current_img_path = os.path.join(current_path, 'img', 'pic')
            current_title_path = os.path.join(local_path, title_folder)

            # 删除所有图片
            for file in [x for x in os.listdir(current_img_path) if x != 'line.jpg']:
                os.remove(os.path.join(current_img_path, file))

            ar = articles[index]

            # 下载并处理图片
            for image in re_img.finditer(ar['article']):
                url = base_img_url+image.group(1)
                with request.urlopen(url) as img:
                    img_path = os.path.join(os.path.curdir, 'temp', image.group(1))
                    with open(img_path, 'wb') as tmp:
                        tmp.write(img.read())
                    with Image.open(img_path) as tmp:
                        tmp.thumbnail((700, tmp.size[1]))
                        w, h = tmp.size
                        tmp.save(img_path+'.jpg')
                    os.remove(img_path)
                    shutil.move(img_path+'.jpg', os.path.join(current_img_path, image.group(1)+'.jpg'))
                img_code = '\n<img src="img/pic/'+image.group(1)+'.jpg" hspace="'+str((760-w)//2)+'">'
                for _ in range(h//22):
                    img_code = img_code+'<br />'
                img_code = img_code + '\n'

                ar['article'] = ar['article'].replace(image.group(0), img_code)

                print(image.group(0))
                # print(image.group(1))

            # ar['article'] = ar['article'].replace('\\r\\n', '\n')

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

            # 生成xml文件
            with open(os.path.join(current_path, 'pages.xml'), 'w', encoding='utf-8') as file:
                file.write(article)

            # 生成标题
            with request.urlopen(base_title_url+parse.quote(ar['title'])+'/false') as title_img:
                with open(os.path.join(current_title_path, '%02d'% (index+1)+'.png'), 'wb') as title_file:
                    title_file.write(title_img.read())
            with request.urlopen(base_title_url + parse.quote(ar['title']) + '/true') as title_img:
                with open(os.path.join(current_title_path, 'd_%02d' % (index + 1) + '.png'), 'wb') as title_file:
                    title_file.write(title_img.read())

            print('【'+ar['title']+'】更新完成')

print('全部更新完成')
os.system('pause')
