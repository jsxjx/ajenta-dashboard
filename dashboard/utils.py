import csv
from collections import defaultdict, OrderedDict
from itertools import chain


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict and sort it by value."""
    z = x.copy()
    z.update(y)
    return OrderedDict(sorted(z.items(), key=lambda x: x[1], reverse=True))


def read_users_csv():
    """Read the 'UsersExport.csv' file used in calculate_calls_by_country()."""
    input_file = open('static/UsersExport.csv')
    columns = 'Username,Group'.split(',')

    reader = csv.DictReader(input_file)
    desired_cols = (tuple(row[col] for col in columns) for row in reader)

    return dict(desired_cols)


def time_in_range(start, end, time):
    if start <= end:
        return start <= time <= end
    else:
        return start <= time or time <= end


def concurrent_lines(calls):
    """Concurrent lines calculation."""
    calls_dict = defaultdict(list)

    # Create a dictionary of caller names and join/leave times
    for call in calls:
        caller_name = call['callername']
        join_time = call['jointime']
        leave_time = call['leavetime']
        calls_dict[caller_name] += (join_time, leave_time)

    # Check if line was active at the given time
    def line_active_at(call_id, time):
        time_pairs = calls_dict.get(call_id)
        for pair in xrange(0, len(time_pairs), 2):
            if time_in_range(time_pairs[pair], time_pairs[pair + 1], time):
                return True

    times_list = list(chain.from_iterable(calls_dict.values()))

    # Create a list with the active lines for each time
    lines_by_time = defaultdict(list)
    for time in times_list:
        lines_by_time[time] = [call_id for call_id in calls_dict if line_active_at(call_id, time)]

    return lines_by_time


def concurrent_lines_per_day(calls):
    """Find the max concurrent lines number for each day"""
    lines_by_time = concurrent_lines(calls)

    max_lines_by_day = defaultdict(int)
    for time, call_id in lines_by_time.iteritems():
        day = time.date()
        max_lines_by_day[day] = max(max_lines_by_day[day], len(set(call_id)))

    return max_lines_by_day


def participants_per_call(calls, unique_call_id):
    """Find the max concurrent lines number for each UniqueCallID"""
    lines_by_time = concurrent_lines(calls)

    max_lines_by_call = defaultdict(int)
    for time, caller_name in lines_by_time.iteritems():
        max_lines_by_call[unique_call_id] = max(max_lines_by_call[unique_call_id], len(set(caller_name)))

    return max_lines_by_call[unique_call_id]
