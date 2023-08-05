import psycopg2
import pymorphy2
import re
import collections
import math


def make_lemmas(host, dbname, user, password):
    """
    Creates lemmas from
    """

    conn_string = f"host='{host}' dbname='{dbname}' user='{user}' password='{password}'"
    morph = pymorphy2.MorphAnalyzer()

    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute('SELECT id, data FROM documents;')

    for record in cur.fetchall():
        lemmas = []
        words = re.sub(r'\W', ' ', record[1]).split()
        for word in words:
            p = morph.parse(word)[0]
            lemmas.append(p.normal_form)

        counter = collections.Counter(lemmas)
        for k, v in counter.items():
            cur.execute('INSERT INTO lemma (doc_id, text, amount) VALUES (%s, %s, %s)', (record[0], k, v))

        conn.commit()

    cur.close()
    conn.close()


def calculate_tf_idf(host, dbname, user, password):
    """
    Calculates tf-idf for lemmas
    """

    conn_string = f"host='{host}' dbname='{dbname}' user='{user}' password='{password}'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute('SELECT doc_id, text, amount FROM lemma;')

    for record in cur.fetchall():
        cur.execute('SELECT sum(amount) FROM lemma group by doc_id having doc_id=%s', (record[0],))
        all_words_amount = cur.fetchone()[0]
        tf = record[2] / all_words_amount
        cur.execute('SELECT count(DISTINCT doc_id) FROM lemma')
        doc_amount = cur.fetchone()[0]
        cur.execute('SELECT count(DISTINCT doc_id) FROM lemma where text=%s', (record[1],))
        docs_having_lemma = cur.fetchone()[0]
        idf = math.log10(doc_amount / docs_having_lemma)
        cur.execute('UPDATE lemma SET tf_idf=%s where doc_id=%s AND text=%s', (float(tf) * idf, record[0], record[1]))
        conn.commit()

    cur.close()
    conn.close()


def create_tables(host, dbname, user, password):
    """
    Creates tables for documents and lemmas
    """

    conn_string = f"host='{host}' dbname='{dbname}' user='{user}' password='{password}'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    with open('create_tables.sql', mode='r') as query_file:
        query = query_file.read()

    cur.execute(query)
