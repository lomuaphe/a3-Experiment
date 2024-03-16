import pandas as pd
import numpy as np
from sklearn.utils import resample
import seaborn as sns
import matplotlib.pyplot as plt

# convert comma decimals to float --> to integer percentages
convert_to_percentage = lambda x: int(float(x.replace(',', '.')) * 100)

# Datasets loaded
answers_df = pd.read_csv('answers.csv', sep=',')
correctan_df = pd.read_csv('correctan.csv', sep=';', converters={'TruePercent': convert_to_percentage})

# Df merged based on 'Vis' column
merged_df = pd.merge(answers_df, correctan_df, on='Vis', how='left')

# Cleveland error equation
# Case: percentage set to 0 when person gets the exact percentage
merged_df['Error'] = merged_df.apply(
    lambda row: 0 if row['ReportedPercent'] == row['TruePercent'] 
    else np.round(np.log2(abs(row['ReportedPercent'] - row['TruePercent']) + 1/8), 2), axis=1)

# Save file
output_merged_errors_path = 'merged_answers_errors.csv'
merged_df.to_csv(output_merged_errors_path, index=False)
output_merged_errors_path, merged_df.head()

# RANKING
# Classify graph types
def classify_vis(vis):
    if vis.startswith('Tree'):
        return 'Treemap'
    elif vis.startswith('Pie'):
        return 'Pie Chart'
    elif vis.startswith('Donut'):
        return 'Donut Chart'
    elif vis.startswith('Stacked'):
        return 'Stacked Bar Chart'
    else:
        return 'Other'

merged_df['VisType'] = merged_df['Vis'].apply(classify_vis)

# Calculate average error for each graph type
vis_errors = merged_df.groupby('VisType')['Error'].mean().round(2).reset_index()

# Rank by average error
vis_errors = vis_errors.sort_values(by='Error').reset_index(drop=True)

# Adding a rank column
vis_errors['Rank'] = vis_errors['Error'].rank(method='min')
vis_errors, vis_errors['Rank']



#BOOTSTRAPED CI
# Define fx to calculate 95% conf intervals w/bootstrapping
def bootstrap_confidence_interval(data, n_bootstrap=1000):
    bootstrap_means = []
    for _ in range(n_bootstrap):
        # Sample with replacement
        bootstrap_sample = resample(data)
        bootstrap_mean = bootstrap_sample.mean()
        bootstrap_means.append(bootstrap_mean)
    # Calculate the percentiles for 2.5% and 97.5% to get the 95% confidence interval
    lower_bound = np.percentile(bootstrap_means, 2.5)
    upper_bound = np.percentile(bootstrap_means, 97.5)
    return lower_bound, upper_bound

# Classify graph types
merged_df['VisType'] = merged_df['Vis'].apply(classify_vis)

# init columns for lower and upper bounds
vis_errors['Lower CI'] = 0.0
vis_errors['Upper CI'] = 0.0

# Calculate 95% conf intervals for each tyope
for vis_type in vis_errors['VisType']:
    error_data = merged_df[merged_df['VisType'] == vis_type]['Error']
    lower_bound, upper_bound = bootstrap_confidence_interval(error_data)
    vis_errors.loc[vis_errors['VisType'] == vis_type, 'Lower CI'] = np.round(lower_bound, 2)
    vis_errors.loc[vis_errors['VisType'] == vis_type, 'Upper CI'] = np.round(upper_bound, 2)

# Savefile
output_vis_errors_ci_path = 'visualization_errors_ranking_with_ci.csv'
vis_errors.to_csv(output_vis_errors_ci_path, index=False)

output_vis_errors_ci_path, vis_errors


#BOXPLOT
# Load_data
file_path = 'visualization_errors_ranking_with_ci.csv'
data = pd.read_csv(file_path)
data_sorted = data.sort_values('Error', ascending=True)

data.head()
fig, ax = plt.subplots(figsize=(8, 6))
fig.subplots_adjust(left=0.25)

# For each vis type, plot 'Error' as central point and 'Lower CI' and 'Upper CI' as error bars
for i, row in data_sorted.iterrows():
    position = len(data_sorted) - 1 - i  # Invert position to match the ascending error order
    ax.errorbar(row['Error'], position, 
                xerr=[[row['Error'] - row['Lower CI']], [row['Upper CI'] - row['Error']]], 
                fmt='o', color='black', capsize=5, capthick=2, elinewidth=2, markersize=10)
#Axes
ax.set_xlim(1, 5)
ax.set_yticks(np.arange(len(data_sorted['VisType'])))
ax.set_yticklabels(data_sorted['VisType'].iloc[::-1])  # Reverse the label order to match plotting
ax.set_xlabel('Log Error')
ax.set_title('Pixel Master Results')

# Save plt
plot_path = 'visualization_error_plot.png'
fig.savefig(plot_path)
plot_path