from db import db
from utils.utils import num_tokens_from_string
from utils.logging import logging
from utils.openai_wrappers import get_embedding
from utils.pinecone_wrappers import get_matching_chunks

COMPLETION_MODEL = 'text-davinci-003'
TEMPERATURE = 0.0

logger = logging.getLogger()

'''
chunks dict: 
    {
        ID:  {
            "id": ID as int,
            "score": score as float,
            "metadata": {
                "doc_chunk_id": 44743.0,
                "doc_id": 20657.0,
                "domain_id": 27.0                
            },
            "uri": uri,
            "text": text,
            "used": isUsed
        }
    }

    {
        "27": {
            "id": 27,
            "score": 0.737494111,
            "metadata": {
                "doc_chunk_id": 27.0,
                "doc_id": 15.0,
                "domain_id": 1.0
            },
            "uri": "Changes in Drug Level Laboratory Results _ DoseMe Help Center.pdf",
            "text": "different, DoseMeRx will tend to prefer the one most like the population model (as this is more \ncommon in the population). Therefore, it may recommend a different dose than what would be \ncustomary for a patient if only the most recent result was considered.\nHere are two approaches to consider when this is encountered:\nIf the accuracy of the outlier drug level is questionable:\n\u0000. Consider obtaining another level if possible to validate the accuracy of the most recent \nlevel.\n\u0000. If you cannot obtain a level, exclude the last level and DoseMeRx will calculate the dose \nbased on the prior existing levels.\nIf the most recent drug level value is considered to be correct:\n9/14/23, 4:09 PM Changes in Drug Level Laboratory Results | DoseMe Help Center\nhttps://help.doseme-rx.com/en/articles/3353676-changes-in-drug-level-laboratory-results 2/2doseme-rx.com\n\u0000. Exclude earlier drug levels (if the last result is considered correct and you think a change \nhas taken place).",
            "used": true
        }    
    }
'''

def get_chunks_from_query(domain_id, user_message):
    chunks = {}

    print("getting query embedding")
    query_embedding = get_embedding(user_message)

    print("getting chunks ids")
    chunks = get_matching_chunks(domain_id, query_embedding)
    if not chunks:
        raise Exception('No chunks found - check index')

    print("getting chunk text from ids")
    _set_chunk_text_from_ids(chunks)

    logger.info(chunks)
    return chunks


# mutate chunks by adding {"uri": uri, "text", text} to each value dict
# chunks is dict where
#   key is chunk_id, and value is obj with score, text
def _set_chunk_text_from_ids(chunks):
    ids = list(chunks.keys())
    rows = db.get_document_chunks_from_ids(ids)
    for row in rows:
        doc_chunk_id = row["doc_chunk_id"]
        chunk_text = row["chunk_text"]
        doc_uri = row["doc_uri"]
        print(f"id: {doc_chunk_id}, text: {chunk_text[:20]}")
        chunks[str(doc_chunk_id)]["uri"] = doc_uri
        chunks[str(doc_chunk_id)]["text"] = chunk_text


