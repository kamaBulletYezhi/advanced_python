import ast
import matplotlib
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from matplotlib import pyplot as plt
matplotlib.use("Agg")


class MyVisitor:
    """
    Моего интеллекта не хватило на то,
    что бы понять,
    как корректно унаследоваться от ast.NodeVisitor,
    поэтому родилось данное чудовище.

    Attributes
    ----------
    G: nx.Graph
        граф для дальнейшей отрисовки
    num: int
        уникальный id вершин из G
        нужен для создания G
    labels: dict[num: int, descr: str]
        descr --- строка с описанием вершины num из G

    """

    def __init__(self):
        self.G = nx.Graph()
        # фиктивная вершина что бы не ломать метод MyVisitor.visit
        self.G.add_node(
            0,
            node_type="Skript",
            layer=0
        )
        self.num = 0
        self.labels = {}
        self.color_map = {}

    def visit(self, node: ast.AST, parent: int):
        self.num += 1
        node_num = self.num
        node_name = type(node).__name__  # вроде приемлимо смотрится
        curr_color = 0.5

        if isinstance(node, (ast.Load, ast.Store, ast.Del)):
            return
        if isinstance(node, ast.BinOp):
            node_name += ':\n' + type(node.op).__name__
        elif isinstance(node, ast.Constant):
            curr_color = 0.33
            node_name = 'const:\n' + (f"'{node.value}'"
                                      if type(node.value) is str
                                      else str(node.value))
        elif isinstance(node, ast.Name):
            curr_color = 0.66
            node_name = f"name:\n'{node.id}'"
        elif isinstance(node, ast.Compare):
            curr_color = 0.9
            node_name += ":\n" + "'" + \
                         "' '".join(type(a).__name__ for a in node.ops) + "'"

        if isinstance(node, ast.FormattedValue):
            # строка type(node).__name__ не вмещается в квадрат узла
            node_name = "FormatVal"

        self.color_map[node_num] = curr_color
        self.labels[node_num] = node_name
        node_layer = self.G.nodes[parent]["layer"] + 1

        self.G.add_node(
            node_num,
            node_type=node_name,
            layer=node_layer
        )
        self.G.add_edge(
            parent,
            node_num,
        )
        for child in ast.iter_child_nodes(node):
            self.visit(child, node_num)


def main(file_name):
    with open(file_name) as file:
        func_ast_obj = ast.parse(file.read()).body[0]

    # проходимся DFS и строим граф G
    my_vis = MyVisitor()
    my_vis.visit(func_ast_obj, 0)
    G = my_vis.G
    # удаляем фиктивную вершину
    G.remove_node(0)

    labels = my_vis.labels
    colors = [my_vis.color_map[node] for node in G.nodes()]
    pos = graphviz_layout(G, prog="dot")

    fig = plt.figure(figsize=(70, 50))

    nx.draw_networkx(
        G,
        pos=pos,
        node_shape="s",
        node_size=14000,
        width=2,
        arrowsize=25,
        # node_color="white",
        font_size=17,
        labels=labels,
        with_labels=True,
        arrows=True,
        cmap=plt.get_cmap('plasma'),
        node_color=colors,
        ax=fig.add_subplot()
    )
    fig.savefig("artifacts/graph.png")


if __name__ == "__main__":
    main("easy.py")
