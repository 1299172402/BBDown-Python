# BBDown-Python
一个仿照BBDown的程序，不过是用python写的并且试图支持图形界面

## 登录程序

- [login](https://github.com/1299172402/BBDown-Python/blob/main/login.py)

- [x] 支持web登录
- [x] 支持tv接口1登录（http://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code）
- [x] 支持tv接口2登录（https://passport.snm0516.aisee.tv/x/passport-tv-login/qrcode/auth_code）
- [x] 支持自动更新cookie和token

## 下载程序
- [ ] 从网址中截取av，bv，ep，ss，md
- [ ] 下载来源（网页，TV，大陆，区域）
- [ ] 调用aria2c下载

## 开发流程

1. 写出控制台程序
2. 实现GUI（毕竟GUI效率太低。。。）

## 其他想法，随记

# 务必牢记的的是，你只是一个普通学生，不必要花太多时间在此事上
# 一定以其他与写代码无关的事为重
  
登录仅使用tv接口 + refresh 接口产生的值。（tv1或tv2到时候考虑，不过应该是一样的。如果一样的话，就只看登录界面的缩放程度）  
  
优先满足对国内番剧TV端下载  
然后国内番剧web下载  
之后国外  
？选集下载。通过GetEpInfo时的列表来处理  
  
GUI设计？  
  
  
ffmpeg混流（后事，先下flv原文件，便于在网盘间传输  

aria2c 需要 cookie 才能下载  

？TV端支持 1080p+ 即使普通用户？  
TV端部分视频无水印，这是否与UPOS有关？（这是后事了  

qn 125 HDR？（后事）  
fxxxk 80 参数？（后事）获取全画质？  
hevc(h.265) avc(h.264)？（后事，现在优先avc，虽然它较大，不过也可以再考虑）  

只改变BBDown的不能直接下载flv和无法在手机上运行即可  

## API说明文档

[自动更新cookie和token的说明](https://github.com/1299172402/BBDown-Python/blob/main/login.md)
