def write_nlp_db(nlp, df, filepath="./nlp.db"):
    from datetime import datetime
    start = datetime.now()
    texts = df["text"] # Process all of the texts
    print("Processing {} texts".format(len(texts)))
    docs = list(nlp.pipe(texts))

    print("Processed {} docs in {} seconds".format(len(docs), datetime.now() - start))
    
    from medspacy.io import DocConsumer, DbReader, DbWriter, Pipeline, DbConnect
    import sqlite3
    conn = sqlite3.connect(filepath)
    doc_consumer = DocConsumer(nlp)
    
    for doc in docs:
        doc_consumer(doc)
        
    db_conn = DbConnect(conn=conn)
    writer = DbWriter(db_conn, "ents", create_table=True, drop_existing=True)
    for doc in docs:
        writer.write(doc)
        
    conn.close()
    print()
    print("Saved output from {} docs to '{}'".format(len(docs), filepath))