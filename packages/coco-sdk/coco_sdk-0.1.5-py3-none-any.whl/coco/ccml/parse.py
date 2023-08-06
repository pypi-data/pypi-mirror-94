import re

from typing import List

import lxml.etree as ET


# Consts.
SPECIFIC_TAG_REGEX = "<(\/|)({0})(|[^\<\>]+)>"


def rename_tag(text: str, tag_name: str, new_tag_name: str):
    """
    Rename tags in XML included text.

    Arguments:
        text: (string) Target XML included string.
        tag_name: (string) Tag name to rename.
        new_tag_name: (string) Target tag name.

    Returns:
        Updated XML string (string).
    """
    et = ET.fromstring(f"<body>{text}</body>")
    found_tags = et.xpath(f"//{tag_name}")

    for tag in found_tags:
        tag.tag = new_tag_name
    return ET.tounicode(et)[6:-7]


def remove_tag(text: str, tag_name: str):
    """
    Remove tag without removing the tag content.

    Arguments:
        text: (string) Target XML included string.
        tag_name: (string) Tag name to remove.

    Returns:
         Updated XML string (string).
    """
    reg = re.compile(SPECIFIC_TAG_REGEX.format(tag_name))

    for match in reg.finditer(text):
        text = text.replace(match[0], "")

    return text


def remove_invalid_tags(text: str, valid_tags: List):
    """
    Remove invalid tags from text input.

    Arguments:
        text: (string) Target XML included string.
        valid_tags: (list) White list of tags to leave.

    Returns:
        Clean text (string).
    """
    et = ET.fromstring(f"<body>{text}</body>")

    result_text = ET.tostring(et).decode("utf-8")

    for tag_name in list(set([tag.tag for tag in et.iter()])):
        if tag_name not in valid_tags:
            result_text = remove_tag(text=result_text, tag_name=tag_name)

    return result_text


def clear_xml_tags(text: str):
    """
    Remove all xml tags from text.
    Arguments:
        text: (string) Target string.
    Returns:
        Clean text without XML tags. (string)
    """
    return ET.tostring(
        ET.fromstring(f"<wrap>{text}</wrap>".encode("utf-8")),
        method="text",
        encoding="utf-8",
    ).decode("utf-8")
