# -*- coding=utf8 -*-
from ts2gh import Graph
from ts import Transition, State, Label, TransitionSystem, read_ts_from_json
from typing import List, Set
import random
import json


def satisfy(gh: Graph, state: State):
    labels = gh.get_label(state).AP  # 由此获得状态state所需要满足的原子命题，即label
    for c_phy in c_phy_list:  # todo
        if len(list(set(c_phy).difference(labels))) == 0:
            return False
    return True


def dfs(gh: Graph):
    rr: Set[State] = set()  # 已经访问过的状态
    uu: List[State] = list()  # 实现栈的功能
    ii: List[State] = gh.initList  # 初始状态集
    b = True
    diff: List[State] = list(set(ii).difference(rr))  # 从I中去除R
    while len(diff) and b:  # 如果集合diff不为空，且b保持正确
        j = random.randint(0, len(diff)-1)
        state = diff[j]
        # visit(state)
        uu.append(state)  # push state into stack U
        rr.add(state)  # mark state as reachable
        while len(uu) and b:
            s_ = uu[-1]  # s'=top(U) 取栈顶元素
            post_s_ = gh.find_neighbours(s_)  # post(s')
            post_s_diff_rr = list(set(post_s_).difference(rr))  # post(s')/R
            if len(post_s_diff_rr) == 0:
                b = b and satisfy(gh, s_)
                if b:
                    uu.pop()  # pop U
            else:
                i = random.randint(0, len(post_s_diff_rr) - 1)
                s__ = post_s_diff_rr[i]  # let s'':element of post(s')/R
                uu.append(s__)  # push s'' into stack U
                rr.add(s__)  # mark s'' as reachable
        pass
        diff = list(set(ii).difference(rr))  # 更新差集
    if b:
        return "yes"
    else:
        return "no", uu
    pass


if __name__ == "__main__":
    with open("phy.json", encoding='utf-8') as f:
        data = json.load(f)
    # 每一个状态都满足phy，c_phy是不满足phy的情况，我们的目标是找反例c_phy
    c_phy_list = data["c_phy"]
    # ts = read_ts_from_json("ts_mutex.json")    # 有信号量y
    ts = read_ts_from_json("ts_mutex_2.json")    # 没有信号量y
    g = Graph(ts)
    result = dfs(g)
    counter_example = open("counter_example.txt", "w")  # 生成counterexample的txt文档
    if result == "yes":
        counter_example.write("yes")
        print("yes")
    else:
        print("no")
        counter_example.write("no\n")
        init = ts.initial_states[0].s_name    # 初始状态
        for state in result[1]:
            print(state.s_name)
            if state.s_name == init:
                counter_example.write(state.s_name)
            else:
                counter_example.write(" -> " + state.s_name)
        counter_example.close()
    f.close()
