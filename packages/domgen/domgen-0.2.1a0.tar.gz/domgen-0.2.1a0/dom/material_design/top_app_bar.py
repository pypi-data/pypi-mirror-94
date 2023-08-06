import typing

from .. import plain_elements as dom
from . import component_register


class MenuButton(dom.Component):
    __slots__ = ("attributes", "classes")

    def apply_attributes(self, attributes: dom.Attributes) -> None:
        self.classes = attributes.pop("classes", set())
        self.classes |= {
            "material-icons",
            "mdc-top-app-bar__navigation-icon",
            "mdc-icon-button",
        }
        self.attributes = attributes
        if "aria_label" not in self.attributes:
            self.attributes["aria_label"] = "Open navigation menu"

    def set_content(self, content: dom.Content) -> None:
        self.content = dom.Button(classes=self.classes, **self.attributes)(
            *(content or ["menu"])
        )


class _AppBarBase(dom.Component):
    __slots__ = ("menu_button", "title", "toolbar_buttons", "navigation_drawer")
    menu_button: MenuButton
    title: dom.Content
    toolbar_buttons: dom.Content
    navigation_drawer: dom.Element

    def apply_attributes(self, attributes: dom.Attributes) -> None:
        self.menu_button = attributes.get("menu_button", None)
        self.title = attributes.get("title", [])
        self.toolbar_buttons = attributes.get("toolbar_buttons", [])
        self.navigation_drawer = attributes.get("navigation_drawer", None)


class _Standard(_AppBarBase):
    __slots__ = ()

    def set_content(self, content: dom.Content) -> None:
        self.content = dom.ElementGroup(
            dom.Header(classes={"mdc-top-app-bar"})(
                dom.ContentDivision(classes={"mdc-top-app-bar__row"})(
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-start",
                        }
                    )(
                        self.menu_button or "",
                        dom.Span(classes={"mdc-top-app-bar__title"})(*self.title),
                    ),
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-end",
                        },
                        role="toolbar",
                    )(*self.toolbar_buttons),
                )
            ),
            self.navigation_drawer if self.navigation_drawer else "",
            dom.MainContent(
                classes={
                    "mdc-top-app-bar--fixed-adjust",
                    "mdc-drawer-app-content" if self.navigation_drawer else "",
                }
            )(*content),
        )


class _Short(_AppBarBase):
    __slots__ = ("collapsed",)
    collapsed: bool

    def apply_attributes(self, attributes: dom.Attributes) -> None:
        self.collapsed = attributes.get("collapsed", False)
        return super().apply_attributes(attributes)

    def set_content(self, content: dom.Content) -> None:
        self.content = dom.ElementGroup(
            dom.Header(
                classes={
                    "mdc-top-app-bar",
                    "mdc-top-app-bar--short",
                    "mdc-top-app-bar--short-collapsed" if self.collapsed else "",
                }
            )(
                dom.ContentDivision(classes={"mdc-top-app-bar__row"})(
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-start",
                        }
                    )(
                        self.menu_button or "",
                        dom.Span(classes={"mdc-top-app-bar__title"})(*self.title),
                    ),
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-end",
                        },
                        role="toolbar",
                    )(*self.toolbar_buttons),
                )
            ),
            self.navigation_drawer if self.navigation_drawer else "",
            dom.MainContent(
                classes={
                    "mdc-top-app-bar--short-fixed-adjust",
                    "mdc-drawer-app-content" if self.navigation_drawer else "",
                }
            )(*content),
        )


class _Fixed(_AppBarBase):
    __slots__ = ()

    def set_content(self, content: dom.Content) -> None:
        self.content = dom.ElementGroup(
            dom.Header(classes={"mdc-top-app-bar", "mdc-top-app-bar--fixed"})(
                dom.ContentDivision(classes={"mdc-top-app-bar__row"})(
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-start",
                        }
                    )(
                        self.menu_button or "",
                        dom.Span(classes={"mdc-top-app-bar__title"})(*self.title),
                    ),
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-end",
                        },
                        role="toolbar",
                    )(*self.toolbar_buttons),
                )
            ),
            self.navigation_drawer if self.navigation_drawer else "",
            dom.MainContent(
                classes={
                    "mdc-top-app-bar--fixed-adjust",
                    "mdc-drawer-app-content" if self.navigation_drawer else "",
                }
            )(*content),
        )


class _Prominent(_AppBarBase):
    __slots__ = ()

    def set_content(self, content: dom.Content) -> None:
        self.content = dom.ElementGroup(
            dom.Header(classes={"mdc-top-app-bar", "mdc-top-app-bar--prominent"})(
                dom.ContentDivision(classes={"mdc-top-app-bar__row"})(
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-start",
                        }
                    )(
                        self.menu_button or "",
                        dom.Span(classes={"mdc-top-app-bar__title"})(*self.title),
                    ),
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-end",
                        },
                        role="toolbar",
                    )(*self.toolbar_buttons),
                )
            ),
            self.navigation_drawer if self.navigation_drawer else "",
            dom.MainContent(
                classes={
                    "mdc-top-app-bar--prominent-fixed-adjust",
                    "mdc-drawer-app-content" if self.navigation_drawer else "",
                }
            )(*content),
        )


class _Dense(_AppBarBase):
    __slots__ = ()

    def set_content(self, content: dom.Content) -> None:
        self.content = dom.ElementGroup(
            dom.Header(classes={"mdc-top-app-bar", "mdc-top-app-bar--dense"})(
                dom.ContentDivision(classes={"mdc-top-app-bar__row"})(
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-start",
                        }
                    )(
                        self.menu_button or "",
                        dom.Span(classes={"mdc-top-app-bar__title"})(*self.title),
                    ),
                    dom.Section(
                        classes={
                            "mdc-top-app-bar__section",
                            "mdc-top-app-bar__section--align-end",
                        },
                        role="toolbar",
                    )(*self.toolbar_buttons),
                )
            ),
            self.navigation_drawer if self.navigation_drawer else "",
            dom.MainContent(
                classes={
                    "mdc-top-app-bar--dense-fixed-adjust",
                    "mdc-drawer-app-content" if self.navigation_drawer else "",
                }
            )(*content),
        )


class TopAppBar(dom.Component):
    """Top App Bar.

    https://material.io/components/app-bars-top/

    Comes in 5 variants:
      - Standard
      - Short
      - Fixed
      - Prominent
      - Dense

    Takes the following parameters:
      - `variant`: One of `'standard'`, `'short'`, `'fixed'`, `'prominent'`,
        and `'dense'`. Selects the kind of top app bar to use.
      - `menu_button`: If present, should be an instance of MenuButton. Used
        to activate the menu. No functionality is provided by default.
      - `title`: Text (or elements) to display as the page title.
      - `toolbar_buttons`: A collection of elements to display as buttons in
        the app bar.
      - `navigation_drawer`: If present, should be an instance of
        NavigationDrawer.
      - `collapsed`: True to always collapse the app bar (Short app bar only).
    """

    __slots__ = ()
    content: _AppBarBase

    def apply_attributes(self, attributes: dom.Attributes) -> None:
        component_register(
            "https://starwort.github.io/domgen/cdn/styles/top_app_bar.css",
            "https://starwort.github.io/domgen/cdn/javascript/top_app_bar.js",
        )
        self.content = {
            "standard": _Standard,
            "short": _Short,
            "fixed": _Fixed,
            "prominent": _Prominent,
            "dense": _Dense,
        }[attributes.get("variant", "standard")](**attributes)

    def set_content(self, content: dom.Content) -> None:
        self.content.set_content(content)
