import logging

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from open_webui.env import PAYMENT_SERVICE_URL, CHAT_USAGE_SERVICE_URL, CHAT_USAGE_API_KEY
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


@router.get('/payments/balance')
async def get_user_balance(user=Depends(get_verified_user)):
    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
    try:
        r = await session.get(
            f'{CHAT_USAGE_SERVICE_URL}/api/v1/users/',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {CHAT_USAGE_API_KEY}',
            },
        )
        data = await r.json()

        users = data.get('users', [])
        user_balance = None
        for u in users:
            # for dev only 
            if u.get('id') == "19d98736-b895-46c5-b3f8-7da99f0107c9":
                user_balance = u
                break
            # if u.get('id') == user.id:
            #     user_balance = u
            #     break

        if user_balance is None:
            raise HTTPException(status_code=404, detail='User not found in usage service')

        return JSONResponse(content={
            'id': user_balance['id'],
            'balance': user_balance['balance'],
            'name': user_balance.get('name', ''),
            'email': user_balance.get('email', ''),
        })
    except HTTPException:
        raise
    except aiohttp.ClientError as e:
        log.error(f'Chat usage service error: {e}')
        raise HTTPException(status_code=502, detail='Usage service unavailable')
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
