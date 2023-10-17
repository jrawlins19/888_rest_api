from db import run_query, build_update_query


# Runs an SQL query to get active child objects (Sports -> Events, Events -> Selections)
# if there are active children, set the parent to active, and inactive if no children are found
def check_parent_active(table: str, parent_table: str, column_name: str, parent_id: int):
    query = "SELECT id FROM {0} WHERE {1} = {2} AND active = 1".format(table, column_name, parent_id)
    items = run_query(query)
    if len(items) >= 1:
        update_parent_active(parent_table, parent_id, 1)
    else:
        update_parent_active(parent_table, parent_id, 0)


# Updates the parent row to be inactive/active
def update_parent_active(table: str, parent_id: int, is_active: int):
    query = build_update_query(table, {"active": is_active}, ["id == {0}".format(parent_id)])
    items = run_query(query)
    # if we updated events here, we also need to check sports
    if table == 'events':
        check_parent_active(table, 'sports', 'sport', items[0][5])
