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

