
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .utils import sort_labels

################################################################################################################################
## 
################################################################################################################################

################################################################
## get_descrete_cmap ~ for color consistency
################################################################
def get_discrete_cmap(labels):
    labs = sort_labels(labels)
    colors_ok = ['lightgray', 'silver', 'darkgray', 'dimgray']
    colors_ng = ['red', 'firebrick', 'indianred', 'lightcoral', 'orange', 'gold', ]
    colors = colors_ok + colors_ng
    cmap = dict()
    for lab in labs:
        if 'ok' in lab.lower():
            cmap[lab] = colors_ok.pop(0)
        elif 'ng' in lab.lower():
            cmap[lab] = colors_ng.pop(0)
        else: 
            cmap[lab] = colors.pop(0)
    return cmap


################################################################
## pie ~ plotly go.pie
################################################################
def pie(df, by, facet=None, cmap=None, hole=0, template='plotly_white'):
    '''
    plot pie chart
    '''
    # prep colors
    if cmap is None:
        cmap = get_discrete_cmap(df[by])
    
    # filter
    groupby_ = [by, facet] if facet is not None else [by]
    data = (
        df.filter(['filename', by, facet])
        .groupby(groupby_)['filename'].count().reset_index()
        .assign(color = lambda df: [cmap[x] for x in df[by]])
    )

    # prep facets
    facets = dict()
    if facet is not None:
        title = facet.upper
        subtitles = []
        facets_ = sort_labels(data[facet])
        for fc in facets_:
            facets[fc] = data[data[facet]==fc].drop(columns=facet)
            subtitles.append(fc)
    else:
        title = None
        subtitles = None
        facets['total'] = data
    
    # create figure
    n_cols = len(facets)
    fig = make_subplots(
        rows=1, cols=n_cols,
        specs=[[{'type': 'domain'}] * n_cols],
        subplot_titles=subtitles,
    )

    # add graphs
    for j, (facet_name, facet_data) in enumerate(facets.items()):
        labels = facet_data[by]
        values = facet_data['filename']
        colors = facet_data['color']
        fig.add_trace(
            go.Pie(labels=labels, values=values, hole=hole, scalegroup='one', ),
            row=1, col=j+1, 
        )

    # update traces
    fig.update_traces(
        textposition='inside',
        textinfo='label+value+percent',
        textfont_size=14,
        marker=dict(colors=colors),
    )

    # update layout
    fig.update_layout(
        autosize=True,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin=dict(l=0, r=0, b=0, t=0),
        template=template
    ) 

    return fig

################################################################
## violin ~ plotly go.violin
################################################################
def violin(df, x, y, label=None, facet=None, title=None, cmap=None, height=300, negative_keyword='ok', template="plotly_white"):
    
    # default color - 나중에 반영
    DEFAULT_COLOR = 'lightgray'
    
    # add temporary facet if facet is None
    if facet is None:
        df = df.assign(temporary_facet = 'total')
        facet = 'temporary_facet'
    if label is None:
        df = df.assign(temporary_label = 'total')
        label = 'temporary_label'
    if cmap is None:
        cmap = get_discrete_cmap(df[label])
        
    # facet
    facets = dict()
    facets_ = sorted(df[facet].unique())
    for i, facet_ in enumerate(facets_):
        df_facet = df[df[facet]==facet_]
        facets[facet_] = dict()
        # labels
        labels_ = sort_labels(df_facet[label].unique())
        for j, label_ in enumerate(labels_):
            df_label = df_facet[df_facet[label]==label_]
            facets[facet_][label_] = df_label
                
    # 
    n_rows = len(facets)
    fig = make_subplots(
        rows=n_rows, cols=1,
        subplot_titles=facets_
    )

    # add graphs
    for i, (facet_, facet_dict) in enumerate(facets.items()):
        showlegend = False if i > 0 else True
        for label_, data in facet_dict.items():
            side = 'negative' if negative_keyword.lower() in label_.lower() else 'positive'
            fig.add_trace(
                go.Violin(
                    x=data[x].astype(str), y=data[y],
                    line_color=cmap[label_],
                    side=side,
                    width=0.8,
                    showlegend=showlegend, legendgroup=label_, name=label_, scalegroup=label_, 
                ), row=i+1, col=1, 
            )

    # aes
    fig.update_traces(
        box_visible = False, meanline_visible=True
    )
    fig.update_layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center'},
        violinmode='overlay',
        height=height*n_rows,
        template=template, 
    )
    
    return fig


################################################################
## violin ~ plotly go.violin
################################################################
def boxplot(df, x, y, label=None, facet=None, title=None, cmap=None, height=300, boxmean=True, template="plotly_white"):
    
    # default color - 나중에 반영
    DEFAULT_COLOR = 'darkgray'
    
    # add temporary facet if facet is None
    if facet is None:
        df = df.assign(temporary_facet = 'total')
        facet = 'temporary_facet'
    if label is None:
        df = df.assign(temporary_label = 'total')
        label = 'temporary_label'
    if cmap is None:
        cmap = get_discrete_cmap(df[label])
        
    # facet
    facets = dict()
    facets_ = sorted(df[facet].unique())
    for i, facet_ in enumerate(facets_):
        df_facet = df[df[facet]==facet_]
        facets[facet_] = dict()
        # labels
        labels_ = sort_labels(df_facet[label].unique())
        for j, label_ in enumerate(labels_):
            df_label = df_facet[df_facet[label]==label_]
            facets[facet_][label_] = df_label
                
    # 
    n_rows = len(facets)
    fig = make_subplots(
        rows=n_rows, cols=1,
        subplot_titles=facets_
    )

    # add graphs
    for i, (facet_, facet_dict) in enumerate(facets.items()):
        showlegend = False if i > 0 else True
        for label_, data in facet_dict.items():
            fig.add_trace(
                go.Box(
                    x=data[x].astype(str), y=data[y],
                    line_color=cmap[label_],
                    width=0.5,
                    boxmean=boxmean,
                    showlegend=showlegend, legendgroup=label_, name=label_, offsetgroup=label_, 
                ), row=i+1, col=1, 
            )

    # aes
    fig.update_layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center'},
        height=height*n_rows,
        template=template, 
    )
    
    return fig
