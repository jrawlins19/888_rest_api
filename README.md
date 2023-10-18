# 888 Interview

## Assumptions made:

* Deletion of objects would be done on a deleted flag and TTL in a real world prod environment
* Filters would be generated from the front end such as text inputs or dropdowns
  * e.g. a search input would generate a request for the object with a filter object {label: x, type: LIKE, value: y}
* For simplicity, all fields are returned when retrieving values from the DB

Made use of as much raw SQL as possible

## Notes
For the DB schemas, any multiple option field such as statuses are stored as integers. e.g. status: 1 = Pending, 2 = Started, 3 = Ended, 4 = Cancelled

Boolean options are stored as integers too. 0 = false, 1 = true

## To build
run install.sh

tests can be run using test.sh, it makes use of a test db

live can be run using start.sh