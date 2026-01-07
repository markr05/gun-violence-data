import pandas as pd
data_set = "../data/gun-violence-data_01-2013_03-2018.csv"

def main():
  df = pd.read_csv(data_set)
  df['date'] = pd.to_datetime(df['date'])
  start_date = "2017-01-01"
  end_date = "2018-01-01"
  df = df[df['date'] >= start_date]
  df = df[df['date'] < end_date]
  df['is_home_invasion'] = df['participant_relationship'].str.contains('Home Invasion', na=False)
  df['is_drive_by'] = df['participant_relationship'].str.contains('Drive by', na=False)
  df['is_random_mass_shooting'] = df['participant_relationship'].str.contains('Mass shooting - Random victims', na=False)
  df['is_mass_shooting'] = df['participant_relationship'].str.contains('Mass shooting - Perp Knows Victims', na=False)
  df['is_gang_violence'] = df['participant_relationship'].str.contains('Gang', na=False)
  df['is_friends'] = df['participant_relationship'].str.contains('Friends', na=False)
  df['is_family'] = df['participant_relationship'].str.contains('Family', na=False)
  df['is_significant_other'] = df['participant_relationship'].str.contains('Significant others - current or former', na=False)
  df['is_armed_robbery'] = df['participant_relationship'].str.contains('Armed Robbery', na=False)
  df = df.drop(columns=['incident_url', 'source_url', 'incident_url_fields_missing', 'congressional_district', 'incident_characteristics', 'location_description', 'n_guns_involved','participant_name', 'participant_age_group', 'gun_stolen', 'gun_type', 'participant_status', 'participant_type', 'sources', 'state_house_district', 'state_senate_district', 'notes'])
  important_cols = ['longitude', 'latitude']
  df = df.dropna(subset=important_cols)
  df.to_csv("../data/clean-gun-violence-data.csv", index=False)

if __name__ == "__main__":
  main()