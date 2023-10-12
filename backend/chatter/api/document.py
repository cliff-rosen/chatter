from db import local_db as db


def insert_document(domain_id, doc_uri, doc_title, doc_text, doc_blob):
    conn = db.get_connection()
    db.insert_document(
        conn,
        domain_id,
        doc_uri, doc_title, doc_text, doc_blob
    )
    conn.close()
