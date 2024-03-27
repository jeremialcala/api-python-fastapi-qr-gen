# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from uuid import uuid4
from mongoengine import *
from enums import Status
from .tool_settings import Settings

settings = Settings()
log = logging.getLogger(settings.environment)
connect(
    db=settings.db_name,
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host
)


class QrCode(Document):
    uuid = UUIDField(required=True, unique=True, default=uuid4())
    data = StringField(required=True)
    name = StringField(required=True)
    imageFile = StringField(required=True)
    creatorEmail = EmailField()
    result = StringField()
    createdAt = DateTimeField(required=True, default=datetime.now())
    status = IntField(required=True, default=Status.REG.value)
    statusDate = DateTimeField(required=True, default=datetime.now())

    def get_qr_image(self):
        with open(self.imageFile, "r") as qr:
            data = qr.read()
        return data

    @staticmethod
    def get_qr_code_by_uuid(_uuid):
        return [qrCode for qrCode in QrCode.objects(uuid=_uuid)][-1]
