# -*- coding=utf8 -*-
from ts2gh import Graph
from ts import Transition, State, Label, TransitionSystem, read_ts_from_json, out_ts_graph, out_ts_graph_origin
from typing import List, Set
import random
import json
from dfs_bad import satisfy,dfs

if __name__ == "__main__":
    with open("c_phy.json", encoding='utf-8') as f:
        data = json.load(f)
    # 每一个状态都满足phy，c_phy是不满足phy的情况，我们的目标是找反例c_phy
    c_phy_list: list = data["c_phy"]
    ts = read_ts_from_json("ts_mutex.json")    # 有信号量y
    # ts = read_ts_from_json("ts_mutex_2.json")    # 没有信号量y
    g = Graph(ts)
    result = dfs(g)
    out_ts_graph_origin(ts, 'transition_system_original.gv')   # 有信号量时画这个图
    # out_ts_graph(result[1], ts, 'transition_system_counterexample.gv')   # 没有信号量时画这个图
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