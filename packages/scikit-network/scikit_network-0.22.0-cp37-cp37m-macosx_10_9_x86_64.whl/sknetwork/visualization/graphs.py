#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on April 2020
@authors:
Thomas Bonald <bonald@enst.fr>
Quentin Lutz <qlutz@enst.fr>
"""
from typing import Optional, Iterable, Union, Tuple

import numpy as np
from scipy import sparse

from sknetwork.clustering.louvain import BiLouvain
from sknetwork.embedding.spring import Spring
from sknetwork.visualization.colors import STANDARD_COLORS, COOLWARM_RGB


def min_max_scaling(x: np.ndarray, x_min: Optional[float] = None, x_max: Optional[float] = None) -> np.ndarray:
    """Shift and scale vector to be between 0 and 1."""
    x = x.astype(float)
    if x_min is None:
        x_min = np.min(x)
    if x_max is None:
        x_max = np.max(x)
    x -= x_min
    if x_max > x_min:
        x /= (x_max - x_min)
    else:
        x = .5 * np.ones_like(x)
    return x


def rescale(position: np.ndarray, width: float, height: float, margin: float, node_size: float, node_size_max: float,
            display_node_weight: bool):
    """Rescale position and adjust parameters.

    Parameters
    ----------
    position :
        array to rescale
    width :
        Horizontal scaling parameter
    height :
        Vertical scaling parameter
    margin :
        Minimal margin for the plot
    node_size :
        Node size (used to adapt the margin)
    node_size_max :
        Maximum node size (used to adapt the margin)
    display_node_weight :
        If ``True``, display node weight (used to adapt the margin)

    Returns
    -------
    position :
        Rescaled positions
    width :
        Rescaled width
    height :
        Rescaled height
    """
    x = position[:, 0]
    y = position[:, 1]
    span_x = np.max(x) - np.min(x)
    span_y = np.max(y) - np.min(y)
    x = min_max_scaling(x)
    y = 1 - min_max_scaling(y)
    position = np.vstack((x, y)).T

    # rescale
    if width and not height:
        height = width
        if span_x and span_y:
            height *= span_y / span_x
    elif height and not width:
        width = height
        if span_x and span_y:
            width *= span_x / span_y

    position = position * np.array([width, height])

    # margins
    margin = max(margin, node_size_max * display_node_weight, node_size)
    position += margin
    width += 2 * margin
    height += 2 * margin
    return position, width, height


def get_label_colors(label_colors: Optional[Iterable]):
    """Return label svg colors.

    Examples
    --------
    >>> get_label_colors(['black'])
    array(['black'], dtype='<U5')
    >>> get_label_colors({0: 'blue'})
    array(['blue'], dtype='<U64')
    """
    if label_colors is not None:
        if isinstance(label_colors, dict):
            keys = list(label_colors.keys())
            values = list(label_colors.values())
            label_colors = np.array(['black'] * (max(keys) + 1), dtype='U64')
            label_colors[keys] = values
        elif isinstance(label_colors, list):
            label_colors = np.array(label_colors)
    else:
        label_colors = STANDARD_COLORS.copy()
    return label_colors


def get_node_colors(n: int, labels: Optional[Iterable], scores: Optional[Iterable],
                    membership: Optional[sparse.csr_matrix],
                    node_color: str, label_colors: Optional[Iterable],
                    score_min: Optional[float] = None, score_max: Optional[float] = None) -> np.ndarray:
    """Return the colors of the nodes using either labels or scores or default color."""
    node_colors = np.array(n * [node_color]).astype('U64')
    if labels is not None:
        if isinstance(labels, dict):
            keys = np.array(list(labels.keys()))
            values = np.array(list(labels.values())).astype(int)
            labels = -np.ones(n, dtype=int)
            labels[keys] = values
        elif isinstance(labels, list):
            if len(labels) != n:
                raise ValueError("The number of labels must be equal to the corresponding number of nodes.")
            else:
                labels = np.array(labels)
        index = labels >= 0
        label_colors = get_label_colors(label_colors)
        node_colors[index] = label_colors[labels[index] % len(label_colors)]
    elif scores is not None:
        colors_score = COOLWARM_RGB.copy()
        n_colors = colors_score.shape[0]
        colors_score_svg = np.array(['rgb' + str(tuple(colors_score[i])) for i in range(n_colors)])
        if isinstance(scores, dict):
            keys = np.array(list(scores.keys()))
            values = np.array(list(scores.values()))
            scores = (min_max_scaling(values, score_min, score_max) * (n_colors - 1)).astype(int)
            node_colors[keys] = colors_score_svg[scores]
        else:
            if isinstance(scores, list):
                if len(scores) != n:
                    raise ValueError("The number of scores must be equal to the corresponding number of nodes.")
                else:
                    scores = np.array(scores)
            scores = (min_max_scaling(scores, score_min, score_max) * (n_colors - 1)).astype(int)
            node_colors = colors_score_svg[scores]
    elif membership is not None:
        if isinstance(label_colors, dict):
            raise TypeError("Label colors must be a list or an array when using a membership.")
        label_colors = get_label_colors(label_colors)
        node_colors = label_colors
    return node_colors


def get_node_widths(n: int, seeds: Union[int, dict, list], node_width: float, node_width_max: float) -> np.ndarray:
    """Return the node widths."""
    node_widths = node_width * np.ones(n)
    if seeds is not None:
        if type(seeds) == dict:
            seeds = list(seeds.keys())
        elif np.issubdtype(type(seeds), np.integer):
            seeds = [seeds]
        if len(seeds):
            node_widths[np.array(seeds)] = node_width_max
    return node_widths


def get_node_sizes(weights: np.ndarray, node_size: float, node_size_min: float, node_size_max: float, node_weight) \
        -> np.ndarray:
    """Return the node sizes."""
    if node_weight and np.min(weights) < np.max(weights):
        node_sizes = node_size_min + np.abs(node_size_max - node_size_min) * weights / np.max(weights)
    else:
        node_sizes = node_size * np.ones_like(weights)
    return node_sizes


def get_node_sizes_bipartite(weights_row: np.ndarray, weights_col: np.ndarray, node_size: float, node_size_min: float,
                             node_size_max: float, node_weight) -> (np.ndarray, np.ndarray):
    """Return the node sizes for bipartite graphs."""
    weights = np.hstack((weights_row, weights_col))
    if node_weight and np.min(weights) < np.max(weights):
        node_sizes_row = node_size_min + np.abs(node_size_max - node_size_min) * weights_row / np.max(weights)
        node_sizes_col = node_size_min + np.abs(node_size_max - node_size_min) * weights_col / np.max(weights)
    else:
        node_sizes_row = node_size * np.ones_like(weights_row)
        node_sizes_col = node_size * np.ones_like(weights_col)
    return node_sizes_row, node_sizes_col


def get_edge_colors(adjacency: sparse.csr_matrix, edge_labels: Optional[list], edge_color: str,
                    label_colors: Optional[Iterable]) -> Tuple[np.ndarray, np.ndarray, list]:
    """Return the edge colors."""
    n_row, n_col = adjacency.shape
    n_edges = adjacency.nnz
    adjacency_labels = (adjacency > 0).astype(int)
    adjacency_labels.data = -adjacency_labels.data
    edge_colors_residual = []
    if edge_labels:
        label_colors = get_label_colors(label_colors)
        for i, j, label in edge_labels:
            if i < 0 or i >= n_row or j < 0 or j >= n_col:
                raise ValueError('Invalid node index in edge labels.')
            if adjacency[i, j]:
                adjacency_labels[i, j] = label % len(label_colors)
            else:
                color = label_colors[label % len(label_colors)]
                edge_colors_residual.append((i, j, color))
    edge_order = np.argsort(adjacency_labels.data)
    edge_colors = np.array(n_edges * [edge_color]).astype('U64')
    index = np.argwhere(adjacency_labels.data >= 0).ravel()
    if len(index):
        edge_colors[index] = label_colors[adjacency_labels.data[index]]
    return edge_colors, edge_order, edge_colors_residual


def get_edge_widths(adjacency: sparse.coo_matrix, edge_width: float, edge_width_min: float, edge_width_max: float,
                    display_edge_weight: bool) -> np.ndarray:
    """Return the edge widths."""
    weights = adjacency.data
    edge_widths = None
    if len(weights):
        if display_edge_weight and np.min(weights) < np.max(weights):
            edge_widths = edge_width_min + np.abs(edge_width_max - edge_width_min) * (weights - np.min(weights))\
                          / (np.max(weights) - np.min(weights))
        else:
            edge_widths = edge_width * np.ones_like(weights)
    return edge_widths


def svg_node(pos_node: np.ndarray, size: float, color: str, stroke_width: float = 1, stroke_color: str = 'black') \
        -> str:
    """Return svg code for a node.

    Parameters
    ----------
    pos_node :
        (x, y) coordinates of the node.
    size :
        Radius of disk in pixels.
    color :
        Color of the disk in SVG valid format.
    stroke_width :
        Width of the contour of the disk in pixels, centered around the circle.
    stroke_color :
        Color of the contour in SVG valid format.

    Returns
    -------
    SVG code for the node.
    """
    x, y = pos_node.astype(int)
    return """<circle cx="{}" cy="{}" r="{}" style="fill:{};stroke:{};stroke-width:{}"/>\n"""\
        .format(x, y, size, color, stroke_color, stroke_width)


def svg_pie_chart_node(pos_node: np.ndarray, size: float, membership: np.ndarray, colors: np.ndarray,
                       stroke_width: float = 1, stroke_color: str = 'black') -> str:
    """Return svg code for a pie-chart node."""
    x, y = pos_node.astype(float)
    n_colors = len(colors)
    out = ""
    cumsum = np.zeros(membership.shape[1] + 1)
    cumsum[1:] = np.cumsum(membership)
    if cumsum[-1] == 0:
        return svg_node(pos_node, size, 'white', stroke_width=3)
    sum_membership = cumsum[-1]
    cumsum = np.multiply(cumsum, (2 * np.pi) / cumsum[-1])
    x_array = size * np.cos(cumsum) + x
    y_array = size * np.sin(cumsum) + y
    large = np.array(membership > sum_membership / 2).ravel()
    for index in range(membership.shape[1]):
        out += """<path d="M {} {} A {} {} 0 {} 1 {} {} L {} {}" style="fill:{};stroke:{};stroke-width:{}" />\n"""\
            .format(x_array[index], y_array[index], size, size, int(large[index]),
                    x_array[index + 1], y_array[index + 1], x, y, colors[index % n_colors], stroke_color, stroke_width)
    return out


def svg_edge(pos_1: np.ndarray, pos_2: np.ndarray, edge_width: float = 1, edge_color: str = 'black') -> str:
    """Return svg code for an edge."""
    x1, y1 = pos_1.astype(int)
    x2, y2 = pos_2.astype(int)
    return """<path stroke-width="{}" stroke="{}" d="M {} {} {} {}"/>\n"""\
        .format(edge_width, edge_color, x1, y1, x2, y2)


def svg_edge_directed(pos_1: np.ndarray, pos_2: np.ndarray, edge_width: float = 1, edge_color: str = 'black',
                      node_size: float = 1.) -> str:
    """Return svg code for a directed edge."""
    vec = pos_2 - pos_1
    norm = np.linalg.norm(vec)
    if norm:
        x, y = ((vec / norm) * node_size).astype(int)
        x1, y1 = pos_1.astype(int)
        x2, y2 = pos_2.astype(int)
        return """<path stroke-width="{}" stroke="{}" d="M {} {} {} {}" marker-end="url(#arrow)"/>\n"""\
            .format(edge_width, edge_color, x1, y1, x2 - x, y2 - y)
    else:
        return ""


def svg_text(pos, text, font_size=12, align_right=False):
    """Return svg code for text."""
    x, y = pos.astype(int)
    text = str(text).replace('&', ' ')
    if align_right:
        return """<text text-anchor="end" x="{}" y="{}" font-size="{}">{}</text>"""\
            .format(x, y, font_size, text)
    else:
        return """<text x="{}" y="{}" font-size="{}">{}</text>"""\
            .format(x, y, font_size, text)


def svg_graph(adjacency: Optional[sparse.csr_matrix] = None, position: Optional[np.ndarray] = None,
              names: Optional[np.ndarray] = None,
              labels: Optional[Iterable] = None, scores: Optional[Iterable] = None,
              membership: Optional[sparse.csr_matrix] = None,
              seeds: Union[list, dict] = None, width: Optional[float] = 400, height: Optional[float] = 300,
              margin: float = 20, margin_text: float = 3, scale: float = 1, node_order: Optional[np.ndarray] = None,
              node_size: float = 7, node_size_min: float = 1, node_size_max: float = 20,
              display_node_weight: bool = False, node_weights: Optional[np.ndarray] = None, node_width: float = 1,
              node_width_max: float = 3, node_color: str = 'gray',
              display_edges: bool = True, edge_labels: Optional[list] = None,
              edge_width: float = 1, edge_width_min: float = 0.5,
              edge_width_max: float = 20, display_edge_weight: bool = True,
              edge_color: Optional[str] = None, label_colors: Optional[Iterable] = None,
              font_size: int = 12, directed: bool = False, filename: Optional[str] = None) -> str:
    """Return SVG image of a graph.

    Parameters
    ----------
    adjacency :
        Adjacency matrix of the graph.
    position :
        Positions of the nodes.
    names :
        Names of the nodes.
    labels :
        Labels of the nodes (negative values mean no label).
    scores :
        Scores of the nodes (measure of importance).
    membership :
        Membership of the nodes (label distribution).
    seeds :
        Nodes to be highlighted (if dict, only keys are considered).
    width :
        Width of the image.
    height :
        Height of the image.
    margin :
        Margin of the image.
    margin_text :
        Margin between node and text.
    scale :
        Multiplicative factor on the dimensions of the image.
    node_order :
        Order in which nodes are displayed.
    node_size :
        Size of nodes.
    node_size_min :
        Minimum size of a node.
    node_size_max:
        Maximum size of a node.
    node_width :
        Width of node circle.
    node_width_max :
        Maximum width of node circle.
    node_color :
        Default color of nodes (svg color).
    display_node_weight :
        If ``True``, display node weights through node size.
    node_weights :
        Node weights (used only if **display_node_weight** is ``True``).
    display_edges :
        If ``True``, display edges.
    edge_labels :
        Labels of the edges, as a list of tuples (source, destination, label)
    edge_width :
        Width of edges.
    edge_width_min :
        Minimum width of edges.
    edge_width_max :
        Maximum width of edges.
    display_edge_weight :
        If ``True``, display edge weights through edge widths.
    edge_color :
        Default color of edges (svg color).
    label_colors:
        Colors of the labels (svg colors).
    font_size :
        Font size.
    directed :
        If ``True``, considers the graph as directed.
    filename :
        Filename for saving image (optional).

    Returns
    -------
    image : str
        SVG image.

    Example
    -------
    >>> from sknetwork.data import karate_club
    >>> graph = karate_club(True)
    >>> adjacency = graph.adjacency
    >>> position = graph.position
    >>> from sknetwork.visualization import svg_graph
    >>> image = svg_graph(adjacency, position)
    >>> image[1:4]
    'svg'
    """
    # check adjacency
    if adjacency is None:
        if position is None:
            raise ValueError("You must specify either adjacency or position.")
        else:
            n = position.shape[0]
            adjacency = sparse.csr_matrix((n, n)).astype(int)
    else:
        n = adjacency.shape[0]

    # node order
    if node_order is None:
        node_order = np.arange(n)

    # position
    if position is None:
        spring = Spring()
        position = spring.fit_transform(adjacency)

    # node colors
    node_colors = get_node_colors(n, labels, scores, membership, node_color, label_colors)

    # node sizes
    if node_weights is None:
        node_weights = adjacency.T.dot(np.ones(n))
    node_sizes = get_node_sizes(node_weights, node_size, node_size_min, node_size_max, display_node_weight)

    # node widths
    node_widths = get_node_widths(n, seeds, node_width, node_width_max)

    # rescaling
    position, width, height = rescale(position, width, height, margin, node_size, node_size_max, display_node_weight)

    if names is not None:
        text_length = np.max(np.array([len(str(name)) for name in names]))
        width += text_length * font_size * .5

    # scaling
    position *= scale
    height *= scale
    width *= scale

    svg = """<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n""".format(width, height)

    # edges
    if display_edges:
        adjacency_coo = sparse.coo_matrix(adjacency)

        if edge_color is None:
            if names is None:
                edge_color = 'black'
            else:
                edge_color = 'gray'

        if directed:
            svg += """<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" >\n"""
            svg += """<path d="M0,0 L0,6 L9,3 z" fill="{}"/></marker></defs>\n""".format(edge_color)

        edge_colors, edge_order, edge_colors_residual = get_edge_colors(adjacency, edge_labels, edge_color,
                                                                        label_colors)
        edge_widths = get_edge_widths(adjacency_coo, edge_width, edge_width_min, edge_width_max, display_edge_weight)

        for ix in edge_order:
            i = adjacency_coo.row[ix]
            j = adjacency_coo.col[ix]
            color = edge_colors[ix]
            if directed:
                svg += svg_edge_directed(pos_1=position[i], pos_2=position[j], edge_width=edge_widths[ix],
                                         edge_color=color, node_size=node_sizes[j])
            else:
                svg += svg_edge(pos_1=position[i], pos_2=position[j],
                                edge_width=edge_widths[ix], edge_color=color)

        for i, j, color in edge_colors_residual:
            if directed:
                svg += svg_edge_directed(pos_1=position[i], pos_2=position[j], edge_width=edge_width,
                                         edge_color=color, node_size=node_sizes[j])
            else:
                svg += svg_edge(pos_1=position[i], pos_2=position[j],
                                edge_width=edge_width, edge_color=color)

    # nodes
    for i in node_order:
        if membership is None:
            svg += svg_node(position[i], node_sizes[i], node_colors[i], node_widths[i])
        else:
            if membership[i].nnz == 1:
                index = membership[i].indices[0]
                svg += svg_node(position[i], node_sizes[i], node_colors[index], node_widths[i])
            else:
                svg += svg_pie_chart_node(position[i], node_sizes[i], membership[i].todense(),
                                          node_colors, node_widths[i])

    # text
    if names is not None:
        for i in range(n):
            svg += svg_text(position[i] + node_sizes[i] + (margin_text, 0), names[i], font_size)
    svg += """</svg>\n"""

    if filename is not None:
        with open(filename + '.svg', 'w') as f:
            f.write(svg)

    return svg


def svg_digraph(adjacency: Optional[sparse.csr_matrix] = None, position: Optional[np.ndarray] = None,
                names: Optional[np.ndarray] = None,
                labels: Optional[Iterable] = None, scores: Optional[Iterable] = None,
                membership: Optional[sparse.csr_matrix] = None,
                seeds: Union[list, dict] = None, width: Optional[float] = 400, height: Optional[float] = 300,
                margin: float = 20, margin_text: float = 10, scale: float = 1, node_order: Optional[np.ndarray] = None,
                node_size: float = 7, node_size_min: float = 1, node_size_max: float = 20,
                display_node_weight: bool = False, node_weights: Optional[np.ndarray] = None, node_width: float = 1,
                node_width_max: float = 3, node_color: str = 'gray',
                display_edges: bool = True, edge_labels: Optional[list] = None,
                edge_width: float = 1, edge_width_min: float = 0.5,
                edge_width_max: float = 5, display_edge_weight: bool = True,
                edge_color: Optional[str] = None, label_colors: Optional[Iterable] = None,
                font_size: int = 12, filename: Optional[str] = None) -> str:
    """Return SVG image of a digraph.

    Parameters
    ----------
    adjacency :
        Adjacency matrix of the graph.
    position :
        Positions of the nodes.
    names :
        Names of the nodes.
    labels :
        Labels of the nodes (negative values mean no label).
    scores :
        Scores of the nodes (measure of importance).
    membership :
        Membership of the nodes (label distribution).
    seeds :
        Nodes to be highlighted (if dict, only keys are considered).
    width :
        Width of the image.
    height :
        Height of the image.
    margin :
        Margin of the image.
    margin_text :
        Margin between node and text.
    scale :
        Multiplicative factor on the dimensions of the image.
    node_order :
        Order in which nodes are displayed.
    node_size :
        Size of nodes.
    node_size_min :
        Minimum size of a node.
    node_size_max :
        Maximum size of a node.
    display_node_weight :
        If ``True``, display node in-weights through node size.
    node_weights :
        Node weights (used only if **display_node_weight** is ``True``).
    node_width :
        Width of node circle.
    node_width_max :
        Maximum width of node circle.
    node_color :
        Default color of nodes (svg color).
    display_edges :
        If ``True``, display edges.
    edge_labels :
        Labels of the edges, as a list of tuples (source, destination, label)
    edge_width :
        Width of edges.
    edge_width_min :
        Minimum width of edges.
    edge_width_max :
        Maximum width of edges.
    display_edge_weight :
        If ``True``, display edge weights through edge widths.
    edge_color :
        Default color of edges (svg color).
    label_colors :
        Colors of the labels (svg color).
    font_size :
        Font size.
    filename :
        Filename for saving image (optional).

    Returns
    -------
    image : str
        SVG image.

    Example
    -------
    >>> from sknetwork.data import painters
    >>> graph = painters(True)
    >>> adjacency = graph.adjacency
    >>> position = graph.position
    >>> from sknetwork.visualization import svg_digraph
    >>> image = svg_graph(adjacency, position)
    >>> image[1:4]
    'svg'
    """
    return svg_graph(adjacency=adjacency, position=position, names=names, labels=labels, scores=scores,
                     membership=membership, seeds=seeds, width=width, height=height, margin=margin,
                     margin_text=margin_text, scale=scale, node_order=node_order, node_size=node_size,
                     node_size_min=node_size_min, node_size_max=node_size_max, display_node_weight=display_node_weight,
                     node_weights=node_weights, node_width=node_width, node_width_max=node_width_max,
                     node_color=node_color, display_edges=display_edges, edge_labels=edge_labels,
                     edge_width=edge_width, edge_width_min=edge_width_min, edge_width_max=edge_width_max,
                     display_edge_weight=display_edge_weight, edge_color=edge_color, label_colors=label_colors,
                     font_size=font_size, directed=True, filename=filename)


def svg_bigraph(biadjacency: sparse.csr_matrix,
                names_row: Optional[np.ndarray] = None, names_col: Optional[np.ndarray] = None,
                labels_row: Optional[Union[dict, np.ndarray]] = None,
                labels_col: Optional[Union[dict, np.ndarray]] = None,
                scores_row: Optional[Union[dict, np.ndarray]] = None,
                scores_col: Optional[Union[dict, np.ndarray]] = None,
                membership_row: Optional[sparse.csr_matrix] = None,
                membership_col: Optional[sparse.csr_matrix] = None,
                seeds_row: Union[list, dict] = None, seeds_col: Union[list, dict] = None,
                position_row: Optional[np.ndarray] = None, position_col: Optional[np.ndarray] = None,
                reorder: bool = True, width: Optional[float] = 400,
                height: Optional[float] = 300, margin: float = 20, margin_text: float = 3, scale: float = 1,
                node_size: float = 7, node_size_min: float = 1, node_size_max: float = 20,
                display_node_weight: bool = False,
                node_weights_row: Optional[np.ndarray] = None, node_weights_col: Optional[np.ndarray] = None,
                node_width: float = 1, node_width_max: float = 3,
                color_row: str = 'gray', color_col: str = 'gray', label_colors: Optional[Iterable] = None,
                display_edges: bool = True, edge_labels: Optional[list] = None, edge_width: float = 1,
                edge_width_min: float = 0.5, edge_width_max: float = 10, edge_color: str = 'black',
                display_edge_weight: bool = True,
                font_size: int = 12, filename: Optional[str] = None) -> str:
    """Return SVG image of a bigraph.

    Parameters
    ----------
    biadjacency :
        Biadjacency matrix of the graph.
    names_row :
        Names of the rows.
    names_col :
        Names of the columns.
    labels_row :
        Labels of the rows (negative values mean no label).
    labels_col :
        Labels of the columns (negative values mean no label).
    scores_row :
        Scores of the rows (measure of importance).
    scores_col :
        Scores of the columns (measure of importance).
    membership_row :
        Membership of the rows (label distribution).
    membership_col :
        Membership of the columns (label distribution).
    seeds_row :
        Rows to be highlighted (if dict, only keys are considered).
    seeds_col :
        Columns to be highlighted (if dict, only keys are considered).
    position_row :
        Positions of the rows.
    position_col :
        Positions of the columns.
    reorder :
        Use clustering to order nodes.
    width :
        Width of the image.
    height :
        Height of the image.
    margin :
        Margin of the image.
    margin_text :
        Margin between node and text.
    scale :
        Multiplicative factor on the dimensions of the image.
    node_size :
        Size of nodes.
    node_size_min :
        Minimum size of nodes.
    node_size_max :
        Maximum size of nodes.
    display_node_weight :
        If ``True``, display node weights through node size.
    node_weights_row :
        Weights of rows (used only if **display_node_weight** is ``True``).
    node_weights_col :
        Weights of columns (used only if **display_node_weight** is ``True``).
    node_width :
        Width of node circle.
    node_width_max :
        Maximum width of node circle.
    color_row :
        Default color of rows (svg color).
    color_col :
        Default color of cols (svg color).
    label_colors :
        Colors of the labels (svg color).
    display_edges :
        If ``True``, display edges.
    edge_labels :
        Labels of the edges, as a list of tuples (source, destination, label)
    edge_width :
        Width of edges.
    edge_width_min :
        Minimum width of edges.
    edge_width_max :
        Maximum width of edges.
    display_edge_weight :
        If ``True``, display edge weights through edge widths.
    edge_color :
        Default color of edges (svg color).
    font_size :
        Font size.
    filename :
        Filename for saving image (optional).

    Returns
    -------
    image : str
        SVG image.

    Example
    -------
    >>> from sknetwork.data import movie_actor
    >>> biadjacency = movie_actor()
    >>> from sknetwork.visualization import svg_bigraph
    >>> image = svg_bigraph(biadjacency)
    >>> image[1:4]
    'svg'
    """
    n_row, n_col = biadjacency.shape

    # node positions
    if position_row is None or position_col is None:
        position_row = np.zeros((n_row, 2))
        position_col = np.ones((n_col, 2))
        if reorder:
            bilouvain = BiLouvain()
            bilouvain.fit(biadjacency)
            index_row = np.argsort(bilouvain.labels_row_)
            index_col = np.argsort(bilouvain.labels_col_)
        else:
            index_row = np.arange(n_row)
            index_col = np.arange(n_col)
        position_row[index_row, 1] = np.arange(n_row)
        position_col[index_col, 1] = np.arange(n_col) + .5 * (n_row - n_col)
    position = np.vstack((position_row, position_col))

    # node colors
    if scores_row is not None and scores_col is not None:
        if isinstance(scores_row, dict):
            scores_row = np.array(list(scores_row.values()))
        if isinstance(scores_col, dict):
            scores_col = np.array(list(scores_col.values()))
        scores = np.hstack((scores_row, scores_col))
        score_min = np.min(scores)
        score_max = np.max(scores)
    else:
        score_min = None
        score_max = None

    colors_row = get_node_colors(n_row, labels_row, scores_row, membership_row, color_row, label_colors,
                                 score_min, score_max)
    colors_col = get_node_colors(n_col, labels_col, scores_col, membership_col, color_col, label_colors,
                                 score_min, score_max)

    # node sizes
    if node_weights_row is None:
        node_weights_row = biadjacency.dot(np.ones(n_col))
    if node_weights_col is None:
        node_weights_col = biadjacency.T.dot(np.ones(n_row))
    node_sizes_row, node_sizes_col = get_node_sizes_bipartite(node_weights_row, node_weights_col,
                                                              node_size, node_size_min, node_size_max,
                                                              display_node_weight)

    # node widths
    node_widths_row = get_node_widths(n_row, seeds_row, node_width, node_width_max)
    node_widths_col = get_node_widths(n_col, seeds_col, node_width, node_width_max)

    # rescaling
    if not width and not height:
        raise ValueError("You must specify either the width or the height of the image.")
    position, width, height = rescale(position, width, height, margin, node_size, node_size_max, display_node_weight)

    # node names
    if names_row is not None:
        text_length = np.max(np.array([len(str(name)) for name in names_row]))
        position[:, 0] += text_length * font_size * .5
        width += text_length * font_size * .5
    if names_col is not None:
        text_length = np.max(np.array([len(str(name)) for name in names_col]))
        width += text_length * font_size * .5

    # scaling
    position *= scale
    height *= scale
    width *= scale
    position_row = position[:n_row]
    position_col = position[n_row:]

    svg = """<svg width="{}" height="{}"  xmlns="http://www.w3.org/2000/svg">\n""".format(width, height)

    # edges
    if display_edges:
        biadjacency_coo = sparse.coo_matrix(biadjacency)

        if edge_color is None:
            if names_row is None and names_col is None:
                edge_color = 'black'
            else:
                edge_color = 'gray'

        edge_colors, edge_order, edge_colors_residual = get_edge_colors(biadjacency, edge_labels, edge_color,
                                                                        label_colors)
        edge_widths = get_edge_widths(biadjacency_coo, edge_width, edge_width_min, edge_width_max, display_edge_weight)

        for ix in edge_order:
            i = biadjacency_coo.row[ix]
            j = biadjacency_coo.col[ix]
            color = edge_colors[ix]
            svg += svg_edge(pos_1=position_row[i], pos_2=position_col[j], edge_width=edge_widths[ix], edge_color=color)

        for i, j, color in edge_colors_residual:
            svg += svg_edge(pos_1=position_row[i], pos_2=position_col[j], edge_width=edge_width, edge_color=color)

    # nodes
    for i in range(n_row):
        if membership_row is None:
            svg += svg_node(position_row[i], node_sizes_row[i], colors_row[i], node_widths_row[i])
        else:
            if membership_row[i].nnz == 1:
                index = membership_row[i].indices[0]
                svg += svg_node(position_row[i], node_sizes_row[i], colors_row[index], node_widths_row[i])
            else:
                svg += svg_pie_chart_node(position_row[i], node_sizes_row[i], membership_row[i].todense(),
                                          colors_row, node_widths_row[i])

    for i in range(n_col):
        if membership_col is None:
            svg += svg_node(position_col[i], node_sizes_col[i], colors_col[i], node_widths_col[i])
        else:
            if membership_col[i].nnz == 1:
                index = membership_col[i].indices[0]
                svg += svg_node(position_col[i], node_sizes_col[i], colors_col[index], node_widths_col[i])
            else:
                svg += svg_pie_chart_node(position_col[i], node_sizes_col[i], membership_col[i].todense(),
                                          colors_col, node_widths_col[i])
    # text
    if names_row is not None:
        for i in range(n_row):
            svg += svg_text(position_row[i] - (margin_text + node_sizes_row[i], 0), names_row[i], font_size, True)
    if names_col is not None:
        for i in range(n_col):
            svg += svg_text(position_col[i] + (margin_text + node_sizes_col[i], 0), names_col[i], font_size)
    svg += """</svg>\n"""

    if filename is not None:
        with open(filename + '.svg', 'w') as f:
            f.write(svg)

    return svg
