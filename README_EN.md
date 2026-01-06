# xfce-bing-wallpaper-everyday

[🇨🇳 中文版](./README.md) | English Version

🖼️ A simple Python script to **automatically set Bing's daily wallpaper** as your XFCE desktop background every day.

The script automatically detects the running environment:
- On regular Linux: uses `xfconf-query` to set the wallpaper
- On Termux + proot Debian (e.g., tiny computer environment): directly modifies the configuration file

Wallpapers are saved by default to the `~/.bing` directory with the filename format `YYYY-MM-DD_Title.jpg`.

## 🚀 Usage

Just run the script:

```bash
python3 xfce_bing_wallpaper_everyday.py
```

The script will:
1. Download today's Bing wallpaper
2. Save it to `~/.bing`
3. Set it as your current desktop wallpaper

⚠️ **Note**: Before the first run, make sure you have started the XFCE desktop at least once (to generate the required configuration files).

## 🖥️ Special Notes for tiny computer Environment

🔗 Project link: https://github.com/Cateners/tiny_computer

📱 This is a complete Debian 12 + XFCE desktop environment running via proot on Android (no need for Termux itself).

⚙️ In this environment, due to the absence of a DBus session, the wallpaper change **does not take effect immediately**.

✅ **Solution**: After the script runs, manually restart the desktop (close and reopen the VNC/graphic interface) or log out and log back in to see the new wallpaper.

## ⏰ Scheduled Task (Recommended)

🕐 To truly achieve “daily automatic wallpaper change”, it’s recommended to add a crontab scheduled task.

Edit your crontab:

```bash
crontab -e
```

Add the following line (executes daily at 1:05 AM; replace the path with your actual script location):

```cron
5 1 * * * python3 /path/to/xfce_bing_wallpaper_everyday.py
```

If you want to capture logs for debugging, add output redirection:

```cron
5 1 * * * python3 /path/to/xfce_bing_wallpaper_everyday.py >> ~/.bing/bing.log 2>&1
```

## 🔙 How to Restore the Default Wallpaper

🎨 Default wallpaper paths vary by distribution. Common examples:

- **Manjaro XFCE**: `/usr/share/backgrounds/xfce/illyria-default.jpg` or similar
- **Debian XFCE**: Usually from the `desktop-base` package, e.g., `/usr/share/images/desktop-base/default`

🛠️ You can manually select the system default wallpaper via desktop settings, or use this command (adjust the path as needed):

```bash
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s /usr/share/backgrounds/xfce/illyria-default.jpg
```

(Only works in regular Linux environments)

**🌟 Enjoy a fresh beautiful Bing image every day!**