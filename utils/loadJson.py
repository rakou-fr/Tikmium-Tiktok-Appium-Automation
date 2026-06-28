# Source - https://stackoverflow.com/q/20199126
# Posted by R.R.C., modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-21, License - CC BY-SA 4.0

import json

def load_json():
    with open('./utils/data/utils.json', 'r', encoding='utf-8') as json_data:
        return json.load(json_data)