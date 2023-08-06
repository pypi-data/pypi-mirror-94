import json
import typing
from abc import ABCMeta, abstractmethod
from textwrap import indent


def transform(attributes: typing.Dict[str, typing.Any]) -> typing.Dict[str, str]:
    """Transform `attributes` for serialisation.

    `attributes` is not mutated; a new dictionary is returned.

    `classes`, if present, must be a `set` of classes to apply to the
    element. Empty strings will be removed from this set, so they are
    useable to toggle a class with a boolean.

    Any attribute name with an underscore in it has its underscores
    transformed into hyphens (for ARIA, JavaScript `data-` attributes,
    and similar) - use two underscores to represent a literal underscore.

    Additionally, single trailing underscores are removed.

    Attribute values are serialised as JSON, and non-strings are then
    serialised as JSON again (to be XHTML-compliant and avoid breaking
    arrays or objects as attribute values).
    """
    new_attributes = {}
    classes = attributes.pop("classes", set())
    if classes:
        attributes["class"] = " ".join(classes - {""})
    for key, value in attributes.items():
        if not isinstance(value, str):
            # convert value to a string containing JSON
            value = json.dumps(value)
        # convert value to a JSON-encoded string (double quotes, for HTML
        # attribute values)
        value = json.dumps(value.replace('"', "&quot;"))
        # remove single trailing underscore
        if key[-1] == "_" and key[-2] != "_":
            key = key[:-1]
        # replace double underscore with single underscore, and other
        # underscores with hyphens
        key = key.replace("__", " ").replace("_", "-").replace(" ", "_")
        new_attributes[key] = value
    return new_attributes


class Element(metaclass=ABCMeta):
    """Base class for all elements

    You should never need to inherit from this directly - use `Component` in
    most cases, or for custom elements use `Container` and `Void`

    When any element is created, its `apply_attributes` method is guaranteed
    to be called first, followed by its `set_content` method.

    Note: If the element is then called (HTML-style content initialisation)
    then its `set_content` method will be called again
    """

    __slots__ = ()

    def __init__(
        self, *content: typing.Union["Element", str], **attributes: typing.Any
    ) -> None:
        self.apply_attributes(attributes)
        self.set_content(list(content))

    def __call__(self, *content: typing.Union["Element", str]) -> "Element":
        self.set_content(list(content))
        return self

    @abstractmethod
    def serialise(self, minify: bool = True) -> str:
        """Return an HTML representation of the model"""

    @abstractmethod
    def set_content(self, content: typing.List[typing.Union["Element", str]]) -> None:
        """Set content - called by __init__ and __call__"""

    @abstractmethod
    def apply_attributes(self, attributes: typing.Dict[str, typing.Any]) -> None:
        """Apply attributes - called by __init__

        Guaranteed to be called before set_content"""

    def __str__(self) -> str:
        return self.serialise(minify=False)


class TextElement(Element):
    __slots__ = ("content",)
    content: str

    def serialise(self, minify: bool = True) -> str:
        """Return an HTML representation of the model"""
        return self.content

    def set_content(self, content: typing.List[typing.Union["Element", str]]) -> None:
        self.content = content[0]
        if not isinstance(self.content, str):
            raise TypeError(
                "Text content must be a single string (got {!r})".format(
                    type(self.content).__qualname__
                )
            )
        if len(content) != 1:
            raise TypeError(
                "Text content must be a single string (got {} items)".format(
                    len(content)
                )
            )

    def apply_attributes(self, attributes: typing.Dict[str, typing.Any]) -> None:
        if attributes:
            raise TypeError("Text content cannot have attributes")


class Container(Element):
    """Base class for all container/non-void elements

    Most inheriters only need to define `tag`
    """

    __slots__ = ("tag", "content", "attributes")
    tag: str
    content: typing.List["Element"]
    attributes: typing.Dict[str, typing.Any]

    def serialise(self, minify: bool = True) -> str:
        """Return an HTML representation of the model"""
        return (
            "<"
            + self.tag
            + (
                (" " + " ".join(f"{k}={v}" for k, v in self.attributes.items()))
                if self.attributes
                else ""
            )
            + ">"
            + ("" if minify else "\n")
            + indent(
                ("" if minify else "\n").join(
                    child.serialise(minify=minify) for child in self.content
                ),
                "    ",
                lambda i: not minify,
            )
            + ("" if minify else "\n")
            + f"</{self.tag}>"
        )

    def set_content(self, content: typing.List[typing.Union["Element", str]]) -> None:
        self.content = [
            child if isinstance(child, Element) else TextElement(child)
            for child in content
        ]

    def apply_attributes(self, attributes: typing.Dict[str, typing.Any]) -> None:
        self.attributes = transform(attributes)

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + ", ".join(repr(child) for child in self.content)
            + (", " if self.content and self.attributes else "")
            + ", ".join(f"{k}={v!r}" for k, v in self.attributes.items())
            + ")"
        )


class Void(Element):
    """Base class for all non-container/void elements

    Most inheriters only need to define `tag`
    """

    __slots__ = ("tag", "attributes")
    tag: str
    attributes: typing.Dict[str, typing.Any]

    def serialise(self, minify: bool = True) -> str:
        """Return an HTML representation of the model"""
        return (
            "<"
            + self.tag
            + (
                (" " + " ".join(f"{k}={v}" for k, v in self.attributes.items()))
                if self.attributes
                else ""
            )
            + " />"
        )

    def set_content(self, content: typing.List[typing.Union["Element", str]]) -> None:
        if content:
            raise TypeError("Void elements cannot have content")

    def apply_attributes(self, attributes: typing.Dict[str, typing.Any]) -> None:
        self.attributes = transform(attributes)

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + ", ".join(f"{k}={v}" for k, v in self.attributes.items())
            + ")"
        )


class Component(Element):
    """Base class for custom components

    `apply_attributes` is always called before `set_content` so it can be
    used to control the behaviour of the component
    """

    __slots__ = ("content",)
    content: Element

    def serialise(self, minify: bool = True) -> str:
        """Return an HTML representation of the model"""
        return self.content.serialise(minify=minify)
