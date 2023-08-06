from datetime import date
from typing import Union

from django.contrib.sites.managers import CurrentSiteManager as _CurrentSiteManager
from django.db.models import QuerySet

from calendarweek import CalendarWeek


class CurrentSiteManagerWithoutMigrations(_CurrentSiteManager):
    """CurrentSiteManager for auto-generating managers just by query sets."""

    use_in_migrations = False


class DateRangeQuerySetMixin:
    """QuerySet with custom query methods for models with date ranges.

    Filterable fields: date_start, date_end
    """

    def within_dates(self, start: date, end: date):
        """Filter for all objects within a date range."""
        return self.filter(date_start__lte=end, date_end__gte=start)

    def in_week(self, wanted_week: CalendarWeek):
        """Filter for all objects within a calendar week."""
        return self.within_dates(wanted_week[0], wanted_week[6])

    def on_day(self, day: date):
        """Filter for all objects on a certain day."""
        return self.within_dates(day, day)


class SchoolTermQuerySet(QuerySet, DateRangeQuerySetMixin):
    """Custom query set for school terms."""


class SchoolTermRelatedQuerySet(QuerySet):
    """Custom query set for all models related to school terms."""

    def within_dates(self, start: date, end: date) -> "SchoolTermRelatedQuerySet":
        """Filter for all objects within a date range."""
        return self.filter(school_term__date_start__lte=end, school_term__date_end__gte=start)

    def in_week(self, wanted_week: CalendarWeek) -> "SchoolTermRelatedQuerySet":
        """Filter for all objects within a calendar week."""
        return self.within_dates(wanted_week[0], wanted_week[6])

    def on_day(self, day: date) -> "SchoolTermRelatedQuerySet":
        """Filter for all objects on a certain day."""
        return self.within_dates(day, day)

    def for_school_term(self, school_term: "SchoolTerm") -> "SchoolTermRelatedQuerySet":
        return self.filter(school_term=school_term)

    def for_current_school_term_or_all(self) -> "SchoolTermRelatedQuerySet":
        """Get all objects related to current school term.

        If there is no current school term, it will return all objects.
        """
        from aleksis.core.models import SchoolTerm

        current_school_term = SchoolTerm.current
        if current_school_term:
            return self.for_school_term(current_school_term)
        else:
            return self

    def for_current_school_term_or_none(self) -> Union["SchoolTermRelatedQuerySet", None]:
        """Get all objects related to current school term.

        If there is no current school term, it will return `None`.
        """
        from aleksis.core.models import SchoolTerm

        current_school_term = SchoolTerm.current
        if current_school_term:
            return self.for_school_term(current_school_term)
        else:
            return None


class GroupManager(CurrentSiteManagerWithoutMigrations):
    """Manager adding specific methods to groups."""

    def get_queryset(self):
        """Ensure all related data is loaded as well."""
        return super().get_queryset().select_related("school_term")


class GroupQuerySet(SchoolTermRelatedQuerySet):
    pass
