# LAnn标注工具

## LAnn简介
![演示视频](https://github.com/Freeshman/LAnn/blob/master/example.gif)
LAnn（Little Annotator）是一个标注三元组的纯前段中文标注工具。具有使用简单的特点，采用网页的形式，使用浏览器便可运行。标注过程、结果直观，易后处理。基本不用配置，快速上手。

[试一试](https://freeshman.github.io/LAnn/LittleAnn.html)

## LAnn读取文件
标注工具可以直接读取：
- 原始文本
- BIO命名实体标注后的文本
- LAnn标注过的文本
## 标注流程
### 实体（关系）的标注或取消：
鼠标选中文字（或双击快速选中），点击界面右边的实体（关系）按钮，完成标注；或点击取消按钮消除先前的标注。
### 三元组的标注：
- 鼠标分别依次点击SPO，完成三元组的标注；
- 在选择三元组时，“已选中”标签会变成粉红色进行提示；
- 三元组未完成标记前，点击错误，可点击取消消除当前选中的标记；
- 已标注的三元组再次进行标记可取消之前的标记。
- 依次点击两个实体类型的元素，将会跳出关系选择界面进行三元组标注（针对关系不出现在文本中的情况）
### 类VIM操作：
- h,j,k,l移动光标，g和；键分别向左右移动两个字符
- n、b翻页
- w、e跳转到上一个或下一个标记实体或关系
- r跳转到标记结尾
- 空格选中，移动光标框选：s标记为实体；f标记为关系；a取消当前标记（还支持快速修改：光标在实体或关系区域内时，不用选中可直接修改）
- 不用空格选中，直接按s或者f默认选中两个字符进行标注
- p分别标记[s，p，o]，双按p标记并锁定标记，但只能锁定s或者s，p这两种形式，单独锁定p或者p，o不支持
- 可输入数字进行上下左右光标和页面的跳转，按回车直接跳转到指定数字页面，ctrl+g跳转到指定字符处

## 光标自动右移
为了尽量减少人工按键，添加了光标自动右移功能，自动移动不会干预人工移动。

## 标注格式
语料文本的标注结果文件（.lann）每行为一个字符，包含三列，每列用”\t“隔开，分别对应字符域、实体关系域和三元组域。

- 字符域：为统一格式和方便预览，原始文本的换行符“\n”用“\_换行符\_”代替。
- 实体关系域：采用BIO标注方式。
- 三元组域：包含相同S的三元组都记录在S首字符那一行，三元组之间采用“;”相隔，方便分割；SPO用“>”相隔。不构成三元组的字符该域为“X”。
## Django后台辅助标注
LAnnBack为后台辅助标记部分，内含实体分类模型和序列标注模型。

- 勾选**序列辅助标注** 会将当前页面的文本进行序列预标注
- 设定实体或关系时，辅助给出相应的分类和概率

两个模型采用的Pytorch框架，两个模型各自对应一个things2id，读取各自的label文件，共享字符转id文件。

辅助标注后台如果收到带有标签的样本，将在new文件夹下记录新的样本，用于后期模型的训练。

开启辅助标注后台：

`python manage.py runserver 0.0.0.0:8000`

**注意:** 如果辅助标注服务器为本地计算机，需要安装django-cors-headers和设置来解决跨域访问问题。

## TODO

- [x] 三元组的编辑
- [ ] 整合分词
- [x] 智能算法辅助标注
- [ ] 翻译为英文版
- [x] 添加VIM模式
