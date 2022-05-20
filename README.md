# xfce-bing-wallpaper-everyday
xfce每日bing壁纸. Set bing wallpaper for xfce everyday automatically.

# 使用方法

直接运行

```
python3 xfce_bing_wallpaper_everyday.py
```

会自动把壁纸下载到 `~/.bing` 目录下，并设置为壁纸

# 定时任务

添加每日定时任务，自动换壁纸
可以在cronjob里加上这个
路径换成你自己的

```
05 01 * * * python3 /home/nate/gitRepo/manjaro_xfce_bing_wallpaper/manjaro_bing_wallpaper_everyday.py
```

如果执行不了，可以加上日志输出
```
20 09 * * * python3 /home/nate/gitRepo/manjaro_xfce_bing_wallpaper/manjaro_bing_wallpaper_everyday.py > /home/nate/.bing/bing.log 2>&1
```

# 还原

Manjaro的默认图是这个 `/usr/share/backgrounds/xfce/illyria-default.jpg`，可以随时还原回去
