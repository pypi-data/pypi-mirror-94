import collections


__NODECACHE__ = dict()


def get_nodes_from_root(root, memoize=False):
    """Returns the root and all its predecessors in the graph.

    Defines a BFS order on the compute graph of blocks.

    *Args:*

    + `root (Block)`: the root of the STS graph
    + `memoize (bool)`: potential speedup in return for static sts graph
        assumption

    *Returns:*

    + `nodes (tuple[list])`: root and predecessor nodes in the graph
    """
    if memoize and root in __NODECACHE__.keys():
        return __NODECACHE__[root]
    deque = collections.deque()
    nodes = list()
    visited = set()

    prec = root.prec()
    nodes.append(root)
    visited.add(root)

    for element in prec:
        deque.append(element)

    while deque:
        this_node = deque.popleft()
        if this_node not in visited:
            nodes.append(this_node)
            visited.add(this_node)
            prec = this_node.prec()

            for element in prec:
                deque.append(element)
        else:
            continue
    if memoize:
        __NODECACHE__[root] = nodes
    return nodes


def get_graph_from_root(root):
    """Returns the compute graph with `root` as the single base node.

    *Args:*

    + `root (Block)`: the root of the STS graph

    *Returns:*

    + `graph (dict[list[Block...]])`: {node, [predecessor nodes]}
    """
    deque = collections.deque()
    graph = dict()
    visited = set()

    prec = root.prec()
    graph[root.name] = list()
    visited.add(root)

    for element in prec:
        deque.append(element)
        graph[root.name].append(element.name)

    while deque:
        this_node = deque.popleft()
        if this_node not in visited:
            graph[this_node.name] = list()
            visited.add(this_node)
            prec = this_node.prec()

            for element in prec:
                deque.append(element)
                graph[this_node.name].append(element.name)
        else:
            continue

    return graph


def get_name2block_from_root(root):
    """Gets a `{name: block}` dict starting from the passed root node.

    *Args:*

    + `root (Block)`: the root node

    *Returns:*

    `graph (dict)`: a dict with structure `{name : block}`
    """
    deque = collections.deque()
    graph = dict()
    visited = set()

    prec = root.prec()
    graph[root.name] = root
    visited.add(root)

    for element in prec:
        deque.append(element)

    while deque:
        this_node = deque.popleft()
        if this_node not in visited:
            graph[this_node.name] = this_node
            visited.add(this_node)
            prec = this_node.prec()

            for element in prec:
                deque.append(element)
        else:
            continue

    return graph


def set_cache_mode(root, cache, memoize=True):
    """
    Sets root and all predecessor nodes cache mode to `cache`.

    *Args:*

    + `root (Block)`: a block
    + `cache (bool)`: whether or not to cache block calls
    + `memoize (bool)`: potential speedup in return for static sts graph
        assumption
    """
    nodes = get_nodes_from_root(root, memoize=memoize)
    for node in nodes:
        node.is_cached = cache


def clear_cache(root, memoize=True):
    """
    Clears cache of all predecessor nodes of root.
    This does *not* reset the cache mode of any node;
    to turn off caching, call `set_cache_mode(root, False)`

    *Args:*

    + `root (Block)`: a block
    + `memoize (bool)`: potential speedup in return for static sts graph
        assumption
    """
    nodes = get_nodes_from_root(root, memoize=memoize)
    for node in nodes:
        node.clear_cache()
