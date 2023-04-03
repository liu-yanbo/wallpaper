"""
爬取 bing 每日高清壁纸
"""

import requests
import os

file_readme = 'README.md'
file_bing = 'wallpaper.md'

bing_title = '## Bing Wallpaper'
bing_uri = 'https://cn.bing.com'
bing_api = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&nc=1612409408851&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160'

small_format = '&pid=hp&w=384&h=216&rs=1&c=4'
large_format = '&w=1000'

md_2 = '|   |   |   |'
md_3 = '| :----: | :----: | :----: |'
line_img = '|![]({}) {} [下载原图]({}) | ![]({}) {} [下载原图]({}) |![]({}) {} [下载原图]({}) |'


def read():
    imgs = []
    with open(file_readme, 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines[4:]:
            if not line.isspace():
                img_arr = line.split('|')
                for img in img_arr:
                    if img != '' and img != '\n':
                        imgs.append(img)

    return imgs


def write():
    today = get_today()
    md_1 = today['md_1']
    md_new = today['md_new']
    imgs = read()
    imgs.insert(0, md_new)
    os.remove(file_readme)
    with open(file_readme, 'ab') as file:
        file.write(bing_title.encode())
        file.write('\n'.encode())
        file.write(md_1)
        file.write('\n'.encode())
        file.write(md_2.encode())
        file.write('\n'.encode())
        file.write(md_3.encode())
        file.write('\n'.encode())
        i = 1
        for img in imgs:
            file.write('|'.encode())
            file.write(img.encode())
            if i % 3 == 0:
                file.write('|'.encode())
                file.write('\n'.encode())
            i += 1
        if i % 3 != 1:
            file.write('|'.encode())


def get_today():
    resp = requests.get(url=bing_api)
    if resp.status_code == 200:
        json_str = resp.json()
        images = json_str['images']
        images_0 = images[0]
        start_date = images_0['startdate']
        title = images_0['title']
        copyright = images_0['copyright']
        url = images_0['url']
        img_url = bing_uri + url
        small_url = img_url + small_format
        md_1 = f'![]({img_url}) Today [{title}]({img_url + large_format})'.encode()
        md_new = f'![]({small_url}) {start_date} [下载原图]({img_url})'
        md_wall_new = f'{start_date}|[{copyright}]({img_url})\n'
        return {'md_1': md_1, 'md_new': md_new, 'md_wall_new': md_wall_new}


def write_wallpaper():
    today = get_today()
    md_wall_new = today['md_wall_new']
    wallpapers = read_wallpaper()
    wallpapers.insert(1, md_wall_new)
    os.remove(file_bing)
    with open(file_bing, 'ab') as file:
        file.write(bing_title.encode())
        file.write('\n'.encode())
        for wallpaper in wallpapers:
            file.write(wallpaper.encode())


def read_wallpaper():
    with open(file_bing, 'r', encoding='utf8') as file:
        lines = file.readlines()
        return lines[1:]


def main():
    write()
    write_wallpaper()


if __name__ == '__main__':
    main()
