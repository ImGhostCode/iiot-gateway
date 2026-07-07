"""
Schema:
  TABLE devices  — device_id, protocol, first/last seen, point_count, latest_json
  TABLE alerts   — id, rule_name, severity, device_id, measurement, value,
                   threshold, condition, timestamp

File DB: data/gateway.db
"""

import json
import logging
import sqlite3
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from gateway.core.datapoint import DataPoint

logger = logging.getLogger(__name__)

DB_PATH = Path("data/gateway.db")

DDL = """
CREATE TABLE IF NOT EXISTS devices (
    device_id    TEXT PRIMARY KEY,
    protocol     TEXT NOT NULL,
    first_seen   TEXT NOT NULL,
    last_seen    TEXT NOT NULL,
    point_count  INTEGER NOT NULL DEFAULT 0,
    latest_json  TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS alerts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name    TEXT NOT NULL,
    severity     TEXT NOT NULL,
    device_id    TEXT NOT NULL,
    measurement  TEXT NOT NULL,
    value        REAL NOT NULL,
    threshold    REAL NOT NULL,
    condition    TEXT NOT NULL,
    timestamp    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_alerts_severity   ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_device_id  ON alerts(device_id);
CREATE INDEX IF NOT EXISTS idx_alerts_timestamp  ON alerts(timestamp DESC);
"""

def _get_conn(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn

def init_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = _get_conn(db_path)
    conn.executescript(DDL)
    conn.commit()
    logger.info(f"SQLite DB is already at '{db_path}'")
    return conn

@dataclass
class DeviceInfo:
    device_id: str
    protocol: str
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    latest: dict[str, float] = field(default_factory=dict)
    point_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "protocol": self.protocol,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "latest": self.latest,
            "point_count": self.point_count,
            "online": self._is_online(),
        }
    
    def _is_online(self) -> bool:
        delta = (datetime.now(timezone.utc) - self.last_seen).total_seconds()
        return delta < 30
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "DeviceInfo":
        return cls(
            device_id=row["device_id"],
            protocol=row["protocol"],
            first_seen=datetime.fromisoformat(row["first_seen"]),
            last_seen=datetime.fromisoformat(row["last_seen"]),
            latest=json.loads(row["latest_json"]),
            point_count=row["point_count"],
        )
    
class DeviceStore:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._lock = threading.Lock()
        self._cache: dict[str, DeviceInfo] = {}
        self._load_from_db()

    def _load_from_db(self) -> None:
        rows = self._conn.execute("SELECT * FROM devices").fetchall()
        for row in rows:
            info = DeviceInfo.from_row(row)
            self._cache[info.device_id] = info
        logger.info(f"DeviceStore: loadded {len(self._cache)} device from SQLite")

    def update(self, point: DataPoint) -> None:
        with self._lock:
            now_iso = point.timestamp.isoformat()

            if point.device_id not in self._cache:
                info = DeviceInfo(
                    device_id=point.device_id,
                    protocol=point.protocol,
                    first_seen=point.timestamp,
                    last_seen=point.timestamp,
                    latest={point.measurement: point.value},
                    point_count=1
                )
                self._cache[point.device_id] = info
                self._conn.execute(
                    """INSERT INTO devices
                    (device_id, protocol, first_seen, last_seen, point_count, latest_json)
                    VALUES (?, ?, ?, ?, 1, ?)
                    """,
                    (point.device_id, point.protocol, now_iso, now_iso,
                    json.dumps(info.latest))
                )
            else:
                info = self._cache[point.device_id]
                info.last_seen = point.timestamp
                info.latest[point.measurement] = point.value
                info.point_count += 1
                self._conn.execute(
                    """UPDATE devices
                    SET last_seen=?, point_count=?, latest_json=?
                    WHERE device_id=?
                    """,
                    (now_iso, info.point_count, 
                     json.dumps(info.latest), point.device_id)
                )

            self._conn.commit()

    def get_all(self) -> list[dict]:
        with self._lock:
            return [d.to_dict() for d in self._cache.values()]
        
    def get(self, device_id: str) -> dict | None:
        with self._lock:
            info = self._cache.get(device_id)
            return info.to_dict() if info else None
    
    def count(self) -> int:
        with self._lock:
            return len(self._cache)
        
    def total_points(self) -> int:
        with self._lock:
            return sum(d.point_count for d in self._cache.values())
        
@dataclass
class AlertRecord:
    rule_name: str
    severity: str
    device_id: str
    measurement: str
    value: float
    threshold: float
    condition: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "rule_name": self.rule_name,
            "severity": self.severity,
            "device_id": self.device_id,
            "measurement": self.measurement,
            "value": self.value,
            "threshold": self.threshold,
            "condition": self.condition,
            "timestamp": self.timestamp.isoformat(),
        }
    

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "AlertRecord":
        return cls(
            id=row["id"],
            rule_name=row["rule_name"],
            severity=row["severity"],
            device_id=row["device_id"],
            measurement=row["measurement"],
            value=row["value"],
            threshold=row["threshold"],
            condition=row["condition"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
        )
    
class AlertStore:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._lock = threading.Lock()

    def add(self, alert: AlertRecord) -> None:
        with self._lock:
            cursor = self._conn.execute(
                """INSERT INTO alerts
                   (rule_name, severity, device_id, measurement,
                    value, threshold, condition, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (alert.rule_name, alert.severity, alert.device_id,
                 alert.measurement, alert.value, alert.threshold,
                 alert.condition, alert.timestamp.isoformat()),
            )
            self._conn.commit()
            alert.id = cursor.lastrowid  # update ID

    def get_all(
        self,
        severity: str | None = None,
        device_id: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        conditions = []
        params: list[Any] = []

        if severity:
            conditions.append("severity = ?")
            params.append(severity)
        if device_id:
            conditions.append("device_id = ?")
            params.append(device_id)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.extend([limit, offset])

        with self._lock:
            rows = self._conn.execute(
                f"SELECT * FROM alerts {where} ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                params,
            ).fetchall()
        return [AlertRecord.from_row(r).to_dict() for r in rows]

    def total_count(self, severity: str | None = None, device_id: str | None = None) -> int:
        conditions = []
        params: list[Any] = []
        if severity:
            conditions.append("severity = ?")
            params.append(severity)
        if device_id:
            conditions.append("device_id = ?")
            params.append(device_id)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        with self._lock:
            row = self._conn.execute(
                f"SELECT COUNT(*) as cnt FROM alerts {where}", params
            ).fetchone()
        return row["cnt"]
