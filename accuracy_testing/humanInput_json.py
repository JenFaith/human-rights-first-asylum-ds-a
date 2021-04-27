import pandas as pd


file_name = ''

test_data = pd.read_csv(file_name)
test_data.columns = ['old_idx', 'uuid', 'aws_link', 'data_entry_name',
                     'application', 'date', 'country_of_origin',
                     'panel_members', 'outcome', 'protected_grounds',
                     'based_violence', 'keywords', 'references',
                     'gender', 'indigenous', 'applicant_language',
                     'is_credible',	'is_one_year',	'city_origin',
                     'state_origin', 'notes_random', 'empty', 'empty1']

test_data.drop(['old_idx', 'empty', 'empty1', 'data_entry_name', 'aws_link', 'notes_random'],
    axis=1, inplace=True)


# Remove '.pdf' from UUID
def trim_pdf(s):
    return s[:-4]


# Standardize for later analysis
def gender_prep(s):
    try:
        if s == 'n/a':
            return ''
        return s.lower()
    except AttributeError:
        return ''


# Apply '.pdf' removal to uuid column
test_data['uuid'] = test_data['uuid'].apply(trim_pdf)
# Apply empty string to n/a values
test_data['gender'] = test_data['gender'].apply(gender_prep)


json_file = test_data.to_json(orient='records')


# Write the JSON file to disk to allow for passing into the API
# This data should always represent the 'truth' to test against
with open('human_ocr.json', 'w') as f:
    f.write(json_file)


