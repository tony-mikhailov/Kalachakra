from django.urls import path
from rest_framework.urls import app_name

from . import views

app_name='saraswati'
urlpatterns = [
    path('', views.index, name='index'),
    # path('edit', views.edit, name='edit'),
    path('today', views.today, name='today'),
    path('month', views.month, name='month'),
    path('<int:year>/<int:month>/<int:day>', views.day, name='day'),
    path('<int:year>/<int:month>/', views.common_month, name='common_month'),
    path('<int:year>/<int:month>/spec', views.common_month, name='common_month_spec'),

    path('api/today', views.today_json, name='today_json'),
    
    path('api/<int:year>/<int:month>/<int:day>', views.day_json, name='day_json'),
    path('api/<int:year>/<int:month>/<int:day>/delete_event', views.delete_event, name='day_delete'),
    path('api/<int:year>/<int:month>/<int:day>/events', views.day_events_json, name='events_json'),
    # path('api/<int:year>/<int:month>/<int:day>/addevent', views.add_event_json),
    
    path('api/<int:year>/<int:month>', views.month_json, name='month_json'),
    path('api/hurals', views.hurals_json, name='hurals_json'),
    path('api/rituals', views.rituals_json, name='rituals_json'),
    path('api/ritual/<int:id>', views.ritual_json, name='ritual_json'),
    path('api/login', views.api_login),
    path('api/logout', views.api_logout),
    path('api/user', views.api_user),

]
