import os

import flask
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from neo4j import GraphDatabase

load_dotenv()

app = Flask('app')


def init_driver(uri: str, username: str, password: str):
    # Create a new Driver instance
    app.driver = GraphDatabase.driver(uri, auth=(username, password))

    # Verify the connection details
    app.driver.verify_connectivity()
    return app.driver


driver = init_driver(
    os.getenv('NEO4J_URI'),
    os.getenv('NEO4J_USERNAME'),
    os.getenv('NEO4J_PASSWORD')
)


class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.message), e.status_code


def get_events_from_db(tx, name: str):
    result = tx.run("""
        MATCH (p:Person {fullName: $name})-[r:PARTICIPATED_IN]->(e:Event)
        WITH p, collect(e) AS events, collect(r) AS rels, collect(e.eventId) AS event_ids
        CALL apoc.export.graphml.data(p+events, rels, null, {stream:true})
        YIELD data
        RETURN  data, event_ids
    """, name=name)
    return result.values('data', 'event_ids')


@app.route('/', methods=['GET'])
def get_person_events():
    name = request.args.get('name')
    if not name:
        raise InvalidAPIUsage(
            "Задайте имя в параметрах запроса. "
            f"Пример: http://localhost:{os.getenv('FLASK_RUN_PORT')}/"
            "?name=Ахромеева+Алина+Ивановна"
        )

    with driver.session() as session:
        events = session.execute_read(get_events_from_db, name=name)

    if not events:
        raise InvalidAPIUsage(f"Не найден: {name}.", 404)
    events_xml, event_ids = events[0][0], events[0][1]

    filename = request.args.get('filename', default='output.graphml')
    with open(filename, 'w') as graphml_file:
        graphml_file.write(events_xml)
    response = {
        'message': f"События для {name} записаны в файл '{filename}'.",
        'events': event_ids
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    app.run()
