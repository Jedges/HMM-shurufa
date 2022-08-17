import re
import os
import json
from jsonpath import jsonpath


rule = re.compile(r'[\u4E00-\u9FA5`~!@#$%^&*()_\-+=<>?:"{}|,.;·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘，。、|\n]{1,}')
for file in os.listdir('./corpus/wiki_zh'):
    for filename in os.listdir('./corpus/wiki_zh/'+file):
        fw = open('./corpus/corpus_pre.txt', 'a', encoding='utf-8')
        #print("当前处理文件:%s" %('./corpus/wiki_zh/'+file+'/'+filename))
        with open('./corpus/wiki_zh/'+file+'/'+filename, 'r', encoding='utf-8', errors='ignore') as fr:
            row_data=json.loads(fr.readline())
            text=jsonpath(row_data,"$..text")
            for txt in text: 
                for w in rule.findall(txt):
                    fw.write(w)
        fr.close()
        fw.close()
print("语料文件预处理完毕")
