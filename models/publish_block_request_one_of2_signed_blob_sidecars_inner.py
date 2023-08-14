# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from models.publish_block_request_one_of2_signed_blob_sidecars_inner_message import PublishBlockRequestOneOf2SignedBlobSidecarsInnerMessage


class PublishBlockRequestOneOf2SignedBlobSidecarsInner(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    PublishBlockRequestOneOf2SignedBlobSidecarsInner - a model defined in OpenAPI

        message: The message of this PublishBlockRequestOneOf2SignedBlobSidecarsInner [Optional].
        signature: The signature of this PublishBlockRequestOneOf2SignedBlobSidecarsInner [Optional].
    """

    message: Optional[PublishBlockRequestOneOf2SignedBlobSidecarsInnerMessage] = Field(alias="message", default=None)
    signature: Optional[str] = Field(alias="signature", default=None)

    @validator("signature")
    def signature_pattern(cls, value):
        assert value is not None and re.match(r"^0x[a-fA-F0-9]{192}$", value)
        return value

PublishBlockRequestOneOf2SignedBlobSidecarsInner.update_forward_refs()
