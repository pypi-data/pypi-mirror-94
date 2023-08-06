from django.utils.translation import gettext as _

from health_check.backends import BaseHealthCheckBackend

from aleksis.core.models import DataCheckResult


class DataChecksHealthCheckBackend(BaseHealthCheckBackend):
    """Checks whether there are unresolved data problems."""

    critical_service = False

    def check_status(self):
        if DataCheckResult.objects.filter(solved=False).exists():
            self.add_error(_("There are unresolved data problems."))

    def identifier(self):
        return self.__class__.__name__
