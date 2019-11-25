import pandas as pd
import json

df = pd.read_csv('simulation_results.csv')
df_json = df.to_json(orient='columns')

json_data = json.loads(df_json)

print(json_data.keys())
# print(json_data["Date"])

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)