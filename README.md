# Lab-Network-Attacks-and-Countermeasures
Labs for Network Attacks and Countermeasures(COMP130071.01)@ Fudan University

## Lab1 抓包文件统计

### 作业要求
p1p1.17.ip.56.pcap 是某服务器上的抓包文件（仅保留了数据包头信息），请编写一个分析程序分析这个文件完成相应指标的统计。具体要求如下：
- 统计出该公司服务器所提供的业务服务种类（假设不同端口对应于不同的业务）。
- 统计出各业务所对应的TCP请求sin包总数（含重传），TCP链接总数（通过三次握手后建立的）和TCP半链接总数（非正常的）。
- 统计出各业务所对应的数据包重传次数和重传率（按重传的数据包个数/该业务所有数据包个数）。
- 统计出各业务所对应的TCP链接重置请求次数，需区分是服务端发起还是客户端发起。
- 统计出服务器网络流量（不区分收发）最大的时间段（从开始时间开始以5分钟为间隔）及最大流量。

### 思路概述
借助pyshark模块进行统计分析。

[Github仓库](https://github.com/KimiNewt/pyshark) | [文档](http://kiminewt.github.io/pyshark/) | [segmentfault专栏](https://segmentfault.com/a/1190000006043576)

### troubleshooting
- 在MacOS下安装pyshark可能会因为缺少某些模块而不能正常运行，**建议在Linux系统下进行实验**。
  ```
  pip install pyshark
  ```

- 抓包文件比较大，全部统计完大概需要一小时左右，调试时建议先用前1000个包做测试。

## Lab2 从针对WEB Mail的网络嗅探数据中提取信息

### 作业要求
采用wireshark 打开网络嗅探数据文件。
利用wireshark的功能（如过滤、流拼接等），进行初步分析。
将相关数据导出到文件。
根据相关的编码，提取和转换相关内容，尽可能获取解码后的信息。（也可自己编程实现，或设立服务器向浏览器回放流内容实现）
尝试获取：
- 收件人邮箱、发件人邮箱、邮件标题、邮件正文、邮件附件。
- 邮箱中存在的邮件列表（可选）。
- WEB mail网站所采用的身份认证方法（可选，需要逆向分析还原后的Javascript）。

### 思路概述

先使用wireshark获得邮件信息流，使用python的urllib模块进行解析。parse_web_mail.ipynb实现了邮件基本信息的获取。

### troubleshooting
使用WireShark监听网络时，需要授予管理员权限：[Mac OS X下进行网络抓包](http://blog.csdn.net/wolfwind521/article/details/41629539)。

## Lab3 UDP扫描编程

### 作业要求
使用UDP协议，通过对ICMP_PORT UNREACH错误的检测，编程实现UDP端口扫描。通过自己编写的扫描工具，可获得被扫描机器的UDP端口开放信息。

### 思路概述
借助python的scapy模块进行扫描，具体原理参考[这篇文章](http://www.freebuf.com/sectool/94507.html)。

扫描结束后，可以用`netstat -an`命令可以查看端口开放情况来与扫描结果进行比对。

### troubleshooting
- 在MacOS下安装scapy会遇到很多支持问题，可以尝试按照如下方法解决。
  - [MacOS安装scapy](http://www.cnblogs.com/ToDoToTry/p/5323118.html)
  - [如何修复“ImportError: No module named scapy.all”](https://linux.cn/article-4400-1.html)
  - [ImportError: No module named dumbnet](https://stackoverflow.com/questions/40272077/importerror-no-module-named-dumbnet-when-trying-to-run-a-script-that-leverage)

  推荐在linux系统上进行实验。
  ```
  pip install scapy
  ```

- **不推荐在校园网环境下扫描学校DNS服务器**，推荐扫描VMware虚拟机软件上的windows。

- **首先需要关闭windows防火墙**，并且保证扫描主机和被扫描主机能够相互ping通。

  在cmd/bash中查看本机IP：
  ```
  ipconfig  % windows
  ifconfig  % Unix
  ```
- 如果用VMware上的Linux虚拟机作为扫描主机，需要用super user权限运行。

- [扫描结果始终返回None的解决方法](https://segmentfault.com/q/1010000009473176?sort=created)。

## Lab6 木马后门程序
### 作业要求
所编写软件运行于目标主机，通过网络接收客户端连接，在目标主机上执行客户端提交的指令。
- 编程实现一个木马/后门程序，接受用户端指令，并在目标主机上执行，返回执行结果。
- 在虚拟机上运行服务端软件，模拟木马/后门。在主机上运行客户端软件，连接虚拟机上的服务端软件，远程执行指令。
- 使该软件开机自动运行。
- 利用该软件，从客户端操控服务端，建立一个用户Hacker, 密码设为HackerPWD，并添加到管理员组。

### 思路概述
借助Python的socket和os模块，在server.py中绑定某一端口等待client连接并接受client发送的指令，运行之后将系统返回的输出结果发送给client即可。

添加新用户时需要super user权限，可以在server.py启动时伪装成系统进程来骗取用户输入root密码并保存。

开机自启的实现：
- linux系统需要在/etc/rc.local文件中添加相应的命令来实现程序的开机启动。
- windows系统则需要修改注册表。

### troubleshooting
- [Broken pipe & Connection Reset by Peer的原理及解决](http://lovestblog.cn/blog/2014/05/20/tcp-broken-pipe/)
- server.py退出之后再次运行可能会报“address already in use”，是因为socket端口尚未完全释放的原因，可以手动kill程序并等一段时间后再次运行。
- 实验开始之前要保证攻击主机和被攻击主机能够相互ping通。

---
If you have better solutions, please send a pull request.
