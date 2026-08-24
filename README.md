# 🎬 GraphFlix — CognoDB Graph Explorer

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GraphFlix-success)](https://graphflix-cognodb-movie-explorer.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-CognoDB-purple)](https://console.cognodb.com/)
[![Deployment](https://img.shields.io/badge/Deployment-Render-blueviolet)](https://render.com/)

A graph-powered movie discovery application built using **CognoDB**, **Neo4j's official Python driver**, **Python Flask**, and **Cypher**.

This project was developed as part of the **WEXA AI — Build a Graph Database Application take-home assignment**.

---

## 🔗 Project Links

### 🌐 Live Demo

**GraphFlix Web Application:**

https://graphflix-cognodb-movie-explorer.onrender.com/

### 💻 GitHub Repository

**Source Code:**

https://github.com/T1A3105/GraphFlix-CognoDB-Movie-Explorer

---

# 📌 1. Project Overview

**GraphFlix** is a web application that allows users to discover movies through the relationships between:

- Movies
- Actors
- Directors
- Genres

Instead of treating every movie as an independent database record, GraphFlix models the connections between movies and the people and genres associated with them.

The application uses **CognoDB as the graph database layer** and uses **Cypher queries** to perform graph traversals.

A user can:

1. Search for a movie.
2. Select a movie from the search results.
3. View the movie's details.
4. View connected actors, directors, and genres.
5. Get movie recommendations through shared graph relationships.
6. Explore second-hop movie connections.
7. View aggregated genre statistics directly from the graph.

---

# 🎯 2. Objective

The objective of this project is to demonstrate how a graph database can be used to build a complete application where the important information is based on **relationships and connections**.

The project demonstrates:

- Graph data modeling
- Nodes and relationships
- Cypher queries
- Multi-hop graph traversal
- Parameterized database queries
- Graph-based recommendations
- REST API development
- Flask web application development
- Database error handling
- Environment-based configuration
- Cloud deployment

---

# 💡 3. Use Case

## Movie Discovery Through Connections

Traditional movie search generally answers questions such as:

> "Find movies whose title contains Inception."

GraphFlix goes beyond simple search.

It can answer relationship-based questions such as:

> "Which movies are connected to Inception through shared actors?"

> "Which movies are connected through actors and genres?"

> "What movies can be discovered two relationship hops away?"

These are natural graph problems because the value comes from understanding the relationships between entities.

---

# 🧠 4. Why a Graph Database?

A graph database is a natural fit for this application because movies have many interconnected relationships.

For example:

```text
Leonardo DiCaprio
        |
     ACTED_IN
        |
    Inception
        |
    IN_GENRE
        |
     Sci-Fi


#The same actor can be connected to many movies:

Leonardo DiCaprio
      |
      +---- ACTED_IN ----> Inception
      |
      +---- ACTED_IN ----> Titanic
      |
      +---- ACTED_IN ----> The Departed
      |
      +---- ACTED_IN ----> Shutter Island

#This makes graph traversal very useful for recommendations.

For example:

Inception
   |
   | ACTED_IN
   v
Leonardo DiCaprio
   |
   | ACTED_IN
   v
The Departed

A relational database could perform this using multiple joins and intermediate result sets.

In a graph database, the relationship path is directly represented in the data model and can be traversed naturally using Cypher.

#Graph database advantages demonstrated by this project

Natural representation of relationships
Easy multi-hop traversal
Relationship-based recommendations
Shared actor discovery
Shared genre discovery
Second-hop exploration

🏗️ 5. Technology Stack
Technology	Purpose
Python	Application programming language
Flask	Web application and REST API
CognoDB	Managed graph database
Neo4j Python Driver	Database connectivity
Cypher / openCypher	Graph queries
HTML	Web page structure
CSS	UI styling
JavaScript	Frontend interactions
Gunicorn	Production WSGI server
Render	Cloud deployment
Git / GitHub	Version control and source hosting
#🕸️ 6. Graph Data Model

#GraphFlix uses three primary node types.

Nodes
Movie

Properties:

title
year
rating
Person

Properties:

name

A Person can represent an actor or director.

Genre

Properties:

name
Aggregations across connected nodes

#🔗 7. Relationships

The graph contains the following typed relationships.

Actor → Movie
(:Person)-[:ACTED_IN]->(:Movie)

This represents an actor who appeared in a movie.

Director → Movie
(:Person)-[:DIRECTED]->(:Movie)

This represents a director who directed a movie.

Movie → Genre
(:Movie)-[:IN_GENRE]->(:Genre)

This represents the genre associated with a movie.

#📊 8. Graph Model Diagram
                   ┌───────────────┐
                   │    Person     │
                   │ Leonardo      │
                   │ DiCaprio      │
                   └───────┬───────┘
                           │
                       ACTED_IN
                           │
                           ▼
                   ┌───────────────┐
                   │     Movie     │
                   │   Inception   │
                   │    2010       │
                   │    8.8        │
                   └───────┬───────┘
                           │
                       IN_GENRE
                           │
                           ▼
                   ┌───────────────┐
                   │     Genre     │
                   │    Sci-Fi     │
                   └───────────────┘

#📁 9. Project Structure

GraphFlix-CognoDB-Movie-Explorer/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   └── queries.py
│
├── cypher/
│   ├── schema.cypher
│   └── queries.cypher
│
├── data/
│   └── movies.csv
│
├── scripts/
│   └── seed.py
│
├── static/
│   ├── app.js
│   └── styles.css
│
├── templates/
│   └── index.html
│
├── .gitignore
├── Procfile
├── render.yaml
├── requirements.txt
├── SETUP_WINDOWS.md
└── README.md

#🔍 10. Application Architecture

                    User
                     |
                     v
              Web Browser
                     |
                     v
          HTML / CSS / JavaScript
                     |
                     v
                Flask API
                     |
                     v
          Parameterized Cypher
                     |
                     v
              Neo4j Driver
                     |
                     v
                 CognoDB
                     |
                     v
             Graph Data Model

#Frontend

The frontend is implemented using:

HTML
CSS
JavaScript

#It provides:

Movie search
Movie result cards
Graph insight panel
Recommendation results
Two-hop discovery results
Popular genre statistics
Loading states
Empty states
Database status

#Backend

Flask provides REST API endpoints that communicate with CognoDB.

#Database

CognoDB stores the movie graph and executes the Cypher queries.

#🔎 11. Main Application Features
11.1 Movie Search

The user can enter a movie title such as:

Inception

The application queries CognoDB and returns matching movies.

Example:

Inception
2010 · Rating 8.8

Sci-Fi
Thriller
#🎬 11.2 Movie Details

When the user selects a movie, GraphFlix retrieves:

Movie title
Release year
Rating
Genres
Actors
Directors

For example, selecting Inception displays:

Inception

Year / Rating
2010 · 8.8

Genres
Sci-Fi, Thriller

Actors
Leonardo DiCaprio
Joseph Gordon-Levitt
Tom Hardy

Directors
Christopher Nolan

#⭐ 11.3 Graph-Based Recommendations

GraphFlix recommends movies based on shared graph connections.

For example, for Inception, the application can discover:

The Dark Knight
The Departed
Shutter Island
Catch Me If You Can
Titanic

These recommendations are not simply based on text similarity.

They are discovered using graph relationships such as shared actors and shared genres.

Example relationship:

Inception
    |
    | ACTED_IN
    v
Leonardo DiCaprio
    |
    | ACTED_IN
    v
The Departed
#🔀 11.4 Multi-Hop / Two-Hop Discovery

One of the important requirements of the assignment is demonstrating multi-hop traversal.

GraphFlix implements a two-hop discovery query.

Conceptually:

Movie
  ↓
Actor
  ↓
Movie
  ↓
Actor
  ↓
Movie

For example, selecting Inception can discover movies such as:

Ford v Ferrari
Saving Private Ryan
Good Will Hunting
The Martian
The Prestige
The Terminal

The application reports the number of relevant second-hop actors for each result.

This demonstrates that the application is using graph traversal rather than a simple movie table lookup.

#🧮 11.5 Popular Genre Aggregation

The application also performs aggregation directly on the graph.

The UI displays:

Drama       11 movies · 8.28 avg rating
Sci-Fi       5 movies · 8.36 avg rating
Thriller     4 movies · 8.50 avg rating
Action       4 movies · 8.35 avg rating
Crime        3 movies · 8.53 avg rating
Adventure    3 movies · 8.10 avg rating
Mystery      2 movies · 8.35 avg rating
Romance      2 movies · 8.10 avg rating
War          1 movie  · 8.60 avg rating
Comedy       1 movie  · 7.40 avg rating

These values are aggregated directly from the graph.

#🧑‍💻 12. Main Cypher Queries

The application queries are maintained in:

app/queries.py

Additional query documentation is available in:

cypher/queries.cypher

The project includes queries for:

Movie search

Find movies based on a parameterized title search.

Movie details

Traverse the movie's relationships to retrieve:

Actors
Directors
Genres
Recommendations

Traverse:

Movie → Actor → Movie

and calculate shared actors and shared genres.

Two-hop discovery

Traverse multiple graph relationships to discover second-hop movies.

Genre aggregation

Traverse movie-to-genre relationships and calculate:

Number of movies
Average rating
#🔐 13. Parameterized Queries and Security

The application uses parameters with the official Neo4j Python driver.

User input is not directly concatenated into Cypher queries.

Conceptually:

MATCH (m:Movie)
WHERE toLower(m.title) CONTAINS toLower($title)
RETURN m

The movie title is supplied as a query parameter.

This approach avoids building Cypher statements using raw user input.

#🌱 14. Seed Data

The project includes realistic movie seed data:

data/movies.csv

The graph can be populated using:

scripts/seed.py

This means another developer can reproduce the graph database rather than relying on manually entered records.

#⚙️ 15. Environment Configuration

Database credentials are not stored in the source code.

The application reads configuration from environment variables.

Required variables:

COGNODB_URI=bolt+s://YOUR-INSTANCE-ID.databases.cognodb.cloud
COGNODB_USER=cognodb
COGNODB_PASSWORD=YOUR_GENERATED_PASSWORD

The .env file is intentionally excluded from Git using:

.gitignore

Therefore, database credentials are not committed to the GitHub repository.

#🖥️ 16. Run Locally
Step 1 — Clone the repository
git clone https://github.com/T1A3105/GraphFlix-CognoDB-Movie-Explorer.git
cd GraphFlix-CognoDB-Movie-Explorer
Step 2 — Create a virtual environment
Windows
python -m venv .venv
.venv\Scripts\activate
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
Step 3 — Install dependencies
pip install -r requirements.txt
Step 4 — Configure CognoDB

Create a .env file in the project root:

COGNODB_URI=bolt+s://YOUR-INSTANCE-ID.databases.cognodb.cloud
COGNODB_USER=cognodb
COGNODB_PASSWORD=YOUR_GENERATED_PASSWORD

Do not commit this file.

Step 5 — Seed the database
python scripts/seed.py
Step 6 — Start the application
python -m app.main

Open:

http://127.0.0.1:5000
#☁️ 17. Cloud Deployment

The application is deployed using Render.

Deployment configuration is included in:

render.yaml

The application uses:

Gunicorn

# 📸 Screenshots

## GraphFlix Application

![GraphFlix Application](https://github.com/user-attachments/assets/507de87c-3325-4e8b-a4ab-ce42c2432a90)

## Inception — Graph Insights

![Inception Graph Insights](https://github.com/user-attachments/assets/c9618b9a-b70d-4ba4-8d8d-a48a4054e73e)

as the production WSGI server.

The deployed application is available at:

https://graphflix-cognodb-movie-explorer.onrender.com/
