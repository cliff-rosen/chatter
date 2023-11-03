from db import db


def insert_document(domain_id, doc_uri, doc_title, doc_text, doc_blob):
    db.insert_document(
        domain_id,
        doc_uri, doc_title, doc_text, doc_blob
    )

