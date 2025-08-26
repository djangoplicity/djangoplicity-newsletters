# newsletters/templatetags/newsletter_extras.py

import pytz
from django import template

register = template.Library()

@register.filter
def dual_timezone_display(value):
    """
    Receives a datetime (release_date) and returns a string with
    the times in MST and EDT, displaying the full date only if it changes
    Example 11 Sept. 2025 4:00 p.m. MST / 7:00 p.m. EDT
    11 Sept. 2025 10:00 p.m. MST / 12 Sept 2025 1:00 a.m. EDT
    """
    if not value:
        return ""

    mst_zone = pytz.timezone("America/Phoenix")
    edt_zone = pytz.timezone("America/New_York")

    mst = value.astimezone(mst_zone)
    edt = value.astimezone(edt_zone)

    if mst.date() == edt.date():
        return (
            mst.strftime("%-d %b. %Y %-I:%M %p MST")
            + " / "
            + edt.strftime("%-I:%M %p %Z")
        )
    else:
        return (
            mst.strftime("%-d %b. %Y %-I:%M %p MST")
            + " / "
            + edt.strftime("%-d %b. %Y %-I:%M %p %Z")
        )
