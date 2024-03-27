# -*- coding: utf-8 -*-
import logging
from uuid import uuid4

import segno
from fastapi import HTTPException, status
from fastapi.responses import FileResponse

from classes import QrCode, QrCodeRequest, Settings
from constants import QR_IMAGE_DIRECTORY, QR_CODE_ID

settings = Settings()
log = logging.getLogger(settings.environment)


async def ctr_create_qr_code(request: QrCodeRequest) -> QrCode:
    log.info(f"generating a new qr code {request.data} for this {request.email}")
    qr_code_id = uuid4()
    qr_code = QrCode(
        uuid=qr_code_id,
        name=request.name,
        data=request.data,
        creatorEmail=request.email,
        imageFile=f"{QR_IMAGE_DIRECTORY}{qr_code_id}.png"
    )
    try:
        qr = segno.make_qr(request.data)
        qr.save(qr_code.imageFile, scale=10)
        qr_code.save()
    except Exception as e:
        log.error(e.__str__())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Some internal error happened")
    return qr_code


async def ctr_get_qr_code_by_uuid(_uuid: str):
    log.info(f"finding a qr code id: {_uuid}")
    try:
        qr_code = QrCode().get_qr_code_by_uuid(_uuid)
    except ValueError as e:
        log.error(e.__str__())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We could not find this resource")
    except Exception as e:
        log.error(e.__str__())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Some internal error happened")
    return qr_code


async def ctr_stream_qr(qr_code: QrCode):
    return FileResponse(
        qr_code.imageFile,
        media_type="image/png",
        headers={QR_CODE_ID: str(qr_code.uuid)})
