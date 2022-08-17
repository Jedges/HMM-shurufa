def pysplit(word, wordList):
    """
    @function: 进行拼音划分, 返回拼音划分结果列表
    @word: 待划分的拼音, 并且是无空格字符串,
    @wordList: 划分规则
    @return: 所有可能的划分结果
    """
    ans = [] if word not in wordList else [(word,)]
    wordLen = len(word)
    for i in range(1, wordLen ):
        if word[0:i] in wordList:
            res=pysplit(word[i:], wordList)
            for item in res:
                ans.append((word[:i],)+item)
    return ans