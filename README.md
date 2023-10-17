# 888 Interview

## Assumptions made:

* Deletion of objects would be done on a deleted flag and TTL in a real world prod environment
* Filters would be generated from the front end such as text inputs or dropdowns
  * e.g. a search input would generate a request for the object with a filter object {label: x, type: LIKE, value: y}


Made use of as much raw SQL as possible

## To build
run install.sh

tests can be run using test.sh, it makes use of a test db

live can be run using start.sh