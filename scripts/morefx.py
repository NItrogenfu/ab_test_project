import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. 加载数据
# ============================================================
df = pd.read_excel('online_ad_AB.xlsx')
print("✅ 数据加载成功！")
print(f"总样本量: {len(df)}")
print(f"字段列表: {df.columns.tolist()}\n")


# ============================================================
# 2. 广告频率分析（ad_count）
# ============================================================
print("="*50)
print("【分析一】广告频率 vs 转化率")
print("="*50)

freq_analysis = df.groupby('ad_count')['made_purchase'].agg(['count', 'mean'])
freq_analysis.columns = ['用户数', '转化率']
freq_filtered = freq_analysis[freq_analysis['用户数'] >= 30]

print(freq_filtered)

# 画图
plt.figure()
freq_filtered['转化率'].plot(kind='line', marker='o')
plt.title('广告观看次数 vs 转化率')
plt.xlabel('观看广告次数')
plt.ylabel('转化率')
plt.grid(True)
plt.show()


# ============================================================
# 3. 时段分析（peak_ad_hours）
# ============================================================
print("\n" + "="*50)
print("【分析二】各时段广告效果")
print("="*50)

hour_analysis = df.groupby(['peak ad hours', 'test group'])['made_purchase'].mean().unstack()
hour_analysis['lift'] = (hour_analysis['ad'] - hour_analysis['psa']) / hour_analysis['psa'] * 100

print("各时段，广告组 vs 对照组转化率：")
print(hour_analysis)

# 画图
plt.figure()
hour_analysis[['ad', 'psa']].plot(kind='bar', figsize=(12,6))
plt.title('各时段广告组 vs 对照组转化率')
plt.xlabel('时段')
plt.ylabel('转化率')
plt.grid(True)
plt.show()


# ============================================================
# 4. 日期分析（days_with_most_add）
# ============================================================
print("\n" + "="*50)
print("【分析三】各日期广告效果")
print("="*50)

day_analysis = df.groupby(['days_with_most_add', 'test group'])['made_purchase'].mean().unstack()
day_analysis['lift'] = (day_analysis['ad'] - day_analysis['psa']) / day_analysis['psa'] * 100

print("各日期，广告组 vs 对照组转化率：")
print(day_analysis)

# 画图
plt.figure()
day_analysis[['ad', 'psa']].plot(kind='bar', figsize=(12,6))
plt.title('各日期广告组 vs 对照组转化率')
plt.xlabel('日期')
plt.ylabel('转化率')
plt.grid(True)
plt.show()


# ============================================================
# 5. 总结输出
# ============================================================
print("\n" + "="*50)
print("【分析总结】")
print("="*50)

# 最佳时段
best_hour = hour_analysis['lift'].idxmax()
best_hour_lift = hour_analysis.loc[best_hour, 'lift']
print(f"最佳投放时段: {best_hour}时，提升幅度 {best_hour_lift:.1f}%")

# 最佳日期
best_day = day_analysis['lift'].idxmax()
best_day_lift = day_analysis.loc[best_day, 'lift']
print(f"最佳投放日期: 第{best_day}天，提升幅度 {best_day_lift:.1f}%")

# 最高转化率对应的广告次数
best_freq = freq_filtered['转化率'].idxmax()
best_freq_rate = freq_filtered.loc[best_freq, '转化率']
print(f"最优广告次数: {best_freq}次，转化率 {best_freq_rate:.2%}")
