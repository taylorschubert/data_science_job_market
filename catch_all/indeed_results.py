import json
import os
import pprint as pp


project_path = os.path.join(os.sep, 'data', 'pnc', 'pl52590', 'projects',
                           'job_scraper')

result_path = os.path.join(os.sep, project_path, 'job_crawler', 'results')

for (dirpath, dirnames, filenames) in os.walk(result_path, followlinks=False):
    if dirpath == result_path:
        all_files = filenames
    else:
        continue

raw_files = []
formatted_files = []

for file in all_files:
    if (file[:6] == 'indeed') or (file[:10] == 'pnc_indeed'):
        raw_files.append(file)
    if file[:9] == 'formatted':
        formatted_files.append(file)

for file in raw_files:
    with open(os.path.join(os.sep, result_path, file)) as raw_file:
        data = json.load(raw_file)
        for row in data:
            row['summary_1'] = ' '.join(row['summary_1'])
            row['summary_1'] = row['summary_1'].replace('\n', '')
            row['summary_2'] = ' '.join(row['summary_2'])
            row['summary_2'] = row['summary_2'].replace('\n', '')
            row['summary_3'] = ' '.join(row['summary_3'])
            row['summary_3'] = row['summary_3'].replace('\n', '')
    with open(os.path.join(os.sep, result_path, str('formatted_' + file)), 'w') as formatted_file:
         json.dump(data, formatted_file)
