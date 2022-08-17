# -*- coding: utf-8 -*-

import pypinyin 
import json
import math
import re

dirname = './data'


def load():

    file = 'corpus/corpus_pre.txt' 
    rule = re.compile(r'[\u4e00-\u9fa5]{2,}')
    with open(file, 'r', encoding='utf-8') as f:
        seqs = rule.findall(f.read())
    return seqs


def init_start(seqs):

    """
    @function:统计初始化概率矩阵，计算汉字出现在词首的概率，
    """
    start_prob = {}  
    tot = 0

    for seq in seqs:
        tot+=1
        if len(seq) == 0:
            continue
        if seq[0] not in start_prob.keys():
            start_prob[seq[0]]=1
        else:
            start_prob[seq[0]] +=  1

    # 防止概率计算的时候因为越算越小导致计算机无法比较，所有的概率都进行了自然对数运算。
    for key in start_prob.keys():
        start_prob[key] = math.log(start_prob.get(key) / tot)

    save('start_prob', start_prob)


def init_trans(seqs):
    """
    @function:找出字典中每个汉字后面出现的汉字集合，并统计概率。
    """

    trans_prob = {} 
    for seq in seqs:

        if len(seq) == 0:
            continue

        seq = [_ for _ in seq]


        seq.insert(0, 'BOS')
        seq.append('EOS')

        # init the occurence of "[pre][post]"
        for index, post in enumerate(seq):
            if index:
                pre = seq[index - 1]
                if post not in trans_prob.keys():
                    trans_prob[post] = {}
                if pre not in trans_prob[post].keys():
                    trans_prob[post][pre]=1
                else:
                    trans_prob[post][pre]+=1

    for key in trans_prob.keys():
        tot = sum(trans_prob.get(key).values())
        for pre in trans_prob.get(key).keys():
            trans_prob[key][pre] = math.log(trans_prob[key].get(pre) / tot)

    save('trans_prob', trans_prob)


def init_emiss(seqs):
    """
    @function:统计每个汉字对应的拼音以及在日常情况下的使用概率
    """

    emiss_prob = {} 

    for seq in seqs:

        if len(seq) == 0:
            continue

        pinyin = pypinyin.lazy_pinyin(seq)

        for py, word in zip(pinyin, seq):
            py=py.replace('ue', 've', -1)
            if word not in  emiss_prob.keys():
                emiss_prob[word] = {}
            if py not in emiss_prob[word].keys():
                emiss_prob[word][py]=1
            else:
                emiss_prob[word][py]+=1


    for word in emiss_prob.keys():
        tot = sum(emiss_prob.get(word).values())
        for key in emiss_prob.get(word):
            emiss_prob[word][key] = math.log(emiss_prob[word][key] / tot)

    save('emiss_prob', emiss_prob)


def init_pinyin_states():

    with open(dirname+'/emiss_prob.json') as f:
        emiss_prob = json.load(f)
    
    pinyin_states = {}
    for key in emiss_prob.keys():
        for pinyin in emiss_prob.get(key):
            if not pinyin_states.get(pinyin, None):
                pinyin_states[pinyin] = []
            pinyin_states[pinyin].append(key)
    
    save('pinyin_states',pinyin_states)


def save(filename, data):
    with open(dirname+'/' + filename + '.json', 'w') as f:
        json.dump(data, f, indent=2)
        

def init():

    seqs = load()

    print("Init began")
    
    print("Init start_prob")
    init_start(seqs)
    print("Init trans_prob")
    init_emiss(seqs)
    print("Init emiss_prob")
    init_trans(seqs)
    print("Init pinyin_states")
    init_pinyin_states()
    
    print('Init Finished')


if __name__=='__main__':
    init()

    
    