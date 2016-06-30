import csv
from itertools import chain
from collections import defaultdict, OrderedDict, Counter

from django.db.models import Count, Q

from .models import Call


def time_in_range(start, end, time):
    if start <= end:
        return start <= time <= end
    else:
        return start <= time or time <= end


# Concurrent lines calculation
def concurrent_lines(calls):
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

    # Find the max concurrent lines number for each day
    max_lines_by_day = defaultdict(int)
    for time, call_id in lines_by_time.iteritems():
        day = time.date()
        max_lines_by_day[day] = max(max_lines_by_day[day], len(set(call_id)))

    return max_lines_by_day


# Read the 'UsersExport.csv' file used in calculate_calls_by_country()
def read_users_csv():
    input_file = open('static/UsersExport.csv')
    columns = 'Username,Group'.split(',')

    reader = csv.DictReader(input_file)
    desired_cols = (tuple(row[col] for col in columns) for row in reader)

    return dict(desired_cols)


# Return the 10 most active users of the given Tenant for the given date range
def calculate_user_stats(username, selected_db, start_date, end_date):
    users = Call.objects.using(selected_db). \
        values_list('callername', flat=True). \
        filter(jointime__date__range=(start_date, end_date)).all()

    if username != "All":
        users = users.filter(tenantname=username)

    top_users = (Counter(users).most_common(10))
    return OrderedDict(top_users)


# Return the 10 most active rooms of the given Tenant for the given date range
def calculate_room_stats(username, selected_db, start_date, end_date):
    rooms = Call.objects.using(selected_db). \
                values('conferencename'). \
                annotate(count=Count('uniquecallid', distinct=True)). \
                filter(jointime__date__range=(start_date, end_date)). \
                order_by('-count')[:10]

    if username != "All":
        rooms = Call.objects.using(selected_db). \
                    values('conferencename'). \
                    annotate(count=Count('uniquecallid', distinct=True)). \
                    filter(tenantname=username, jointime__date__range=(start_date, end_date)). \
                    order_by('-count')[:10]

    top_rooms = OrderedDict()
    for room in rooms:
        top_rooms[room['conferencename']] = room['count']

    return top_rooms


# Return the calls made for the given Tenant for the given date range and group by day
def calculate_calls_per_day(username, selected_db, start_date, end_date):
    calls = Call.objects.using(selected_db). \
        filter(jointime__date__range=(start_date, end_date)). \
        extra({'date': "date(jointime)"}). \
        values('date'). \
        annotate(count=Count('uniquecallid', distinct=True))

    if username != "All":
        calls = Call.objects.using(selected_db). \
            filter(jointime__date__range=(start_date, end_date), tenantname=username). \
            extra({'date': "date(jointime)"}). \
            values('date'). \
            annotate(count=Count('uniquecallid', distinct=True))

    calls_per_day = OrderedDict()
    for call in calls:
        calls_per_day[call['date']] = call['count']

    return calls_per_day


# Return the calls made for the given Tenant for the given date range
def calculate_concurrent_lines(username, selected_db, start_date, end_date):
    calls = Call.objects.using(selected_db). \
        values('callername', 'jointime', 'leavetime'). \
        filter(jointime__date__gte=start_date,
               leavetime__date__lte=end_date,
               callstate="COMPLETED"). \
        filter(~Q(callername__contains="QUALITY"))

    if username != "All":
        calls = Call.objects.using(selected_db). \
            values('callername', 'jointime', 'leavetime'). \
            filter(tenantname=username,
                   jointime__date__gte=start_date,
                   leavetime__date__lte=end_date,
                   callstate="COMPLETED"). \
            filter(~Q(callername__contains="QUALITY"))

    return concurrent_lines(calls)


# Return CallerIDs for the given Tenant for the given date range
def calculate_calls_by_country(username, selected_db, start_date, end_date):
    calls = Call.objects.using(selected_db). \
        values_list('callerid', flat=True). \
        filter(jointime__date__gte=start_date, leavetime__date__lte=end_date).all()

    if username != "All":
        calls = calls.filter(tenantname=username)

    # Create a dictionary from the 'UsersExport.csv' file
    users_dict = read_users_csv()

    # Return a count of the countries and filter out Guests with undefined values
    return Counter([users_dict.get(caller) for caller in calls if caller != 'Guest'])


# Return platforms for the given Tenant for the given date range
def calculate_platform_stats(username, selected_db, start_date, end_date):
    platforms = Call.objects.using(selected_db). \
        values_list('applicationname', flat=True). \
        filter(jointime__date__range=(start_date, end_date)).all()

    if username != "All":
        platforms = platforms.filter(tenantname=username)

    return Counter(filter(None, platforms))


# Return Operating Systems for the given Tenant for the given date range
def calculate_os_stats(username, selected_db, start_date, end_date):
    os = Call.objects.using(selected_db). \
        values_list('applicationos', flat=True). \
        filter(jointime__date__range=(start_date, end_date)).all()

    if username != "All":
        os = os.filter(tenantname=username)

    return Counter(filter(None, os))


# Return a combined report for JISC and Gateway4 tenants
def generate_cdr_report(selected_db, start_date, end_date):
    cdr = Call.objects.using(selected_db). \
        filter(jointime__date__range=(start_date, end_date)). \
        filter(Q(tenantname="JISC") | Q(tenantname="Gateway4")).all()
    return cdr


# Return all the available tenants in order to populate the Tenant drop-down menu
def get_tenants():
    ajenta_tenants = list(Call.objects.using('ajenta_io').values_list('tenantname', flat=True).distinct())
    oydiv_tenants = list(Call.objects.using('platformc').values_list('tenantname', flat=True).distinct())

    tenants = ajenta_tenants + oydiv_tenants
    tenants.append("All - ajenta.io")
    tenants.append("All - platformc")
    tenants_list = [(tenant, tenant) for tenant in set(tenants)]

    return sorted(tenants_list, key=lambda (a, b): (a.lower(), b))
