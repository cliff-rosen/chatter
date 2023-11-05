
'''
retrieve
 single row as obj
 multiple rows as list
update
delete

'''

# retrieve multiple rows
def get_conversation(conversation_id):
    rows = None
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    conversation_id,
                    user_id,
                    domain_id,
                    conversation_text
                FROM conversation
                WHERE conversation_id = %s
                """,
                        (conversation_id, ))
            rows = cur.fetchall()
    except Exception as e:
        print("***************************")
        print("DB error in get_conversation")
        print(e)
    return rows
