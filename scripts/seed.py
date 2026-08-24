from pathlib import Path
import csv
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')

URI = os.getenv('COGNODB_URI')
USER = os.getenv('COGNODB_USER', 'cognodb')
PASSWORD = os.getenv('COGNODB_PASSWORD')

if not URI or not PASSWORD:
    raise SystemExit('Set COGNODB_URI and COGNODB_PASSWORD in .env')

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def run(tx):
    tx.run('MATCH (n) DETACH DELETE n').consume()
    movies = list(csv.DictReader((ROOT/'data'/'movies.csv').open(encoding='utf-8')))
    for row in movies:
        tx.run('MERGE (m:Movie {title:$title}) SET m.year=$year, m.rating=$rating', title=row['title'], year=int(row['year']), rating=float(row['rating']))
        for genre in row['genres'].split('|'):
            tx.run('MERGE (g:Genre {name:$genre}) MERGE (m:Movie {title:$title})-[:IN_GENRE]->(g)', genre=genre, title=row['title'])
        for actor in row['actors'].split('|'):
            tx.run('MERGE (p:Person {name:$actor}) MERGE (p)-[:ACTED_IN]->(m:Movie {title:$title})', actor=actor, title=row['title'])
        for director in row['directors'].split('|'):
            tx.run('MERGE (p:Person {name:$director}) MERGE (p)-[:DIRECTED]->(m:Movie {title:$title})', director=director, title=row['title'])

with driver.session() as s:
    s.execute_write(run)
print('Seeded GraphFlix data successfully.')
driver.close()
