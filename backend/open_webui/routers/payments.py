import logging

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from open_webui.env import PAYMENT_SERVICE_URL
from open_webui.utils.auth import get_verified_user

log = logging.getLogger(__name__)

router = APIRouter()


@router.post('/payments')
async def create_payment(request: Request, user=Depends(get_verified_user)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid request body')

    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
    try:
        r = await session.post(
            f'{PAYMENT_SERVICE_URL}/v1/payments',
            json=body,
            headers={'Content-Type': 'application/json'},
        )
        data = await r.json()
        return JSONResponse(content=data, status_code=r.status)
    except aiohttp.ClientError as e:
        log.error(f'Payment service error: {e}')
        raise HTTPException(status_code=502, detail='Payment service unavailable')
    finally:
        await session.close()


@router.get('/payments/{trx_id}')
async def get_payment_status(
    trx_id: str, user=Depends(get_verified_user)
):
    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
    try:
        r = await session.get(
            f'{PAYMENT_SERVICE_URL}/v1/payments/{trx_id}',
            headers={'Content-Type': 'application/json'},
        )
        data = await r.json()
        return JSONResponse(content=data, status_code=r.status)
    except aiohttp.ClientError as e:
        log.error(f'Payment service error: {e}')
        raise HTTPException(status_code=502, detail='Payment service unavailable')
    finally:
        await session.close()
