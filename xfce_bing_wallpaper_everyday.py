import json
import os.path
import re
import subprocess
import urllib.request
from datetime import datetime


def get_bing_wallpaper(image_folder='~/.bing'):
    # 图片保存路径 默认为 `~/.bing`
    image_folder = os.path.expanduser(image_folder)
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)

    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    req = urllib.request.Request(url)

    # parsing response
    res = urllib.request.urlopen(req).read()
    data = json.loads(res.decode('utf-8'))
    # print(data)
    image_url = f"https://www.bing.com{data['images'][0]['url']}"

    image_path = os.path.join(image_folder, f"{datetime.now().strftime('%Y-%m-%d')}_{data['images'][0]['title']}.jpg")
    urllib.request.urlretrieve(image_url, image_path)
    return image_path


def change_wallpaper(new_wallpaper_path):
    # 这个是全局配置，相当于模板文件，在创建新用户的时候会复制到用户目录下
    # global_config_file = '/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml'
    # 用户自己的配置，这个才是需要修改的文件
    user_config_file = '~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml'
    user_config_file = os.path.expanduser(user_config_file)
    with open(user_config_file, 'r', encoding='utf-8') as f:
        content = f.read()
        pat = '(image-path.*value=").*(")'
        res = re.findall(pat, content)
        # print(res)

    # 通过命令修改配置
    # https://unix.stackexchange.com/questions/596070/how-to-change-wallpaper-on-xfce-from-terminal
    # 用这个命令的确可以修改配置文件
    # xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s "/home/nate/data/test 测试文件/风景/IMG_5910.jpg"
    # 这个可以列出所有属性
    # xfconf-query --channel xfce4-desktop --list

    # 遍历属性，找出所有的图片

    # crontab执行xfconf-query命令报错: 无法初始化 libxfconf：无法在没有 X11 $DISPLAY 的情况下自动启动 D-Bus.
    # 解决: 缺少环境变量，手动查询path: echo $DBUS_SESSION_BUS_ADDRESS
    # path一般是 unix:path=/run/user/1000/bus
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'

    res = subprocess.check_output('xfconf-query --channel xfce4-desktop --list', shell=True, encoding='utf-8', env=os.environ.copy())
    for x in res.split():
        if any([y in x for y in ['image-path', 'last-image', 'last-single-image']]):
            print(x)
            # 替换图片属性
            cmd = f'xfconf-query -c xfce4-desktop -p {x} -s "{new_wallpaper_path}"'
            os.system(cmd)


image_path = get_bing_wallpaper()
# print(image_path)
change_wallpaper(image_path)
print('执行完毕！')
