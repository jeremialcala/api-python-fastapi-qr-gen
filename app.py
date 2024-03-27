import json
import logging.config
import time
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi import status

from classes import Settings, QrCodeRequest
from constants import PROCESSING_TIME, CONTENT_TYPE, APPLICATION_JSON
from controllers import ctr_create_qr_code, ctr_get_qr_code_by_uuid, ctr_stream_qr
from utils import configure_logging

description = """
This is QRCode Generator, this component Generates QrCodes from some data send in request.

## QrCode 

* /create: this endpoint allows you to **Create QrCode from some data in the request**.

* 

"""

""" 
    TODO: Add security validator components
"""

tags_metadata = [
    {
        "name": "Generate",
        "description": "In this operation using some simple data, "
                       "you will create a new Qr Code, ",
    },
    {
        "name": "Token",
        "description": "This endpoint will authenticate a client and generate a token for resource access",
    },
]

settings = Settings()
log = logging.getLogger(settings.environment)


app = FastAPI(
    openapi_tags=tags_metadata,
    on_startup=[configure_logging],
    title="QR Generator",
    description=description,
    summary="Generates data represented in QR Codes",
    version="0.0.1",
    terms_of_service="https://web-ones.com",
    contact={
      "name": "Jeremi Alcala",
      "url": "https://web-ones.com",
      "email": "jeremialcala@gmail.com",
    },
    license_info={
      "name": "Apache 2.0",
      "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.middleware("http")
async def interceptor(request: Request, call_next):
    log.info(f"new request from: {request.client}")
    start_time = time.time()

    response = Response(
        content=json.dumps({"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "msg": "INTERNAL SERVER ERROR"}),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers={CONTENT_TYPE: APPLICATION_JSON}
    )
    try:
        event_id = uuid4()
        request.state.event_id = str(event_id)
        log.info(request.url.path)
        [log.debug(f"Header! -> {hdr}: {val}") for hdr, val in request.headers.items()]
        response = await call_next(request)

    except Exception as e:
        log.error(e.args)
    finally:
        process_time = "{:f}".format(time.time() - start_time)
        response.headers[PROCESSING_TIME] = str(process_time)
        log.info(f"This request was processed on {process_time} seconds")
        return response


@app.post("/qr")
async def create_qr_code(_request: QrCodeRequest):
    return await ctr_stream_qr(await ctr_create_qr_code(request=_request))


@app.get("/qr")
async def get_qr_from_uuid(_uuid: str):
    return await ctr_stream_qr(await ctr_get_qr_code_by_uuid(_uuid=_uuid))

