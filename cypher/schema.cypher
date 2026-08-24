// Optional constraints/indexes. CognoDB supports openCypher; run these if supported by your plan.
CREATE INDEX movie_title IF NOT EXISTS FOR (m:Movie) ON (m.title);
CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name);
CREATE INDEX genre_name IF NOT EXISTS FOR (g:Genre) ON (g.name);
