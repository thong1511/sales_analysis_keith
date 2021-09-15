import os
import pandas as pd
import matplotlib.pyplot as plt

# Merge all files into one
files = [x for x in os.listdir('./SalesAnalysis/Sales_Data')]

full_data = pd.DataFrame()
for x in files:
    each_month_data = pd.read_csv('./SalesAnalysis/Sales_Data/'+x)
    full_data = pd.concat([full_data, each_month_data])

# Add column "month" to dataset & remove NaN
full_data['month'] = full_data['Order Date'].str[0:2]
full_data.dropna(how='all', inplace=True)

# Convert object to numeric (3 columns)
full_data = full_data[full_data['month'].str[0:2]!='Or']
full_data['month'] = full_data['month'].astype('int32')
full_data['Price Each'] = pd.to_numeric(full_data['Price Each'])
full_data['Quantity Ordered'] = pd.to_numeric(full_data['Quantity Ordered'])



### Q1: Best month for sales?

full_data['sales'] = full_data['Price Each']*full_data['Quantity Ordered']
result_q1 = full_data.groupby('month').sum()['sales']

months = range(1, 13)
plt.bar(months, result_q1)
plt.xticks(months)
plt.show()



### Q2: Best city for sales?

full_data['city'] = full_data['Purchase Address'].apply(lambda x: x.split(',')[1].lstrip() + ' (' + x.split(',')[2].split(' ')[1] + ')')
result_q2 = full_data.groupby('city').sum()
resultq2_list = [value for value in result_q2['sales']]

# Visualization
cities = [city for city, df in full_data.groupby('city')]

resultq2_df = pd.DataFrame()
resultq2_df['city'] = cities
resultq2_df['sales'] = resultq2_list
resultq2_df.sort_values(by='sales', ascending=False, inplace=True)

plt.bar(resultq2_df['city'], resultq2_df['sales'])
plt.xticks(resultq2_df['city'], rotation=45, size=5)
plt.ylabel('Sales in USD')
plt.xlabel('Cities')
plt.show()



### Q3: What time should we display advertisements to maximise the likelihood of customers' buying products?

full_data['Order Date'] = pd.to_datetime(full_data['Order Date'])
full_data['hour'] = full_data['Order Date'].dt.hour
result_q3 = full_data.groupby('hour').count()['Order ID']

# Visualization
hours = [hour for hour, df in full_data.groupby('hour')]
plt.bar(hours, result_q3)
plt.xticks(hours)
plt.grid()
plt.show()



### Q4: What products are most often sold together?

# Create new df for Q4
df_q4 = pd.DataFrame()
df_q4['Order ID'] = full_data['Order ID']
df_q4['Product'] = full_data['Product']

# Remove duplicates
df_q4 = df_q4[df_q4['Order ID'].duplicated(keep=False)]
df_q4['Grouped'] = df_q4.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df_q4 = df_q4[['Order ID', 'Grouped']].drop_duplicates()

# Count quantity of products in pairs
from itertools import combinations
from collections import Counter

count = Counter()

for record in df_q3['Grouped']:
    record_list = record.split(',')
    count.update(Counter(combinations(record_list, 2)))

for key, value in count.most_common(5):
    print(key, value)



### Q5: Product sold the most? Why is that?

most_sold_product = full_data.groupby('Product').sum()['Quantity Ordered'].max()

# Prepare for graph
products = [product for product, df in full_data.groupby('Product')]
total_quantity = full_data.groupby('Product').sum()['Quantity Ordered']
prices = full_data.groupby('Product').mean('Price Each')

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, total_quantity, color='b')
ax2.plot(products, prices, 'r')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='b')
ax2.set_ylabel('Prices', color='r')
ax1.set_xticklabels(products, rotation='vertical', size=8)
plt.show()
