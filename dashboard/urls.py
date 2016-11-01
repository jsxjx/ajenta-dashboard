from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user-stats', views.user_stats, name='user_stats'),
    url(r'^room-stats', views.room_stats, name='room_stats'),
    url(r'^calls-per-day', views.calls_per_day, name='calls_per_day'),
    url(r'^participants-per-call', views.participants_per_call, name='participants_per_call'),
    url(r'^concurrent-lines', views.concurrent_lines, name='concurrent_lines'),
    url(r'^concurrent-gateway-ports', views.concurrent_gateway_ports, name='concurrent_gateway_ports'),
    url(r'^platform-stats', views.platform_stats, name='platform_stats'),
    url(r'^os-stats', views.os_stats, name='os_stats'),
    url(r'^current-calls', views.current_calls, name='current_calls'),
    url(r'^calls-by-country', views.calls_by_country, name='calls_by_country'),
    url(r'^cdr', views.cdr_report, name='cdr_report'),
]
