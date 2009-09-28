"""
Attributes for Index of Attributes
http://www.w3.org/TR/REC-html40/index/attributes.html
"""

from trustedhtml.utils import get_dict
from trustedhtml.classes import Element
from trustedhtml.rules import css
from trustedhtml.rules.html.elements import elements
from trustedhtml.rules.html.attributes import attributes

# We don`t want to support whole document.
# We share content only as a part of our page.
# So we separate it (remove from allowed).
docement_elements = [
    'body',
    'head',
    'html',
    'link',
    'meta',
    'title',
]

# We don`t want to support frames. Like document elements.
frame_elements = [
    'frame',
    'frameset',
    'noframes',
]

# We don`t want to support
form_elements = [
    'button',
    'fieldset',
    'form',
    'input',
    'label',
    'legend',
    'optgroup',
    'option',
    'select',
    'textarea',
]

remove_elements = [
    # It can change meaning of url, so it must be disabled
    'base',
    # It will break fonts
    'basefont',
    # Deprecated
    'center',
    # Deprecated
    'dir',
    # Deprecated, it will break fonts
    'font',
    # Deprecated
    'isindex',
    # Deprecated
    'menu',
    # We want to show text that must be shown only if user agent  
    # don`t support (execute) script. Because of we disable any script.
    'noscript',
    # Deprecated
    's',
    # Deprecated
    'strike',
    # It will break style sheets
    'style',
    # Deprecated
    'u',
]

remove_elements_with_content = [
    # It is deprecated, and it is security hole.
    'applet',
    # It is security hole.
    'iframe',
    # Strange, but we don`t want to allow it.
    'script',
]


# We must specified css rules for all elements.
# So, we want to use as little elements as possible.
simple_elements = [
    'a',
    'address',
    'blockquote',
    'br',
    'caption',
    'del',
    'div',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr',
    'ins',
    'img',
    'li',
    'object',
    'ol',
    'p',
    'pre',
    'q',
    'param',
    'small',
    'span',
    'strong',
    'sub',
    'sup',
    'table',
    'tbody',
    'td',
    'th',
    'tr',
    'ul',
    'noindex', # This not w3c tag, but it is used by Yandex search engine
]

# But we specified rare elements.
# They can`t be generated by TinyMCE.
rare_elements = [
    'abbr',
    'acronym',
    'area',
    'b',
    'bdo',
    'big',
    'cite',
    'code',
    'col',
    'colgroup',
    'dd',
    'dfn',
    'dl',
    'dt',
    'i',
    'kbd',
    'map',
    'samp',
    'tfoot',
    'thead',
    'tt',
    'var',
]

# Remove attributes for all elements:
remove_attributes_for_all = [
    # It can overwrite sites accesskey:
    'accesskey',
    # We don`t want to allow to use id,
    # reserved for core site functions and view.
    'id',
    # We don`t want to allow to use classes,
    # reserved for core site functions and view.
    'class',
    # It is deprecated and not used:
    'compact',
    # It is deprecated and will break view:
    'bgcolor',
    # It will break view
    'frameborder',
    # It is deprecated and will break view:
    'hspace',
    # We want to disable all scripts:
    'onblur',
    'onchange',
    'onclick',
    'ondblclick',
    'onfocus',
    'onkeydown',
    'onkeypress',
    'onkeyup',
    'onload',
    'onmousedown',
    'onmousemove',
    'onmouseout',
    'onmouseover',
    'onmouseup',
    'onreset',
    'onselect',
    'onsubmit',
    'onunload',
    # It is deprecated and will break view:
    'nowrap',
    # It is deprecated and will break view:
    'vspace',
]

# Remove attributes for specified elements:
remove_attributes_for_element = {}

remove_attributes_for_element['body'] = [
    # It will break text align:
    'align',
    # Deprecated, it will break view
    'alink',
    # Deprecated, it will break view
    'background',
    # Deprecated, it will break view
    'link',
    # Deprecated, it will break view
    'text',
    # Deprecated, it will break view
    'vlink',
]

# It is deprecated, it can be disabled if aligning of images will be disabled.
#remove_attributes_for_element['br'] = [
#    'clear',
#]

# It is deprecated, it can be disabled if aligning in tables will be disabled.
#remove_attributes_for_element['caption'] = [
#    'align',
#]

remove_attributes_for_element['col'] = [
    # It will break view
    'width',
]

remove_attributes_for_element['colgroup'] = [
    # It will break view
    'width',
]

remove_attributes_for_element['div'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['h1'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['h2'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['h3'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['h4'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['h5'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['h6'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['html'] = [
    # It is deprecated and can break view:
    'version'
]

remove_attributes_for_element['hr'] = [
    # It will break text align:
    'align',
    # It is deprecated and will break view: 
    'noshade',
    # It is deprecated and will break view:
    'size',
    # It is deprecated and will break view:
    'width',
]

remove_attributes_for_element['img'] = [
    # It will break text align:
    'align',
    # It is deprecated and will break view:
    'border',
    # Fix: it must be disabled if area and map elements will be disabled:
    #'ismap',
    # Fix: it must be disabled if area and map elements will be disabled:
    #'usemap',
]

remove_attributes_for_element['input'] = [
    # It will break text align:
    'align',
    # Fix: it must be disabled if area and map elements will be disabled:
    #'ismap',
    # It can break meaning of button
    'src',
    # Fix: it must be disabled if area and map elements will be disabled:
    #'usemap',
]

remove_attributes_for_element['legend'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['li'] = [
    # It is deprecated and it will break formatting
    'type',
    # It is deprecated and it will break formatting
    'value',
]

remove_attributes_for_element['object'] = [
    # It will break text align:
    'align',
    # It is deprecated and will break view:
    'border',
    # Fix: it must be disabled if area and map elements will be disabled:
    #'usemap',
]

remove_attributes_for_element['ol'] = [
    # It is deprecated and it will break formatting
    'start',
    # It is deprecated and it will break formatting
    'type',
]

remove_attributes_for_element['p'] = [
    # It will break text align:
    'align',
]

remove_attributes_for_element['pre'] = [
    # It is deprecated and it will break formatting
    'width',
]

remove_attributes_for_element['table'] = [
    # It will break text align:
    'align',
    # It will break view:
    'border',
    # It will break view:
    'cellpadding',
    # It will break view:
    'cellspacing',
    # It will break view:
    'frame',
    # It will break view:
    'rules',
    # It will break view:
    'width',
]

remove_attributes_for_element['td'] = [
    # It will break view:
    'height',
    # It will break view:
    'width',
]

remove_attributes_for_element['th'] = [
    # It will break view:
    'height',
    # It will break view:
    'width',
]

remove_attributes_for_element['ul'] = [
    # It is deprecated and it will break formatting
    'type',
]

replace_attributes_for_all = {
    'style': css.common,
}

replace_attributes_for_element = {}

replace_attributes_for_element['img'] = {
    'style': css.images,
}

replace_attributes_for_element['caption'] = {
    'style': css.tables,
}

replace_attributes_for_element['thead'] = {
    'style': css.tables,
}

replace_attributes_for_element['tfoot'] = {
    'style': css.tables,
}

replace_attributes_for_element['tbody'] = {
    'style': css.tables,
}

replace_attributes_for_element['tr'] = {
    'style': css.tables,
}

replace_attributes_for_element['td'] = {
    'style': css.tables,
}

replace_attributes_for_element['th'] = {
    'style': css.tables,
}

def get_elements(leave):
    result = {}
    for name, value in get_dict(source=elements, leave=leave).iteritems():
        remove = remove_attributes_for_all + remove_attributes_for_element.get(name, [])
        replace = {}
        replace.update(replace_attributes_for_all)
        replace.update(replace_attributes_for_element.get(name, {}))
        rules = get_dict(attributes[name], remove=remove, append=replace)
        element = Element(rules=rules, empty_element=value.empty_element,
            optional_start=value.optional_start, optional_end=value.optional_end,
            contents=value.contents, save_content=value.save_content)
        result[name] = element
    for name in remove_elements_with_content:
        element = Element(remove_element=True, save_content=False)
        result[name] = element
    return result
    
simple = get_elements(simple_elements)
normal = get_elements(simple_elements + rare_elements)

# Fix: anchors (in this order, because of empty_element)
#replace_elements['a'] = Or(rules=[
#    Elements(empty_element=True, rules=get_dict(
#        source=elements,
#        replace={
#            'name': values['name~r'],
#        })
#    ),
#    Elements(empty_element=False, rules=get_dict(
#        source=elements,
#        replace={
#            'href': values['href~r'],
#        })
#    ),
#])

# Fix: check values:
#values['char'] = character
## alignment char, e.g. char=':' (COL, COLGROUP, TBODY, TD, TFOOT, TH, THEAD, TR)
#
#values['charoff'] = length
## offset for alignment char (COL, COLGROUP, TBODY, TD, TFOOT, TH, THEAD, TR)
#
#values['charset'] = charset
## char encoding of linked resource (A, LINK, SCRIPT)
#
#values['checked'] = RegExp(regexp=r'(checked)$')
## for radio buttons and check boxes (INPUT)
#
#values['cite'] = uri
## URI for source document or msg (BLOCKQUOTE, Q)
#
#values['cite'] = uri
## info on reason for change (DEL, INS)
#
#values['classid'] = uri
## identifies an implementation (OBJECT)
#
#values['codebase'] = uri
## base URI for classid, data, archive (OBJECT)
#
#values['codetype'] = content_type
## content type for code (OBJECT)
#
#values['cols'] = multi_lengths
## list of lengths, default: 100% = 1 col (FRAMESET)
#
#values['cols'] = number_required
##  (TEXTAREA)
#
#values['colspan'] = number
## number of cols spanned by cell (TD, TH)
#
#values['content'] = text_required
## associated information (META)
#
#values['coords'] = coords # Fix: The number and order of values depends on the shape being defined.
## comma-separated list of lengths (AREA)
#
#values['coords'] = coords
## for use with client-side image maps (A)
#
#values['data'] = uri
## reference to object's data (OBJECT)
#
#values['datetime'] = datetime
## date and time of change (DEL, INS)
#
#values['declare'] = RegExp(regexp=r'(declare)$')
## declare but don't instantiate flag (OBJECT)
#
#values['defer'] = RegExp(regexp=r'(defer)$')
## UA may defer execution of script (SCRIPT)
#
#values['dir'] = RegExp(regexp=r'(ltr|rtl)$')
## direction for weak/neutral text (All elements but APPLET, BASE, BASEFONT, BDO, BR, FRAME, FRAMESET, IFRAME, PARAM, SCRIPT)
#
#values['dir~r'] = RegExp(regexp=r'(ltr|rtl)$', element_exception=True)
## directionality (BDO)
#
#values['disabled'] = RegExp(regexp=r'(disabled)$')
## unavailable in this context (BUTTON, INPUT, OPTGROUP, OPTION, SELECT, TEXTAREA)
#
#values['enctype'] = content_type
##  (FORM)
#
#values['for'] = name
## matches field ID value (LABEL)
#
#values['headers'] = idrefs
## list of id's for header cells (TD, TH)
#
#values['href'] = uri
## URI for linked resource (A, AREA, LINK)
#
#values['href~r'] = uri_required
## Used by href version of tag A
#
#values['href'] = uri
## URI that acts as base URI (BASE)
#
#values['hreflang'] = language_code # Fix: may only be used when href is specified.
## language code (A, LINK)
#
#values['http-equiv'] = name
## HTTP response header name (META)
#
#values['marginheight'] = pixels
## margin height in pixels (FRAME, IFRAME)
#
#values['marginwidth'] = pixels
## margin widths in pixels (FRAME, IFRAME)
#
#values['maxlength'] = number
## max chars for text fields (INPUT)
#
#values['media'] = media_descs
## designed for use with these media (STYLE)
#
#values['media'] = media_descs
## for rendering on these media (LINK)
#
#values['multiple'] = RegExp(regexp=r'(multiple)$')
## default is single selection (SELECT)
#
#values['nohref'] = RegExp(regexp=r'(nohref)$')
## this region has no action (AREA)
#
#values['noresize'] = RegExp(regexp=r'(noresize)$')
## allow users to resize frames? (FRAME)
#
#values['profile'] = uris
## named dictionary of meta info (HEAD)
#
#values['rows'] = multi_lengths
## list of lengths, default: 100% = 1 row (FRAMESET)
#
#values['rows'] = number_required
##  (TEXTAREA)
#
#values['rowspan'] = number
## number of rows spanned by cell (TD, TH)
#
#values['scheme'] = text
## select form of content (META)
#
#values['scope'] = RegExp(regexp=r'(row|col|rowgroup|colgroup)$')
## scope covered by header cells (TD, TH)
#
#values['scrolling'] = RegExp(regexp=r'(yes|no|auto)$')
## scrollbar or none (FRAME, IFRAME)
#
#values['selected'] = RegExp(regexp=r'(selected)$')
##  (OPTION)
#
#values['shape'] = RegExp(regexp=r'(default|rect|circle|poly)$')
## controls interpretation of coords (AREA)
#
#values['shape'] = RegExp(regexp=r'(default|rect|circle|poly)$')
## for use with client-side image maps (A)
#
#values['span'] = positive_number
## COL attributes affect N columns (COL)
#
#values['span'] = positive_number
## default number of columns in group (COLGROUP)
#
#values['standby'] = text
## message to show while loading (OBJECT)
#
#values['style'] = style_sheet
## associated style info (All elements but BASE, BASEFONT, HEAD, HTML, META, PARAM, SCRIPT, STYLE, TITLE)
#
#values['summary'] = text
## purpose/structure for speech output (TABLE)
#
#values['tabindex'] = number
## position in tabbing order (A, AREA, BUTTON, INPUT, OBJECT, SELECT, TEXTAREA)
#
#values['target'] = frame_target
## render in this frame (A, AREA, BASE, FORM, LINK)
#
#values['title'] = text
## advisory title (All elements but BASE, BASEFONT, HEAD, HTML, META, PARAM, SCRIPT, TITLE)
#
#values['valign'] = RegExp(regexp=r'(top|middle|bottom|baseline)$')
## vertical alignment in cells (COL, COLGROUP, TBODY, TD, TFOOT, TH, THEAD, TR)
