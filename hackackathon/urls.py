# Copyright (C) 2025-now  p.fernandezf <p@fernandezf.es> & iago.rivas <delthia@delthia.com>

from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Hackackathon Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("gestion.urls")),
]
