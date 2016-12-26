## 脚本使用说明

#### 用途

用于给懒人快速创建repo，创建dev分支并且设置为默认分支

初始化codecov，在dev根目录创建codecov-token文件保存codecov的upload-token

初始化travis，开启hook的开关，配置自定义环境变量

*注意*需要提前在github上给codecov和travis设置好权限

#### 文件头部的配置文件分为

* Api config    唯一需要修改的是travis使用的api地址，public的是org，private是com
* Token config  需要在git页面获取个人的AccessToken（需要一定的写权限），在codecov的页面获取AccessToken
* Github repo config    配置你本次创建的repo的名称、描述等
* Travis config 配置在travis中的环境变量


