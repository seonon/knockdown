# 将题目装进微信

每个人都有微信，每个人都随身带着微信，微信小程序提供了一个快速便捷编写程序的选项。
最近要参加一个竞赛，有官方题库分发下来，为了利用零碎的时间熟悉题目，我做了这个小程序，随时随地的背题。题库是独立的，我把小程序分享出来，只要制作自己的题库，任何人都可以制作自己的答题、背题小程序

## 程序界面及特性

主要有两个界面，主界面上选择练习方式，问题界面答题、背题。目前支持顺序学习，乱序学习和学习收藏的问题。

### 界面

![Home](https://raw.githubusercontent.com/seonon/knockdown/master/doc/images/home.PNG)
![Picture Support](dhttps://raw.githubusercontent.com/seonon/knockdown/master/doc/images/picture.PNG)
![Favorite](https://raw.githubusercontent.com/seonon/knockdown/master/doc/images/favorite.PNG)

### 特性

1. 记录答题进度，使用local storage存储答题的进度
2. 乱序答题
3. 收藏题目，重点复习
4. 题目完全放在本地，免除服务端开发，快速部署
5. 提供脚本将文本文件格式的题目转化为题库，图片使用特殊的标记添加

## 具体使用

一共分三步：

1. 准备题库
2. 使用微信开发者工具调试
3. 预览小程序/上传小程序，开始背题

### 准备题库


我提供了一个Python脚本，来将文本格式的题目解析为js格式的题库，即/scripts/parse.py。

#### 处理题目

首先将原始题目保存为文本，然后使用该脚本将其解析为题库
该脚本对格式要求不高，以下几种题目结构都能正确识别

```python
# 题目和选项在一行
1. 哪个小程序可以快速背题？A. KnockDown B. GreatChinaDream
# 题目和选项不在一行
1. 哪个小程序可以快速背题？
A. KnockDown B. GreatChinaDream
# 选项多行
1. 哪个小程序可以快速背题？
A. KnockDown
B. GreatChinaDream
```

⚠️注意事项

1. 题目编号和题干、选项字母和选项内容之间必须有分隔符号，目前支持的分隔符号有.，。和空格
2. 新的题目必须从行首开始，且题目必须有编号，且编号后必须要分隔符号
3. 选项必须是大写字母，即A，B，C...Z，选项后必须有分隔符号
4. 如果题干或选项中有大写字母，务必确保该大写字母后没有分隔符号，以免错误的解析为选项

#### 处理图片

若原始题目中有图片，有两种处理方式：

1. 将图片保存在小程序资源文件夹中，但是小程序的大小被限制在2M，图片太多的话就不能使用这种方式处理了
2. 上传到图片CDN上，选择哪个CDN取决于个人选择，[SM.MS](https://sm.ms/)是比较简便的选择

不管那种处理方式，都需要把图片的地址按照图片标记方式插入到题目的文本文件中，标记语法为

```html
<picture src=https://i.loli.net/2018/07/21/5b52ead65f0b2.png>
或者
<picture src="https://i.loli.net/2018/07/21/5b52ead65f0b2.png">
```

需要注意的是，图片一定要插在题干和选项之间

```html
1. 下图所示是哪个小程序？
<picture src=https://i.loli.net/2018/07/21/5b52ead65f0b2.png>
A. KnockDown B. GreatChinaDream
<!-->本地图片存储，路径必须是相对路径<-->
1. 下图所示是哪个小程序？ <picture src=../../resource/avatar.png>A. KnockDown B. GreatChinaDream
```

#### 答案

答案有两种处理方式，第一种，答案在题目文件中，在这种情况下，答案需要出现在选项后面，即：

```python
1. 哪个小程序可以快速背题？A. KnockDown B. GreatChinaDream A
# 或
1. 哪个小程序可以快速背题？A. KnockDown B. GreatChinaDream 
A
```

第二种，提供另外的答案文本文件，答案的组织没要求，解析脚本会顺序的顺序读出文件中所有大写字母，并在读取题目文件的过程中动态的将这些选项依次的匹配上去。

⚠️注意事项

1. 如果指定了答案文件，题目中就不能有答案，且答案文件中选项个数和题目数一定要匹配

```python
# 答案文件组织
1-5 ABDFA
6-10 BDACA
11-15 DEAFD   CCDCB
1-5 ABDFA
6-10 BDACA
 DEAFD  16-20 CCDCB
1-5 ABDFA
B
DA
CA
11-15 DEAFD  16-20 CCDCB
```

#### 解析脚本的使用

该脚本使用python编写，需要保证电脑上安装有python，python2.7和python3均支持。

##### 脚本帮助

```shell
$ python parse.py -h
# usage: parse.py [-h] [-a ANSWER_SHEET] rawfile output
# 
# positional arguments:
#   rawfile               text file contains questions 
#   output                output filename
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -a ANSWER_SHEET, --answer_sheet ANSWER_SHEET
#                         add a answer sheet if the answers are not included in
#                         the text question file
```

rawfile即题目文本文件，output为输出文件，请指定为.js格式。可选参数answer_sheet即答案文件。
具体使用方式如下：

```python
# 答案在题目中
python parse.py questionsetwithanswer.txt res.js
# 答案不在题目中，这时必须指定答案文件
python parse.py questionsetwithoutanswer.txt res.js -a answser_sheet.txt
```

### 使用微信开发者工具调试

小程序上手请参考[微信小程序](https://developers.weixin.qq.com/miniprogram/dev/index.html).

#### 替换题库

使用上一步生成的题库替换原来题库，题库位置为/resource/res.js。

#### 将图片复制到资源目录下

如果使用本地图片存储，需要将图片放到资源目录下

#### 预览/上传

下面就可以愉快的使用了！