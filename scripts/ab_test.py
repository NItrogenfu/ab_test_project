import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# 1. 读取数据
# 假设你下载的文件名为 online_ad_AB.csv，并放在和这个脚本相同的目录下
try:
    df = pd.read_excel('online_ad_AB.xlsx')
    print("✅ 数据加载成功！")
except FileNotFoundError:
    print("❌ 文件未找到，请检查文件名和路径是否正确。")
    exit()

# 2. 数据概览
print(f"总样本量: {len(df)}")
print(df.head())

# 3. 计算转化率
group_stats = df.groupby('test group')['made_purchase'].agg(['count', 'sum', 'mean'])
group_stats.columns = ['用户数', '购买数', '转化率']
print("\n📊 各组转化率统计：")
print(group_stats)

# 4. 卡方检验
# 创建交叉表：行是实验组，列是是否购买
contingency_table = pd.crosstab(df['test group'], df['made_purchase'])
print("\n📋 交叉表：")
print(contingency_table)

# 执行卡方检验
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print("\n🔬 假设检验结果：")
print(f"卡方统计量: {chi2:.4f}")
print(f"P值: {p_value:.10f}")  # 打印更多小数位，便于观察

# 5. 结论
alpha = 0.05
if p_value < alpha:
    print("\n✅ 结论：差异统计显著（p < 0.05），广告投放有效地提升了转化率。")
else:
    print("\n❌ 结论：差异不显著（p >= 0.05），没有足够证据表明广告投放提升了转化率。")