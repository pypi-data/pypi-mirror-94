#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :my.py
# @Time     :2021/2/4
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import pandas as pd
import matplotlib.pyplot as plt
fig = plt.figure()
fig.set(alpha=0.2)

def get_info(inputs):
    return inputs.info()

def get_desc(inputs):
    return inputs.describe()

def survived(inputs):
    plt.subplot2grid((2, 3), (0, 0))  # 在一张大图里分列几个小图
    inputs.Survived.value_counts().plot(kind='bar')  # 柱状图 
    plt.title(u"获救情况 (1为获救)")  # 标题
    plt.ylabel(u"人数")

    plt.subplot2grid((2, 3), (0, 1))
    inputs.Pclass.value_counts().plot(kind="bar")
    plt.ylabel(u"人数")
    plt.title(u"乘客等级分布")

    plt.subplot2grid((2, 3), (0, 2))
    plt.scatter(inputs.Survived, inputs.Age)
    plt.ylabel(u"年龄")  # 设定纵坐标名称
    plt.grid(b=True, which='major', axis='y')
    plt.title(u"按年龄看获救分布 (1为获救)")

    plt.subplot2grid((2, 3), (1, 0), colspan=2)
    inputs.Age[inputs.Pclass == 1].plot(kind='kde')
    inputs.Age[inputs.Pclass == 2].plot(kind='kde')
    inputs.Age[inputs.Pclass == 3].plot(kind='kde')
    plt.xlabel(u"年龄")  # plots an axis lable
    plt.ylabel(u"密度")
    plt.title(u"各等级的乘客年龄分布")
    plt.legend((u'头等舱', u'2等舱', u'3等舱'), loc='best')  # sets our legend for our graph.

    plt.subplot2grid((2, 3), (1, 2))
    inputs.Embarked.value_counts().plot(kind='bar')
    plt.title(u"各登船口岸上船人数")
    plt.ylabel(u"人数")
    return plt

def attribute(inputs):
    Survived_0 = inputs.Pclass[inputs.Survived == 0].value_counts()
    Survived_1 = inputs.Pclass[inputs.Survived == 1].value_counts()
    df = pd.DataFrame({u'获救': Survived_1, u'未获救': Survived_0})
    df.plot(kind='bar', stacked=True)
    plt.title(u"各乘客等级的获救情况")
    plt.xlabel(u"乘客等级")
    plt.ylabel(u"人数")
    return plt
