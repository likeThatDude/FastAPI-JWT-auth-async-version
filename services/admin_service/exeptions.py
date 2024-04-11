from fastapi import HTTPException
from starlette import status

exception_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Data not found in the database',
    headers={
        'WWW-Authenticate': 'Bearer'
    }
)

exception_403 = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='You do not have sufficient permissions',
    headers={
        'WWW-Authenticate': 'Bearer'
    }
)

exception_500 = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Internal server error occurred',
    headers={
        'WWW-Authenticate': 'Bearer'
    }
)
