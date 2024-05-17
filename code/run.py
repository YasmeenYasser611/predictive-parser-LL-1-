import networkx as nx
import matplotlib.pyplot as plt
from tokenizer import Tokenizer
from parser_f import *

def tokenize():
    # Tokenize the file content
    file_content = ""
    with open("input_source.txt", 'r') as file:
        for line in file:
            file_content += line
        file.close()

    token_iter = Tokenizer.token_iter(file_content)
    
    # Parse the tokens
    psr = Parser(token_iter)
    psr.parse()
    

    # Get the parse tree
    parse_tree = psr.get_parse_tree()

    # Draw the parse tree
    plt.figure(figsize=(10, 8))

    # Create a layout for the tree
    pos = hierarchy_pos(parse_tree, root=next(iter(parse_tree.nodes)), width=3., vert_gap=0.3, vert_loc=0.)

    # Draw nodes and edges
    node_labels = nx.get_node_attributes(parse_tree, 'label')
    nx.draw_networkx_nodes(parse_tree, pos=pos, nodelist=pos.keys(), node_size=500, node_color='skyblue')
    nx.draw_networkx_edges(parse_tree, pos=pos)

    # Draw labels only for nodes with positions
    for node, position in pos.items():
        if node in node_labels:
            plt.text(position[0], position[1], node_labels[node], horizontalalignment='center', fontsize=7)

    # Show the plot
    plt.title("Parse Tree")
    plt.axis('off')  # Hide axes
    plt.show()

def hierarchy_pos(G, root=None, width=10., vert_gap=0.8, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=10, vert_gap=0.8, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    if len(children) != 0:
        dx = width / (len(children))
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                  pos=pos, parent=root, parsed=parsed)
    return pos

if __name__ == '__main__':
    #filename = 'text3.txt'  # Change this to the path of your input file
    tokenize()
