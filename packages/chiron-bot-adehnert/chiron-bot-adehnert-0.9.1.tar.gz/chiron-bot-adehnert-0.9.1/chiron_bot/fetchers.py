# -*- coding: utf-8 -*-

"""
Standard chiron fetcher functions
"""

from __future__ import print_function, unicode_literals

import os
import re
import sys
from random import choice

#pylint:disable=c-extension-no-member
from lxml import etree
import requests

if sys.version_info.major < 3:
    from backports import csv #pylint:disable=import-error
else:
    import csv

try:
    unichr
except NameError as exc: # not available in Py3
    unichr = chr #pylint:disable=invalid-name,redefined-builtin

parser = etree.HTMLParser(encoding='UTF-8') #pylint:disable=invalid-name

# I feel like it's clearer to handle the known/unknown split explicitly
# with if/else, rather than having the default case fall off the end of
# the if.
#pylint:disable=no-else-return

def fetch_and_parse_xml(url):
    """Fetch a URL and return parsed XML"""
    response = requests.get(url, stream=True)
    xml = etree.fromstring(response.content, parser)
    return xml, response

#####################
# Code for Fetchers #
#####################

# Generic fetchers (parametrizable by site)

def fetch_bugzilla(base_url):
    """
    Return a fetcher for a bugzilla instance

    >>> url, n = fetch_bugzilla("https://bugzilla.redhat.com")("123456")
    >>> url
    u'https://bugzilla.redhat.com/show_bug.cgi?id=123456'
    >>> n
    'System with Syntax - S635MP motherboard will not install'
    """
    def bugzilla_fetcher(ticket):
        """Inner Bugzilla fetcher"""
        url = '%s/show_bug.cgi?id=%s' % (base_url, ticket)
        xml, dummy_response = fetch_and_parse_xml(url)
        title = xml.xpath('string(//span[@id="short_desc_nonedit_display"])')
        if title:
            return url, title
        else:
            return url, None
    return bugzilla_fetcher

def fetch_trac(base_url):
    """
    Return a fetcher for a Trac instance

    >>> url, n = fetch_trac("https://debathena.mit.edu/trac")("123")
    >>> url
    u'https://debathena.mit.edu/trac/ticket/123'
    >>> n
    u'debathena-ssl-certificates should include a CRL'
    >>> url, n = fetch_trac("https://scripts.mit.edu/trac")("123")
    >>> url
    u'https://scripts.mit.edu/trac/ticket/123'
    >>> n
    u'scripts-remove works poorly with non-Athena accounts'
    """
    def trac_fetcher(ticket):
        """Inner Trac fetcher"""
        url = '%s/ticket/%s' % (base_url, ticket)
        response = requests.get(url + '?format=csv')
        if response.status_code == 200:
            reader = csv.DictReader(response.text.split('\n'))
            row = next(reader)
            return url, row.get('summary', None)
        else:
            return url, None
    return trac_fetcher


def fetch_jira(url, api_url=None, req=None):
    """
    Return a fetcher for a Jira instance

    >>> fetch_jira("https://issues.apache.org")("ZOOKEEPER-1234")
    (u'https://issues.apache.org/jira/browse/ZOOKEEPER-1234', u'basic cleanup in LearnerHandler')

    Some Jira instances may use different hostnames for interactive usage than
    for API usage, for example due to using client certs for API authentication
    and some other mechanism for normal authentication. When the URLs differ,
    set the api_url option as well as the initial "url" parameter. You can also
    supply a custom `requests.Session` object with custom cookies, client
    certs, or other parameters needed to authenticate.

    For example:
    >>> def make_fetch_jira():
    ...     r = requests.Session()
    ...     r.verify = "/path/to/ca.pem"
    ...     r.cert = ("/path/to/public.crt", "/path/to/private.key")
    ...     return fetch_jira("https://jira.example.com", api_url="https://api.example.com", req=r)
    """

    if api_url is None:
        api_url = url
    if req is None:
        req = requests.Session()

    def fetch(ticket):
        """Inner Jira fetcher"""
        full_api = "%s/jira/rest/api/2/issue/%s?fields=summary" % (api_url, ticket, )
        # Other fields: description, status, ...
        html_url = "%s/jira/browse/%s" % (url, ticket, )
        resp = req.get(full_api)
        try:
            return html_url, resp.json()['fields']['summary']
        except KeyError:
            return html_url, None
    return fetch


def fetch_github(user, repo, ):
    """
    Return a fetcher for a Github instance

    >>> fetch_github("sipb", "chiron")("2")
    (u'https://github.com/sipb/chiron/issues/2', u'Teach debothena about its bugtracker')
    """
    def fetch(ticket):
        """Inner GitHub fetcher"""
        url = 'https://api.github.com/repos/%s/%s/issues/%s' % (user, repo, ticket, )
        response = requests.get(url)
        try:
            return response.json()['html_url'], response.json()['title']
        except KeyError:
            return url, None
    return fetch

# Project-specific fetchers

def fetch_rfc(number):
    """
    RFC fetcher

    >>> fetch_rfc("1234")
    (u'https://tools.ietf.org/html/rfc1234', 'Tunneling IPX traffic through IP networks')
    """
    url = "https://tools.ietf.org/html/rfc%s" % (number, )
    xml, dummy_response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//meta[@name="DC.Title"]/@content)')
    return url, (title or None)

fetch_cve_rhbz = fetch_bugzilla("https://bugzilla.redhat.com") #pylint:disable=invalid-name

def fetch_cve(ticket):
    #pylint:disable=line-too-long
    """
    CVE fetcher

    >>> url, n = fetch_cve("CVE-2015-1234")
    RHBZ url='https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2015-1234' title='CVE-2015-1234 chromium-browser: buffer overflow via race condition in GPU'
    >>> url
    u'https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2015-1234'
    >>> n
    u'[RHBZ] CVE-2015-1234 chromium-browser: buffer overflow via race condition in GPU'
    >>> url, n = fetch_cve("CVE-1999-0012")
    RHBZ url='https://bugzilla.redhat.com/show_bug.cgi?id=CVE-1999-0012' title='None'
    >>> url
    u'http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-1999-0012'
    >>> n
    u'\\nSome web servers under Microsoft Windows allow remote attackers to bypass access restrictions for files with long file names.\\n'
    >>> fetch_cve("CVE-1999-9000")
    RHBZ url='https://bugzilla.redhat.com/show_bug.cgi?id=CVE-1999-9000' title='None'
    (u'http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-1999-9000', None)
    """
    # Try fetching from RHBZ first, since it tends to be better
    url, title = fetch_cve_rhbz(ticket)
    print("RHBZ url='%s' title='%s'" % (url, title))
    if title:
        return url, "[RHBZ] " + title

    url = 'http://cve.mitre.org/cgi-bin/cvename.cgi?name=%s' % ticket
    xml, dummy_response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//tr[th="Description"]/following::tr[1])')
    if title:
        return url, "\n" + title.strip() + "\n"
    else:
        return url, None

def fetch_scripts_faq(ticket):
    """
    scripts.mit.edu FAQ fetcher

    >>> fetch_scripts_faq("136")
    (u'http://scripts.mit.edu/faq/136', u'Is scripts.mit.edu appropriate for my\\xa0site?')
    """
    url = 'http://scripts.mit.edu/faq/%s' % ticket
    xml, dummy_response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//h3[@class="storytitle"])')
    if title:
        return url, title
    else:
        return url, None

def fetch_launchpad(ticket):
    """
    Launchpad fetcher

    >>> fetch_launchpad("123456")
    (u'https://bugs.launchpad.net/bugs/123456', u'podcast crashes amarok')
    """
    url = 'http://api.launchpad.net/1.0/bugs/%s' % ticket
    response = requests.get(url)
    try:
        return response.json()['web_link'], response.json()['title']
    except KeyError:
        return url, None

def fetch_debbugs(base_url):
    """
    Debbugs (Debian bugtracker) fetcher

    >>> url, n = fetch_debbugs("https://bugs.debian.org")("123456")
    >>> url
    u'https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=123456'
    >>> n
    'ITP: eazel-engine -- Crux theme for GTK+'
    """
    def debbugs_fetcher(ticket):
        """Inner Debbugs fetcher"""
        url = '%s/cgi-bin/bugreport.cgi?bug=%s' % (base_url, ticket)
        xml, dummy_response = fetch_and_parse_xml(url)
        title = xml.xpath('normalize-space(//h1/child::text()[2])')
        if title:
            return url, title
        else:
            return url, None
    return debbugs_fetcher

def fetch_dsa(number):
    """
    Debian Security Advisories fetcher

    >>> fetch_dsa("DSA-1234")
        -> DSA URLs in page: []
    (u'https://security-tracker.debian.org/tracker/DSA-1234', 'ruby1.6')
    """
    url = "https://security-tracker.debian.org/tracker/%s" % (number, )
    xml, dummy_response = fetch_and_parse_xml(url)
    dsa_xpath = '//a[text()="Debian"]/@href[starts-with(.,"http://www.debian.org/security/")]'
    dsa_urls = xml.xpath(dsa_xpath)
    title = xml.xpath('string(//tr[td/b="Description"]/td[2])') or None
    print("    -> DSA URLs in page: %s" % (dsa_urls, ))
    if dsa_urls:
        dsa_url = dsa_urls[0]
    else:
        dsa_url = url
    return dsa_url, title


def fetch_pokemon(ticket):
    """
    Pokemon fetcher (by Pokedex number)

    >>> url, n = fetch_pokemon("123")
    >>> url
    u'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'
    >>> n
    u'Scyther (Bug, Flying)'
    """
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number' #pylint:disable=line-too-long
    response = requests.get(url + '?action=raw')
    for line in response.text.split('\n'):
        if line[0:7] == '{{rdex|':
            (num, name) = line.split('|')[2:4]
            try:
                if int(num) == int(ticket):
                    return url, "%s (%s)" % (name, ", ".join(line.split('}')[0].split('|')[5:]))
            except ValueError:
                pass
    return url, None

def fetch_mit_class(ticket):
    """
    MIT class fetcher

    >>> url, n = fetch_mit_class("6.828")
    >>> url
    u'http://student.mit.edu/catalog/search.cgi?search=6.828'
    >>> n
    '6.828 Operating System Engineering'
    """
    url = 'http://student.mit.edu/catalog/search.cgi?search=%s' % (ticket, )
    xml, dummy_response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//h3)')
    if title:
        return url, title.strip()
    else:
        return url, None

def fetch_whats(whats):
    """
    whats fetcher (MIT SIPB acronym database)

    >>> fetch_whats("SIPB")
    (u'https://stuff.mit.edu/cgi/whats.cgi?SIPB', 'Student Information Processing Board')
    """
    url = "https://stuff.mit.edu/cgi/whats.cgi?%s" % (whats, )
    xml, dummy_response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//dl/dd)')
    if title:
        title = title.strip()
    return url, (title or None)

def undebathena_fun(ticket): #pylint:disable=unused-argument
    """Generate a random fake Debathena package name and file to divert"""
    url = 'http://debathena.mit.edu/trac/wiki/PackageNamesWeDidntUse'
    xml, dummy_response = fetch_and_parse_xml(url)
    package = choice(xml.xpath('id("content")//li')).text.strip()
    directory = choice(['/etc', '/bin', '/usr/bin', '/sbin', '/usr/sbin',
                        '/dev/mapper', '/etc/default', '/var/run'])
    filename = choice(os.listdir(directory))
    return url, "%s should divert %s/%s" % (package, directory, filename)

def fetch_bible_esvapi2(verse):
    #pylint:disable=line-too-long
    r"""
    Bible fetcher using esvapi.org v2

    #>>> fetch_bible_esvapi2("John 4:8")
    #(u'http://www.esvapi.org/v2/rest/passageQuery?key=TEST&passage=John+4%3A8&output-format=plain-text', u'\n=======================================================\nJohn 4:8\n   [8](For his disciples had gone away into the city to buy food.) (ESV)\n(From The Holy Bible, English Standard Version. See http://www.crosswaybibles.org and http://www.esvapi.org/.)')
    """
    url = 'http://www.esvapi.org/v2/rest/passageQuery'
    params = (('key', 'TEST'), ('passage', verse), ('output-format', 'plain-text'))
    response = requests.get(url, params=params)
    copyright_msg = "(From The Holy Bible, English Standard Version. See http://www.crosswaybibles.org and http://www.esvapi.org/.)"
    text = "\n%s\n%s" % (response.text, copyright_msg, )
    return response.url, text


BIBLE_RE = re.compile(r"(?P<book>(\d+ )?[0-9a-z]+) (?P<verse>[0-9:-]+)", re.IGNORECASE)
STRIP_NL_RE = re.compile("[ \r]*\n[ \r]*")

def fetch_ibibles(translation):
    r"""
    Bible fetcher, using ibibles.net

    >>> fetch_ibibles("niv")("mat 5:3-4") #doctest:+NORMALIZE_WHITESPACE,+ELLIPSIS
    (u'https://ibibles.net/quote.php?niv-mat/5:3-4',
     u'"Blessed are the poor in spirit, ..., for they will be comforted.')
    >>> fetch_ibibles("kjv")("Matthew 5:3") #doctest:+NORMALIZE_WHITESPACE
    (u'https://ibibles.net/quote.php?kjv-Matthew/5:3',
     u'Blessed are the poor in spirit: for theirs is the kingdom of heaven.')
    >>> fetch_ibibles("niv")("1 Timothy 3:9") #doctest:+NORMALIZE_WHITESPACE
    (u'https://ibibles.net/quote.php?niv-1 Timothy/3:9',
     u'They must keep hold of the deep truths of the faith with a clear conscience.')
    >>> fetch_ibibles("niv")("1ti 3:9") #doctest:+NORMALIZE_WHITESPACE
    (u'https://ibibles.net/quote.php?niv-1ti/3:9',
     u'They must keep hold of the deep truths of the faith with a clear conscience.')
    """

    def ibibles_fetcher(full_verse):
        """Inner ibibles fetcher"""
        parsed_verse = BIBLE_RE.match(full_verse)
        if not parsed_verse:
            return None, None
        params = translation, parsed_verse.group("book"), parsed_verse.group("verse")
        url = 'https://ibibles.net/quote.php?%s-%s/%s' % params
        xml, dummy_response = fetch_and_parse_xml(url)
        body = xml.xpath('//body/text()')
        text = re.sub(STRIP_NL_RE, '\n', ''.join(body).strip())
        return url, text

    return ibibles_fetcher


def fetch_xkcd(comic):
    """
    XKCD fetcher

    >>> fetch_xkcd("123")
    (u'http://xkcd.com/123/', 'xkcd: Centrifugal Force')
    """
    url = 'http://xkcd.com/%s/' % (comic, )
    xml, response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//title)')
    if title and response.status_code == 200:
        return url, title
    else:
        return url, None

def fetch_unicode(codepoint):
    """
    Unicode fetcher (number->char)

    This would work with a browser, but we seem to be blocked by Cloudflare
    now, so Chiron's Unicode support seems to be broken. So, uh, test that it
    hasn't resumed working.

    >>> url, n = fetch_unicode("2603")
    Unicode: 'Unicode Character 'SNOWMAN' (U+2603)' '200'
    >>> url
    u'https://www.fileformat.info/info/unicode/char/2603/index.htm'
    >>> n
    u"Unicode Character 'SNOWMAN' (U+2603): \\u2603"
    """
    url = 'https://www.fileformat.info/info/unicode/char/%s/index.htm' % (codepoint, )
    xml, response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//title)')
    print("Unicode: '%s' '%s'" % (title, response.status_code))
    if title and response.status_code == 200:
        return url, title + ': ' + unichr(int(codepoint, 16))
    else:
        return url, None

def fetch_unicode_char(character):
    """
    Unicode fetcher (char->number)

    >>> url, n = fetch_unicode_char("\u1234")
    >>> url
    u'https://www.fileformat.info/info/unicode/char/1234/index.htm'
    >>> n
    "Unicode Character 'ETHIOPIC SYLLABLE SEE' (U+1234)"
    """
    codepoint = format(ord(character), 'x')
    url = 'https://www.fileformat.info/info/unicode/char/%s/index.htm' % (codepoint, )
    xml, response = fetch_and_parse_xml(url)
    title = xml.xpath('string(//title)')
    if title and response.status_code == 200:
        return url, title
    else:
        return url, "U+%s" % (codepoint, )

def fetch_airport(code):
    """
    Airport fetcher (code->location)

    >>> url, n = fetch_airport("BOS")
    >>> url
    u'http://www.gcmap.com/airport/BOS'
    >>> n
    u'Boston, Massachusetts, United States (General Edward Lawrence Logan International Airport)'
    """
    url = 'http://www.gcmap.com/airport/%s' % (code, )
    xml, response = fetch_and_parse_xml(url)
    place = xml.xpath('string(//meta[@name="geo.placename"]/@content)')
    name = xml.xpath('string(//td[@class="fn org"])')
    if place and response.status_code == 200:
        if name:
            title = "%s (%s)" % (place, name, )
        else:
            title = place
        return url, title
    else:
        return url, None


# Special constant-text fetchers

def deal_with_assassin(_ticket):
    """Fetcher to reduce misdirected Guild office combos"""
    return ("NO COMBOS OVER ZEPHYR",
            """DO @b(NOT) ASK FOR OR SEND THE OFFICE COMBO
OVER ZEPHYR, EVEN PERSONAL ZEPHYR.
Instead, look in /mit/assassin/Office. If you don't have access,
ask to be added.""")

def invoke_science(_ticket):
    """"Science" ASCII art fetcher"""
    return ("SCIENCE!",
            r"""
  ____   ____ ___ _____ _   _  ____ _____
 / ___| / ___|_ _| ____| \ | |/ ___| ____|
 \___ \| |    | ||  _| |  \| | |   |  _|
  ___) | |___ | || |___| |\  | |___| |___
 |____/ \____|___|_____|_| \_|\____|_____|
""")

def invoke_debothena(ticket):
    """"Debothena" ASCII art fetcher, for testing"""
    return (ticket,
            u"""
╺┳┓┏━╸┏┓ ┏━┓╺┳╸╻ ╻┏━╸┏┓╻┏━┓
 ┃┃┣╸ ┣┻┓┃ ┃ ┃ ┣━┫┣╸ ┃┗┫┣━┫
╺┻┛┗━╸┗━┛┗━┛ ╹ ╹ ╹┗━╸╹ ╹╹ ╹
""")
