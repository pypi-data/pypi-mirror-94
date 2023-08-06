import re
import uuid

from typing import Dict

from . import parse
from .consts import CCML_DICTIONARY


# Consts.
XML_TAG_REG = r"<((\/|)+[a-z]+)({gensym})+([a-z]+)"


def __convert_to_ccml(text: str, tags_dictionary: Dict):
    """
    Handle tag replacement in target text.

    Arguments:
        text: (string) Target text.
        tags_dictionary: (dict) Tags dictionary, key to replace with value.

    Returns:
        CCML text (string).
    """
    result_text = text

    gensym_str = uuid.uuid4().hex[:5]

    for ccml_tag, tag_name in tags_dictionary.items():
        if tag_name:
            if ":" in tag_name:
                tag_name = tag_name.replace(":", gensym_str)
            result_text = parse.rename_tag(
                text=result_text, tag_name=ccml_tag, new_tag_name=tag_name
            )

    res = re.sub(XML_TAG_REG.format(gensym=gensym_str), "<\g<1>:\g<4>", result_text)

    return res


def ccml_to_aws_polly(text_input):
    """
    Convert CCML tags to AWS Polly SSML tags and remove wrong tags.

    Arguments:
        text_input: (string) CCML input to convert to AWS Polly SSML.

    Returns:
        AWS Polly SSML text (string).
    """
    aws_polly_ccml_tags = list(CCML_DICTIONARY["aws_polly"].keys())
    common_ccml_tags = list(CCML_DICTIONARY["common"].keys())

    clean_text = parse.remove_invalid_tags(
        text=text_input, valid_tags=[*aws_polly_ccml_tags, *common_ccml_tags]
    )

    aws_polly_ssml = __convert_to_ccml(
        text=clean_text, tags_dictionary=CCML_DICTIONARY["aws_polly"]
    )

    return aws_polly_ssml


def ccml_to_amazon(text_input):
    """
    Convert CCML tags to Amazon SSML tags and remove wrong tags.

    Arguments:
        text_input: (string) CCML input to convert to Amazon SSML.

    Returns:
        Amazon SSML text (string).
    """
    amazon_ccml_tags = list(CCML_DICTIONARY["amazon"].keys())
    common_ccml_tags = list(CCML_DICTIONARY["common"].keys())

    clean_text = parse.remove_invalid_tags(
        text=text_input, valid_tags=[*amazon_ccml_tags, *common_ccml_tags]
    )

    amazon_ssml = __convert_to_ccml(
        text=clean_text, tags_dictionary=CCML_DICTIONARY["amazon"]
    )
    return amazon_ssml


def ccml_to_google(text_input):
    """
    Convert CCML tags to Google SSML tags and remove wrong tags.

    Arguments:
        text_input: (string) CCML input to convert to Google SSML.

    Returns:
        Google SSML text (string).
    """
    google_ccml_tags = list(CCML_DICTIONARY["google"].keys())
    common_ccml_tags = list(CCML_DICTIONARY["common"].keys())

    clean_text = parse.remove_invalid_tags(
        text=text_input, valid_tags=[*google_ccml_tags, *common_ccml_tags]
    )

    return __convert_to_ccml(text=clean_text, tags_dictionary=CCML_DICTIONARY["google"])


def ccml_to_twiml(text_input):
    """
    Convert CCML tags to Twilio SSML(TwiML) tags and remove wrong tags.

    Arguments:
        text_input: (string) CCML input to convert to Twilio SSML(TwiML).

    Returns:
        TwiML text (string).
    """
    twilio_ccml_tags = list(CCML_DICTIONARY["twilio"].keys())
    common_ccml_tags = list(CCML_DICTIONARY["common"].keys())

    clean_text = parse.remove_invalid_tags(
        text=text_input, valid_tags=[*twilio_ccml_tags, *common_ccml_tags]
    )

    return __convert_to_ccml(text=clean_text, tags_dictionary=CCML_DICTIONARY["twilio"])
