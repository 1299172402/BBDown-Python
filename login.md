# 哔哩哔哩自动刷新token和cookies

本操作需要通过TV端登录的access_token和refresh_token，网页端登录的结果无法应用。

## 请求方式：POST
## 网址：`https://passport.bilibili.com/api/v2/oauth2/refresh_token`

## 请求体
|字段|类型|必要性|内容|备注|
|---|---|---|---|---|
|access_key|str|必要|access_token| |
|appkey|str|必要|4409e2ce8ffd12b8|TV端用appkey，其盐值为59b43e04ad6965f34319062b478f83dd。并不确定其他appkey及其盐值是否可用|
|refresh_token|str|必要|refresh_token| |
|ts|num|必要|时间戳|时间戳需要取整数|
|sign|str|必要|计算后的盐值|计算方法如下|

### sign盐值计算方法
1. 先取除了sign的其他字段拼接，如`access_key=xxxxxxx&appkey=4409e2ce8ffd12b8&refresh_token=xxxxxx&ts=xxxxxxx`  
注意：此步骤必须按字段的字母从a到z排序拼接
2. 将上方拼接后的字符串加上盐值，如`access_key=xxxxxxx&appkey=4409e2ce8ffd12b8&refresh_token=xxxxxx&ts=xxxxxxx59b43e04ad6965f34319062b478f83dd`
3. 对拼接完成后的字符串`access_key=xxxxxxx&appkey=4409e2ce8ffd12b8&refresh_token=xxxxxx&ts=xxxxxxx59b43e04ad6965f34319062b478f83dd`做md5计算
4. 所得的md5值（字母小写）即为请求体中sign的值

## 响应体

根字段
|字段|类型|内容|
|---|---|---|
|ts|num|时间戳|
|code|num|0|
|data|dict|详细信息|

data字段
|字段|类型|内容|备注|
|---|---|---|---|
|token_info|dict|token登录信息|用于APP和TV端|
|cookie_info|list|cookie登录信息|用于网页端|
|sso|list|`["https://passport.bilibili.com/api/v2/sso","https://passport.biligame.com/api/v2/sso","https://passport.bigfunapp.cn/api/v2/sso"]`|单点登录，上方的token和cookie仅可在这些网站登录使用|
|is_tourist|bool|是否为游客|true/false|大多数情况下访问这个接口都是登录的，也就是True|

token_info字段
|字段|类型|内容|备注|
|---|---|---|---|
|mid|num|用户uid| |
|access_token|str| |新的access_token，与之前不一样，暂未测试之前的access_token是否失效|
|refresh_token|str| |新的refresh_token，与之前不一样，暂未测试之前的refresh_token是否失效|
|expires_in|num|2592000|此次token有效期（单位：秒），2592000秒=30天。暂未测试指的是access_token还是两个都失效|

cookie_info字段
|字段|类型|内容|备注|
|---|---|---|---|
|cookies|list|cookies|内部有5种cookie，见下表分析|
|domains|list|`[".bilibili.com",".biligame.com",".bigfunapp.cn"]`|cookies可用的域名|


cookies字段
|字段|类型|内容|备注|
|---|---|---|---|
|name|str|bili_jct<br/>DedeUserID<br/>DedeUserID__ckMd5<br/>sid<br/>SESSDATA|懂的都懂|
|value|str|5个cookie各自的值|
|http_only|num|0| |
|expires|num|1617718954|此cookie有效期（单位：秒），1617718954秒=51.2975315年。或许可以认为他是永久的？？|
|type|num|0| |

<details>
<summary>查看响应示例：</summary>

```json
{
  "ts": 1615126954,
  "code": 0,
  "data": {
    "token_info": {
      "mid": ***,
      "access_token": "***",
      "refresh_token": "***",
      "expires_in": 2592000
    },
    "cookie_info": {
      "cookies": [
        {
          "name": "bili_jct",
          "value": "***",
          "http_only": 0,
          "expires": 1617718954,
          "type": 0
        },
        {
          "name": "DedeUserID",
          "value": "***",
          "http_only": 0,
          "expires": 1617718954,
          "type": 0
        },
        {
          "name": "DedeUserID__ckMd5",
          "value": "***",
          "http_only": 0,
          "expires": 1617718954,
          "type": 0
        },
        {
          "name": "sid",
          "value": "***",
          "http_only": 0,
          "expires": 1617718954,
          "type": 0
        },
        {
          "name": "SESSDATA",
          "value": "***",
          "http_only": 1,
          "expires": 1617718954,
          "type": 0
        }
      ],
      "domains": [
        ".bilibili.com",
        ".biligame.com",
        ".bigfunapp.cn"
      ]
    },
    "sso": [
      "https://passport.bilibili.com/api/v2/sso",
      "https://passport.biligame.com/api/v2/sso",
      "https://passport.bigfunapp.cn/api/v2/sso"
    ],
    "is_tourist": False
  }
}
```

</details>




<details>
<summary>仅仅写了一点，不过打算还是算了</summary>

```markdown
# 哔哩哔哩二维码登录

## Web接口

### 请求二维码网址

请求方式：`GET`  
网址：`https://passport.bilibili.com/qrcode/getLoginUrl`

响应体中关键部分
|本文档中的名称|在返回值的位置|
|---|---|
|qrocde_url|`res["data"]["url"]`|
|oauthKey|`res["data"]["oauthKey"]`|

将`qrocde_url`所包含的网址编码为二维码通过哔哩哔哩手机端扫描确认即可

### 请求二维码的扫描结果

请求方式：`POST`
网址：`https://passport.bilibili.com/qrcode/getLoginInfo`

请求体
|名称|值|必要性|
|---|---|---|
|`oauthKey`|oauthKey|必要|
|`gourl`|`http://www.bilibili.com`|可选，是其他网址也可以|

响应体中关键部分
|本文档中的名称|在返回值的位置|
|---|---|
|status|res["status"]
```

</details>

##### 相关工作
- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)
- [BBDown](https://github.com/nilaoda/BBDown)
- [bilibili_autorec](https://github.com/DarrenIce/bilibili_autorec)