#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright 2016 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import time
import urllib2
import feedparser


BITBUCKET = "https://bitbucket.org/lazka/quodlibet/downloads/"

RELEASES = [
    "3.7.1 (2016-09-25)",
    "3.7.0 (2016-08-27)",
    "3.6.2 (2016-05-24)",
    "3.6.1 (2016-04-05)",
    "3.6.0 (2016-03-24)",
    "3.5.3 (2016-01-16)",
    "3.5.2 (2016-01-13)",
    "3.5.1 (2015-10-14)",
    "3.5.0 (2015-10-07)",
    "3.4.1 (2015-05-24)",
    "3.4.0 (2015-04-09)",
    "3.3.1 (2015-01-10)",
    "3.3.0 (2014-12-31)",
    "3.2.2 (2014-10-03)",
    "3.2.1 (2014-08-16)",
    "3.2.0 (2014-08-01)",
]


def release_link(version):
    return ("https://quodlibet.readthedocs.io/en/latest/"
            "changelog.html#release-%s" % version.replace(".", "-"))


def release_date(date):
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                         time.strptime(date, "%Y-%m-%d"))


BUILDS = {
    "osx-quodlibet": {
        "title": "Quod Libet (OS X)",
        "os": "",
        "releases": [
            ("3.7.1", "0", BITBUCKET + "QuodLibet-%s.dmg"),
            ("3.7.0", "0", BITBUCKET + "QuodLibet-%s.dmg"),
            ("3.6.1", "0", BITBUCKET + "QuodLibet-%s.zip"),
            ("3.5.2", "1", BITBUCKET + "QuodLibet-%s-v2.zip"),
            ("3.5.2", "0", BITBUCKET + "QuodLibet-%s.zip"),
            ("3.5.1", "0", BITBUCKET + "QuodLibet-%s.zip"),
            ("3.5.0", "1", BITBUCKET + "QuodLibet-%s-v2.zip"),
            ("3.5.0", "0", BITBUCKET + "QuodLibet-%s.zip"),
            ("3.4.1", "1", BITBUCKET + "QuodLibet-%s.zip"),
            ("3.4.1", "0", BITBUCKET + "QuodLibet-%s.zip"),
        ],
    },
    "osx-exfalso": {
        "title": "Ex Falso (OS X)",
        "os": "",
        "releases": [
            ("3.7.1", "0", BITBUCKET + "ExFalso-%s.dmg"),
            ("3.7.0", "0", BITBUCKET + "ExFalso-%s.dmg"),
            ("3.6.1", "0", BITBUCKET + "ExFalso-%s.zip"),
            ("3.5.2", "1", BITBUCKET + "ExFalso-%s-v2.zip"),
            ("3.5.2", "0", BITBUCKET + "ExFalso-%s.zip"),
            ("3.5.1", "0", BITBUCKET + "ExFalso-%s.zip"),
            ("3.5.0", "1", BITBUCKET + "ExFalso-%s-v2.zip"),
            ("3.5.0", "0", BITBUCKET + "ExFalso-%s.zip"),
            ("3.4.1", "1", BITBUCKET + "ExFalso-%s.zip"),
            ("3.4.1", "0", BITBUCKET + "ExFalso-%s.zip"),
        ],
    },
    "windows": {
        "title": "Quod Libet / Ex Falso (Windows)",
        "os": "windows",
        "releases": [
            ("3.7.1", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
            ("3.7.0", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
            ("3.6.1", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
            ("3.6.0", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
            ("3.5.2", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
            ("3.5.1", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
            ("3.5.0", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
            ("3.4.1", "0", BITBUCKET + "quodlibet-%s-installer.exe"),
        ],
    },
    "windows-portable": {
        "title": "Quod Libet / Ex Falso (Windows Portable)",
        "os": "windows",
        "releases": [
            ("3.7.1", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
            ("3.7.0", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
            ("3.6.1", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
            ("3.6.0", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
            ("3.5.2", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
            ("3.5.1", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
            ("3.5.0", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
            ("3.4.1", "0", BITBUCKET + "quodlibet-%s-portable.exe"),
        ],
    },
    "default": {
        "title": "Quod Libet / Ex Falso",
        "os": "linux",
        "releases": [
            ("3.7.1", "0", ""),
            ("3.7.0", "0", ""),
            ("3.6.2", "0", ""),
            ("3.6.1", "0", ""),
            ("3.6.0", "0", ""),
            ("3.5.2", "0", ""),
            ("3.5.1", "0", ""),
            ("3.5.0", "0", ""),
            ("3.4.1", "0", ""),
        ],
    },
}

TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" \
xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle" \
xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>%(title)s</title>
    <link>%(link)s</link>
%(items)s\
</channel>
</rss>
"""

ITEM = """\
    <item>
      <title>Version %(version_desc)s</title>
      <sparkle:releaseNotesLink>
        %(changelog)s
      </sparkle:releaseNotesLink>
      <link>%(changelog)s</link>
      <pubDate>%(date)s</pubDate>
      <enclosure url="%(url)s" %(os)s sparkle:version="%(version_key)s" \
length="%(length)s" type="application/octet-stream" />
    </item>
"""


def main():
    release_dates = {}
    for r in RELEASES:
        version, date = r.split()
        date = release_date(date.strip("()"))
        release_dates[version] = date

    for type_id, type_ in BUILDS.items():
        items = []
        title = type_["title"]
        os_ = type_["os"]
        for version, build, url in type_["releases"]:
            print type_id, version
            try:
                url = url % version
            except TypeError:
                pass
            if url:
                r = urllib2.urlopen(url)
                length = r.info().get("Content-Length", "0")
                r.close()
            else:
                length = "0"
            version_desc = version
            version_key = version
            if build != "0":
                version_desc += " (v%d)" % (int(build) + 1, )
                version_key += "." + build
            date = release_dates[version]
            item = ITEM % {
                "version_desc": version_desc,
                "version_key": version_key,
                "length": length,
                "url": url,
                "date": date,
                "changelog": release_link(version),
                "os": ("sparkle:os=\"%s\"" % os_) if os_ else "",
            }
            items.append(item)

        result = TEMPLATE % {
            "title": title,
            "link": "https://quodlibet.readthedocs.io/en/latest/downloads.html",
            "items": "".join(items),
        }

        path = type_id + ".rss"
        with open(path, "wb") as h:
            h.write(result)
        feedparser.parse(path)

if __name__ == "__main__":
    main()
