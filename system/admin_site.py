from django.contrib.admin.sites import AdminSite
from django.conf.urls import url
from .views import DashboardMainView, AdminHelpView


class DashboardSite(AdminSite):
    """ Use to allow custom dashboard views."""

    def get_urls(self):
        """Add dashboard view to admin urlconf."""
        urls = super(DashboardSite, self).get_urls()
        del urls[0]
        custom_url = [
            url(r'^$', self.admin_view(DashboardMainView.as_view()),
                name="index"),
            url(r'^help/$', self.admin_view(AdminHelpView.as_view()),
                name="help")
        ]

        return custom_url + urls
