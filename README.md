# LAnn标注工具
## 当前分支
- 目前为封闭域关系三元组标注，不提供新关系的标注，之前开放域关系三元组版本将不再维护。
- 计划脱离对Django框架的依赖，借助PyQt的WebEngine实现标注界面和Python程序数据传输，更好地支持Pytorch和数据处理，已基本打通JS和Python之间的墙壁，霍霍哈哈哈哈。
## LAnn简介
![演示视频](https://github.com/Freeshman/LAnn/blob/master/example.gif)
LAnn（Little Annotator）是一个用于标注三元组的纯前段中文标注工具。具有使用简单的特点，采用网页的形式，使用浏览器便可运行。标注过程、结果直观，易后处理。基本不用配置，快速上手。可只用于NER标注，也可以适当修改，改为POS标注或者分词标注。

[试一试](https://freeshman.github.io/LAnn/LittleAnn.html)
## 快速上手
### 配置实体类型
![实体类型](https://github.com/Freeshman/LAnn/blob/master/entity_relation_class_config.png)
### 配置按键映射（如需要）
![实体关系类型](https://github.com/Freeshman/LAnn/blob/master/key_config.png)
### 配置辅助标注模型
![实体关系类型](https://github.com/Freeshman/LAnn/blob/master/model_config.png)
## LAnn读取文件
标注工具可以直接读取：
- 原始文本
- BIO命名实体标注后的文本
- LAnn标注过的文本
## 标注流程
### 实体的标注或取消：
鼠标选中文字（或双击快速选中），点击界面右边的实体按钮，点击实体类型（或按相应的数字键）完成标注，直接按空格将默认使用服务器给出的分类（服务器可用情况下）；或点击取消按钮（或按“a”键）消除先前的标注。
### 三元组的标注：
- 依次点击两个实体类型的元素（s,o），跳出关系选择界面进行三元组标注
- 在选择(锁定)元素时，“已选中(锁定)”标签会变成粉红色进行提示
- 选中元素后，可点击取消消除当前元素的标记
- 选中元素后，点击空白处（或按空格键）将取消选中
- 已标注的三元组再次进行标记可取消之前的标记

### 类VIM操作：
- h,j,k,l移动光标，g和；键分别向左右移动两个字符
- n、b翻页
- w、e跳转到上一个或下一个标记实体
- r跳转到标记结尾
- 空格选中，移动光标框选：s标记为实体；a取消当前标记（还支持快速修改：光标在实体或关系区域内时，不用选中可直接修改）
- 不用空格选中，直接按s或者f默认选中两个字符进行标注
- p分别标记[s，o]，双按p标记并锁定标记，但只能锁定s
- 可输入数字进行上下左右光标和页面的跳转，按回车直接跳转到指定数字页面，ctrl+g跳转到指定字符处

### 字符增删
 有时候不可避免地需要增删字符，此时需要对三元组的索引进行调整，因此设计并加入了此功能。
 
 - 删除字符
 
 点击删除键（或按“x”）删除光标处的字符，如果当前字符对应有三元组，则三元组直接被舍弃。
 
 - 插入字符
 
 点击插入键（或按“u”）在光标前插入指定的字符，字符的标签默认为“O”，如有必要，重新标注实体。如果需要在页面最后位置处插入字符，需要间接操作才能实现（因为这种情况比较少见，故不再优化）。
 
 删除的字符会默认为插入的字符，因此在删除后直接按插入键会恢复删除的字符，间接实现撤销功能。
## 标注存储格式
语料文本的标注结果文件（.lann）每行为一个字符，包含三列，每列用”\t“隔开，分别对应字符域、实体关系域和三元组域。

- 字符域：为统一格式和方便预览，原始文本的换行符“\n”用“\_换行符\_”代替。
- 实体关系域：采用BIO标注方式。
- 三元组域：包含相同S的三元组都记录在S首字符那一行，三元组之间采用“;”相隔，方便分割；SPO用“>”相隔。不构成三元组的字符该域为“X”。
***使用前两个域分割后即为NER数据集。***
## Django后台辅助标注
LAnnBack为后台辅助标记部分，可支持实体分类模型、序列标注模型和关系分类模型。
**前段：**
- 勾选**序列辅助标注** 会将当前页面的文本进行序列预标注
- 设定实体或关系时，辅助给出相应的分类和概率
**后端:**
- 接收数据形式根据server.js确定
- LAnnBack/UI.py文件中，process、seqlab和triple_relation_classfy分别对应实体分类、序列标注和关系分类方法，适当修改调用自己的模型。
- 辅助标注后台如果收到带有标签的样本，将在new文件夹下记录新的样本，用于后期模型的训练。

开启辅助标注后台：

`python manage.py runserver 0.0.0.0:8000`

**注意:** 如果辅助标注服务器为本地计算机，需要安装django-cors-headers和设置来解决跨域访问问题。

## TODO

- [x] 三元组的编辑
- [-] 整合分词
- [x] 智能算法辅助标注
- [-] 翻译为英文版
- [x] 添加VIM模式
- [ ] 更优美的三元组显示方式
- [ ] 语料标注质量提升
