"""Modely pro validaci a práci s daty."""

import base64
import json

from pydantic import BaseModel, field_validator


class StagResponse(BaseModel):
    """Po přáhlášení STAG vrátí na zadanou url ticket a userinfo."""

    ticket: str
    userinfo: dict

    @field_validator("userinfo", mode="before")
    def parse_userinfo(cls, v) -> dict:
        """Dekóduje userInfo."""
        padding_needed = 4 - len(v) % 4

        v += "=" * padding_needed
        decoded = base64.b64decode(v)
        clean_decoded = decoded.decode("utf-8", errors="ignore")

        return json.loads(clean_decoded)
