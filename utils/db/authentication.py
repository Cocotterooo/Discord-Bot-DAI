import os
from supabase import create_client, Client


def supabase_autenticated(db_url: str, db_api_key: str, db_email: str, db_email_pass: str) -> Client:
    supabase: Client = create_client(db_url, db_api_key)
    session = None
    try:
        supabase.auth.sign_in_with_password({
            "email": db_email,
            "password": db_email_pass})
        print("💚 Supabase - Login Success")
    except Exception as e:
        print(f"💔 Supabase - Login Failed: {e}")

    #access_token = session.session.access_token
    #supabase.postgrest.auth(access_token)
    return supabase


#user=User(id='785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d', 
# app_metadata={'provider': 'email', 'providers': ['email']}, user_metadata={}, aud='authenticated', confirmation_sent_at=None, recovery_sent_at=None, email_change_sent_at=None, new_email=None, new_phone=None, invited_at=None, action_link=None, email='fcocoterooo@gmail.com', phone='', created_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 674129, tzinfo=TzInfo(UTC)), confirmed_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 679864, tzinfo=TzInfo(UTC)), email_confirmed_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 679864, tzinfo=TzInfo(UTC)), phone_confirmed_at=None, last_sign_in_at=datetime.datetime(2024, 9, 29, 15, 57, 6, 42032, tzinfo=TzInfo(UTC)), role='authenticated', updated_at=datetime.datetime(2024, 9, 29, 15, 57, 6, 43990, tzinfo=TzInfo(UTC)), identities=[UserIdentity(id='785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d', identity_id='6ddb0a22-44f3-4eab-b2a9-c744ed6eaa08', user_id='785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d', identity_data={'email': 'fcocoterooo@gmail.com', 'email_verified': False, 'phone_verified': False, 'sub': '785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d'}, provider='email', created_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 676921, tzinfo=TzInfo(UTC)), last_sign_in_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 676856, tzinfo=TzInfo(UTC)), updated_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 676921, tzinfo=TzInfo(UTC)))], is_anonymous=False, factors=None) 
# session=Session(provider_token=None, provider_refresh_token=None, 
# access_token='eyJhbGciOiJIUzI1NiIsImtpZCI6IkpqdUFPOFhIQ1c5dUhld00iLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3F1cm16bmlveHhhbGJzdm52dmNlLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI3ODVjNDY3Zi05YzZlLTQzZDctYTRlNy02ZjRmMGZiYWNmOWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzI3NjI5MDI2LCJpYXQiOjE3Mjc2MjU0MjYsImVtYWlsIjoiZmNvY290ZXJvb29AZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6e30sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3Mjc2MjU0MjZ9XSwic2Vzc2lvbl9pZCI6IjE1NzY2YjdhLWVlYTEtNDNiOS1iMDc0LWIyM2ZjMThlYzIxZiIsImlzX2Fub255bW91cyI6ZmFsc2V9.YnC53Ad8YnPiypjdyTcXEgRROzEF-W7WL6DJuSoma_8', refresh_token='gPF9YZBEmDn2kkGftlpibg', expires_in=3600, expires_at=1727629026, token_type='bearer', user=User(id='785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d', app_metadata={'provider': 'email', 'providers': ['email']}, user_metadata={}, aud='authenticated', confirmation_sent_at=None, recovery_sent_at=None, email_change_sent_at=None, new_email=None, new_phone=None, invited_at=None, action_link=None, email='fcocoterooo@gmail.com', phone='', created_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 674129, tzinfo=TzInfo(UTC)), confirmed_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 679864, tzinfo=TzInfo(UTC)), email_confirmed_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 679864, tzinfo=TzInfo(UTC)), phone_confirmed_at=None, last_sign_in_at=datetime.datetime(2024, 9, 29, 15, 57, 6, 42032, tzinfo=TzInfo(UTC)), role='authenticated', updated_at=datetime.datetime(2024, 9, 29, 15, 57, 6, 43990, tzinfo=TzInfo(UTC)), identities=[UserIdentity(id='785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d', identity_id='6ddb0a22-44f3-4eab-b2a9-c744ed6eaa08', user_id='785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d', identity_data={'email': 'fcocoterooo@gmail.com', 'email_verified': False, 'phone_verified': False, 'sub': '785c467f-9c6e-43d7-a4e7-6f4f0fbacf9d'}, provider='email', created_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 676921, tzinfo=TzInfo(UTC)), last_sign_in_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 676856, tzinfo=TzInfo(UTC)), updated_at=datetime.datetime(2024, 9, 29, 9, 52, 59, 676921, tzinfo=TzInfo(UTC)))], is_anonymous=False, factors=None))

#supabase_autenticated(DB_URL, DB_API_KEY)

'''supabase: Client = create_client(DB_URL, DB_API_KEY)
session = None
data = supabase.table('posts').select('*').execute()
print(data)
try:
    session = supabase.auth.sign_in_with_password({
        "email": "fcocoterooo@gmail.com",
        "password": "CatapultaDAi"})
except Exception as e:
    print(f"Supabase - Login Failed: {e}")

data = supabase.table('posts').select('*').execute()
print(data)
access_token = session.session.access_token
#supabase.postgrest.auth(access_token)
data = supabase.table('posts').select('*').execute()
supabase.table("posts").insert([{
    "id": 3,
    "date_published": "2024-09-29T19:09:30.257589+00:00",
    "media_type": "",
    "caption": "",
    "media_url": "",
    "permalink": ""
}]).execute()
print(data)'''