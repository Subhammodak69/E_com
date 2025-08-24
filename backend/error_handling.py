from fastapi import HTTPException, status
import re
from sqlalchemy.exc import IntegrityError



def handle_integrity_error(e: IntegrityError):
    error_message = str(e.orig)
    match = re.search(r'Key \((.*?)\)=\((.*?)\) already exists', error_message)
    if match:
        field_name = match.group(1)
        field_value = match.group(2)
        readable_field = field_name.replace('_', ' ').capitalize()
        detail_msg = f"{readable_field} '{field_value}' already exists"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail_msg)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")