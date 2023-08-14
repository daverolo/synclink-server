# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from models.publish_block_request_one_of2_signed_blob_sidecars_inner_message import PublishBlockRequestOneOf2SignedBlobSidecarsInnerMessage
from models.publish_block_request_one_of2_signed_block_message import PublishBlockRequestOneOf2SignedBlockMessage


class ProduceBlockV3ResponseDataOneOf(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ProduceBlockV3ResponseDataOneOf - a model defined in OpenAPI

        block: The block of this ProduceBlockV3ResponseDataOneOf [Optional].
        blob_sidecars: The blob_sidecars of this ProduceBlockV3ResponseDataOneOf [Optional].
    """

    block: Optional[PublishBlockRequestOneOf2SignedBlockMessage] = Field(alias="block", default=None)
    blob_sidecars: Optional[List[PublishBlockRequestOneOf2SignedBlobSidecarsInnerMessage]] = Field(alias="blob_sidecars", default=None)

ProduceBlockV3ResponseDataOneOf.update_forward_refs()
