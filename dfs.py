# -*- coding=utf8 -*-
from ts2gh import Graph
from ts import Transition, State, Label, TransitionSystem, read_ts_from_json
from typing import List, Set


def satisfy(gh: Graph, state: State):
    labels = gh.get_label(state).AP  # 由此获得状态state所需要满足的原子命题，即label
    fi = ['c1', 'w2']
    #if len(list(set(labels).difference(fi))) == 1:
    if labels == fi:
        return False
    else:
        return True


def dfs(gh: Graph):
    rr: Set[State] = set()  # 已经访问过的状态
    uu: List[State] = list()  # 实现栈的功能
    ii: List[State] = gh.initList  # 初始状态集
    b = True
    diff: List[State] = list(set(ii).difference(rr))  # 从I中去除R
    while len(diff) and b:  # 如果集合diff不为空，且b保持正确
        for state in diff:
            # visit(state)
            uu.append(state)  # push state into stack U
            rr.add(state)  # mark state as reachable
            while len(uu) and b:
                s_ = uu[-1]  # s'=top(U) 取栈顶元素
                post_s_ = gh.find_neighers(s_)  # post(s')
                post_s_diff_rr = list(set(post_s_).difference(rr))  # post(s')/R
                if len(post_s_diff_rr) == 0:
                    uu.pop()  # pop U
                    b = b and satisfy(gh, s_)
                else:
                    for s__ in post_s_diff_rr:  # let s'':element of post(s')/R
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
    ts = read_ts_from_json("ts_mutex.json")
    g = Graph(ts)
    result = dfs(g)
    if result == "yes":
        print("yes")
    else:
        print("no")
        for state in result[1]:
            print(state.s_name)
