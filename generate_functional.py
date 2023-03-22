import numpy as np
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 1 (success) > 4 (unreach) > 3 (table collision) > 2 (obj collision) > 5 (failed to grasp)

method_name = 'GoES'

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
classifiers=['SEC', 'SECN']
TOPN = 10

env1='shelf008'
env2='diner001'

plot_type='Bar' # Box


_DIR_additional = 'experiments/additional_N_to_400_500'

objs = {
    'shelf008': [
        ['pan',12],
        ['scissor',7] ],
    'diner001': [
        ['fork', 6],
        ['spatula', 14]
    ]
}




filter_experiments = {
    'shelf008': np.arange(401,416),
    'diner001': np.arange(501,516)
}
opt_experiments = {
    'shelf008': np.arange(416,425),
    'diner001': np.arange(516,525)
}

filter_experiments_N = {
    'shelf008': np.arange(601,616),
    'diner001': np.arange(701,716)
}
opt_experiments_N = {
    'shelf008': np.arange(616,625),
    'diner001': np.arange(716,725)
}

df = pd.read_csv('data/functional.csv')
df.loc[ df.Method=='GraspOptES', 'Method'] = method_name

### Success



df_filter = df[df.Method == 'Filter']
df_opt = df[df.Method == method_name]

df_temp = df[['Sample size', 'experiment', 'Method', 'success', 'Classifier']]
df_temp = df_temp.groupby(['Sample size', 'experiment', 'Method', 'Classifier']).sum().reset_index()
# df_temp.success = df_temp.success/len(objs[env])

fig, ax = plt.subplots()

sns.pointplot(ax=ax, data=df_temp[df_temp.Classifier=='SEC'], x='Sample size', y='success', hue='Method', errorbar='sd', linestyles='-')
sns.pointplot(ax=ax, data=df_temp[df_temp.Classifier=='SECN'], x='Sample size', y='success', hue='Method', errorbar='sd', linestyles='--')

# sns.pointplot(ax=ax, data=df_temp2, x='orig_sample_size', y='success')
# plt.savefig('avg_success.pdf')
plt.show()


### Time

df_time = df[['Sample size', 'Method', 'time','Classifier', 'env']]
df_time = df_time.groupby(['Sample size', 'Method', 'Classifier', 'env']).mean().reset_index()

fig, ax = plt.subplots()
sns.pointplot(ax=ax, data=df_time[df_time.Classifier == 'SEC'], x='Sample size', y='time', hue='Method', errorbar='sd', linestyles='-')
sns.pointplot(ax=ax, data=df_time[df_time.Classifier == 'SECN'], x='Sample size', y='time', hue='Method', errorbar='sd', linestyles='--')
# plt.savefig('avg_time.pdf')
plt.show()

### First grasp

df_temp = df[['Sample size', 'experiment', 'Method', 'success', 'Classifier']]
df_temp = df_temp.iloc[::TOPN, :]
df_temp = df_temp.groupby(['Sample size', 'experiment', 'Method', 'Classifier']).sum().reset_index()

fig, ax = plt.subplots()
sns.pointplot(ax=ax, data=df_temp[df_temp.Classifier=='SEC'], x='Sample size', y='success', hue='Method', errorbar='sd', linestyles='-')
sns.pointplot(ax=ax, data=df_temp[df_temp.Classifier=='SECN'], x='Sample size', y='success', hue='Method', errorbar='sd', linestyles='--')
# sns.pointplot(ax=ax, data=df_temp2, x='orig_sample_size', y='success')
# plt.savefig('avg_success.pdf')
plt.show()


### Utility

def assign_utility(x):
    if x.Method == 'Filter':
        return x.init_utility
    else:
        return x.final_utility

df_temp = df[['Sample size', 'init_utility', 'final_utility', 'Method', 'Classifier']]
df_temp = df_temp.assign(Utility = df_temp.apply(assign_utility, axis=1))


fig, ax = plt.subplots(2)
sns.boxplot(ax=ax[0], data=df_temp[df_temp.Classifier=='SEC'], x='Sample size', y='Utility', hue='Method')
sns.boxplot(ax=ax[1], data=df_temp[df_temp.Classifier=='SECN'], x='Sample size', y='Utility', hue='Method')
# sns.boxplot(ax=ax, data=df_opt, x='sample_size', y='final_utility')
# ax.set_xlabel([0, 6000])
ax[0].legend([],[])
plt.show()


df_temp = pd.read_csv('data/df_temp_N_idea.csv')
df_temp = df_temp.rename(columns={'new_success':'Avg. Success / Object'})

fig, ax = plt.subplots(ncols=2, nrows=2)

df_temp = df_temp.groupby(['Sample size', 'Method', 'Classifier', 'experiment', 'obj']).mean().reset_index()
# df_temp['Avg. Success / Object']= df_temp['Avg. Success / Object']

sns.boxplot(ax=ax[0][0], x="Sample size", y="Avg. Success / Object",
            hue="Method", data=df_temp[(df_temp.Classifier=='SEC') & (df_temp.obj == 'spatula014')])

sns.boxplot(ax=ax[0][1], x="Sample size", y="Avg. Success / Object",
            hue="Method", data=df_temp[(df_temp.Classifier=='SECN') & (df_temp.obj == 'spatula014')])

sns.boxplot(ax=ax[1][0], x="Sample size", y="Avg. Success / Object",
            hue="Method", data=df_temp[(df_temp.Classifier=='SEC') & (df_temp.obj == 'pan012')])

sns.boxplot(ax=ax[1][1], x="Sample size", y="Avg. Success / Object",
            hue="Method", data=df_temp[(df_temp.Classifier=='SECN') & (df_temp.obj == 'pan012')])

plt.show()