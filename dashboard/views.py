import csv
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from .forms import UserForm, AdminForm
from .queries import *
from .graphs import generate_graph, generate_pie_chart
from .utils import merge_two_dicts

# Dictionary of reports and the equivalent view functions.
report_dict = {
    'User Stats': 'user_stats',
    'Room Stats': 'room_stats',
    'Calls per day': 'calls_per_day',
    'Maximum concurrent lines': 'concurrent_lines',
    'Calls by country': 'calls_by_country',
    'Platform Stats': 'platform_stats',
    'OS Stats': 'os_stats',
    'Download CDR Report': 'cdr_report',
}


@login_required
def index(request):
    #  If this is a POST request, then process the form data.
    if request.method == 'POST':
        if request.user.is_staff:
            form = AdminForm(request.POST)
            form.fields['tenant'].choices = get_tenants()
            request.session['username'] = request.POST.get('tenant')
        else:
            form = UserForm(request.POST)
            request.session['username'] = request.user.username

        if form.is_valid():
            # Redirect to the right view function, based on the button pressed.
            try:
                requested_report = report_dict[request.POST['report']]
                request.session['start_date'] = request.POST.get('start_date')
                request.session['end_date'] = request.POST.get('end_date')
                request.session['selected_db'] = 'platformc'

                if request.session['start_date'] < '2016-09-15':
                    request.session['both_dbs'] = True
                else:
                    request.session['both_dbs'] = False

                return redirect(requested_report)
            except Exception as exception:
                print exception

    # If it is a GET, then create a blank form.
    else:
        if request.user.is_staff:
            form = AdminForm()
            form.fields['tenant'].choices = get_tenants()
        else:
            form = UserForm()

        # Set form fields to previous values.
        # If this is the first time the form is loaded,
        # then the session variables will be empty and therefore the error is ignored.
        try:
            form.fields['start_date'].initial = datetime.strptime(request.session['start_date'], '%d/%m/%Y')
            form.fields['end_date'].initial = datetime.strptime(request.session['end_date'], '%d/%m/%Y')
            form.fields['tenant'].initial = request.session['username']
        except(AssertionError, KeyError):
            pass

    return render(request, 'index.html', {'form': form})


@login_required
@permission_required('authentication.can_view_stats', raise_exception=True)
def user_stats(request):
    # Session variables can be empty if the user types the 'user-stats' URL,
    # without having sent a POST request from the form in the index page.
    # In order to avoid this error, the user is redirected to the index page
    # until a proper POST request is sent.
    try:
        username = request.session['username']
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    users = calculate_user_stats(username,
                                 selected_db,
                                 datetime.strptime(start_date, '%d/%m/%Y'),
                                 datetime.strptime(end_date, '%d/%m/%Y')
                                 )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_users = calculate_user_stats(username,
                                         selected_db,
                                         datetime.strptime(start_date, '%d/%m/%Y'),
                                         datetime.strptime(end_date, '%d/%m/%Y')
                                         )
        users = merge_two_dicts(users, old_users)

    title = '10 most active users'

    (ids, graph_json) = generate_graph(users, title, username, start_date, end_date)

    return render(request, 'stats/user_stats.html', {'ids': ids, 'graph_json': graph_json})


@login_required
@permission_required('authentication.can_view_stats', raise_exception=True)
def room_stats(request):
    # Similar as above. Please check the comment in user_stats() where the logic is explained.
    try:
        username = request.session['username']
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    rooms = calculate_room_stats(username,
                                 selected_db,
                                 datetime.strptime(start_date, '%d/%m/%Y'),
                                 datetime.strptime(end_date, '%d/%m/%Y')
                                 )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_rooms = calculate_room_stats(username,
                                         selected_db,
                                         datetime.strptime(start_date, '%d/%m/%Y'),
                                         datetime.strptime(end_date, '%d/%m/%Y')
                                         )
        rooms = merge_two_dicts(rooms, old_rooms)

    title = '10 most active rooms'

    (ids, graph_json) = generate_graph(rooms, title, username, start_date, end_date)

    return render(request, 'stats/room_stats.html', {'ids': ids, 'graph_json': graph_json})


@login_required
@permission_required('authentication.can_view_stats', raise_exception=True)
def calls_per_day(request):
    # Similar as above. Please check the comment in user_stats() where the logic is explained.
    try:
        username = request.session['username']
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    calls = calculate_calls_per_day(username,
                                    selected_db,
                                    datetime.strptime(start_date, '%d/%m/%Y'),
                                    datetime.strptime(end_date, '%d/%m/%Y')
                                    )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_calls = calculate_calls_per_day(username,
                                            selected_db,
                                            datetime.strptime(start_date, '%d/%m/%Y'),
                                            datetime.strptime(end_date, '%d/%m/%Y')
                                            )
        calls = merge_two_dicts(calls, old_calls)

    title = 'Calls per day'

    (ids, graph_json) = generate_graph(calls, title, username, start_date, end_date)

    return render(request, 'stats/calls_per_day.html', {'ids': ids, 'graph_json': graph_json})


@login_required
@permission_required('authentication.can_view_stats', raise_exception=True)
def concurrent_lines(request):
    # Similar as above. Please check the comment in user_stats() where the logic is explained.
    try:
        username = request.session['username']
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    lines = calculate_concurrent_lines(username,
                                       selected_db,
                                       datetime.strptime(start_date, '%d/%m/%Y'),
                                       datetime.strptime(end_date, '%d/%m/%Y')
                                       )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_lines = calculate_concurrent_lines(username,
                                               selected_db,
                                               datetime.strptime(start_date, '%d/%m/%Y'),
                                               datetime.strptime(end_date, '%d/%m/%Y')
                                               )
        lines = merge_two_dicts(lines, old_lines)

    title = 'Maximum concurrent lines'

    (ids, graph_json) = generate_graph(lines, title, username, start_date, end_date)

    return render(request, 'stats/concurrent_lines.html', {'ids': ids, 'graph_json': graph_json})


@login_required
@permission_required('authentication.can_view_stats', raise_exception=True)
def platform_stats(request):
    # Similar as above. Please check the comment in user_stats() where the logic is explained.
    try:
        username = request.session['username']
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    platforms = calculate_platform_stats(username,
                                         selected_db,
                                         datetime.strptime(start_date, '%d/%m/%Y'),
                                         datetime.strptime(end_date, '%d/%m/%Y')
                                         )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_platforms = calculate_platform_stats(username,
                                                 selected_db,
                                                 datetime.strptime(start_date, '%d/%m/%Y'),
                                                 datetime.strptime(end_date, '%d/%m/%Y')
                                                 )
        platforms = merge_two_dicts(platforms, old_platforms)

    title = 'Vidyo Platform stats'

    (ids, graph_json) = generate_pie_chart(platforms, title, username, start_date, end_date)

    return render(request, 'stats/platform_stats.html', {'ids': ids, 'graph_json': graph_json})


@login_required
@permission_required('authentication.can_view_stats', raise_exception=True)
def os_stats(request):
    # Similar as above. Please check the comment in user_stats() where the logic is explained.
    try:
        username = request.session['username']
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    os = calculate_os_stats(username,
                            selected_db,
                            datetime.strptime(start_date, '%d/%m/%Y'),
                            datetime.strptime(end_date, '%d/%m/%Y')
                            )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_os = calculate_os_stats(username,
                                    selected_db,
                                    datetime.strptime(start_date, '%d/%m/%Y'),
                                    datetime.strptime(end_date, '%d/%m/%Y')
                                    )
        os = merge_two_dicts(os, old_os)

    title = 'OS stats'

    (ids, graph_json) = generate_pie_chart(os, title, username, start_date, end_date)

    return render(request, 'stats/os_stats.html', {'ids': ids, 'graph_json': graph_json})


@login_required
@permission_required('authentication.can_view_stats', raise_exception=True)
@user_passes_test(lambda u: u.username == 'ActionAid')
def calls_by_country(request):
    # Similar as above. Please check the comment in user_stats() where the logic is explained.
    try:
        username = request.session['username']
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    countries = calculate_calls_by_country(username,
                                           selected_db,
                                           datetime.strptime(start_date, '%d/%m/%Y'),
                                           datetime.strptime(end_date, '%d/%m/%Y')
                                           )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_countries = calculate_calls_by_country(username,
                                                   selected_db,
                                                   datetime.strptime(start_date, '%d/%m/%Y'),
                                                   datetime.strptime(end_date, '%d/%m/%Y')
                                                   )
        countries = merge_two_dicts(countries, old_countries)

    title = 'Calls per country'

    (ids, graph_json) = generate_graph(countries, title, username, start_date, end_date)

    return render(request, 'stats/calls_by_country.html', {'ids': ids, 'graph_json': graph_json})


@login_required
@user_passes_test(lambda u: u.username == 'Jisc')
def cdr_report(request):
    # Similar as above. Please check the comment in user_stats() where the logic is explained.
    try:
        selected_db = request.session['selected_db']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
    except KeyError:
        return redirect(index)

    report = generate_cdr_report(selected_db,
                                 datetime.strptime(start_date, '%d/%m/%Y'),
                                 datetime.strptime(end_date, '%d/%m/%Y')
                                 )

    if request.session['both_dbs']:
        selected_db = 'ajenta.io'
        old_report = generate_cdr_report(selected_db,
                                         datetime.strptime(start_date, '%d/%m/%Y'),
                                         datetime.strptime(end_date, '%d/%m/%Y')
                                         )
        report = merge_two_dicts(report, old_report)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=CDR.csv'

    fields = report.model._meta.fields

    writer = csv.writer(response)
    column_names = [field.name for field in fields]

    writer.writerow(column_names)

    for obj in report:
        writer.writerow([getattr(obj, column) for column in column_names])

    return response
