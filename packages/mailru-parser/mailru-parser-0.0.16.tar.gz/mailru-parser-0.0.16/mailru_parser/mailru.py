# -*- coding:utf-8 -*-
import HTMLParser
import json
import re
import unicodedata
from urllib import quote, unquote
from urlparse import urlparse, urlunsplit, urlsplit
from lxml import etree

from mailru_parser.exceptions import EmptySerp, MatchCaptchaError, MailRuParserError
from pyquery import PyQuery


class MailRuParser(object):
    params_regexr = re.U | re.M | re.DOTALL | re.I

    json_data_re = re.compile('var STP\s*=\s*(\{.*?\});', flags=params_regexr)

    captcha_re = {
        'captcha': re.compile('<img src="(/ar_captcha\?id=.*?)"', params_regexr),
        'sqid': re.compile('<input.*?name=\"sqid\".*?value=\"([^\"]+)\".*?>', params_regexr),
        'sf': re.compile('<input.*?name=\"back\".*?value=\"([^\"]+)\".*?>', params_regexr),
        'errback': re.compile('<input.*?name=\"errback\".*?value=\"([^\"]+)\".*?>', params_regexr),
        'q': re.compile('<input.*?name=\"q\".*?value=\"([^\"]+)\".*?>', params_regexr)
    }

    captcha_image_url = "http://go.mail.ru{image_url}"


    def __init__(self, content, snippet_fileds=('d', 'p', 'u', 't', 's', 'm')):
        self.content = to_unicode(content)
        self.snippet_fileds = snippet_fileds

        self._json_data = None

    def get_serp(self):
        if self._get_not_found():
            return {'pc': 0, 'sn': []}

        pagecount = self.get_pagecount()
        if pagecount == 0:
            return {'pc': 0, 'sn': []}

        snippets = self.get_snippets()

        if not snippets:
            raise MailRuParserError('Not found snippets')

        return {'pc': pagecount, 'sn': snippets}

    def _get_not_found(self):
        match = re.search(
            ur'<h2 class="not-found__title">\s*По данному запросу ничего не найдено\s*</h2>',
            self.content,
            flags=self.params_regexr
        )
        return bool(match)

    def get_pagecount(self):
        match = re.search('foundCount:\s*(\d+),', self.content, flags=self.params_regexr)
        if not match:
            raise MailRuParserError('Not exists foundCount')

        return int(match.group(1))

    def is_blocked(self):
        return

    def _get_captcha_sqid(self):
        match = re.search(
            '<input type="hidden" name="sqid" value="([^"]+?)"',
            self.content,
            flags=self.params_regexr
        )
        if not match:
            raise MailRuParserError('Not found captcha sqid')
        return match.group(1)

    def _get_captcha_q(self):
        match = re.search(
            '<input type="hidden" name="q" value="([^"]+?)"',
            self.content,
            flags=self.params_regexr
        )
        if not match:
            raise MailRuParserError('Not found captcha q')
        return match.group(1)

    def _get_captcha_back(self):
        match = re.search(
            '<input type="hidden" name="back" value="([^"]+?)"',
            self.content,
            flags=self.params_regexr
        )
        if not match:
            raise MailRuParserError('Not found captcha back')
        return match.group(1)

    def _get_captcha_errback(self):
        match = re.search(
            '<input type="hidden" name="errback" value="([^"]+?)"',
            self.content,
            flags=self.params_regexr
        )
        if not match:
            raise MailRuParserError('Not found captcha sqid')
        return match.group(1)

    def get_captcha_data(self):
        if '<div class="antirobot' not in self.content:
            return

        sqid = self._get_captcha_sqid()
        q = self._get_captcha_q()
        back = self._get_captcha_back()
        errback = self._get_captcha_errback()

        url = 'http://go.mail.ru/ar_captcha?id={0}'.format(sqid)
        return {
            'url': url,
            'q': q,
            'sqid': sqid,
            'back': back,
            'errback': errback,
            'SequreWord': None,
            'ajax': '1',
        }

    def get_snippets(self):

        dom = PyQuery(self.content)
        elements = dom('li.result__li')

        snippets = []
        position = 0
        for element in elements:
            html = HTMLParser.HTMLParser().unescape(etree.tostring(element))
            snippet = self._parse_snippet(html)
            position += 1
            snippet['p'] = position
            snippets.append(snippet)
        return snippets

    def _get_url_title(self, html):
        match = re.search(
            '<h3 class="result__title">.*?<a\s*class="light-link"[^>]+?,\s+\'(.*?)\',\s+[^>]+?>\s*(.*?)\s*</a>\s*</h3>',
            html,
            flags=self.params_regexr
        )
        if not match:
            raise MailRuParserError('not found url and title')

        return match.group(1), match.group(2)

    def _get_descr(self, html):
        if 's' not in self.snippet_fileds:
            return None

        match = re.search(
            '<div class="result__snp">\s*(.*?)\s*</div>',
            html,
            flags=self.params_regexr
        )
        if not match:
            return None

        return HTMLParser.HTMLParser().unescape(match.group(1))

    def _parse_snippet(self, html):

        url, title = self._get_url_title(html)
        try:
            domain = get_full_domain_without_scheme(url)
        except UnicodeError as e:
            raise e

        snippet = {
            'd': domain,  # domain
            'u': url,  # url
            'm': self._is_map_snippet(html),  # map
            't': None,  # title snippet
            's': self._get_descr(html),  # body snippet
        }

        if 't' in self.snippet_fileds:
            snippet['t'] = title

        return snippet

    def _is_map_snippet(self, html):
        return False

    @property
    def json_data(self):
        if self._json_data:
            return self._json_data

        match = self.json_data_re.search(self.content)
        if not match:
            raise MailRuParserError('json not found')

        self._json_data = json.loads(match.group(1))
        return self._json_data


def to_unicode(content, from_charset=None):
    u"""Безопасное приведение к юникоду

    :type  content: str
    :param content: текст
    :type  from_charset: str
    :param from_charset: Кодировка исходного текста

    :rtype: unicode
    :returns: текст, преобразованный в юникод
    """
    if type(content) == unicode:
        return content

    charsets = {
        'utf-8' : 'utf8',
        'utf8' : 'utf8',
        'cp1251' : 'cp1251',
        'cp-1251' : 'cp1251',
        'windows-1251' : 'cp1251',
        'win-1251' : 'cp1251',
        '1251' : 'cp1251',
        'русdows-1251': 'cp1251',
        'koi8-r' : 'koi8-r'
    }
    if type(from_charset) in (str, unicode):
        from_charset = str(from_charset.lower())

    try:
        from_charset = charsets[from_charset]
        return unicode(content, encoding=from_charset)

    except KeyError:
        for from_charset in ('utf8', 'cp1251', 'koi8-r', None):
            try:
                if from_charset is not None:
                    return unicode(content, encoding=from_charset)
                else:
                    return unicode(content)
            except UnicodeError:
                continue

        raise UnicodeError('Can not be converted to Unicode')

    except UnicodeError:
        return unicode(content, encoding=from_charset, errors='ignore')

def normalize(url, charset='utf-8'):
    def _clean(string):
        string = unicode(unquote(string), 'utf-8', 'replace')
        return unicodedata.normalize('NFC', string).encode('utf-8')

    default_port = {
        'ftp': 21,
        'telnet': 23,
        'http': 80,
        'gopher': 70,
        'news': 119,
        'nntp': 119,
        'prospero': 191,
        'https': 443,
        'snews': 563,
        'snntp': 563,
    }

    if isinstance(url, unicode):
        url = url.encode(charset, 'ignore')

    if url[0] not in ['/', '-'] and ':' not in url[:7]:
        url = 'http://' + url

    url = url.replace('#!', '?_escaped_fragment_=')

    scheme, auth, path, query, fragment = urlsplit(url.strip())
    (userinfo, host, port) = re.search('([^@]*@)?([^:]*):?(.*)', auth).groups()

    scheme = scheme.lower()

    host = host.lower()
    if host and host[-1] == '.':
        host = host[:-1]
        # take care about IDN domains
    try:
        host = host.decode(charset).encode('idna')  # IDN -> ACE
    except Exception:
        host = host.decode(charset)

    path = quote(_clean(path), "~:/?#[]@!$&'()*+,;=")
    fragment = quote(_clean(fragment), "~")

    query = "&".join(["=".join([quote(_clean(t), "~:/?#[]@!$'()*+,;=") for t in q.split("=", 1)]) for q in query.split("&")])

    if scheme in ["", "http", "https", "ftp", "file"]:
        output = []
        for part in path.split('/'):
            if part == "":
                if not output:
                    output.append(part)
            elif part == ".":
                pass
            elif part == "..":
                if len(output) > 1:
                    output.pop()
            else:
                output.append(part)
        if part in ["", ".", ".."]:
            output.append("")
        path = '/'.join(output)

    if userinfo in ["@", ":@"]:
        userinfo = ""

    if path == "" and scheme in ["http", "https", "ftp", "file"]:
        path = "/"

    if port and scheme in default_port.keys():
        if port.isdigit():
            port = str(int(port))
            if int(port) == default_port[scheme]:
                port = ''

    auth = (userinfo or "") + host
    if port:
        auth += ":" + port
    if url.endswith("#") and query == "" and fragment == "":
        path += "#"
    return urlunsplit((scheme, auth, path, query, fragment))


def get_full_domain_without_scheme(url):
    absolute_url = normalize(url).replace('//www.', '//')
    parsed = urlparse(absolute_url)
    return urlunsplit(('', parsed.netloc, '', '', '')).replace('//', '')
