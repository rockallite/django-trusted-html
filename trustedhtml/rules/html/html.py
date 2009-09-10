# -*- coding: utf-8 -*-

from trustedhtml.classes import Html
from trustedhtml.rules import tags

full = Html(rules={
    'a': tags.a,
    'address': tags.address,
    'b': tags.b,
    'blockquote': tags.blockquote,
    'br': tags.br,
    'caption': tags.caption,
    'cite': tags.cite,
    'div': tags.div,
    'dl': tags.dl,
    'dt': tags.dt,
    'h1': tags.h1,
    'img': tags.img,
    'li': tags.li,
    'ol': tags.ol,
    'p': tags.p,
    'pre': tags.pre,
    'span': tags.span,
    'table': tags.table,
    'tbody': tags.tbody,
    'td': tags.td,
    'tr': tags.tr,
    'ul': tags.ul,
}
, equivalents = {
    'h1': [
        'h2', 'h3', 'h4', 'h5', 'h6',
    ],
    'b': [
        'em', 'i', 'strong', 'sub', 'sup', 'u',
    ],
    'td': [
        'th',
    ],
})