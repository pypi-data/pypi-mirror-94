# PyAppHub

Python package for Swimlane AppHub API

## Install
run `pip install apphub` from a terminal. This package is available for python 2 and python 3.

## Examples

Below are a few basic python examples to get started.

*Note*: If `sw_` is not found at the beginning of a name, the client will
add it for you.

```python
from apphub import AppHub, save_to_disk, clean_response

ah = AppHub('username', 'password')


#Get all swimlane bundles
get_all_bundles = ah.swimbundles.get()

# Get All versions of a swimlane bundle
get_all_versions = ah.swimbundles.get('sw_carbon_black_defense')

# Get One version of a swimlane bundle
get_one_version = ah.swimbundles.get('sw_carbon_black_defense', '1.1.1')

# Clean up get response to return simple data {'<bundle_name>': [<list_of_versions>]}
clean_response(get_all_bundles)

# Search for bundles
srch_by_field = ah.swimbundles.search(fields={'vendor': "Carbon Black"})
srch_by_text = ah.swimbundles.search(text="Carbon Black")

#Download bundle by version
downloaded_bundle = ah.swimbundles.download('sw_carbon_black_defense', '1.1.1')
 
#Save Latest Download Bundle to disk
save_to_disk('/filepath/carbon_black_defense.zip', downloaded_bundle)
```
