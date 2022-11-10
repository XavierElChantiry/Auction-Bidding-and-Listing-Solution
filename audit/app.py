
import swagger_ui_bundle
import connexion
import logging
import logging.config
import yaml
import json
from pykafka import KafkaClient
import datetime
from connexion import NoContent
from os import environ
from flask_cors import CORS, cross_origin

with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('./log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

def postAuction(index):
    """ Get auction History """
    hostname = "%s:%d" % (environ["KAFKA_DNS"],
    app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving BP at index %d" % index)
    try:
        counter = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == "postAuction":
                if counter == index:
                    return msg["payload"], 200
                else:
                    counter += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find BP at index %d" % index)
    return { "message": "Not Found"}, 404


def bidAuction(index):
    """ Get auction History """
    hostname = "%s:%d" % (environ["KAFKA_DNS"],
    app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving BP at index %d" % index)
    try:
        counter = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == "bidAuction":
                if counter == index:
                    return msg["payload"], 200
                else:
                    counter += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find BP at index %d" % index)
    return { "message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
logger = logging.getLogger('basicLogger')

if __name__ == "__main__":

    app.run(port=8110)