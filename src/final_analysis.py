import pandas as pd

def calculate_income_statistics(dataframe, 
                                female_involved = False, 
                                number_killed = -1, 
                                number_injured = -1, 
                                start_date = "2017-01-01", 
                                end_date = "2017-12-31", 
                                state = None, 
                                label = "Total"):
  df = dataframe

  if female_involved == True:
    df = df[df["participant_gender"].str.contains("Female", na=False)]
  if state is not None:
    df = df[df['state'] == state]
  df = df[df["n_killed"] > number_killed]
  df = df[df["n_injured"] > number_injured]
  df = df[df["date"] >= start_date]
  df = df[df["date"] <= end_date]

  avg_income = df['median_income'].mean()
  count = len(df)
  print(label)
  print(f"Incidents matching criteria: {count}.")
  print(f"Average household income: {avg_income:,.2f}\n")

def main():
  data_set = "../data/data_with_income.csv"
  df = pd.read_csv(data_set)

  # example usages
  calculate_income_statistics(df)
  calculate_income_statistics(df, female_involved=True, label="Female Involved")
  calculate_income_statistics(df, state="Tennessee", label="In Tennessee")
  calculate_income_statistics(df, number_injured=2, state="Tennessee", label="In Tennessee with >2 injured")


if __name__ == "__main__":
  main()