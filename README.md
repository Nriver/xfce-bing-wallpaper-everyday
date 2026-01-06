# xfce-bing-wallpaper-everyday

🖼️ 一个简单的 Python 脚本，用于在 XFCE 桌面环境下**每天自动更换 Bing 每日壁纸**。

🔍 脚本会自动检测运行环境：
- 普通 Linux：使用 `xfconf-query` 设置壁纸
- Termux + proot Debian（如 tiny computer 环境）：直接修改配置文件

💾 壁纸默认下载到 `~/.bing` 目录下，文件名格式为 `YYYY-MM-DD_标题.jpg`。

## 🚀 使用方法

直接运行脚本即可：

```bash
python3 xfce_bing_wallpaper_everyday.py
```

📋 脚本会：
1. 下载当天的 Bing 壁纸
2. 保存到 `~/.bing` 目录
3. 自动设置为当前桌面壁纸

⚠️ **注意**：首次运行前，请确保已启动过 XFCE 桌面一次（以生成必要的配置文件）。

## 🖥️ tiny computer（小小电脑）环境特别说明

🔗 项目地址：https://github.com/Cateners/tiny_computer

📱 这是一个在 Android 上通过 proot 运行 Debian 12 + XFCE 桌面的完整环境（无需 Termux）。

⚙️ 在本环境中，由于缺少 DBus 会话，壁纸设置后**不会立即生效**。

✅ **解决方法**：修改壁纸后，手动重启桌面（关闭 VNC/图形界面后重新打开）或重新登录，即可看到新壁纸。

## ⏰ 定时任务（推荐）

🕐 为了实现真正“每日自动换壁纸”，建议添加 crontab 定时任务。

✏️ 编辑 crontab：

```bash
crontab -e
```

➕ 添加以下一行（每天凌晨 1:05 执行，路径请替换为你的实际路径）：

```cron
5 1 * * * python3 /path/to/xfce_bing_wallpaper_everyday.py
```

📝 如果想查看执行日志，可加上输出重定向：

```cron
5 1 * * * python3 /path/to/xfce_bing_wallpaper_everyday.py >> ~/.bing/bing.log 2>&1
```

## 🔙 如何还原默认壁纸

🎨 不同发行版的默认壁纸路径可能不同，以下是常见示例：

- **Manjaro XFCE**：`/usr/share/backgrounds/xfce/illyria-default.jpg` 或类似文件
- **Debian XFCE**：通常来自 `desktop-base` 包，路径如 `/usr/share/images/desktop-base/default`

🛠️ 你可以手动通过桌面设置选择系统默认壁纸，或使用以下命令（需调整路径）：

```bash
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s /usr/share/backgrounds/xfce/illyria-default.jpg
```

（适用于普通 Linux 环境）

**🌟 祝你每天都有惊喜的美图！**