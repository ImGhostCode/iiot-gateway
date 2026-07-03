import logging
import time
from dataclasses import dataclass, field
from typing import Literal

import paho.mqtt.client as mqtt
import yaml

from gateway.core.datapoint import DataPoint

logger = logging.getLogger(__name__)

Serverity = Literal["warning", "critical"]
Condition = Literal[">", ">=", "<", "<=", "==", "!="]

CONDITION_FN = {
    ">": lambda v, t: v > t,
    ">=": lambda v, t: v >= t,
    "<": lambda v, t: v < t,
    "<=": lambda v, t: v <= t,
    "==": lambda v, t: v == t,
    "!=": lambda v, t: v != t,
}

@dataclass
class Rule:
    name: str
    measurement: str
    condition: Condition
    threshold: float
    severity: Serverity = "warning"
    device_id: str = "*"
    cooldown_sec: float = 60
    _last_tringgered: float = field(default=0.0, init=False, repr=False)

    def matches(self, point: DataPoint) -> bool:
        if self.device_id != "*" and self.device_id != point.device_id:
            return False
        return self.measurement == point.measurement

    def evaluate(self, point: DataPoint) -> bool:
        fn = CONDITION_FN.get(self.condition)
        if fn is None:
            logger.error("Rule '{self.name}': condition '{self.condition}' is invalid")
            return False
        return fn(point.value, self.threshold)
    
    def is_cooled_down(self)-> bool:
        return (time.monotonic() - self._last_tringgered) >= self.cooldown_sec
    
    def mark_triggered(self) ->None:
        self._last_tringgered = time.monotonic()

class RuleEngine:
    ALERT_TOPIC = "iiot/alerts"

    def __init__(self, rules_path: str, mqtt_client: mqtt.Client):
        self._rules: list[Rule] = []
        self._mqtt = mqtt_client
        self._load_rules(rules_path)

    def _load_rules(self, path: str) -> None:
        try:
            with open(path, encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
            for item in raw.get("rules", []):
                rule = Rule(
                    name=item["name"],
                    measurement=item["measurement"],
                    condition=item["condition"],
                    threshold=float(item["threshold"]),
                    severity=item.get("severity", "warning"),
                    device_id=item.get("device_id", "*"),
                    cooldown_sec=float(item.get("cooldown_sec", 60)),
                )
                self._rules.append(rule)
            logger.info(f"Rule Engine: loadded {len(self._rules)} rule from '{path}'")
        except FileNotFoundError:
            logger.warning(f"Rule Engine: '{path}' not found, run no rules")
        except Exception as exc:
            logger.error(f"Rule Engine: Error loading rule: {exc}")
        
    def evaluate(self, point: DataPoint) -> None:
        for rule in self._rules:
            if not rule.matches(point):
                continue
            if rule.evaluate(point) and rule.is_cooled_down():
                rule.mark_triggered()
                self._publish_alert(rule, point)

    def _publish_alert(self, rule: Rule, point: DataPoint) -> None:
        import json
        from datetime import datetime, timezone

        payload = json.dumps({
            "rule_name": rule.name,
            "severity": rule.severity,
            "device_id": point.device_id,
            "measurement": point.measurement,
            "value": point.value,
            "threshold": rule.threshold,
            "condition": rule.condition,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        topic = f"{self.ALERT_TOPIC}/{rule.severity}/{point.device_id}"
        self._mqtt.publish(topic, payload, qos=1)

        if rule.severity == "critical":
            logger.critical(
                f"🔴 ALERT [{rule.severity.upper()}] {rule.name} | "
                f"{point.device_id}.{point.measurement} = {point.value}"
                f"{rule.condition} {rule.threshold}"
            )
        else:
            logger.warning(
                f"🟡 ALERT [{rule.severity.upper()}] {rule.name} | "
                f"{point.device_id}.{point.measurement} = {point.value} "
                f"{rule.condition} {rule.threshold}"
            )

