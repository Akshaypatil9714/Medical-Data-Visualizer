import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("/workspace/boilerplate-medical-data-visualizer/medical_examination.csv")

# 2
bmi = (df['weight'] / (df['height']/100) ** 2)
def change (i):
    if i < 25:
        return 0
    else:
        return 1
df['overweight'] = bmi.apply(change)

# 3
normalize_data = {1:0, 2:1, 3:1}

df['cholesterol'] = df['cholesterol'].map(normalize_data)
df['gluc'] = df['gluc'].map(normalize_data)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars = 'cardio', value_vars = (['cholesterol', 'gluc', 'alco', 'active', 'smoke', 'overweight']))
    

    # 6
    df_cat = pd.DataFrame(df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total'))
    

    # 7
    sns.catplot(data=df_cat, x="variable", y="total", hue="value", col="cardio", kind="bar", order=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])


    # 8
    fig = sns.catplot(data=df_cat, x="variable", y="total", hue="value", col="cardio", kind="bar", order=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"]).fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & 
                 (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975)) & (df['ap_lo'] <= df['ap_hi'])]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True


    # 14
    fig, ax = plt.subplots( figsize=(10,8) )
    
    # 15

    sns.heatmap(corr, mask=mask, annot=True, center=0, linewidths=.5, square=True,vmin=-0.15, vmax=0.3, fmt='0.1f')

    # 16
    fig.savefig('heatmap.png')
    return fig
