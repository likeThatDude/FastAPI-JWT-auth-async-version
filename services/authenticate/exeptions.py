from fastapi import HTTPException
from starlette import status

exception_400_banned = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Invalid data provided: User is banned',
    headers={
        'WWW-Authenticate': 'Bearer'
    }
)

exception_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )