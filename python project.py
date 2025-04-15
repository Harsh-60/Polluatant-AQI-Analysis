#Q1)State vs Pollution id
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Replace 'filename.csv' with the path to your CSV file
df = pd.read_csv('pythondata.csv')
# Group data by state and pollutant_id, summing up the pollutant_avg
grouped_data = df.groupby(['state', 'pollutant_id'])['pollutant_avg'].sum().reset_index()

# Create bar plot
plt.figure(figsize=(16, 8))
sns.barplot(data=grouped_data, x='state', y='pollutant_avg', hue='pollutant_id')
plt.title('Total Pollution Average by State and Pollutant ID', fontsize=16)
plt.xlabel('State', fontsize=12)
plt.ylabel('Total Average Pollution Level', fontsize=12)
plt.xticks(rotation=90)
plt.legend(title='Pollutant ID')
plt.tight_layout()
plt.show()
#Q2)Pollution id vs Count of pollution max
import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file
df = pd.read_csv("pythondata.csv")

# Group the data by pollutant ID and sum the max counts
pollution_data = df.groupby('pollutant_id')['pollutant_max'].sum().reset_index()

# Plot a line chart
plt.figure(figsize=(10, 6))
plt.plot(pollution_data['pollutant_id'], pollution_data['pollutant_max'], marker='o', linestyle='-')
plt.title('Pollution ID vs Count of Pollution Max')
plt.xlabel('Pollution ID')
plt.ylabel('Total Max Pollution Count')
plt.grid(True)
plt.tight_layout()
plt.show()
#Q3)count of Pollution avg vs latitude(with trendline and error bar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
df = pd.read_csv("pythondata.csv")

# Group by state to get the count of pollutant_avg and sum of latitude
grouped = df.groupby('state').agg(
    count_pollutant_avg=('pollutant_avg', 'count'),
    sum_latitude=('latitude', 'sum')
).reset_index()

# Calculate error bars (standard deviation as an example) – if needed, simulate
grouped['std_dev'] = np.sqrt(grouped['count_pollutant_avg'])  # basic approximation

# Plot with error bars and trend line
plt.figure(figsize=(14, 8))
sns.regplot(
    data=grouped,
    x='count_pollutant_avg',
    y='sum_latitude',
    scatter=True,
    ci=None,
    marker='o',
    line_kws={"color": "red", "label": "Trendline"}
)

# Add error bars
plt.errorbar(
    grouped['count_pollutant_avg'],grouped['sum_latitude'],yerr=grouped['std_dev'],
    fmt='o',ecolor='gray',alpha=0.5,
    label='Error bars'
)

plt.title("State: Count of Pollutant Avg vs Sum of Latitude (with Trendline and Error Bars)")
plt.xlabel("Count of Pollutant Avg")
plt.ylabel("Sum of Latitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#Q4)city and pollution id vs count of pollution avg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the latest uploaded CSV file
df = pd.read_csv("pythondata.csv")

# Step 1: Group by city and pollutant_id and count the number of pollutant_avg values
city_pollution_avg_count = df.groupby(['city', 'pollutant_id'])['pollutant_avg'].count().reset_index()
city_pollution_avg_count.columns = ['city', 'pollutant_id', 'avg_count']

# Step 2: Get top 20 cities by total pollution_avg counts
top_cities = city_pollution_avg_count.groupby('city')['avg_count'].sum().nlargest(20).index
top20_city_pollution = city_pollution_avg_count[city_pollution_avg_count['city'].isin(top_cities)]

# Step 3: Calculate error bars (mean and std per pollutant_id)
error_data = top20_city_pollution.groupby('pollutant_id')['avg_count'].agg(['mean', 'std']).reset_index()
error_data.columns = ['pollutant_id', 'mean_avg_count', 'std_dev']

# Merge error data back into main dataset
top20_city_pollution = pd.merge(top20_city_pollution, error_data, on='pollutant_id')

# Step 4: Plotting
plt.figure(figsize=(14, 7))
sns.lineplot(data=top20_city_pollution, x='city', y='avg_count', hue='pollutant_id', marker='o')

# Add error bars
for _, row in top20_city_pollution.iterrows():
    plt.errorbar(row['city'], row['avg_count'], yerr=row['std_dev'], fmt='o', color='gray', alpha=0.5)

# Add trendlines per pollutant_id
for pollutant in top20_city_pollution['pollutant_id'].unique():
    subset = top20_city_pollution[top20_city_pollution['pollutant_id'] == pollutant]
    if len(subset) > 1:
        x_vals = range(len(subset))
        y_vals = subset.sort_values('city')['avg_count'].values
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        plt.plot(subset.sort_values('city')['city'], p(x_vals), linestyle='--', label=f'{pollutant} trend')

# Final touches
plt.xticks(rotation=90)
plt.title('Top 20 Cities and Pollutant ID vs Count of Pollution Average\nwith Trendlines and Error Bars')
plt.xlabel('City')
plt.ylabel('Count of Pollution Average')
plt.tight_layout()
plt.show()



#Q5)station and pollution id vs pollution avg
# Final clean version of the full scatter plot code with trendlines and error bars

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("pythondata.csv")

# Step 1: Group by station and pollutant_id and count the number of pollutant_avg values
station_pollution_avg_count = df.groupby(['station', 'pollutant_id'])['pollutant_avg'].count().reset_index()
station_pollution_avg_count.columns = ['station', 'pollutant_id', 'avg_count']

# Step 2: Select top 20 combinations with highest count
top20 = station_pollution_avg_count.sort_values(by='avg_count', ascending=False).head(20)

# Step 3: Calculate mean and standard deviation of avg_count per pollutant_id
error_data = top20.groupby('pollutant_id')['avg_count'].agg(['mean', 'std']).reset_index()
error_data.columns = ['pollutant_id', 'mean_avg_count', 'std_dev']

# Step 4: Merge error data back to the top 20 dataset
top20 = pd.merge(top20, error_data, on='pollutant_id')

# Step 5: Plotting
plt.figure(figsize=(14, 7))
sns.scatterplot(data=top20, x='station', y='avg_count', hue='pollutant_id', style='pollutant_id', s=100)

# Add error bars
plt.errorbar(top20['station'], top20['avg_count'],
             yerr=top20['std_dev'], fmt='none', ecolor='gray', alpha=0.6)

# Add trendlines per pollutant
for pollutant in top20['pollutant_id'].unique():
    subset = top20[top20['pollutant_id'] == pollutant]
    if len(subset) > 1:
        x_vals = range(len(subset))
        y_vals = subset['avg_count'].values
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        plt.plot(subset['station'], p(x_vals), linestyle='--', label=f'{pollutant} trend')

# Plot aesthetics
plt.xticks(rotation=90)
plt.title('Top 20 Stations and Pollutant IDs vs Count of Pollution Average\nwith Trendlines and Error Bars')
plt.xlabel('Station')
plt.ylabel('Count of Pollution Average')
plt.tight_layout()
plt.show()


#Q6)state vs pollution id
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load the dataset
df = pd.read_csv("pythondata.csv")
# Count of pollutant_id per state
pollution_count = df.groupby('state')['pollutant_id'].count().reset_index()
pollution_count.columns = ['state', 'pollution_count']

# Plotting line chart
plt.figure(figsize=(12, 6))
sns.lineplot(data=pollution_count, x='state', y='pollution_count', marker='o')
plt.xticks(rotation=90)
plt.title('Line Chart of State vs Count of Pollution ID')
plt.xlabel('State')
plt.ylabel('Count of Pollution ID')
plt.tight_layout()
plt.show()








