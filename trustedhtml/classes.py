# -*- coding: utf-8 -*-

import re
import copy
from beautifulsoup import BeautifulSoup, NavigableString, Tag
from django.contrib.sites.models import Site
from django.utils.encoding import iri_to_uri

TRUSTED_PREPARINGS = 2
TRUSTED_ITERATIONS = 2
TRUSTED_QUITE = False

class TrustedException(ValueError):
    """Base trustedhtml error"""
    pass

class RequiredException(TrustedException):
    """Example: src attribute for <img />"""
    pass
 
class InvalidException(TrustedException):
    """Example: "none" value for "display" style property"""
    pass
    
class EmptyException(TrustedException):
    """Example: width attribute for <div />"""
    pass
 
class DefaultException(TrustedException):
    """Example: alt attribute for <img />"""
    pass
    
class SequenceException(TrustedException):
    pass
 
class Tag(object):
    def __init__(self, name='', attrs=[]):
        self.name = name
        self.attrs = attrs
    
class Handler(object):
    def __init__(self, profile):
        self.profile = profile
        
    def listener(self, rule, value, state):
        return None
        
class Run(object):
    def __init__(self, trusted_list, handler=None, equivalents={}):
        self.trusted_list = trusted_list
        self.handler = handler
        self.equivalents = equivalents
    
    def check(self, tag):
        if not self.trusted_list:
            tag.attrs = [] 
            return True
        try:
            for index, trusted in enumerate(self.trusted_list):
                quite = index < len(self.trusted_list) - 1
                try:
                    correct = {}
                    dictionary = dict(tag.attrs)
                    for main, validator in trusted.iteritems():
                        attributes = [main]
                        attributes += self.equivalents.get(main, [])
                        for attribute in attributes:
                            if attribute in dictionary:
                                value = dictionary[attribute] 
                            else:
                                value = None
                            try:
                                correct[attribute] = validator.validate(tag.name, attribute, value, 
                                    parent=self, handler=self.handler, quite=quite)
                            except EmptyException:
                                pass
                    order = [attr for attr, value in tag.attrs]
                    other = [attr for attr, value in correct.iteritems() if attr not in order]
                    order.extend(other)
                    sequence = [(order.index(attr), attr, value) for attr, value in correct.iteritems()]
                    sequence.sort()
                    tag.attrs = [(item, value) for index, item, value in sequence]
                    return True
                except RequiredException:
                    continue
        except InvalidException:
            return None
        return False

class String(object):
    def __init__(self, required=False, strip=True, allow_empty=True, case_sensitive=False, 
            invalid=False, tag=None):
        self.quite = TRUSTED_QUITE
        self.required = required
        self.strip = strip
        self.allow_empty = allow_empty
        self.case_sensitive = case_sensitive
        self.invalid = invalid
        self.tag = tag 
        
        self.name = None
        self.attr = None
        self.value = None
        self.parent = None
        self.handler = None
        self.quite = None
        
        
    def handle(self, value, state):
        if self.handler is not None:
            return self.handler.listener(rule=self, value=value, state=state)
        else:
            return None
        
    def finish_print(self, text):
        if not self.quite:
            print text
        
    def finish(self, value, invalid_error=False):
        # Debug report:
        line = '<%s %s = %s : %s ~ %s>' % (
            self.name, self.attr, repr(self.value), repr(value), self.__class__.__name__)
        if invalid_error:
            self.finish_print('\n$' + line)
            raise InvalidException(unicode(line))
        if self.required == True:
            self.finish_print('\n!' + line)
            raise RequiredException(unicode(line))
        if self.required == False:
            if self.value is not None:
                self.finish_print('\n-' + line)
            raise EmptyException(unicode(line))
        self.finish_print('\n+' + line)
        raise DefaultException(unicode(line))
        
    def prepare(self, value):
        if (value is None) or (not self.allow_empty and value == ''):
            self.finish(value)
        value = unicode(value)
        if self.strip:
            value = value.strip()
        return value

    def core(self, value):
        return value

    def validate(self, name, attr, value, parent=None, handler=None, quite=TRUSTED_QUITE):
        self.name = name
        self.attr = attr
        self.value = value
        self.parent = parent
        self.handler = handler
        self.quite = quite
        try:
            value = self.prepare(value)
            value = self.core(value)
        except DefaultException:
            return unicode(self.required)
        if self.invalid:
            self.finish(value, invalid_error=True)
        return value

    def v(self, value, catch=True):
        if catch:
            try:
                return self.validate('name', 'attr', value)
            except TrustedException, error:
                return error
        else:
            return self.validate('name', 'attr', value)

        
class Content(String):         
    def __init__(self, allow_empty=False, **kwargs):
        kwargs['allow_empty'] = allow_empty
        super(Content, self).__init__(**kwargs)


class Char(String):
    def core(self, value):
        if len(value) < 1:
            self.finish(value)
        return value[:1]


class List(String):
    def __init__(self, values, return_defined=True, **kwargs):
        super(List, self).__init__(**kwargs)
        self.values = values
        self.source_values = self.values
        self.return_defined = return_defined
        if not self.case_sensitive:
            self.values = [unicode(value).lower() for value in self.values]
    
    def core(self, value):
        if self.case_sensitive:
            if value not in self.values:
                self.finish(value)
        else:
            if value.lower() not in self.values:
                self.finish(value)
            if self.return_defined:
                return self.source_values[self.values.index(value.lower())]
        return value
        

class Url(Content):
    SCHEMES = ['http', 'https', 'shttp', 
        'ftp', 'sftp', 'file', 'mailto',  
        'svn', 'svn+ssh', 
        'telnet', 'mms', 'ed2k', 
    ]
    GLOBAL_PREFIX = 'http://'
    LOCAL_PREFIX = '/'
    ANCHOR = re.compile(r'^#\w+$')
    ANCHOR_SPACES = re.compile(r'\s')
    
    def __init__(self, local_only=False, allow_local=True, allow_anchor=False, **kwargs):
        super(Url, self).__init__(**kwargs)
        self.local_only = local_only
        self.allow_local = allow_local
        self.allow_anchor = allow_anchor
        if self.local_only == True:
            self.allow_local = True
        if ':' not in self.GLOBAL_PREFIX:
            self.GLOBAL_PREFIX = self.GLOBAL_PREFIX + ':'
        
    def core(self, value):
        value = iri_to_uri(value)
        if ':' not in value:
            if self.allow_anchor:
                spaceless = self.ANCHOR_SPACES.sub('', value)
                if self.ANCHOR.match(spaceless):
                    return spaceless
            if value.startswith(self.LOCAL_PREFIX):
                if self.allow_local:
                    return value
                else:
                    value = unicode(Site.objects.get_current()) + value
            else:
                if self.local_only:
                    return self.LOCAL_PREFIX + value
            value = self.GLOBAL_PREFIX + value
        if self.local_only:
            value = self.handle(value, 'local_only')
            if value is not None:
                return value
            self.finish(value)
        scheme = value[:value.find(':')].lower()
        if scheme not in self.SCHEMES:
            self.finish(value)
        return value

    
class Number(Content):
    _BASE = r'\d{1,7}'
    BASE = _BASE[:]
    FLAGS = 0
    REMOVE = re.compile(r'\s')
    
    def __init__(self, allow_sign=True, garbage_trimming=True, remove_spaces=False, **kwargs):
        super(Number, self).__init__(**kwargs)
        self.allow_sign = allow_sign
        self.garbage_trimming = garbage_trimming
        self.remove_spaces = remove_spaces
        if self.allow_sign:
            self.BASE = '[+-]?' + self.BASE
        if not self.case_sensitive:
            self.FLAGS = re.I
        regexp = '(' + self.BASE + ')'
        self.re_compile(regexp)
        
    def re_compile(self, regexp):
        if not self.garbage_trimming:
            regexp = regexp + '$'
        self.REGEXP = re.compile(unicode(regexp), self.FLAGS)
    
    def core(self, value):
        if self.remove_spaces:
            value = self.REMOVE.sub('', value)
        match = self.REGEXP.match(value)
        if match is None:
            self.finish(value)
        return unicode(match.group(1))


class Length(Number):
    def __init__(self, **kwargs):
        super(Length, self).__init__(**kwargs)
        regexp = '(' + self.BASE + '%?)'
        self.re_compile(regexp)


class Size(Number):
    TRAILINGS = [
        'px', 'cm', 'mm', 'in', 'pt', 'pc',
        'em', 'ex', '%', '',
    ]

    def __init__(self, case_sensitive=False, remove_spaces=True, **kwargs):
        kwargs['remove_spaces'] = remove_spaces
        kwargs['case_sensitive'] = case_sensitive
        super(Size, self).__init__(**kwargs)
        regexp = '(' + self.BASE + '(' + '|'.join(self.TRAILINGS) + '))'
        self.re_compile(regexp)


class ListOrSize(List, Size):
    def __init__(self, values, allow_sign=True, garbage_trimming=True, **kwargs):
        Size.__init__(self, allow_sign=allow_sign, garbage_trimming=garbage_trimming, **kwargs)
        List.__init__(self, values=values, **kwargs) # Use String not Content
    
    def core(self, value):
        # We will use core and catch DefaultException for List or raise it for Size
        old_quite = self.quite 
        try:
            self.quite = True
            return List.core(self, value)
        except TrustedException:
            self.quite = old_quite
            return Size.core(self, value)


class Color(ListOrSize):
    NAMES = ['activeborder', 'activecaption', 'appworkspace', 
        'background', 'buttonface', 'buttonhighlight', 'buttonshadow', 
        'buttontext', 'captiontext', 'graytext', 'highlight', 
        'highlighttext', 'inactiveborder', 'inactivecaption', 
        'inactivecaptiontext', 'infobackground', 'infotext', 'menu', 
        'menutext', 'scrollbar', 'threeddarkshadow', 'threedface', 
        'threedhighlight', 'threedlightshadow', 'threedshadow', 
        'window', 'windowframe', 'windowtext', 'currentcolor', 
    ] + [
        'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',  
        'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
        'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse',
        'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson',
        'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray',
        'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta',
        'darkolivegreen', 'darkorange', 'darkorchid', 'darkred',
        'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
        'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink',
        'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
        'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
        'ghostwhite', 'gold', 'goldenrod', 'gray', 'green',
        'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred',
        'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush',
        'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral',
        'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen',
        'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen',
        'lightskyblue', 'lightslategray', 'lightslategrey',
        'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen',
        'magenta', 'maroon', 'mediumaquamarine', 'mediumblue',
        'mediumorchid', 'mediumpurple', 'mediumseagreen',
        'mediumslateblue', 'mediumspringgreen', 'mediumturquoise',
        'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose',
        'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive',
        'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod',
        'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip',
        'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple',
        'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon',
        'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
        'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
        'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 
        'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
        'yellow', 'yellowgreen', 
    ]
#    NAMES = ['black', 'silver', 'gray', 'white', 'maroon', 'red', 
#        'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 
#        'navy', 'blue', 'teal', 'aqua', ]
        
    
    VALUE = '[+-]?' + Number._BASE + '%?'
    CONDITION = r'(((rgb|hsl)\(' + VALUE + ',' + VALUE + ',' + VALUE + r'\))|' + \
        r'((rgba|hsla)\(' + VALUE + ',' + VALUE + ',' + VALUE + ',((' + \
        Number._BASE + ')?.' + Number._BASE + '|' + VALUE + r')\))|' + \
        r'(#[0-9a-fA-F]{6})|(#[0-9a-fA-F]{3}))'
        
    def __init__(self, case_sensitive=False, allow_sign=False, remove_spaces=True, **kwargs):
        kwargs['case_sensitive'] = case_sensitive
        kwargs['allow_sign'] = allow_sign
        kwargs['remove_spaces'] = remove_spaces
        kwargs['values'] = self.NAMES
        super(Color, self).__init__(**kwargs)
        self.re_compile(self.CONDITION)
        
class Sequence(Content):
    SPACES = re.compile(r'\s+')
    
    def __init__(self, validator=None, delimiter_char=' ', joiner_char=None, appender_char='', **kwargs):
        super(Sequence, self).__init__(**kwargs)
        self.validator = validator
        if self.validator is None:
            self.validator = Content()
        self.delimiter_char = delimiter_char
        self.joiner_char = joiner_char
        if self.joiner_char is None:
            self.joiner_char = self.delimiter_char
        self.appender_char = appender_char

    def sequence(self, value, parts):
        result = []
        for part in parts:
            try:
                result.append(self.validator.validate(self.name, self.attr, part, 
                    parent=self, handler=self.handler, quite=self.quite))
            except RequiredException:
                raise SequenceException
            except EmptyException:
                pass
        return result

    def core(self, value):
        if self.SPACES:
            value = self.SPACES.sub(' ', value).strip()
        parts = value.split(self.delimiter_char)
        try:
            parts = self.sequence(value, parts)
        except SequenceException:
            self.finish(value)
        value = self.joiner_char.join(parts)
        if parts:
            value += self.appender_char
        return unicode(value)


class Style(Sequence, Run):
    def __init__(self, trusted_list, delimiter_char=';', joiner_char='; ', appender_char=';', handler=None, equivalents={}, **kwargs):
        kwargs['delimiter_char'] = delimiter_char
        kwargs['joiner_char'] = joiner_char
        kwargs['appender_char'] = appender_char
        Sequence.__init__(self, **kwargs)
        Run.__init__(self, trusted_list, handler, equivalents)
        
    def sequence(self, value, parts):
        attrs = []
        for part in parts:
            if ':' not in part:
                continue
            part_name = part[:part.find(':')].strip()
            part_value = part[part.find(':')+1:].strip()
            attrs.append((part_name, part_value))
        tag = Tag(self.name, attrs)
        result = self.check(tag)
        if result is None:
            self.finish(value, invalid_error=True)
        if not result:
            raise SequenceException
        return ['%s: %s' % (part_name, part_value) for part_name, part_value in tag.attrs]


class Indent(Sequence):
    # EmptyException is the same to RequiredException.
    # You may use DefaultException to skip value.
    def __init__(self, validator=None, **kwargs):
        if validator is None:
            validator = Size()
        kwargs['validator'] = validator
        super(Indent, self).__init__(**kwargs)
        
    def sequence(self, value, parts):
        if len(parts) not in [1, 2, 4]:
            return False
        result = []
        for part in parts:
            try:
                result.append(self.validator.validate(self.name, self.attr, part, 
                    parent=self, handler=self.handler, quite=self.quite))
            except (RequiredException, EmptyException):
                raise SequenceException
        return result


class Complex(Indent):
    # EmptyException is the same to RequiredException.
    # You may use DefaultException to skip value.
    def __init__(self, trusted_sequence, **kwargs):
        super(Complex, self).__init__(**kwargs)
        self.trusted_sequence = trusted_sequence
        
    def sequence(self, value, parts):
        return self.complex(parts, 0, self.trusted_sequence, 0)    

    def complex(self, parts, part_index, list, list_index):
        if part_index >= len(parts):
            return parts
        if list_index >= len(list):
            raise SequenceException
        try:
            value = list[list_index].validate(self.name, self.attr, parts[part_index], 
                parent=self, handler=self.handler, quite=True)
            result = self.complex(parts, part_index + 1, list, list_index + 1)
            result[part_index] = value
            return result
        except (RequiredException, EmptyException, SequenceException):
            return self.complex(parts, part_index, list, list_index + 1)


class Html(Run):
    # All constants must be lowered. 
    special_chars = [
        ('&', '&amp;'), # Must be first element in list
        ('"', '&quot;'),
        ("'", '&apos;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        #(nbsp_char, nbsp_text),
    ]
    plain_chars = [special_chars[index] for index in range(len(special_chars)-1, -1, -1)] 
    code_re = re.compile('&#(([0-9]+);?|x([0-9A-Fa-f]+);?)')
    code_re_special = dict([(0, '')] + 
        [(ord(char), string) for char, string in special_chars])  
    system_re = re.compile('[\x01-\x1F\s]+')
    
    nbsp_char = u'\xa0'
    nbsp_text = '&nbsp;'
    nbsp_re = re.compile('[' + nbsp_char + ' ]{2,}')
    
    replace_rules = { # Use unicode text for replace
    # dictionary = {tag_name: [list of rules], ...}
    # rules = ([list of attrs], new_tag_name, [list of new_attrs])
    # attrs & new_attrs = (attr, value)
#        'span':
#            [([('style', 'text-decoration: underline;'), ], u'u', []), ],
    }
    
    empty_tags = ['td', 'th', 'caption', 'a', ]
    nbsp_tag = ['td', 'th', ]
    
    start_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', # normal
        'div', 'address', 'fieldset', 'ins', 'del', # w3c 
        'ul', 'ol', 'blockquote', 'table', 'pre', # TinyMCE
    ]
    default_start_tag = 'p'
    
    markupMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
    markupMassage.extend([(re.compile('<!-([^-])'), 
        lambda match: '<!--' + match.group(1))])

    def code_re_suber(self, match):
        try:
            if match.group(2):
                code = int(match.group(2))
            elif match.group(3):
                code = int(match.group(3), 16)
            else:
                code = 0
            if code in self.code_re_special:
                return self.code_re_special[code]
            return unichr(code)
        except (ValueError, OverflowError):
            return ''
    
    def remove_spaces(self, html):
        return self.nbsp_re.sub(self.nbsp_char, html)
    
    def prepare(self, html):
        html = html.replace('\0', '')
        new_html = self.code_re.sub(self.code_re_suber, html)
        if new_html != html:
            print '\n~pre', repr(html), '\n=pre', repr(new_html)
            html = new_html
        html = self.system_re.sub(' ', html)
        html = self.remove_spaces(html)
        return html
    
    def tag_check(self, tag):
        if tag.name not in self.trusted_dictionary:
            print '\n!not', repr(tag.name)  
            return False
        self.trusted_list = self.trusted_dictionary[tag.name]
        return self.check(tag)
        
    def tag_replace(self, tag):
        if tag.name not in self.replace_rules:
            return
        for old_attrs, new_name, new_attrs in self.replace_rules[tag.name]:
            for old_attr, old_value in old_attrs:
                if (old_attr, old_value) not in tag.attrs:
                    break
            else:
                print '\n~rep', repr(tag.name), repr(tag.attrs)
                other_attrs = [(attr, value) for attr, value in tag.attrs 
                    if (attr, value) not in old_attrs]
                other_attrs.extend(new_attrs)
                tag.name = new_name
                tag.attrs = other_attrs
                print '\n=rep', repr(tag.name), repr(tag.attrs)
                break
    
    def clear(self, soup):
        index = 0
        while index < len(soup.contents):
            if isinstance(soup.contents[index], Tag):
                self.tag_replace(soup.contents[index])
                if self.tag_check(soup.contents[index]):
                    self.clear(soup.contents[index])
                else:
                    soup.contents[index].extract()
                    continue
            elif soup.contents[index].__class__ is not NavigableString:
                soup.contents[index].extract()
                continue
            else:
                value = soup.contents[index].string
                value = self.remove_spaces(value)
                for char, string in self.special_chars:
                    value = value.replace(char, string)
                if value != soup.contents[index].string:
                    soup.contents[index].replaceWith(value)
            index = index + 1
        return soup

    def join(self, soup):
        changed = False
        index = 0
        while index < len(soup.contents) - 1:
            if (not isinstance(soup.contents[index + 1], Tag)
                and not isinstance(soup.contents[index], Tag)):
                text = soup.contents[index].string + soup.contents[index + 1].string
                text = self.prepare(text)
                if text != soup.contents[index].string:
                    soup.contents[index].replaceWith(text)
                soup.contents[index + 1].extract()
                changed = True
                continue
            index = index + 1
        return changed

    def collapse(self, soup):
        changed = True
        while changed:
            changed = False
            index = 0
            while index < len(soup.contents):
                if isinstance(soup.contents[index], Tag):
                    self.collapse(soup.contents[index])
                    if (not self.soup.isSelfClosingTag(soup.contents[index].name)
                        and soup.contents[index].name not in self.empty_tags):
                        text = soup.contents[index].renderContents(encoding=None)
                        # encoding=None: Fix bug in BeautifulSoup (don`t work with unicode)
                        text = self.prepare(text)
                        if not text or (text == ' ') or (text == self.nbsp_char 
                            and soup.contents[index].name not in self.nbsp_tag):
                            changed = True
                            if text:
                                soup.contents[index].replaceWith(text)
                            else:
                                soup.contents[index].extract()
                                continue
                index = index + 1
            if not changed:
                if self.join(soup):
                    changed = True
        return soup
        
    def collapse_root(self, soup):
        index = 0
        while index < len(soup.contents):
            if not isinstance(soup.contents[index], Tag):
                text = soup.contents[index].string
                text = self.prepare(text)
                if not text or (text == ' ') or (text == self.nbsp_char):
                    soup.contents[index].extract()
                    continue
            index = index + 1
        return soup

    def need_wrap(self, content, for_next):
        if isinstance(content, Tag):
            if content.name in self.start_tags:
                return False
        else:
            if not for_next and (content.string == '' 
                or content.string == ' ' or content.string == self.nbsp_char):
                return False
        return True
    
    def wrap(self, soup):
        index = 0
        while index < len(soup.contents):
            while index < len(soup.contents) and not self.need_wrap(soup.contents[index], False):
                index += 1
            if index >= len(soup.contents):
                break
            finish = index
            start = Tag(soup, self.default_start_tag)
            while index < len(soup.contents) and self.need_wrap(soup.contents[index], True):
                content = soup.contents[index].extract()
                start.append(content)
            soup.insert(index, start)
        return soup
        
    def get_plain_text(self, soup):
        result = u''
        for content in soup:
            if isinstance(content, Tag):
                result += self.get_plain_text(content)
            else:
                value = content.string
                for char, string in self.plain_chars:
                    value = value.replace(string, char)
                result += value
        return unicode(result)
        
    def get_soup(self, html):
        return BeautifulSoup(html, markupMassage=self.markupMassage,
            convertEntities=BeautifulSoup.ALL_ENTITIES) 
        
    def filter(self, html):
        self.soup = self.get_soup(html)
        self.soup = self.clear(self.soup)
        self.soup = self.collapse(self.soup)
        self.soup = self.collapse_root(self.soup)
        self.soup = self.wrap(self.soup)
        self.plain_text = self.get_plain_text(self.soup)
        return unicode(self.soup)
        
    def __init__(self, raw_html, trusted_dictionary, handler=None):
    # Generate: self.html, self.plain_text
        self.trusted_dictionary = trusted_dictionary
        super(Html, self).__init__(trusted_list=[], handler=handler)
        BeautifulSoup.QUOTE_TAGS = {}
        self.raw_html = unicode(raw_html)
        self.html = self.raw_html
        # print '\n~run', repr(self.html)
        for iteration in xrange(TRUSTED_ITERATIONS + 1):
            for preparing in xrange(TRUSTED_PREPARINGS + 1):
                source_html = self.html
                self.html = self.prepare(self.html)
                if source_html == self.html:
                    break
            else:
                raise ValidationError('Preparing misgiving')
            source_html = self.html
            self.html = self.filter(self.html)
            if source_html == self.html:
                break
            print '\n~fil', repr(source_html)
            print '\n=fil', repr(self.html)
        else:
            raise ValidationError('Iteration misgiving')
        # print '\n=don', repr(self.html)
        
    def __str__(self):
        return self.html

    def __unicode__(self):
        return self.html
