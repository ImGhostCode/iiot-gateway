"""
Endpoints:
    GET /health                      — gateway status + uptime
    GET /metrics                     — overall statistics
    GET /devices                     — list of all devices
    GET /devices/{device_id}         — details of a single device
    GET /devices/{device_id}/latest  — latest measurement of the device
    GET /alerts                      — 50 most recent alerts (filter: severity, device_id)
    GET /rules                       — list of active rules

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
"""

import time
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from gateway.core.store import DeviceStore, AlertStore
from gateway.core.rule_engine import RuleEngine

_device_store = None
_alert_store = None
_rule_engine = None
_start_time = time.monotonic()

app = FastAPI(
    title="IIoT Gateway API",
    description="REST API to monitor and manage Mini IIoT Gateway",
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def init(device_store: DeviceStore, alert_store: AlertStore, rule_engine: RuleEngine):
    global _device_store, _alert_store, _rule_engine
    _device_store = device_store
    _alert_store = alert_store
    _rule_engine = rule_engine

# ──────────────────────────────────────────────
#  Gateway
# ──────────────────────────────────────────────


@app.get("/health", tags=["Gateway"])
def health():
    uptime_sec = time.monotonic() - _start_time
    return {
        "status": "ok",
        "uptime_seconds": round(uptime_sec,1),
        "uptime_human": _fmt_uptime(uptime_sec),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
    }

@app.get("/metrics", tags=["Gateway"])
def metrics():
    _check_ready()
    online = sum(1 for d in _device_store.get_all() if d["online"])
    return {
        "devices": {
            "total": _device_store.count(),
            "online": online,
            "offline": _device_store.count() - online
        },
        "datapoints_processed": _device_store.total_points(),
        "alerts_total": _alert_store.total_count(),
        "rules_loaded": len(_rule_engine._rules),
        "uptime_seconds": round(time.monotonic()- _start_time, 1)
    }

# ──────────────────────────────────────────────
#  Devices
# ──────────────────────────────────────────────

@app.get("/devices", tags=["Devices"])
def list_devices(online_only: bool = Query(False, description="Return online devices only")):
    _check_ready()
    devices = _device_store.get_all()
    if online_only:
        devices = [d for d in devices if d["online"]]
    return {
        "count": len(devices),
        "devices": devices,
    }

@app.get("/devices/{device_id}", tags=["Devices"])
def get_device(device_id: str):
    _check_ready()
    device = _device_store.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found")
    return device

@app.get("/devices/{device_id}/latest", tags=["Devices"])
def get_device_latest(device_id: str):
    _check_ready()
    device = _device_store.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found")
    return {
        "device_id": device_id,
        "last_seen": device["last_seen"],
        "online": device["online"],
        "measurement": device["latest"]
    }

# ──────────────────────────────────────────────
#  Alerts
# ──────────────────────────────────────────────

@app.get("/alerts", tags=["Alerts"])
def list_alerts(
    severity: str | None = Query(None, description="Filter: 'warning' or 'critical'"),
    device_id: str | None = Query(None, description="Filter by device_id"),
    limit: int = Query(50, ge=1, le=200, description="Maximum of alerts"),
    offset: int = Query(0, ge=0, description="Skip n alerts first (pagination)")
):
    _check_ready()
    alerts = _alert_store.get_all(
        severity=severity, device_id=device_id, limit=limit, offset=offset
    )
    total = _alert_store.total_count(severity=severity, device_id= device_id, )
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "alerts": alerts,
    }

# ──────────────────────────────────────────────
#  Rules
# ──────────────────────────────────────────────
@app.get("/rules", tags=["Rules"])
def list_rules():
    _check_ready()
    import time as _time
    rules = []
    for r in _rule_engine._rules:
        elapsed = _time.monotonic() - r._last_triggered
        cooldown_remaining = max(0.0, r.cooldown_sec - elapsed)
        rules.append({
            "name": r.name,
            "device_id": r.device_id,
            "measurement": r.measurement,
            "condition": r.condition,
            "threshold": r.threshold,
            "severity": r.severity,
            "cooldown_sec": r.cooldown_sec,
            "cooldown_remaining_sec": round(cooldown_remaining, 1),
            "ready_to_alert": cooldown_remaining == 0,

        })
    return {
        "count": len(rules),
        "rules": rules
    }

# ──────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────
def _check_ready():
    if _device_store is None:
        raise HTTPException(status_code=503, detail="Gateway is not ready yet")
    
def _fmt_uptime(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {sec}s"
    if m: 
        return f"{m}m {sec}s"
    return f"{sec}s"