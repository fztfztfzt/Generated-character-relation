# -*-  coding: utf-8 -*-
import os
import sys
import jieba
import jieba.posseg as pseg
from config import config
jieba.load_userdict(config['DICT_PATH'])  # 读取自定义词典
needName = {}
names = {}
relationships = {}
count = 0
with open(config['NAME_PATH'], 'r', encoding='utf8') as f:
    for line in f.readlines():
        localNames = line.split()
        for name in localNames:
            needName[name] = localNames[0]
with open(config['DATA_PATH'], 'r', encoding='utf8') as f:
    for line in f.readlines():
        count += 1
        lineNames = []  # 本行所有name
        wordsInfo = pseg.cut(line)
        for word, flag in wordsInfo:
            if flag == 'nr' and len(word) >= 2 and (word in needName):  # 名词
                word = needName[word]
                if (word in names) == False:
                    names[word] = 0
                    relationships[word] = {}
                names[word] += 1
                lineNames.append(word)
        for name1 in lineNames:
            for name2 in lineNames:
                if name1 != name2:
                    if (name2 in relationships[name1]) == False:
                        relationships[name1][name2] = 0
                    relationships[name1][name2] += 1
        sys.stdout.write("\r" + str(count))
with open(config['NODE_PATH'], 'w', encoding='utf8') as f:
    f.write("Id,Label,Weight\n")
    for name, value in names.items():
        f.write(name + ',' + name + ','+str(value) + '\n')
with open(config['EDGE_PATH'], 'w', encoding='utf8') as f:
    f.write("Source,Target,Weight\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                f.write(name + ',' + v + ',' + str(w) + '\n')
