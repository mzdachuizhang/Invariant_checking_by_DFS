from typing import Dict, List, Set, Tuple
from ts import Transition, State, Label, TransitionSystem,read_ts_from_json

class Graph:
    vertexList: Dict[State, Label] = None  # 状态：Label 的一个字典
    edgesList: List[Tuple[State, State]] = None  # 边 [(s0,s1)....]

    def __init__(self, ts: TransitionSystem):
        """
        1.先初始化节点
        2.再初始化边
        :param ts:
        """
        if ts.states is not None:
            self.vertexList = dict()
            for state in ts.states:
                for label in ts.labels:
                    if state.s_name == label.s_name:
                        self.vertexList[state] = label

        if ts.transitions is not None:
            self.edgesList = list()
            for transition in ts.transitions:
                for s1 in self.vertexList.keys():
                    for s2 in self.vertexList.keys():
                        if transition.s1_name == s1.s_name and transition.s2_name == s2.s_name:
                            self.edgesList.append((s1, s2))
        pass

    def __str__(self):
        return ','.join([s1.s_name+"->"+s2.s_name for (s1, s2) in self.edgesList])


if __name__ == "__main__":
    ts = read_ts_from_json("ts_mutex.json")
    g = Graph(ts)
    print(g)
    pass
