import pandas as pd

# Load the dataset
df = pd.read_csv('all.csv')

# Define the columns you are interested in
columns_of_interest = [
    'TreeMap1', 'PieChart1', 'PieChart5', 'TreeMap4', 'PieChart12', 'PieChart11', 
    'TreeMap7', 'DonutChart7', 'StackedBarChart1', 'PieChart4', 'TreeMap12', 
    'PieChart7', 'StackedBarChart9', 'DonutChart9', 'TreeMap9', 'StackedBarChart2', 
    'TreeMap11', 'StackedBarChart4', 'TreeMap5', 'PieChart9', 'DonutChart3', 
    'DonutChart6', 'StackedBarChart8', 'PieChart8', 'TreeMap8', 'StackedBarChart12', 
    'DonutChart1', 'StackedBarChart6', 'StackedBarChart10', 'TreeMap10', 'PieChart2', 
    'PieChart6', 'PieChart10', 'DonutChart12', 'DonutChart10', 'StackedBarChart5', 
    'TreeMap2', 'StackedBarChart7', 'DonutChart5', 'DonutChart4', 'DonutChart2', 
    'StackedBarChart3', 'TreeMap6', 'DonutChart11', 'DonutChart8', 'StackedBarChart11', 
    'PieChart3', 'TreeMap3'
]

# Melt the DataFrame
melted_df = df.melt(value_vars=columns_of_interest, var_name='ChartType', value_name='Value')

# Remove NaN values
melted_df.dropna(inplace=True)
df_filtered = melted_df[~melted_df.isin([0.0, 1.0]).any(axis=1)]

# Save the melted dataframe to a CSV file
melted_csv_path = 'answers-pre.csv'
df_filtered.to_csv(melted_csv_path, index=False)

# Provide the path to the saved file
melted_csv_path

df = pd.read_csv('answers-pre.csv')
df.rename(columns={'ChartType': 'Vis', 'Value': 'ReportedPercent'}, inplace=True)
#index col 1
df.reset_index(inplace=True)
df.rename(columns={'index': 'Index'}, inplace=True)
df['Index'] += 1

# Save csv
updated_csv_path = 'answers.csv'
df.to_csv(updated_csv_path, index=False)

# Provide the path to the saved file
updated_csv_path
