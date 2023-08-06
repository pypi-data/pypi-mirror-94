# 微信公众号文章爬虫（微信文章阅读点赞的获取）

![](https://img.shields.io/pypi/v/wechatarticles)

安装

`pip install wechatarticles`

展示地址：

[数据展示（完整指标）](https://data.wnma3mz.cn/)

[日更两次，获取公众号的最新文章链接](https://data.wnma3mz.cn/demo.html)，暂不支持实时获取阅读点赞

技术交流可以直接联系，微信二维码见末尾（微信；wnma3mz)。烦请进行备注，如wechat_spider

统一回复，项目可正常运行。若不能正常运行，该行会删除。

联系前请注意：

1. 不（能）做自动登录微信公众号、微信

2. 不（能）做实时获取参数

3. 参数过期需要手动更新

4. 换一个公众号需要手动更新

注：本项目仅供学习交流，严禁用于商业用途（该项目也没法直接使用），不能达到开箱即用的水平。使用本项目需要读文档+源码+动手实践，参考示例代码（`test`文件夹下）进行改写。

提示：另外，已经有很多朋友（大佬）通过直接看源码，已经基于这套项目，或者重写，用于各自的需求。

实现思路一:

1. 从微信公众号平台获取微信公众所有文章的url
2. 登录微信PC端或移动端获取文章的阅读数、点赞数、评论信息

完整思路可以参考我的博客: [记一次微信公众号爬虫的经历（微信文章阅读点赞的获取）](https://wnma3mz.github.io/hexo_blog/2017/11/18/记一次微信公众号爬虫的经历（微信文章阅读点赞的获取）/)

批量关注微信公众的方法见：[自动批量关注微信公众号（非逆向）](https://wnma3mz.github.io/hexo_blog/2020/04/11/自动批量关注微信公众号（非逆向）/)


实现思路二：

1. 登陆微信PC端或移动端获取公众号所有文章的url，这种获取到的url数量大于500，具体数值暂未测试
2. 同上种方法，获取文章阅读数、点赞数、评论信息

公开已爬取的公众号历史文章的永久链接，日期均截止commit时间，仅供测试与学习，欢迎各位关注这些优质公众号。

<details>
  <summary>公众号列表</summary>
    <li>科技美学</li>
    <li>共青团中央</li>
    <li>南方周末</li>
    <li>AppSo</li>
</details>


## Notes

更新于2020年12月

更新微信文章阅读点赞在看

1. 爬取失败的时候，可能有以下原因
   1. **运行的时候需要关闭网络代理（抓包软件），或者添加相关参数**
   2. 参数是否最新，获取微信相关参数（cookie、token）时，一定要保证是**对应公众号**的任意文章
   3. 检查代码
   4. 需要关注对应公众号（Maybe）
2. 思路一获取url时，每页间隔可以设定久一点，比如3分钟，持续时间几小时（来自网友测试）
3. 获取文章阅读点赞时，每篇文章可以设定在5-10s左右，过期时间为4小时；若被封，大约5-10分钟就可继续抓取。
4. 思路二获取url时，如果被封，需要24小时整之后才能重新抓取

## python版本

- `python`: 3.6.2、3.7.3

## 功能实现

<details>
  <summary>功能</summary>
    <li>获取某公众号信息</li>
    <li>获取某公众号所有文章数量</li>
    <li>获取某公众号文章的url信息</li>
    <li>获取某公众号所有文章信息（包含点赞数、阅读数、评论信息），需要手动更改循环</li>
    <li>获取某公众号指定文章的信息</li>
    <li>支持微信公众号cookie、token登录，手动复制cookie和token</li>
    <li>支持两种获取文章阅读数和点赞数的方式，下面方式选用其一即可
        <ol>利用抓包工具手动获取</ol>
    </li>
    <li>支持微信文章下载至本地转为md</li>
    <li>支持微信文章下载至本地转为html（图片可选是否保存）</li>
</details>


## 变量名的说明

|     变量名      |        作用        |
| :-------------: | :----------------: |
| official_cookie | 个人公众号的cookie |
|    token     |  个人公众号的token  |
|    appmsg_token     |  个人微信号的appmsg_token  |
| wechat_cookie | 个人微信号的cookie |
| key | 个人微信号的key |
| uin | 个人微信号的uin |
|    nickname     |  需要获取文章的公众号名称  |
|    query     | 筛选公众号文章的关键词  |
| outfile | mitmproxy抓包获取请求的保存文件 |
| begin | 从第几篇文章开始爬取 |
| count | 每次爬取的文章数(最大为5, 但是返回结果可能会大于5) |

## API实例

#### 利用公众号网页版获取微信文章url
此处有次数限制，不可一次获取太多url。解决方案多个账号同时爬取
[test_WechatUrls.py](https://github.com/wnma3mz/wechat_articles_spider/blob/master/test/test_WechatUrls.py)

#### 登录微信PC端获取文章信息
[test_WechatInfo.py](https://github.com/wnma3mz/wechat_articles_spider/blob/master/test/test_WechatInfo.py)

#### 快速获取大量文章urls（利用历史文章获取链接）
[test_GetUrls.py](https://github.com/wnma3mz/wechat_articles_spider/blob/master/test/test_GetUrls.py)

#### 利用公众号获取链接，并获取阅读点赞
[test_ArticlesAPI.py](https://github.com/wnma3mz/wechat_articles_spider/blob/master/test/test_ArticlesAPI.py)

#### 微信文章下载为离线HTML（含图片）
[test_Url2Html.py](https://github.com/wnma3mz/wechat_articles_spider/blob/master/test/test_Url2Html.py)


### 相关文档

见博客与下方文档

official_cookie和token手动获取方式见[这篇文档](https://github.com/wnma3mz/wechat_articles_spider/blob/master/docs/get_cookie_token.md)

wechat_cookie和appmsg_token手动获取的介绍，可以参考[这篇文档](https://github.com/wnma3mz/wechat_articles_spider/blob/master/docs/get_appmsg_token.md)

wechat_cookie和appmsg_token自动获取的介绍（需要安装`mitmproxy`，已放弃），仅供参考[这篇文档](https://github.com/wnma3mz/wechat_articles_spider/blob/master/docs/关于自动获取微信参数.md)。默认开放端口为8080。


## 打赏部分

<figure class="third">
   微信二维码
<img src="https://i.loli.net/2019/09/20/14QGTkfgstDxv9C.jpg"  width="50%" id="wechat_account" /><img src="https://raw.githubusercontent.com/wnma3mz/wechat_articles_spider/master/imgs/wechat.jpg" width="260"><img src="https://raw.githubusercontent.com/wnma3mz/wechat_articles_spider/master/imgs/Alipay.jpg" width="260"><img src="https://raw.githubusercontent.com/wnma3mz/wechat_articles_spider/master/imgs/Alipay_redpaper.jpg" width="260">
</figure>


