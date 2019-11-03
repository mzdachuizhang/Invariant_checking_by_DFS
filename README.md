# Invariant_checking_by_DFS



## Safety properties

安全属性（safety properties）通常意味着没有坏情况（bad situation）发生，那么什么是bad situation呢？

举两个典型的例子：

1. 互斥问题（两个及以上进程**不可以**同时访问临界资源）
2. 死锁问题（哲学家吃饭：不允许所有的哲学家都在等，至少有一个哲学家在吃饭）

以上两个问题，都需要满足括弧内的属性，才能叫做是安全的。



## Invariants

事实上，安全属性只是不变量形式的一种特例，什么是不变量（Invariants）呢？不变量归根结底还是LT properties。

首先我们先回顾一下什么是 LT properties，它是traces的集合，用P表示，本质是对字（也叫words，形式A0A1...）进行约束。如果Ai（i>=0）它们满足condition fi，这就完成了一个（P inv）的定义。

对于Pinv，它有这样的性质：

**若TS满足于Pinv，当且仅当**

- TS中任意path所构成的trace都是P的元素。
- TS中path的任意状态的label function都满足condition fi。
- TS中任意可达状态的label function都满足condtion fi。



## Example

1. 临界资源（fi=~crit1 or ~crit2）
2. 哲学家死锁（~wait0 or ~wait1 or ~wait2 or ~wait3 or ~wait4）

当然，首先假设TS是有限的，仅需使用DFS或者BFS对TS构成的图进行遍历即可。


### DFS 伪代码
``` python
# Input: finite TS and condition fi
# Output: yes(TS satisfies fi) or no + counterexample

set of states R:= null
stack of states U:= null
bool b:=true
while(I (not in R and not null) and b)
    let s in I not in R
    visit s

if b then 
    return "yes"
else 
    return "no" reverse(U)
fi

procedure visit(state s)
    push s,U
    R:=R v {s}
    repeat
        s':=top(U)
        if Post(s') in R then
            pop(U)
            b:=b + (s' satisfies fi)
        else
            let s'' in Post(s')\R
            push s'',U
            R:=R + {s''}
        fi
      until((U=null) v ~b)
endproc
```

## 解决思路

1. ts.json  ->  class TS，见```ts.py```文件.
2. class TS  ->  class Graph，见```ts2gh.py```文件.
3. phy.json  ->  class PHY，见```phy.py```文件.
4. class Graph + class PHY  ->  dfs，见```dfs.py```文件.

**样例输入**
- ts_mutex.json
- ts_deadlock.json
- phy.json

## 优点：

1. 对于任意类型的TS数据，以标准json文件格式化作为输入，即可处理。格式见文档末。
2. 条件condition支持在AP集合上的一元运算符not，以及二元运算符and与or，和括弧，括弧优先级覆盖。





