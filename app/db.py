from neo4j import GraphDatabase
from .config import COGNODB_URI, COGNODB_USER, COGNODB_PASSWORD

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        if not COGNODB_URI or not COGNODB_PASSWORD:
            raise RuntimeError("COGNODB_URI and COGNODB_PASSWORD must be set in .env")
        _driver = GraphDatabase.driver(
            COGNODB_URI,
            auth=(COGNODB_USER, COGNODB_PASSWORD),
        )
    return _driver


def verify():
    driver = get_driver()
    driver.verify_connectivity()


def close():
    global _driver
    if _driver:
        _driver.close()
        _driver = None
