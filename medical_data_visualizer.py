import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv(r'medical_examination.csv')

# 2

BMI = [1 if ((i / df['height'][k] ** 2) * 10000) > 25 else 0 for k, i in enumerate(df['weight'])]

df['overweight'] = BMI

# 3
colest = []
gluc = []
for k, i in enumerate(df['cholesterol']):
    if i > 1 and df['gluc'][k] > 1:
        colest.append(1)
        gluc.append(1)
    elif i <= 1 and df['gluc'][k] <= 1:
        colest.append(0)
        gluc.append(0)
    elif i > 1 & df['gluc'][k] <= 1:
        gluc.append(0)
        colest.append(1)
    else:
        colest.append(0)
        gluc.append(1)

df['cholesterol'] = colest
df['gluc'] = gluc


# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7
    catplot = sns.catplot(x='variable', y='total', hue='value', col='cardio', kind='bar', data=df_cat)

    # 8
    fig = catplot.fig

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11

    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr))

    # 14
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15
    sns.heatmap(corr, mask=mask, annot=True, cmap="rocket", ax=ax, fmt=".1f", linewidths=0.5)
    plt.show()
    # 16
    fig.savefig('heatmap.png')
    return fig
