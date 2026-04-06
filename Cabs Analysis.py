# %% Import libraries
from scipy import stats
import os
import pandas as pd
import matplotlib.pyplot as plt

# %% Get base path of the script
base_path = os.path.dirname(__file__)

# %% Build file paths
companies_path = os.path.join(base_path, 'data', 'company_trips.csv')
neighborhoods_path = os.path.join(base_path, 'data', 'dropoff_trips.csv')
loop_ohare_path = os.path.join(base_path, 'data', 'project_sql_result_07.csv')

# %% Load datasets
df_companies = pd.read_csv(companies_path)
df_neighborhoods = pd.read_csv(neighborhoods_path)

# %% Initial preview
print(f"\n{'='*50}")
print("DATASET: COMPANIES")
print(f"{'='*50}")
print(df_companies.head())

print(f"\n{'='*50}")
print("DATASET: NEIGHBORHOODS")
print(f"{'='*50}")
print(df_neighborhoods.head())

# %% General info
print(f"\n{'='*50}")
print("INFO: COMPANIES")
print(f"{'='*50}")
df_companies.info()

print(f"\n{'='*50}")
print("INFO: NEIGHBORHOODS")
print(f"{'='*50}")
df_neighborhoods.info()

# %% Top 10 neighborhoods
top10_neighborhoods = df_neighborhoods.sort_values(
    by='average_trips', ascending=False
).head(10)

print(f"\n{'='*50}")
print("TOP 10 NEIGHBORHOODS")
print(f"{'='*50}")
print(top10_neighborhoods.round(2))

# %% Chart: trips per company
print(f"\n{'='*50}")
print("CHART: TRIPS PER COMPANY")
print(f"{'='*50}")

df_companies.sort_values('trips_amount', ascending=False).plot(
    x='company_name',
    y='trips_amount',
    kind='bar',
    figsize=(10, 6),
)

plt.title('Taxi companies and number of trips')
plt.xlabel('Company')
plt.ylabel('Number of trips')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# %% Chart: top neighborhoods
print(f"\n{'='*50}")
print("CHART: TOP 10 NEIGHBORHOODS")
print(f"{'='*50}")

top10_neighborhoods.plot(
    x='dropoff_location_name',
    y='average_trips',
    kind='bar',
    figsize=(10, 6),
)

plt.title('Top 10 neighborhoods by drop-offs')
plt.xlabel('Neighborhood')
plt.ylabel('Average trips')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# %% Conclusions: taxi companies
# Flash Cab has the highest number of trips, significantly exceeding other companies.
# Taxi Affiliation Services ranks second with a considerable gap from Flash Cab.
# Several companies show similar levels of activity, indicating competition.
# Overall, the market is dominated by a few major companies.

# %% Conclusions: neighborhoods
# Loop is the most active neighborhood with the highest number of drop-offs.
# River North and Streeterville also show high trip volumes.
# O'Hare appears due to the international airport.
# Most trips end in central and economically active areas.

# %% Load Loop → O'Hare dataset
print(f"\n{'='*50}")
print("DATASET: LOOP → O'HARE")
print(f"{'='*50}")

df_Loop_OHare = pd.read_csv(loop_ohare_path)

print("\nPreview:")
print(df_Loop_OHare.head())

print(f"\nColumns:")
print(df_Loop_OHare.columns)

print(f"\nINFO:")
df_Loop_OHare.info()

# %% Data cleaning and datetime conversion
df_Loop_OHare['start_ts'] = pd.to_datetime(
    df_Loop_OHare['start_ts'],
    dayfirst=True,
    errors='coerce'
)

# Remove invalid rows
df_Loop_OHare = df_Loop_OHare.dropna(subset=['start_ts'])

print(f"\n{'='*50}")
print("INFO AFTER CLEANING")
print(f"{'='*50}")
df_Loop_OHare.info()

# %% Hypotheses
# H0: The average trip duration is the same in rainy and non-rainy conditions.
# H1: The average trip duration is different in rainy conditions.

# %% Hypothesis test
print(f"\n{'='*50}")
print("HYPOTHESIS TEST")
print(f"{'='*50}")

rainy = df_Loop_OHare[df_Loop_OHare['weather_conditions']
                      == 'Bad']['duration_seconds']
good = df_Loop_OHare[df_Loop_OHare['weather_conditions']
                     == 'Good']['duration_seconds']

alpha = 0.05
results = stats.ttest_ind(rainy, good)

print(f"\n{'-'*50}")
print("STATISTICAL RESULTS")
print(f"{'-'*50}")
print(f"p-value: {results.pvalue}")

print(f"\n{'-'*50}")
print("DECISION")
print(f"{'-'*50}")

if results.pvalue < alpha:
    print("Reject the null hypothesis:")
    print("Trip duration changes when it rains.")
else:
    print("Fail to reject the null hypothesis:")
    print("No evidence that trip duration changes due to rain.")

print(f"\n{'-'*50}")
print("AVERAGE DURATIONS")
print(f"{'-'*50}")
print(f"Average duration (rain): {rainy.mean():.2f}")
print(f"Average duration (no rain): {good.mean():.2f}")
