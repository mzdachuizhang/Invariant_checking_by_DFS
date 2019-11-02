from typing import List, Dict, Set
from transition_system import TransitionSystem, State, Transition, Label

class Vertex:
    """顶点类
    用状态、状态中所含的变量及值、状态所含的原子命题及label_function组成
    """
    def __init__(self, state: State, labels: Label):
        self.s_name = state.s_name      #节点名称
        self.val_var = state.val_var    #节点中的变量信息
        self.labels = labels.AP  #节点中应该满足的原子命题（Label functions）
        self.connectedTo = {}

    def __str__(self):
        """转为字符串表示：如<start,nsoda=1∧nbeer=1,(nsoda>0,nbeer>0)>"""
        return "<" + self.s_name + "," \
               + "∧".join([k + "=" + str(v) for k, v in self.val_var.items()]) \
               + ",(" + ",".join(self.labels) + ")>"

    # 从这个顶点添加一个连接到另一个，再添加action
    def addNeighbor(self, nbr, action: Transition.act):
        self.connectedTo[nbr] = action

    # 返回邻接表中的所有的项点
    def getConnections(self):
        return self.connectedTo.keys()

    def getstatename(self):
        return self.s_name

    def getvalue(self):
        return self.val_var

    def getlabel(self):
        return self.labels

    # # 返回从这个顶点到作为参数顶点的边的权重
    # def getweight(self, nbr):
    #     return self.connectedTo[nbr]

class Graph:
    """
    用邻接表来表示图
    """
    def __init__(self):
        self.vertList = {}  # 表中的顶点，用字典表示
        self.numVertices = 0    # 顶点数，初始化为0

    def addVertex(self, state, labels): # 添加顶点
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(state,labels)
        self.vertList[state] = newVertex
        return newVertex

    def getVertex(self, state):
        if state in self.vertList:
            return self.vertList[state]
        else:
            return None

    def __contains__(self, state):
        return state in self.vertList

    def addEdge(self, f, t, action):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], action)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

if __name__ == '__main__':
    g = Graph()
    TransitionSystem.states
    s1 = Stat"<start,nsoda=2∧nbeer=2,(nsoda>0,nbeer>0)>"
    g.addVertex("<start,nsoda=2∧nbeer=2,(nsoda>0,nbeer>0)>")
    # g.addEdge("<start,nsoda=2∧nbeer=2,(nsoda>0,nbeer>0)>","<select,nsoda=2∧nbeer=2,(nsoda>0,nbeer>0)>","coin")