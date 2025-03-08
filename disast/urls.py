from django.urls import path
from . import views

urlpatterns = [
    path('signup/csignup/', views.csignup, name='csignup'),
    path('signup/asignup/', views.asignup, name='asignup'),
    path('login/', views.login_view, name='login'),
    path('citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    path('agency/', views.agency_dashboard, name='agency_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path("scrape/", views.scrape_and_update_disasters, name="scrape_disasters"),
    path("dashboard/", views.disaster_dashboard, name="disaster_dashboard"),
    path("disasters/<str:date>/", views.filter_disasters_by_date, name="disasters_by_date"),
    path("add_disaster/", views.add_disaster, name="add_disaster"),
    path("scrape_disasters/", views.scrape_and_update_disasters, name="scrape_disasters"),
     # Geospatial Visualization
    path('map/', views.disaster_map_view, name='disaster_map')
   
]
