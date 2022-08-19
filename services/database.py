from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from psycopg_pool import ConnectionPool
from psycopg.rows import class_row


@dataclass
class VrtItem:
    fragment_id: str
    md5: str
    type: str
    aremakey: str
    status: str
    creation_time: datetime
    modification_time: datetime


class DatabaseService(object):
    def __init__(self, config: dict):
        self.pool = ConnectionPool(
            f"host={config['database']['host']} port={config['database']['port']} dbname={config['database']['dbname']} user={config['database']['user']} password={config['database']['password']}"
        )

    def get_item_to_process(self) -> Optional[VrtItem]:
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(VrtItem)) as cur:
                return cur.execute(
                    "SELECT * FROM public.vrt_migration_v2 WHERE status = 'TODO' LIMIT 1"
                ).fetchone()

    def update_db_status(self, fragment_id: str, status: str):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE public.vrt_migration_v2 SET status = %s WHERE fragment_id = %s;",
                    (status, fragment_id),
                )

                conn.commit()
