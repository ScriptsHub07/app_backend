from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_google_credentials_for_user(db: Session, user_id: str) -> Credentials:
    token_row = db.query(models.OAuthToken).filter(models.OAuthToken.user_id == user_id, models.OAuthToken.provider == 'google').order_by(models.OAuthToken.created_at.desc()).first()
    if not token_row:
        raise HTTPException(status_code=404, detail="No tokens for user")
    token = token_row.token
    creds = Credentials(
        token=token.get('access_token'),
        refresh_token=token.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        scopes=token.get('scope').split() if token.get('scope') else None,
    )
    return creds


@router.post('/send_email')
def send_email(user_id: str, to: str, subject: str, body: str, db: Session = Depends(get_db)):
    creds = get_google_credentials_for_user(db, user_id)
    service = build('gmail', 'v1', credentials=creds)
    import base64
    from email.mime.text import MIMEText

    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    try:
        result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return {'status': 'sent', 'id': result.get('id')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/create_event')
def create_event(user_id: str, summary: str, start_iso: str, end_iso: str, db: Session = Depends(get_db)):
    creds = get_google_credentials_for_user(db, user_id)
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'start': {'dateTime': start_iso},
        'end': {'dateTime': end_iso},
    }
    try:
        created = service.events().insert(calendarId='primary', body=event).execute()
        return {'status': 'created', 'eventId': created.get('id')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
