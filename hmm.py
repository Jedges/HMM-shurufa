# -*- coding: utf-8 -*-

import json
from pysplit import pysplit


dirname='./data'

def takeSecondFirst(elem):
    return elem[1][0]
def takeFirst(elem):
    return elem[0]

class HMM:
    def __init__(self):
        with open(dirname +'/start_prob.json' , 'r') as f:
            self.start_prob=json.load(f)
        with open(dirname +'/emiss_prob.json' , 'r') as f:
            self.emiss_prob=json.load(f)
        with open(dirname +'/trans_prob.json' , 'r') as f:
            self.trans_prob=json.load(f)
        with open(dirname +'/pinyin_states.json' , 'r') as f:
            self.pinyin_states=json.load(f)
        with open('./data/pinyin.txt', 'r', encoding='utf-8') as f:
            self.pyList = f.read().split(',')


    def viterbi(self, strs):

        seq = pysplit(strs, self.pyList)

        self.min_f = -3.14e+100 
        res = [] 
    
        for n in range(len(seq)):
            length = len(seq[n])
            viterbi = {} 
            for i in range(length):
                viterbi[i] = {}

            for s in self.pinyin_states.get(seq[n][0]):
                viterbi[0][s] = (self.start_prob.get(s, self.min_f) +self.emiss_prob.get(s, {}).get(seq[n][0], self.min_f), -1)

            for i in range(length - 1):
                for s in self.pinyin_states.get(seq[n][i + 1]):
                    viterbi[i + 1][s] = max(
                        [(viterbi[i][pre][0] + self.emiss_prob.get(s, {}).get(seq[n][i + 1], self.min_f)
                          + self.trans_prob.get(s, {}).get(pre, self.min_f), pre) for pre in
                         self.pinyin_states.get(seq[n][i])])

            for s in self.pinyin_states.get(seq[n][-1]):
                viterbi[length - 1][s] = (viterbi[length - 1][s][0] + self.trans_prob.get('EOS', {}).get(s, self.min_f),
                                          viterbi[length - 1][s][1])

            words_list = [x for x in viterbi[length - 1].items()]
            words_list.sort(key=takeSecondFirst, reverse=True)
            for i in range(min(len(words_list), 100)):
                words = [None] * length
                words[-1] = words_list[i][0]

                for n in range(length - 2, -1, -1):
                    words[n] = viterbi[n + 1][words[n + 1]][1]

                res.append((i, ''.join(w for w in words)))
        
        res = list(set(res))
        res.sort(key=takeFirst)
        return [x[1] for x in res]
