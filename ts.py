# coding=utf-8
import json
from typing import List, Set
from graphviz import Digraph


# A transition system TS is a tuple (S, Act, ->, I, AP, L)
class State:
    s_name: str = None
    val_var: Set[str] = None

    def __init__(self, s: str):
        self.s_name, last = s.split(':')
        if last is not None:
            self.val_var = set()
            for var in last.split(","):
                self.val_var.add(var)

    def __str__(self):
        return self.s_name + ":" + ','.join([val for val in self.val_var])

    def to_graph_use(self):
        return self.s_name + "\n" + "<" + ",".join([str(v) for v in self.val_var]) + ">"


class Transition:
    s1_name: str = None  # 迁移前的状态名
    act: str = None  # 动作
    s2_name: str = None  # 迁移后的状态名

    def __init__(self, s: str):
        self.s1_name, self.act, self.s2_name = s.split(' ')

    def __str__(self):
        return self.s1_name+" -"+self.act+"-> "+self.s2_name


class Label:
    s_name: str = None
    AP: List[str] = None

    def __init__(self, s: str):
        if s is not None:
            self.s_name = s[0]
            self.AP = s[1:]

    def __str__(self):
        return self.s_name+":"+','.join([val for val in self.AP])


class TransitionSystem:
    """Transition System"""
    states: List[State] = None
    actions: Set[str] = None
    transitions: List[Transition] = None
    initial_states: List[State] = None
    atomic_propositions: Set[str] = None
    labels: List[Label] = None

    def __init__(self,  # act和ap用set表示，里面的元素不需要重复
                 s_: List[str] = None,
                 act_: Set[str] = None,
                 trans_: List[str] = None,
                 is_: List[str] = None,
                 ap_: Set[str] = None,
                 l_: List[str] = None,
                 ):
        if s_ is not None:
            self.states = list()
            for s in s_:
                state = State(s)
                self.states.append(state)

        self.actions = act_ if act_ is not None else set()

        if trans_ is not None:
            self.transitions = list()
            for tran in trans_:
                transition = Transition(tran)
                self.transitions.append(transition)

        if is_ is not None:
            self.initial_states = list()
            for iss in is_:
                for state in self.states:
                    if iss == state.s_name:
                        self.initial_states.append(state)
                pass

        self.atomic_propositions = ap_ if ap_ is not None else set()
        if l_ is not None:
            self.labels = list()
            for l in l_:
                label = Label(l)
                self.labels.append(label)


def read_ts_from_json(file_path: str) -> TransitionSystem:
    """读入Transition System中的文件
    :param file_path: 文件路径
    """
    with open(file_path, encoding='utf-8') as f:
        ok = json.load(f)
    return TransitionSystem(ok['S'], ok['Act'], ok['Trans'], ok['I'], ok['AP'], ok['L'])


def out_ts_graph_origin(ts: TransitionSystem, filename: str) -> None:
    """将Transition System有向图输出（正确的时候给出）
    :param ts: 要输出的Transition System
    :param filename: 文件类型(扩展名)
    """
    S: List[State] = ts.states  # 存所有状态
    Trans: List[Transition] = ts.transitions  # 存所有转移关系

    # 生成TS的GraphViz有向图
    dot = Digraph(comment='Transition System', format='png')
    for s in S:   # 生成节点 正常的
        str_s = s.to_graph_use()
        str_s_name = s.s_name
        dot.node(name=str_s_name, label=str_s)
    for t in Trans:  # 生成边(转移关系上的动作)
        str_s1 = t.s1_name
        str_act = str(t.act)
        str_s2 = t.s2_name
        dot.edge(str_s1, str_s2, label=str_act)
    dot.render(filename, view=True)


def out_ts_graph(false: List[State], ts: TransitionSystem, filename: str) -> None:
    """将Transition System有向图输出
    :param false: 错误状态的列表
    :param ts: 要输出的Transition System
    :param filename: 文件类型(扩展名)
    """
    S: List[State] = ts.states  # 存所有状态
    Trans: List[Transition] = ts.transitions  # 存所有转移关系

    # 生成TS的GraphViz有向图
    dot = Digraph(comment='Transition System', format='png')
    false_name: List[str] = list()
    black_state = list(set(S) - set(false))    # 没有访问到的状态集合

    for s in false:    # 标记出错的结点
        false_name.append(s.s_name)
    for s in false:  # 生成结点(状态) 标红的
        str_s = s.to_graph_use()
        str_s_name = s.s_name
        dot.node(name=str_s_name, label=str_s, color='red')
    for s in black_state:   # 生成节点 正常的
        str_s = s.to_graph_use()
        str_s_name = s.s_name
        dot.node(name=str_s_name, label=str_s)
    for t in Trans:  # 生成边(转移关系上的动作)
        str_s1 = t.s1_name
        str_act = str(t.act)
        str_s2 = t.s2_name
        if str_s1 in false_name and false_name[false_name.index(str_s1)+1] == str_s2:
            dot.edge(str_s1, str_s2, label=str_act, color='red')
            # false_name.remove(str_s1)    # 去掉已经用过的节点
        else:
            dot.edge(str_s1, str_s2, label=str_act)
    dot.render(filename, view=True)


if __name__ == "__main__":
    ts = read_ts_from_json("ts_mutex.json")
    print(ts.states[0])  # 一个状态
    print(ts.actions[0])  # 一个动作
    print(ts.transitions[0])  # 一个迁移
    print(ts.initial_states[0])  # 一个初始状态
    print(ts.atomic_propositions[0])  # 一个原子命题
    print(ts.labels[0])  # 一个label function
    print(ts.initial_states)
    print(len(ts.transitions))
    pass
