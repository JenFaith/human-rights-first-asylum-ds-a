# To prevent PANDAS from being installed into the project! This is for local use only.
try:
    import pandas as pd
except ModuleNotFoundError as e:
    print(f"{e.name} missing; install package locally, not project wide.")



"""
Get csv from human input to check values of OCR. Outputs into JSON where feature is
main key. Each feature has dictionary with key as uuid and value of feature associated with uuid.

EXAMPLE:
--------
{
  "gender": {
    "140194281-Ali-Fares-A047-654-200-BIA-Apr-30-2013": "male",
    "165227167-K-O-A-BIA-Aug-27-2013": "female",
    . . .
    },
  . . .
}
"""


test_data = pd.read_csv('manual-data-extraction-allcases.csv')
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

# Basic json records pattern
test_data.set_index('uuid', inplace=True)
json_file = test_data.to_json(orient='columns')


# Write the JSON file to disk to allow for passing into the API
# This data should always represent the 'truth' to test against
with open('human_ocr.json', 'w') as f:
    f.write(json_file)


