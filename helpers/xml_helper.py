from lxml import etree
import datetime

from services.database import VrtItem

NAMESPACES_METADATA = {
    "mh": "https://zeticon.mediahaven.com/metadata/20.3/mh/",
    "mhs": "https://zeticon.mediahaven.com/metadata/20.3/mhs/",
}

NAMESPACES_VRT_MESSAGE = {
    None: "http://www.vrt.be/mig/viaa/api",
    "ebu": "urn:ebu:metadata-schema:ebuCore_2012",
}


def generate_essence_archived_event(
    s3_object_key: str, s3_bucket: str, pid: str, md5: str
) -> str:
    root = etree.Element(
        "essenceArchivedEvent",
        nsmap=NAMESPACES_VRT_MESSAGE,
    )
    etree.SubElement(root, "timestamp").text = (
        datetime.datetime.now().astimezone().isoformat()
    )
    etree.SubElement(root, "file").text = s3_object_key
    etree.SubElement(root, "pid").text = pid
    etree.SubElement(root, "s3bucket").text = s3_bucket
    etree.SubElement(root, "md5sum").text = md5
    event = etree.tostring(
        root,
        pretty_print=True,
        encoding="utf-8",
        xml_declaration=True,
    ).decode("utf-8")

    return event


def transform_metadata(xml: str, s3_object_key: str, s3_bucket: str, pid: str) -> bytes:
    with open("./transform.xslt") as f:
        transform = etree.XSLT(etree.parse(f))

    result = transform(
        etree.parse(xml),
        pid=etree.XSLT.strparam(pid),
        s3_object_key=etree.XSLT.strparam(s3_object_key),
        s3_bucket=etree.XSLT.strparam(s3_bucket),
    )
    sidecar = etree.tostring(result, pretty_print=True, encoding="utf-8")

    return sidecar
