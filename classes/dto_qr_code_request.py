# -*- coding: utf-8 -*-
import logging
from pydantic import BaseModel, EmailStr, Field
from faker import Faker
from .tool_settings import Settings

fk = Faker()
settings = Settings()
log = logging.getLogger(settings.environment)


class QrCodeRequest(BaseModel):
    data: str = Field(examples=[fk.company() for _ in range(10)])
    name: str = Field(examples=[fk.name() for _ in range(10)])
    email: EmailStr = Field(examples=[fk.email() for _ in range(10)])
