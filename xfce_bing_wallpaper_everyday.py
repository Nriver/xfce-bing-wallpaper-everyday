import json
import os
import subprocess
import urllib.request
from datetime import datetime
import re
import shutil


def is_termux_environment():
    """判断是否在 Termux（被 PRoot 挂载的 Android）环境中"""
    android_kernel = False
    if os.path.exists("/proc/version"):
        try:
            with open("/proc/version", "r", encoding="utf-8") as f:
                if "Android" in f.read():
                    android_kernel = True
        except:
            pass
    has_storage_or_sd = os.path.exists("/storage") or os.path.exists("/sd")
    return android_kernel and has_storage_or_sd


def is_debian_system():
    """判断当前系统是否为 Debian（包括 proot-distro 安装的）"""
    if os.path.exists("/etc/os-release"):
        try:
            with open("/etc/os-release", "r", encoding="utf-8") as f:
                content = f.read().lower()
                if "id=debian" in content:
                    return True
        except:
            pass
    return os.path.exists("/etc/debian_version")


def is_termux_proot_debian():
    return is_termux_environment() and is_debian_system()


def get_bing_wallpaper():
    """下载 Bing 当日壁纸，保存到 ~/.bing，使用日期_标题.jpg 命名"""
    image_folder = os.path.expanduser('~/.bing')
    os.makedirs(image_folder, exist_ok=True)

    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    image_url = f"https://www.bing.com{data['images'][0]['url']}"
    title = re.sub(r'[<>:"/\\|?*]', '_', data['images'][0]['title'])
    filename = f"{datetime.now().strftime('%Y-%m-%d')}_{title}.jpg"
    image_path = os.path.join(image_folder, filename)

    urllib.request.urlretrieve(image_url, image_path)
    print(f"壁纸下载完成: {image_path}")
    return image_path


def change_wallpaper(new_wallpaper_path):
    """普通 Linux 环境：使用 xfconf-query 设置壁纸"""
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'
    try:
        res = subprocess.check_output(
            'xfconf-query --channel xfce4-desktop --list',
            shell=True, encoding='utf-8', env=os.environ.copy()
        )
    except subprocess.CalledProcessError as e:
        print(f"获取壁纸属性失败: {e}")
        return

    changed = False
    for line in res.splitlines():
        prop = line.strip()
        if any(keyword in prop for keyword in ['image-path', 'last-image', 'last-single-image']):
            print(f"设置属性: {prop}")
            try:
                subprocess.run([
                    "xfconf-query",
                    "-c", "xfce4-desktop",
                    "-p", prop,
                    "-s", new_wallpaper_path
                ], check=True)
                changed = True
            except subprocess.CalledProcessError as e:
                print(f"设置 {prop} 失败: {e}")

    if not changed:
        print("未找到可设置的壁纸属性")


def change_wallpaper_termux(new_wallpaper_path):
    """Termux 环境：精准替换 last-image 的 value 值（不会修改其他属性）"""
    config_file = os.path.expanduser('~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = config_file + f'.bak.{timestamp}'

    if not os.path.exists(config_file):
        print(f"错误：配置文件不存在 → {config_file}")
        print("请先启动一次 XFCE 桌面，让配置文件生成")
        return

    shutil.copy(config_file, backup_file)
    print(f"已备份配置文件 → {backup_file}")

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()

        last_image_count = len(re.findall(r'<property[^>]*name\s*=\s*["\']last-image["\']', content))
        if last_image_count == 0:
            print("警告：文件中未找到任何 last-image 属性")
            return

        changed = 0

        def replace_last_image(match):
            nonlocal changed
            full_prop = match.group(0)
            value_match = re.search(r'value\s*=\s*(["\'])(.*?)\1', full_prop)
            if value_match:
                quote = value_match.group(1)
                old_value = value_match.group(2)
                new_prop = full_prop.replace(
                    f'value={quote}{old_value}{quote}',
                    f'value={quote}{new_wallpaper_path}{quote}'
                )
            else:
                # type="empty" 或无 value 时添加
                new_prop = full_prop.rstrip('/>') + f' type="string" value="{new_wallpaper_path}"/>'
            changed += 1
            return new_prop

        pattern = r'<property\s+[^>]*name\s*=\s*["\']last-image["\'][^>]*?(?:/>|>)'
        new_content = re.sub(pattern, replace_last_image, content, flags=re.IGNORECASE)

        # 处理子 <value> 标签的情况（极少见）
        child_pattern = r'(<property\s+[^>]*name\s*=\s*["\']last-image["\'][^>]*>)\s*<value[^>]*>.*?</value>\s*(?:</property>)'
        def replace_child(match):
            nonlocal changed
            start = match.group(1)
            new_value = f'<value type="string" value="{new_wallpaper_path}"/>'
            changed += 1
            return f'{start}{new_value}</property>'

        new_content = re.sub(child_pattern, replace_child, new_content, flags=re.IGNORECASE | re.DOTALL)

        if changed > 0:
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"成功更新了 {changed} 处 last-image 的值")
            print(f"壁纸路径：{new_wallpaper_path}")
            print("提示：若壁纸未立即生效，可重启桌面或重新登录")
        else:
            print("无需更新（路径可能已一致）")

    except Exception as e:
        print(f"修改配置文件失败: {e}")
        print(f"已保留备份文件：{backup_file}")


if __name__ == "__main__":
    print("正在检测运行环境...\n")

    if is_termux_proot_debian():
        print("检测到 Termux + proot-distro Debian 环境 → 使用直接修改 XML 的方式")
    else:
        print("普通 Linux 环境 → 使用 xfconf-query 设置壁纸")

    print("\n开始下载 Bing 每日壁纸（保存到 ~/.bing）...")
    image_path = get_bing_wallpaper()

    print("\n正在设置壁纸...")
    if is_termux_proot_debian():
        change_wallpaper_termux(image_path)
    else:
        change_wallpaper(image_path)

    print("\n全部执行完毕！每天运行一次即可自动更换壁纸~")