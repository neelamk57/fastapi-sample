import datetime
from starlette.requests import Request
from fastapi import Response
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends
from authlib.integrations.starlette_client import OAuthError
from authlib.integrations.starlette_client import OAuth

CLIENT_ID = '663515348764-tjaudng253e4ogmu9k1hoo59knmg90bq.apps.googleusercontent.com'
CLIENT_SECRET = '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'
# REDIRECT_URI = "https://localhost:8001/auth"
REDIRECT_URI= "https://oauth.wiseyak.com/auth"



oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid profile email',
        'redirect_uri': REDIRECT_URI
    }  
)


router = APIRouter()



@router.get("/login")
async def login(request: Request):
    request.session.clear()
    url = request.url_for('auth')
    print(f"Authorization URL: {url}")
    return await oauth.google.authorize_redirect(request, url)


@router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f"OAuthError: {e}")
        return JSONResponse(content={"message": "couldn't connect"})

    user_info = token.get('userinfo')

    if user_info:
        email = user_info.get('email')
        name = user_info.get('name')

        request.session['user'] = user_info
        request.session['email'] = email
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        request.session['access_token'] = token['access_token']
        request.session['access_token_expires'] = expires.timestamp()

        refresh_token_expires_in = token.get('expires_in')
        if refresh_token_expires_in:
            refresh_token_expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=refresh_token_expires_in)
        else:
            refresh_token_expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)

        request.session['refresh_token'] = token.get('refresh_token')
        request.session['refresh_token_expires'] = refresh_token_expires.timestamp()


    return JSONResponse({"user_info": user_info})


@router.delete('/logout')
def logout(request: Request):
    request.session.clear()
    return Response(status_code=200)

