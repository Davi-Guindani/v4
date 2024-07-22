import supabase
import os

def supabase_client():
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    return supabase.create_client(url, key)
