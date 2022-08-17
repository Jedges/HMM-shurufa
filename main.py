from hmm import HMM
print("智能拼音输入法\n操作介绍：\n1.输入exit退出.\n2. w,s上下页查找")
pinyin=input("请输入拼音或退出:")
ownhmm=HMM()
limit=5
page=0
while pinyin!='exit':
    temp = ownhmm.viterbi(pinyin)
    if len(temp)==0:
        print("查无此拼音")
        pinyin=input("请输入拼音或退出:")
        continue
    ans = [temp[i:i + 5] for i in range(0, len(temp), 5)]
    len_ans=len(ans)
    for i in range(limit):
        print("%d.%s"%(i,ans[page][i]))
    s=input()
    while  s=='w' or s=='s':
        if s=='w':
            if page >=1:
                page=page-1
                for i in range(limit):
                    print("%d.%s"%(i,ans[page][i]))
        else:
            if page<len_ans-1:
                page=page+1
                for i in range(limit):
                    print("%d.%s"%(i,ans[page][i]))
        s=input()
    if '0'<=s<='4':
        print("结果为：",ans[page][eval(s)]) 
    pinyin=input("请输入拼音或退出:")
