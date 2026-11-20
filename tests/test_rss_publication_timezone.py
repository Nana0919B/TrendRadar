"""RSS publication times retain UTC after feedparser normalization."""

from trendradar.crawler.rss.parser import RSSParser


def test_rss_offset_is_normalized_without_losing_timezone():
    items = RSSParser().parse("""<rss version="2.0"><channel><title>News</title>
        <link>https://example.com</link><description>News</description><item>
        <title>Apple news</title><link>https://example.com/apple</link>
        <pubDate>Fri, 20 Nov 2026 12:00:00 +0800</pubDate>
        </item></channel></rss>""")
    assert items[0].published_at == "2026-11-20T04:00:00+00:00"


def test_missing_publication_time_stays_unknown():
    assert RSSParser()._parse_date({}) is None
