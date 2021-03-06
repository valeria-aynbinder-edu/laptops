from django.urls import path

from . import views
from .views import LaptopsView

urlpatterns = [
    path("orders/", views.orders_v2),
    path("stats/totals", views.total_stats),
    path("stats/best_customers", views.best_customers),
    path("laptops", LaptopsView.as_view())
    # path("restaurants/", views.RestaurantsList.as_view()),
    # path("restaurants/<int:pk>", views.restaurant_details),
    # path("reviews/", views.reviews), # filter by user_id
    #restaurants/<int:pk>/reviews
]
