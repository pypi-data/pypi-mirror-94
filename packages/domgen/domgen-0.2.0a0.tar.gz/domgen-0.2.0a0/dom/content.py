from .base_classes import Container, Void


class BlockQuotation(Container):
    """The HTML `<blockquote>` Element (or HTML Block Quotation Element)
    indicates that the enclosed text is an extended quotation. Usually,
    this is rendered visually by indentation (see Notes for how to change
    it). A URL for the source of the quotation may be given using the cite
    attribute, while a text representation of the source can be given using
    the `<cite>` element.
    """

    __slots__ = ()
    tag = "blockquote"


BlockQuote = BlockQuotation


class DescriptionTerm(Container):
    """The HTML `<dt>` element specifies a term in a description or definition
    list, and as such must be used inside a `<dl>` element. It is usually followed
    by a `<dd>` element; however, multiple `<dt>` elements in a row indicate several
    terms that are all defined by the immediate next `<dd>` element.
    """

    tag = "dt"


DT = DescriptionTerm


class DescriptionDetails(Container):
    """The HTML `<dd>` element provides the description, definition, or value for
    the preceding term (`<dt>`) in a description list (`<dl>`).
    """

    tag = "dd"


DD = DescriptionDetails


class DescriptionList(Container):
    """The HTML `<dl>` element represents a description list. The element
    encloses a list of groups of terms (specified using the `<dt>` element)
    and descriptions (provided by `<dd>` elements). Common uses for this
    element are to implement a glossary or to display metadata (a list of
    key-value pairs).
    """

    __slots__ = ()


DL = DescriptionList


class ContentDivision(Container):
    """The HTML Content Division element (`<div>`) is the generic container
    for flow content. It has no effect on the content or layout until styled
    using CSS.
    """

    __slots__ = ()
    tag = "div"


Div = ContentDivision


class Figure(Container):
    """The HTML `<figure>` (Figure With Optional Caption) element represents
    self-contained content, potentially with an optional caption, which is
    specified using the FigureCaption (`<figcaption>`) element.
    """

    __slots__ = ()
    tag = "figure"


class FigureCaption(Container):
    """The HTML `<figcaption>` or Figure Caption element represents a caption
    or legend describing the rest of the contents of its parent `<figure>`
    element.
    """

    __slots__ = ()
    tag = "figcaption"


FigCaption = FigureCaption


class Divider(Void):
    """The HTML `<hr>` element represents a thematic break between
    paragraph-level elements: for example, a change of scene in a story, or a
    shift of topic within a section.
    """

    __slots__ = ()
    tag = "hr"


HR = Divider


class OrderedList(Container):
    """The HTML `<ol>` element represents an ordered list of items — typically
    rendered as a numbered list.
    """

    __slots__ = ()
    tag = "ol"


OL = OrderedList


class UnorderedList(Container):
    """The HTML `<ul>` element represents an unordered list of items, typically
    rendered as a bulleted list.
    """

    __slots__ = ()
    tag = "ul"


UL = UnorderedList


class Paragraph(Container):
    """The HTML `<p>` element represents a paragraph."""

    __slots__ = ()
    tag = "p"


P = Paragraph


class PreformattedText(Container):
    """The HTML `<pre>` element represents preformatted text which is to be
    presented exactly as written in the HTML file.
    """

    __slots__ = ()
    tag = "pre"


Pre = PreformattedText
