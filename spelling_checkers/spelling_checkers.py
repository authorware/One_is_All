# coding:utf-8
# 利用朴素贝叶斯算法思想实现英文拼写检查
# p(c/w)
# 基于big.txt中的单词库
import re
import collections


def load_data(path):
    """以字典方式形成一个英文词汇库"""
    f = open(path, 'r')
    context = f.read()
    words_dict = train(words(context))
    return words_dict


def words(text):
    """利用正则表达式提取数据中所有单词"""
    return re.findall(r'[a-z]+', text.lower())


def train(features):
    """用字典形式储存所有单词，键表示单词，值表示在数据库中出现的次数"""
    model = collections.defaultdict(lambda: 1)  # 初始化所有单词的默认出现的次数值为1
    for i in features:
        model[i] += 1
    return model


def edit(word):
    """w对应的所有可能正确的c"""
    n = len(word)
    alph = 'abcdefghijklmnopqrstuvwxyz'
    c_pro = set([word[0:i] + word[i + 1:] for i in range(n)] +  # 删除一个字母
               [word[0:i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)] +  # 交换一个字母位置
               [word[0:i] + c + word[i + 1:] for i in range(n) for c in alph] +  # 替换一个字母
               [word[0:i] + c + word[i:] for i in range(n + 1) for c in alph])  # 插入一个字母
    return c_pro


def edit_1(word, words_dict):
    """编辑距离是1的所有可能"""
    c = []

    c_pro = edit(word)

    for w in c_pro:
        if w in words_dict:
            c.append(w)

    if len(c)
        # print('在编辑距离1中，寻找写错的单词所对应的所有正确的如下：')
        # print(c)
        # print('共:%d个' % len(c))
        print('修改后为：')

        return c
    else:
        return 0


def edit_2(word, words_dict):
    """编辑距离是2的所有可能"""
    c = []
    for w1 in edit(word) :
        for w2 in edit(w1):
            if w2 in words_dict:
                c.append(w2)
    c = set(c)

    if len(c):

        # print('在编辑距离2中，寻找写错的单词所对应的所有正确的如下：')
        # print(c)
        # print('共:%d个' % len(c))
        print('修改后为：')

        return c
    else:
        return 0


def edit_0(word, words_dict):
    """直接输入正确"""
    if word in words_dict:
        c = [word]

        print('单词输入正确，无需改正')
        # print(c)

    else:
        c = 0
    return c


def correct(word, words_dict):
    """
    p(w/c)概率即正确的c被错写成w的概率，这里用or的先后顺序替代了，
    即正好输对>1次距离>2次距离>什么也不改
    1次距离可能性比2次距离大
    找出1次距离中w对应的应该正确的所有c
    再通过p(c)在词库寻找出现的次数最多的哪个，即概率最大的那个
    就是最后的正确c
    即p(c/w)
    """
    keys = edit_0(word, words_dict) or edit_1(word, words_dict) or edit_2(word, words_dict) or [word]

    # print('在correct函数中,查找单词在先验中出现的次数，也就是概率如下:')

    new_dict = {}
    for i in keys:
        new_dict[i] = words_dict[i]  # i为keys中的每个字符串，也就是word_lists中的键名，通过键名获取其在单词库中的次数值
    sort_dict = sorted(new_dict.items(), key=lambda x: x[1], reverse=True)

    # print(sort_dict)
    # print('由排序结果也就是概率，得到概率最大的是:')

    # p(c)即在p(w/c)的基础上，再考虑原词库中个数最多的，即概率最大的那个，上面的for循环后的代码，就是对下面代码详细解释
    return max(keys, key=lambda x: words_dict[x])


if __name__ == '__main__':
    words_dict = load_data('big.txt')

    word = input('请输入单词:')
    reco = correct(word, words_dict)  # 'teut'是待检查的英文字符

    if word != reco:
        print(reco)

