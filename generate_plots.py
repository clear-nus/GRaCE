import numpy as np
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 1 (success) > 4 (unreach) > 3 (table collision) > 2 (obj collision) > 5 (failed to grasp)

method_name = 'GoES'
env='diner001'

# visualization params
context = {
     'font.size': 14.0,
     'axes.labelsize': 14.0,
     'axes.titlesize': 16.0,
     'xtick.labelsize': 14,
     'ytick.labelsize': 14,
     'legend.fontsize': 14,
     'legend.title_fontsize': 14.0,
     'axes.linewidth': 1.25,
     'grid.linewidth': 1.0,
     'lines.linewidth': 1.5,
     'lines.markersize': 6.0,
     'patch.linewidth': 1.0,
     'xtick.major.width': 1.25,
     'ytick.major.width': 1.25,
     'xtick.minor.width': 1.0,
     'ytick.minor.width': 1.0,
     'xtick.major.size': 6.0,
     'ytick.major.size': 6.0,
     'xtick.minor.size': 4.0,
     'ytick.minor.size': 4.0
    }

style={
         'axes.facecolor': 'white',
         'axes.edgecolor': '.8',
         'axes.grid': False,
         'axes.axisbelow': True,
         'axes.labelcolor': '.15',
         'figure.facecolor': 'white',
         'grid.color': '.8',
         'grid.linestyle': '-',
         'text.color': '.15',
         'xtick.color': '.15',
         'ytick.color': '.15',
         'xtick.direction': 'out',
         'ytick.direction': 'out',
         'patch.edgecolor': 'w',
         'patch.force_edgecolor': True,
         'image.cmap': 'rocket',
         'font.family': ['Helvetica'],
         'font.sans-serif': ['Arial',
          'DejaVu Sans',
          'Liberation Sans',
          'Bitstream Vera Sans',
          'sans-serif'],
         'xtick.bottom': False,
         'xtick.top': False,
         'ytick.left': False,
         'ytick.right': False,
         'axes.spines.left': True,
         'axes.spines.bottom': True,
         'axes.spines.right': True,
         'axes.spines.top': True
    }

sns.set_theme(context=context, style=style)

sampler='graspnet'
method='GraspOptES'
grasp_space='SO3'
classifier='SEC'
TOPN = 10
prefix = f'{sampler}_{classifier}_{method}_{grasp_space}'

plot_type='Bar' # Box
legend_on = True

objs = {
    'shelf008': [
        ['pan',12],
        ['bottle',14],
        ['bowl',8],
        ['bowl',10],
        ['fork',6],
        ['pan',6],
        ['scissor',7] ],
    'diner001': [
        ['bottle', 0],
        ['bowl', 8],
        ['fork', 6],
        ['pan', 12],
        ['spatula', 14]
    ]
}

df = pd.read_csv(f'data/{env}.csv')
df.loc[ df.Method=='GraspOptES', 'Method'] = method_name

df_filter = df[df.Method == 'Filter']
df_opt = df[df.Method == method_name]

### Success

df_temp = df[['Sample size', 'experiment', 'Method', 'success']]
df_temp = df_temp.groupby(['Sample size', 'experiment', 'Method']).mean().reset_index()
df_temp.success = df_temp.success*10
df_temp = df_temp.rename(columns={'success':'Avg. Success / Object'})

fig, ax = plt.subplots(figsize=(4,3))

if plot_type == 'Box':
    graph = sns.boxplot(ax=ax, data=df_temp, x='Sample size', y='Avg. Success / Object', hue='Method', palette="tab10", width=0.5)
elif plot_type == 'Bar':
    graph = sns.barplot(ax=ax, data=df_temp, x='Sample size', y='Avg. Success / Object', hue='Method', errorbar='sd', palette="tab10")

ax.set_ylim([0,10])
fig = graph.get_figure()

if not legend_on:
    ax.legend().set_visible(False)
else:
    plt.legend(ncol=2, bbox_to_anchor=(1.15, 1.15), loc='upper right')

fig.savefig(f"figs/main_top10_success_{env}_{plot_type}_nolegend.pdf", bbox_inches='tight' )

### Time

df_time = df[['Sample size', 'Method', 'time']]
df_time = df_time.rename(columns={'time':'Time, s'})

fig, ax = plt.subplots(figsize=(4,3))

if plot_type == 'Bar':
    # graph = sns.boxplot(ax=ax, data=df_time, x='Sample size', y='time', hue='Method', palette="tab10", width=0.5)
    graph = sns.barplot(ax=ax, data=df_time, x='Sample size', y='Time, s', hue='Method', errorbar='sd', palette='tab10')
elif plot_type=='Box':
    graph = sns.boxplot(ax=ax, data=df_time, x='Sample size', y='Time, s', hue='Method', palette="tab10", width=0.5)

if not legend_on:
    ax.legend().set_visible(False)

fig = graph.get_figure()
fig.savefig(f"figs/main_time_{env}_{plot_type}_nolegend.pdf", bbox_inches='tight' )

### First Grasp

df_temp = df[['Sample size', 'experiment', 'Method', 'success']]
df_temp = df_temp.iloc[::TOPN, :]
df_temp = df_temp.groupby(['Sample size', 'Method', 'experiment']).mean().reset_index()
df_temp = df_temp.rename(columns={'success':'Avg. Success / Object'})

fig, ax = plt.subplots(figsize=(4,3))

if plot_type == 'Bar':
    graph = sns.barplot(ax=ax, data=df_temp, x='Sample size', y='Avg. Success / Object', hue='Method', errorbar='sd', palette='tab10')
elif plot_type == 'Box':
    graph = sns.boxplot(ax=ax, data=df_temp, x='Sample size', y='Avg. Success / Object', hue='Method', palette="tab10", width=0.5)

if not legend_on:
    ax.legend().set_visible(False)
ax.set_ylim([0,1])
fig = graph.get_figure()
fig.savefig(f"figs/main_top1_success_{env}_{plot_type}_nolegend.pdf", bbox_inches='tight' )

### Utility Change

def assign_utility(x):
    if x.Method == 'Filter':
        return x.init_utility
    else:
        return x.final_utility

df_temp = df[['Sample size', 'init_utility', 'final_utility', 'Method']]
df_temp = df_temp.assign(Utility = df_temp.apply(assign_utility, axis=1))


fig, ax = plt.subplots(figsize=(4,3))

if plot_type == 'Bar':
    graph = sns.barplot(ax=ax, data=df_temp, x='Sample size', y='Utility', hue='Method', palette="tab10", width=0.5, errorbar='sd')
elif plot_type == 'Box':
    graph = sns.boxplot(ax=ax, data=df_temp, x='Sample size', y='Utility', hue='Method', palette="tab10", width=0.5)

ax.legend().set_visible(False)
fig = graph.get_figure() 
fig.savefig(f"figs/main_top10_utility_{env}_{plot_type}_nolegend.pdf", bbox_inches='tight' )
