# xiangqi-refund

辣鸡享骑，每天要登记才能退款
享骑倒闭了，大家散了吧。

享骑倒闭了，大家散了吧。

### 运行

下载selenuim 的 chromedriver，http://chromedriver.chromium.org/downloads

改变 xiangqi_refund_selenium.py 文件中的CHROME_DRIVER_PATH的值，指向下载的 chromedriver 所在位置

运行下面代码

```python
python3 xiangqi_refund_selenium.py 小明 13812341234
```

### 定时任务

```bash
$ crontab -u root -e
```

最后一行写

```bash
0 9 * * * python3 /root/xiangqi/xiangqi_refund_selenium.py 小明 13812341234
```

（可选）多次测试可以算上启动时间

```bash
59 8 * * * sleep 55; python3 /root/xiangqi/xiangqi_refund_selenium.py 小明 13812341234
```
