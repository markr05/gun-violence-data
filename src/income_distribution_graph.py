import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("../data/data_with_income.csv")

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 7))

sns.histplot(df['median_income'], kde=True, color='royalblue', bins=50)

national_median = 61372
plt.axvline(national_median, color='red', linestyle='--', linewidth=2, label=f'US Median Income (${national_median:,})')

dataset_mean = df['median_income'].mean()
plt.axvline(dataset_mean, color='green', linestyle='-', linewidth=2, label=f'Incident Site Mean (${dataset_mean:,.0f})')

plt.title('Socioeconomic Analysis: Incident Site Income vs. National Median', fontsize=15)
plt.xlabel('Median Household Income ($)', fontsize=12)
plt.ylabel('Number of Incidents', fontsize=12)
plt.legend()

plt.text(national_median + 2000, plt.ylim()[1]*0.9, 'National Average', color='red', fontweight='bold')

plt.tight_layout()
plt.savefig('../output/income_distribution_comparison.png', dpi=300)
plt.show()