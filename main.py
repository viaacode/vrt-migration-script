# 1. query item in db with status TODO
# 2. check for fragments (tenzij reeds aanwezig via Caro)
# 3a. if fragments => start and wait for batch job to delete fragments (FRAGS_DELETE_SENT en FRAGS_DELETE_FINISHED)
# 3b. no fragments => proceed
# 4. replace all metadata with minimal s3 metadata (METADATA_UPDATED)
# 5. send an essenceArchivedEvent to vrt (ARCHIVED_SENT)

from lxml import etree
from io import BytesIO
from services.mediahaven import MediaHavenService
from services.rabbit import RabbitService
from services.database import DatabaseService
from helpers.xml_helper import (
    generate_essence_archived_event,
    transform_metadata,
    NAMESPACES_METADATA,
)
from viaa.configuration import ConfigParser
from viaa.observability import logging

configParser = ConfigParser()
log = logging.get_logger(__name__, config=configParser)
config = configParser.app_cfg

rabbit = RabbitService(config)
database = DatabaseService(config)
mediahaven = MediaHavenService(config)


def delete_fragment_ids(id: str, fragment_ids: list[str]):
    for fragment_id in fragment_ids:
        mediahaven.delete_fragment_id(fragment_id)

    database.update_db_status(id, "FRAGS_DELETE_FINISHED")


def update_metadata(id: str, sidecar):
    mediahaven.update_item(id, sidecar)
    database.update_db_status(id, "METADATA_UPDATED")


def send_archived_event(id: str, message: str):
    rabbit.publish_message(message)
    database.update_db_status(id, "ARCHIVED_SENT")


if __name__ == "__main__":
    # Get first item from DB with status TODO
    vrt_item = database.get_item_to_process()

    # As long as the database returns items, we keep going.
    while vrt_item:
        vrt_item = database.get_item_to_process()

        # Get all fragment ids for fragments on that item
        item_query_result = mediahaven.query_item(vrt_item.fragment_id)
        pid: str = (
            etree.parse(BytesIO(item_query_result))
            .find("//PID", namespaces=NAMESPACES_METADATA)
            .text
        )

        fragments: list = etree.parse(BytesIO(item_query_result)).findall(
            "//mh:Fragment", namespaces=NAMESPACES_METADATA
        )

        # Get all fragment ids for collaterals of the item
        collateral_query_result = mediahaven.query_collaterals(pid)
        collaterals: list = etree.parse(BytesIO(collateral_query_result)).findall(
            "//mh:FragmentId", namespaces=NAMESPACES_METADATA
        )

        # If we have fragments or collaterals, we will delete them
        fragment_ids = [item.text for item in fragments + collaterals]

        if len(fragment_ids):
            delete_fragment_ids(vrt_item.fragment_id, fragment_ids)

        # Remove all dynamic metadata and put s3 metadata
        bucket = f"mam-highres{vrt_item.type}"
        object_key = vrt_item.aremakey[len(f"MAM/Highres{vrt_item.type}/") :]
        sidecar = transform_metadata(
            BytesIO(item_query_result), object_key, bucket, pid
        )

        update_metadata(vrt_item.fragment_id, BytesIO(sidecar))

        # Send essenceArchivedEvent so VRT can send new metadata for the naked essence
        message = generate_essence_archived_event(object_key, bucket, pid, vrt_item.md5)
        send_archived_event(vrt_item.fragment_id, message)
    pass
