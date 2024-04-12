from fastapi import APIRouter, Response, status

import requests, urllib.parse, html, re
from typing import Optional


router = APIRouter(prefix='/translate', tags=['Translate'])

@router.get('/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
@router.post('/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
async def translate(
        responce: Response,
        text: str,
        to_lang: Optional[str] = 'auto',
        from_lang: Optional[str] = 'auto'
) -> dict:
    '''Translation of texts based on the Google Translate engine'''
    url = 'https://translate.google.com'
    final_url = f'{url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
    request = requests.request(
        method='GET', url=final_url, headers={
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', request.text)
    return {
        'success': True,
        'data': result
    }
