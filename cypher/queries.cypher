// 1. Search movies
MATCH (m:Movie) WHERE toLower(m.title) CONTAINS toLower($q) RETURN m.title, m.year, m.rating LIMIT 12;

// 2. Multi-hop recommendation: Movie -> Actor -> Movie
MATCH (m:Movie {title:$title})<-[:ACTED_IN]-(a:Person)-[:ACTED_IN]->(rec:Movie)
WHERE rec.title <> m.title
RETURN rec.title, count(DISTINCT a) AS sharedActors
ORDER BY sharedActors DESC LIMIT 8;

// 3. Two-hop actor-network traversal: Movie -> Actor -> Movie -> Actor -> Movie
MATCH (m:Movie {title:$title})<-[:ACTED_IN]-(a:Person)-[:ACTED_IN]->(other:Movie)<-[:ACTED_IN]-(b:Person)-[:ACTED_IN]->(rec:Movie)
WHERE rec.title <> m.title AND other.title <> m.title AND rec.title <> other.title
RETURN rec.title, count(DISTINCT b) AS secondHopActors
ORDER BY secondHopActors DESC LIMIT 8;

// 4. Relationally awkward graph question: find movies connected by both shared actors and shared genres.
MATCH (m:Movie {title:$title})<-[:ACTED_IN]-(a:Person)-[:ACTED_IN]->(rec:Movie),
      (m)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec)
WHERE rec.title <> m.title
RETURN rec.title, count(DISTINCT a) AS sharedActors, count(DISTINCT g) AS sharedGenres;
