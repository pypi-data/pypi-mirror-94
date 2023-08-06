import numpy as np
import pandas as pd
import networkx as nx

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from tqdm import tqdm


def plot_network(
    graph,
    ax=None,
    label_key='scientific_name',
    nodes_kws=dict(),
    labels_kws=dict(),
    edges_kws=dict(),
):
    """Visualize given taxonomy."""
    # compute additional properties
    node_labels = {
        n: data.get(label_key, '') for n, data in graph.nodes(data=True)
    }

    # create layout
    pos = nx.nx_agraph.pygraphviz_layout(graph, prog='dot')

    # visualize
    if ax is None:
        ax = plt.gca()

    nx.draw_networkx_nodes(graph, pos, ax=ax, **nodes_kws)
    nx.draw_networkx_labels(
        graph, pos, labels=node_labels, ax=ax, **labels_kws
    )
    nx.draw_networkx_edges(graph, pos, ax=ax, **edges_kws)

    ax.axis('off')

    return ax


def compute_rank_frequencies(
    df_inp,
    rank_list=['species', 'genus', 'class', 'superkingdom'],
    max_taxon_count=5,
    include_hidden_ranks=False,
    include_unmatched_reads=False,
):
    """Compute nested rank frequencies."""
    df = df_inp.copy()

    # consider reads which were not matched
    if include_unmatched_reads:
        df[df['taxid'].isna()] = 'no_taxon'
    else:
        # this will drop unidentified reads, but keep those
        # which have no value at certain ranks
        df = df.dropna(subset=['taxid'])

    # only consider taxons of some minimal frequency
    total_freqs = df['taxid'].value_counts(normalize=True)
    if max_taxon_count is not None:
        total_freqs = total_freqs.head(max_taxon_count)
    top_taxons = total_freqs.index

    if include_hidden_ranks:
        df.loc[~df['taxid'].isin(top_taxons), rank_list] = 'other'
    else:
        df = df[df['taxid'].isin(top_taxons)]

    # some taxons don't have certain ranks, let's fill them up with lower rank values
    for i in range(len(rank_list) - 1):
        df[rank_list[i + 1]] = df[rank_list[i + 1]].combine_first(
            df[rank_list[i]]
        )

    # compute frequencies
    result = []

    previous_rank = None
    previous_order = None
    for i, rank in enumerate(rank_list[::-1]):
        # to align subranks with superranks, we need to remember their order and count respectively
        if previous_order is None:
            freqs = df[rank].value_counts(dropna=False)
        else:
            freq_list = []
            for taxon in previous_order:
                tmp = df.loc[df[previous_rank] == taxon, rank]
                freq_list.append(tmp.value_counts(dropna=False))
            freqs = pd.concat(freq_list)

        previous_rank = rank
        previous_order = freqs.index

        # store result
        result.append(freqs)

    return result


def plot_piechart(
    df_inp,
    ax=None,
    colormap='tab10',
    plot_legend=False,
    label_template='{taxon}',  # can use {taxon}, {count}
    rank_list=['species', 'genus', 'class', 'superkingdom'],
    max_taxon_count=5,
    include_hidden_ranks=False,
    include_unmatched_reads=False,
):
    """Plot nested taxon piechart."""
    # compute frequencies
    freq_list = compute_rank_frequencies(
        df_inp,
        rank_list=rank_list,
        max_taxon_count=max_taxon_count,
        include_hidden_ranks=include_hidden_ranks,
        include_unmatched_reads=include_unmatched_reads,
    )

    # setup plot
    if ax is not None:
        # TODO: handle this in a better way
        ax.set_axis_off()
        plt.sca(ax)
    ax = plt.gca(projection='polar')

    # preliminary setup
    colormap = plt.get_cmap(colormap)
    pos_y_list, height = np.linspace(0, 1, len(rank_list), retstep=True)

    for i, (freqs, pos_y) in enumerate(zip(freq_list, pos_y_list)):
        # compute position and width of each bar
        width_list = freqs / np.sum(freqs) * 2 * np.pi
        pos_x_list = np.cumsum(np.append(0, width_list[:-1]))

        # plot actual bars
        ax.bar(
            x=pos_x_list,
            width=width_list,
            bottom=pos_y,
            height=height,
            color=colormap(i),
            edgecolor='w',
            linewidth=1,
            align='edge',
        )

        # add labels to each bar
        for pos_x, width, taxon, freq in zip(
            pos_x_list, width_list, freqs.index, freqs
        ):
            label_pos_x = pos_x + width / 2
            label_pos_y = pos_y + height / 2

            label = label_template.format(taxon=taxon, count=freq)

            ax.text(
                label_pos_x,
                label_pos_y,
                label,
                ha='center',
                va='center',
                clip_on=False,
            )

    # add rank legend
    if plot_legend:
        ax.legend(
            handles=[
                Patch(facecolor=colormap(i), label=rank)
                for i, rank in enumerate([freq.name for freq in freq_list])
            ],
            loc='best',
        )

    # finalize plot
    ax.set_axis_off()
    ax.set_aspect('equal')

    return ax


def plot_rarefaction_curve(
    df, ax=None, resample_count=3, sample_step_count=30
):
    # compute diversity at sampling points
    steps = np.linspace(1, df.shape[0], num=sample_step_count, dtype=int)

    tmp = []
    for sample_count in tqdm(steps):
        for iter_ in range(resample_count):
            df_sub = df.sample(sample_count)
            diversity = df_sub['taxid'].nunique()

            tmp.append(
                {
                    'subsample_size': sample_count,
                    'subsample_fraction': sample_count / df.shape[0],
                    'iteration': iter_,
                    'unique_taxon_count': diversity,
                }
            )

    df_div = pd.DataFrame(tmp)

    # plot result
    if ax is None:
        ax = plt.gca()

    sns.lineplot(data=df_div, x='subsample_fraction', y='unique_taxon_count')

    ax.set_xlabel('Subsample fraction')
    ax.set_ylabel('Unique OTU count')

    return ax
