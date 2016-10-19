from collections import OrderedDict, Counter

from django.db.models import Count, Q

from .models import Call
from .utils import read_users_csv, concurrent_lines


def calculate_user_stats(username, selected_db, start_date, end_date):
    """Return the 10 most active users of the given Tenant for the given date range."""
    users = Call.objects.using(selected_db). \
        values_list('callername', flat=True). \
        filter(jointime__date__range=(start_date, end_date)).all()

    if username != "All":
        users = users.filter(tenantname=username)

    top_users = (Counter(users).most_common(10))
    return OrderedDict(top_users)


def calculate_room_stats(username, selected_db, start_date, end_date):
    """Return the 10 most active rooms of the given Tenant for the given date range."""
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


def calculate_calls_per_day(username, selected_db, start_date, end_date):
    """Return the calls made for the given Tenant in the given date range and then group by day."""
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


def calculate_concurrent_lines(username, selected_db, start_date, end_date):
    """Return the calls made for the given Tenant in the given date range."""
    calls = Call.objects.using(selected_db). \
        values('callername', 'jointime', 'leavetime'). \
        filter(~Q(applicationname="VidyoReplay"),
               ~Q(applicationname="VidyoGateway"),
               jointime__date__gte=start_date,
               leavetime__date__lte=end_date,
               callstate="COMPLETED")

    if username != "All":
        calls = Call.objects.using(selected_db). \
            values('callername', 'jointime', 'leavetime'). \
            filter(~Q(applicationname="VidyoReplay"),
                   ~Q(applicationname="VidyoGateway"),
                   tenantname=username,
                   jointime__date__gte=start_date,
                   leavetime__date__lte=end_date,
                   callstate="COMPLETED")

    return concurrent_lines(calls)


def calculate_calls_by_country(username, selected_db, start_date, end_date):
    """Return CallerIDs for the given Tenant in the given date range."""
    calls = Call.objects.using(selected_db). \
        values_list('callerid', flat=True). \
        filter(jointime__date__gte=start_date, leavetime__date__lte=end_date).all()

    if username != "All":
        calls = calls.filter(tenantname=username)

    # Create a dictionary from the 'UsersExport.csv' file
    users_dict = read_users_csv()

    # Return a count of the countries and filter out Guests with undefined values
    return Counter([users_dict.get(caller) for caller in calls if caller != 'Guest'])


def calculate_platform_stats(username, selected_db, start_date, end_date):
    """Return Vidyo platforms used by the Tenant in the given date range."""
    platforms = Call.objects.using(selected_db). \
        values_list('applicationname', flat=True). \
        filter(jointime__date__range=(start_date, end_date)).all()

    if username != "All":
        platforms = platforms.filter(tenantname=username)

    return Counter(filter(None, platforms))


def calculate_os_stats(username, selected_db, start_date, end_date):
    """Return Operating Systems used byt the Tenant in the given date range."""
    os = Call.objects.using(selected_db). \
        values_list('applicationos', flat=True). \
        filter(jointime__date__range=(start_date, end_date)).all()

    if username != "All":
        os = os.filter(tenantname=username)

    return Counter(filter(None, os))


def generate_cdr_report(selected_db, start_date, end_date):
    """Return a combined report for JISC and Gateway4 tenants."""
    cdr = Call.objects.using(selected_db). \
        filter(jointime__date__range=(start_date, end_date)). \
        filter(Q(tenantname="JISC") | Q(tenantname="Gateway4")).all()
    return cdr


def calculate_concurrent_gateway_ports(username, selected_db, start_date, end_date):
    """Return the calls made for the given Tenant in the given date range."""
    calls = Call.objects.using(selected_db). \
        values('callername', 'jointime', 'leavetime'). \
        filter(applicationname="VidyoGateway",
               jointime__date__gte=start_date,
               leavetime__date__lte=end_date,
               callstate="COMPLETED")

    if username != "All":
        calls = Call.objects.using(selected_db). \
            values('callername', 'jointime', 'leavetime'). \
            filter(applicationname="VidyoGateway",
                   tenantname=username,
                   jointime__date__gte=start_date,
                   leavetime__date__lte=end_date,
                   callstate="COMPLETED")

    return concurrent_lines(calls)


def get_tenants():
    """Return all the available tenants in order to populate the Tenant drop-down menu."""
    ajenta_tenants = list(Call.objects.using('ajenta.io').values_list('tenantname', flat=True).distinct())
    oydiv_tenants = list(Call.objects.using('platformc').values_list('tenantname', flat=True).distinct())

    tenants = ajenta_tenants + oydiv_tenants
    tenants.append("All - ajenta.io")
    tenants.append("All - platformc")
    tenants_list = [(tenant, tenant) for tenant in set(tenants)]

    return sorted(tenants_list, key=lambda (a, b): (a.lower(), b))
