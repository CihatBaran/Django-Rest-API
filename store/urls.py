"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from online_store.api_views import ProductList, ProductCreate, ProductRetrieveUpdateDestroy, ProductStatAPIView

urlpatterns = [
    path('api/v1/products', ProductList.as_view()),
    path('api/v1/products/new', ProductCreate.as_view()),
    path('api/v1/products/<int:id>/',
         ProductRetrieveUpdateDestroy.as_view()),
    path('api/v1/products/<int:id>/stats', ProductStatAPIView.as_view()),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
