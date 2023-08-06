from enum import IntEnum


# Use IntEnum instead of Enum to allow for JSON serialization
class CarStats(IntEnum):
    CAR_STATUS_RUNNING = 0
    CAR_STATUS_OUT_OF_RACE_ACCIDENT = 1
    CAR_STATUS_OUT_OF_RACE_ENGINE = 2
    CAR_STATUS_IN_GARAGE = 3
    CAR_STATUS_PRERACE = 4
    CAR_STATUS_WAITING = 5
    CAR_STATUS_WARMUP_LAP = 6
    CAR_STATUS_UNKNOWN = 7
    CAR_STATUS_ONDECK = 8
    CAR_STATUS_FINISHED = 9
    CAR_STATUS_DID_NOT_START = 10
    CAR_STATUS_LOST_GPS = 65280
