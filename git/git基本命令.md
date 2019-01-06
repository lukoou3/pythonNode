## 一、设置签名
    git config --global user.name lukoou3
    git config --global user.email 18638489474@163.com

## 二、基本操作
#### 1、状态查看
     git status
查看工作区、暂存区状态

#### 2、添加
    git add [file name]
将工作区的“新建/修改”添加到暂存区

#### 3、提交
    git commit -m "commit message" [file name]
将暂存区的内容提交到本地库

#### 4、查看历史记录
    git reflog

#### 5、前进后退
###### 基于索引值操作[推荐]
    git reset --hard [局部索引值]
    git reset --hard a6ace91
###### 使用^符号：只能后退
    git reset --hard HEAD^
    注：一个^表示后退一步，n 个表示后退n 步
###### 使用~符号：只能后退
    git reset --hard HEAD~n
    注：表示后退n 步

#### 6、reset 命令的三个参数对比
###### --soft 参数
        仅仅在本地库移动HEAD 指针
###### --mixed 参数
        在本地库移动HEAD 指针
        重置暂存区
###### --hard 参数
        在本地库移动HEAD 指针
        重置暂存区
        重置工作区

#### 7、删除文件并找回
前提：删除前，文件存在时的状态提交到了本地库。
操作：` git reset --hard [指针位置] `
删除操作已经提交到本地库：指针位置指向历史记录
删除操作尚未提交到本地库：指针位置使用HEAD

#### 8、比较文件差异
###### git diff [文件名]
    将工作区中的文件和暂存区进行比较
###### git diff [本地库中历史版本] [文件名]
    将工作区中的文件和本地库历史记录比较
    不带文件名比较多个文件

#### 9、分支操作
###### 创建分支
    git branch [分支名]
###### 查看分支
    git branch -v
###### 切换分支
    git checkout [分支名]
###### 合并分支
    第一步：切换到接受修改的分支（被合并，增加新内容）上
    git checkout [被合并分支名]
    第二步：执行merge 命令
    git merge [有新内容分支名]
###### 解决冲突
```diff
第一步：编辑文件，删除特殊符号
第二步：把文件修改到满意的程度，保存退出
第三步：git add [文件名]
第四步：git commit -m "日志信息"
- 注意：此时commit 一定不能带具体文件名
```

## 三、连接远程库
#### 1、查看当前所有远程地址别名
     git remote -v

#### 2、创建远程库地址别名
    git remote add [别名] [远程地址]

#### 3、推送
    git push [别名] [分支名]

#### 4、克隆
    git clone [远程地址]
效果：
完整的把远程库下载到本地
创建origin 远程地址别名
初始化本地库

#### 5、拉取
    pull=fetch+merge
    git fetch [远程库地址别名] [远程分支名]
    git merge [远程库地址别名/远程分支名]
    git pull [远程库地址别名] [远程分支名]
