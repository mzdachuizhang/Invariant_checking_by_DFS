# -*- coding=utf8 -*-
from ts2gh import Graph
from ts import Transition, State, Label, TransitionSystem, read_ts_from_json
from typing import List,Set


def dfs(gh: Graph):
    rr: Set[State] = set()  # 已经访问过的状态
    uu: List[State] = list()  # 实现栈的功能
    ii: List[State] = gh.initList  # 初始状态集
    b = True
    diff: List[State] = list(set(ii).difference(rr))  # 从I中去除R
    while len(diff) and b:  # 如果集合diff不为空，且b保持正确
        for state in diff:
            # visit(state)
            uu.append(state)  # push state into stack uu
            rr.add(state)  # mark state as reachable

            pass
    if b:
        return "yes"
    else:
        return "no", uu
    pass


if __name__ == "__main__":
    ts = read_ts_from_json("ts_mutex.json")
    g = Graph(ts)
    dfs(g)
