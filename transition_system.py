# coding=utf-8
import json
from typing import List, Dict, Set
#from deprecated import deprecated
#from graphviz import Digraph

# A transition system TS is a tuple (S, Act, ->, I, AP, L)
# S, ->, L定义类实现，其他元素直接用字符串表示


class State:
    """"TS元组中的状态(State)类"""
    s_name: str = None  # 状态名
    val_var: Dict[str, int] = None  # 变量的取值，用字典表示

    def __init__(self, s_name_: str, val_var_: Dict):
        """构造器：直接传入location名称和变量字典"""
        self.s_name = s_name_
        self.val_var = val_var_

    # def __str__(self):
    #     """转为字符串表示：如<start,nsoda=1∧nbeer=1>"""
    #     return "<" + self.s_name + "," + "∧".join([k + "=" + str(v) for k, v in self.val_var.items()]) + ">"

    # def to_graph_use(self):
    #    """给绘图用的字符串表示：如start,nsoda=1,nbeer=1"""
    #    return self.s_name + "," + ",".join([k + "=" + str(v) for k, v in self.val_var.items()])

    def __eq__(self, other):
        """判断两状态是否相等：状态名相同且所有变量的值相同"""
        if self.s_name != other.val_var:
            return False
        for k in self.val_var.keys():
            if self.val_var[k] != other.val_var[k]:
                return False
        return True


class Transition:
    """TS元组中的迁移(->)类：一组'S x Act x S'的迁移关系"""
    s1: State = None  # 迁移前的状态
    act: str = None   # 迁移的动作
    s2: State = None  # 迁移后的状态

    def __init__(self, s1_: State, act_: str, s2_: State):
        """构造器：状态，动作，状态"""
        self.s1 = s1_
        self.act = act_
        self.s2 = s2_

    def __str__(self):
        """用字符串表示表示迁移：如<select,nsoda=1∧nbeer=1> -(sget)-> <start,nsoda=0∧nbeer=1>"""
        return str(self.s1) + " -(" + self.act + ")-> " + str(self.s2)


class Label:
    """TS中的labeling function: 就是判断原子命题AP在每个状态是否满足"""
    s_name: str = None  # 状态名
    AP: List[str] = None  # 该状态所要满足的原子命题

    def __init__(self, s_name_: str, AP_: List[str]):
        """构造器：状态名，原子命题"""
        self.s_name = s_name_
        self.AP = AP_

    def __str__(self):
        """转为字符串表示，如：select,nsoda>0,nbeer>0"""
        if len(self.AP) == 0:
            return self.s_name
        return self.s_name + ',' + ','.join(self.AP)

    def to_list(self) -> List[str]:
        """转为list表示，如：[select,nsoda>0,nbeer>0]"""
        ret: List[str] = [self.s_name]
        ret.extend(self.AP)
        return ret


class TransitionSystem:
    """Transition System"""
    states: List[State] = None
    actions: Set[str] = None
    transitions: List[Transition] = None
    initial_states: List[State] = None
    atomic_propositions: Set[str] = None
    labels: List[Label] = None
    phi: Set[str] = None

    def __init__(self,  # act和ap用set表示，里面的元素不需要重复
                 s_: List[State] = None,
                 act_: Set[str] = None,
                 trans_: List[Transition] = None,
                 is_: List[State] = None,
                 ap_: Set[str] = None,
                 l_: List[Label] = None,
                 phi_: Set[str] = None):

        self.states = s_ if s_ is not None else list()
        self.actions = act_ if act_ is not None else set()
        self.transitions = trans_ if trans_ is not None else list()
        self.initial_states = is_ if is_ is not None else list()
        self.atomic_propositions = ap_ if ap_ is not None else set()
        self.labels = l_ if l_ is not None else list()
        self.phi = phi_ if phi is not None else set()

    def to_dict(self):
        """转为字典"""
        return {
            'S': [str(s) for s in self.states],
            'Act': list(self.actions),
            'Trans': [str(t) for t in self.transitions],
            'I': [str(i) for i in self.initial_states],
            'AP': list(self.atomic_propositions),
            'L': [l.to_list() for l in self.labels],
            'PHI': set(self.phi)
        }

def read_ts_from_json(file_path: str) -> TransitionSystem:
    """读入Transition System中的文件
    :param file_path: 文件路径
    """
    with open(file_path, encoding='utf-8') as f:
        ok = json.load(f)
    return TransitionSystem(ok['S'], ok['Act'], ok['Trans'], ok['I'], ok['AP'], ok['L'], ok['PHI'])