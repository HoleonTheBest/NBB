import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

df = pd.read_excel('D:/代码/test1.xlsx')

df = df.sort_values(by='日期', ascending=False).head(14)
df = df.reset_index(drop=True)

outlier_ratio = 0.5


def NBB(df):
    stop_1_loop = False
    df1 = df
    while not stop_1_loop:
        std_deviation = df1['用户量级'].std()
        mean = df1['用户量级'].mean()
        erua = std_deviation / mean
        erua_percentage = erua * 100
        print(f'变异系数：{erua_percentage:.2f}%')
        if erua < 0.1:
            stop_1_loop = True
        else:
            print('数据存在异常波动')
            i = 1
            stop_2_loop = False
            while not stop_2_loop:
                p = np.sum((df1['用户量级'] >= mean - i * std_deviation) & (df1['用户量级'] <= mean + i * std_deviation)) / len(df1) * 100
                if p >= outlier_ratio * 100:
                    new_df = df1[(df1['用户量级'] >= mean - i * std_deviation) & (df1['用户量级'] <= mean + i * std_deviation)]
                    df1 = new_df
                    stop_2_loop = True
                else:
                    i += 0.05
    return df1

result = NBB(df)
df1 = NBB(df)


merged = pd.concat([df, df1])
removed_data = merged.drop_duplicates(keep=False)
print(f'正常数据：{df1}')
print(f'异常数据：{removed_data}')
removed_ratio = len(removed_data) / len(df)
print(f'异常数据占比：{removed_ratio:.2f}%')
if removed_ratio >=0.5:
    print("数据集波动强烈，建议使用环比&单日阈值监测")

df = pd.read_excel('D:/代码/vv.xlsx')
