# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/12 10:30 AM
# LAST MODIFIED ON:
# AIM: 状态机器

from automata.state_machine import StateMachine

from automata.sequence import StrSequence
from sentence_spliter.logic_graph import long_short_cuter, simple_cuter, special_cuter
from sentence_spliter.spliter import cut_to_sentences
machine = StateMachine(special_cuter())
#machine = StateMachine(special_graph)
# machine = StateMachine(logic_simple)
if __name__ == '__main__':
    novel = '/Users/Shared/小说/女频小说25本-Estella/女频小说25本-Estella/你原来是这样的叶先生.txt'
    with open(novel, 'r') as f:
        data = f.read()

    sentence_org = '在很久很久以前......... 有座山。山里有座庙啊!!!庙里竟然有个老和尚！？。。。。www.baidu.com.1.2.3'
    #'“我和你讨论的不是一个东西，死亡率与死亡比例是不同的” “你知道么？CNN你们总是制造假新闻。。。”'
    sentence = StrSequence(sentence_org)


    # sentence = StrSequence('《掏出绝命岛!》真好看。')
    machine.run(sentence, verbose=True)
    print('\n'.join(sentence.sentence_list()))
