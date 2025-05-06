from enum import StrEnum


class OrderStatusEnum(StrEnum):
    unlisted = "unlisted"
    ordered = "ordered"
    done = "done"
