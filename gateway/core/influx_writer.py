import logging

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from gateway.config.settings import config
from gateway.core.datapoint import DataPoint

logger = logging.getLogger(__name__)

class InfluxWriter:
    def __init__(self):
        self._client = InfluxDBClient(
            url=config.infuxdb.url,
            token=config.infuxdb.token,
            org=config.infuxdb.org
        )
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._bucket = config.infuxdb.bucket
        logger.info("InfluxWriter ok -> bucket '{self._bucket}'")

    def write(self, point: DataPoint) -> None:
        try:
            influx_point = (
                Point(point.measurement)
                .tag("device_id", point.device_id)
                .tag("protocol", point.protocol)
                .field("value", point.value)
                .time(point.timestamp)
            )

            for key, val in point.tags.items():
                influx_point = influx_point.tag(key, val)

            self._write_api.write(bucket=self._bucket, record=influx_point)
            logger.debug(
                f"Wrote: {point.device_id}.{point.measurement} = {point.value}" 
            )
        except Exception as exc:
            logger.error(f"InfluxDB write error {point.device_id}: {exc}")

    def close(self) -> None:
        self._client.close()