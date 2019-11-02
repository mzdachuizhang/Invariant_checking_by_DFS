# coding=utf-8
import json
from typing import List, Set


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


class Transition:
    s1_name: str = None  # 迁移前的状态名
    act: str = None  # 动作
    s2_name: str = None  # 迁移后的状态名

    def __init__(self, s: str):
        self.s1_name, self.act, self.s2_name = s.split(' ')


class Label:
    s_name: str = None
    AP: List[str] = None

    def __init__(self, s: str):
        if s is not None:
            self.s_name = s[0]
            self.AP = s[1:]


class TransitionSystem:
    """Transition System"""
    states: List[State] = None
    actions: Set[str] = None
    transitions: List[Transition] = None
    initial_states: List[str] = None
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

        self.initial_states = is_ if is_ is not None else list()
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


if __name__ == "__main__":
    ts = read_ts_from_json("ts_mutex.json")
    print(ts)
    pass
