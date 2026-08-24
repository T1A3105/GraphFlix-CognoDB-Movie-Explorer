SEARCH_MOVIES = """
MATCH (m:Movie)
WHERE toLower(m.title) CONTAINS toLower($q)
OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
RETURN m.title AS title, m.year AS year, m.rating AS rating,
       collect(DISTINCT a.name) AS actors, collect(DISTINCT g.name) AS genres
ORDER BY m.rating DESC, m.title
LIMIT 12
"""

MOVIE_DETAILS = """
MATCH (m:Movie {title: $title})
OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
RETURN m.title AS title, m.year AS year, m.rating AS rating,
       collect(DISTINCT a.name) AS actors,
       collect(DISTINCT g.name) AS genres,
       collect(DISTINCT d.name) AS directors
"""

RECOMMEND = """
MATCH (m:Movie {title: $title})<-[:ACTED_IN]-(actor:Person)-[:ACTED_IN]->(rec:Movie)
WHERE rec.title <> m.title
WITH rec, count(DISTINCT actor) AS sharedActors
OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec)
WITH rec, sharedActors, count(DISTINCT g) AS sharedGenres
RETURN rec.title AS title, rec.year AS year, rec.rating AS rating,
       sharedActors, sharedGenres,
       (sharedActors * 2 + sharedGenres + rec.rating / 10.0) AS score
ORDER BY score DESC, rec.rating DESC
LIMIT 8
"""

TWO_HOP = """
MATCH (m:Movie {title: $title})<-[:ACTED_IN]-(a:Person)-[:ACTED_IN]->(other:Movie)
      <-[:ACTED_IN]-(b:Person)-[:ACTED_IN]->(rec:Movie)
WHERE rec.title <> m.title AND other.title <> m.title AND rec.title <> other.title
RETURN rec.title AS title, count(DISTINCT a) AS firstHopActors,
       count(DISTINCT b) AS secondHopActors
ORDER BY secondHopActors DESC, firstHopActors DESC, title
LIMIT 8
"""

TOP_GENRES = """
MATCH (g:Genre)<-[:IN_GENRE]-(m:Movie)
RETURN g.name AS genre, count(m) AS movies, round(avg(m.rating) * 100) / 100.0 AS avgRating
ORDER BY movies DESC, avgRating DESC
"""
