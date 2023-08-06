import typing

from .. import plain_elements as dom

_INITIALISER_CSS_URLS = set()
_FINALISER_JS_URLS = set()


def component_register(css_url: str, js_url: str) -> None:
    """MDC components will call this function during their initialisation to
    register with the module variables above. Using this function manually is
    not recommended, but will probably work to register both CSS and finalising
    JS to be included with the MDC loader components"""
    _INITIALISER_CSS_URLS.add(css_url)
    _FINALISER_JS_URLS.add(js_url)


def clear_component_cache():
    """Use this to clear the cache of used components.

    Useful for if the same Python process is used to generate several pages
    using Material elements.
    """
    _INITIALISER_CSS_URLS.clear()
    _FINALISER_JS_URLS.clear()


class MDCInitialiser(dom.Component):
    """Place this in the head of your document to include the required CSS.

    Takes keyword argument `theme` with a value of either `"dark"` (default)
    or `"light"`.

    Expects no content, and as such any content passed will be ignored.
    """

    __slots__ = ("theme_variant",)
    theme_variant: typing.Literal["dark", "light"]

    def apply_attributes(self, attributes: typing.Dict[str, typing.Any]) -> None:
        self.theme_variant = attributes.get("theme", "dark")
        extra_kws = set(attributes.keys()) - {"theme"}
        assert extra_kws == set(), "Unexpected keyword arguments passed: " + ", ".join(
            extra_kws
        )

    def set_content(
        self, content: typing.List[typing.Union[dom.Element, str]] = None
    ) -> None:
        self.content = dom.ElementGroup(
            *[dom.ExternalStyleSheet(href=css_url) for css_url in _INITIALISER_CSS_URLS]
        )

    def serialise(self, minify: bool) -> str:
        self.set_content()
        return super().serialise(minify=minify)


class MDCFinaliser(dom.Component):
    """Place this at the bottom of your document to include the required JS.

    Expects no content, and as such any content passed will be ignored.
    """

    __slots__ = ()

    def apply_attributes(self, attributes: typing.Dict[str, typing.Any]) -> None:
        if attributes:
            raise TypeError("MDCFinaliser components take no attributes")

    def set_content(
        self, content: typing.List[typing.Union[dom.Element, str]] = None
    ) -> None:
        self.content = dom.ElementGroup(
            *[dom.Script(src=js_url) for js_url in _FINALISER_JS_URLS]
        )

    def serialise(self, minify: bool) -> str:
        self.set_content()
        return super().serialise(minify=minify)
