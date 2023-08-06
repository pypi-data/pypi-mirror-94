class _DoublyLinkedBase:
  """该类提供了双向链表的基础"""

  #-------------------------- 嵌套节点类 --------------------------
  
  class _Node:
    """用于存储双链接节点的一个简单的私有类"""

    def __init__(self, element, prev, next):     
      """创建一个新节点"""       
      self._element = element                           # 节点元素
      self._prev = prev                                 # 上一个节点引用
      self._next = next                                 # 下一个节点引用

  #-------------------------- 链表构造函数 --------------------------

  def __init__(self):                                   
    """创建一个空链表"""
    self._header = self._Node(None, None, None)
    self._trailer = self._Node(None, None, None)
    self._header._next = self._trailer                  # 尾节点在头节点后面
    self._trailer._prev = self._header                  # 头节点在尾节点后面
    self._size = 0                                      # 元素个数

  #-------------------------- 公有的访问方法 --------------------------

  def __len__(self):
    """返回链表中的元素数"""
    return self._size

  def is_empty(self):
    """返回链表是否为空的真值"""
    return self._size == 0

  #-------------------------- 私有的改变链表结构的方法 --------------------------

  def _insert_between(self, e, predecessor, successor):
    """在两个现有节点之间添加元素e并返回新节点"""
    newest = self._Node(e, predecessor, successor)      # 链接至相邻节点
    predecessor._next = newest
    successor._prev = newest
    self._size += 1
    return newest

  def _delete_node(self, node):
    """从列表中删除节点（非头尾节点）并返回其元素"""
    predecessor = node._prev
    successor = node._next
    predecessor._next = successor
    successor._prev = predecessor
    self._size -= 1
    element = node._element                             # 记录被删除的元素
    node._prev = node._next = node._element = None      # 弃用节点
    return element                                      # 返回被删除的元素


class PositionalList(_DoublyLinkedBase):
  """允许位置存取元素的顺序容器--基于双向链表"""

  #-------------------------- 嵌套位置类 --------------------------

  class Position:
    """判断位置是否一致时，用 "==" 而不是 "is" """

    def __init__(self, container, node):
      """用户不应调用构造函数"""
      self._container = container
      self._node = node

    def element(self):
      """返回存储在此位置的元素"""
      return self._node._element

    def __eq__(self, other):
      """返回self与other位置是否一致的真值"""
      return type(other) is type(self) and other._node is self._node

  #------------------------------- 私有的获取位置的方法 -------------------------------

  def _validate(self, p):
    """返回相应位置的节点，如果无效则引发相应的错误"""
    if not isinstance(p, self.Position):
      raise TypeError('p 必须是正确的位置Position类型')
    if p._container is not self:
      raise ValueError('p 不属于当前这个容器')
    if p._node._next is None:    
      raise ValueError('p 已失效')
    return p._node

  def _make_position(self, node):
    """返回给定节点的位置实例（如果属于头尾节点，则返回None）"""
    if node is self._header or node is self._trailer:
      return None                              # 边界冲突
    else:
      return self.Position(self, node)         # 合法位置

  #------------------------------- 公有的访问方法 -------------------------------

  def first(self):
    """返回列表中的第一个位置（如果列表为空，则返回None）"""
    return self._make_position(self._header._next)

  def last(self):
    """返回列表中的最后一个位置（如果列表为空，则返回None）"""
    return self._make_position(self._trailer._prev)

  def before(self, p):
    """返回位置p之前的位置（如果p是第一个，则返回None）。"""
    node = self._validate(p)
    return self._make_position(node._prev)

  def after(self, p):
    """返回位置p之后的位置（如果p是最后一个，则返回None）"""
    node = self._validate(p)
    return self._make_position(node._next)

  def __iter__(self):
    """一个迭代器，正向生成列表元素"""
    cursor = self.first()
    while cursor is not None:
      yield cursor.element()
      cursor = self.after(cursor)

  #------------------------------- 增删改等方法 -------------------------------

  # 因为需要返回位置，而不是节点，故重写insert函数
  def _insert_between(self, e, predecessor, successor):
    """在现有节点之间添加元素并返回新位置"""
    node = super()._insert_between(e, predecessor, successor)
    return self._make_position(node)

  def add_first(self, e):
    """在链表前面插入元素e并返回新位置"""
    return self._insert_between(e, self._header, self._header._next)

  def add_last(self, e):
    """在链表后面插入元素e并返回新位置"""
    return self._insert_between(e, self._trailer._prev, self._trailer)

  def add_before(self, p, e):
    """将元素e插入链表中p所在位置之前并返回新位置"""
    original = self._validate(p)
    return self._insert_between(e, original._prev, original)

  def add_after(self, p, e):
    """将元素e插入链表中p所在位置之后并返回新位置"""
    original = self._validate(p)
    return self._insert_between(e, original, original._next)

  def delete(self, p):
    """删除并返回p所在位置的元素"""
    original = self._validate(p)
    return self._delete_node(original)  # 用继承的方法返回元素

  def replace(self, p, e):
    """将位置p处的元素更换为e，返回位置p原来的元素"""
    original = self._validate(p)
    old_value = original._element       # 临时存储旧元素
    original._element = e               # 替换为新元素
    return old_value                    # 返回旧元素值
