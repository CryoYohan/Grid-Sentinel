from types import SimpleNamespace
from unittest.mock import patch

from rss_feed import RSSFeed


def test_fetch_yellow_red_alerts_returns_matching_entries():
    entries = [
        SimpleNamespace(title="Yellow Alert declared", summary="Grid status update", link="yellow"),
        SimpleNamespace(title="Routine maintenance", summary="No alert", link="ignored"),
        SimpleNamespace(title="System Red Alert", summary="Supply is critical", link="red"),
    ]

    with patch("rss_feed.feedparser.parse", return_value=SimpleNamespace(entries=entries)):
        alerts = RSSFeed().fetch_yellow_red_alerts()

    assert [alert["url"] for alert in alerts] == ["yellow", "red"]
    assert alerts[0]["text"] == "Yellow Alert declared Grid status update"


def test_fetch_yellow_red_alerts_ignores_unrelated_entries():
    entries = [SimpleNamespace(title="Power advisory", summary="Balamban", link="ignored")]

    with patch("rss_feed.feedparser.parse", return_value=SimpleNamespace(entries=entries)):
        alerts = RSSFeed().fetch_yellow_red_alerts()

    assert alerts == []
