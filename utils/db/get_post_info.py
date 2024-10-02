from supabase import Client

async def get_post_info(post_id: int, supabase: Client) -> dict:
    try:
        response = supabase.table('posts').select('permalink, caption, media_url, likes_count, comments_count, date_published, media_type').eq('id', post_id).execute()
        response = response.data[0]
        return response
    except Exception as e:
        print(f"❌ Error: get_post_info() - ID: {post_id}: {e}")
        return None
    