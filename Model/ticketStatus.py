from enum import Enum


class TicketStatus(Enum):
    UNREDEEMED = 0
    REDEEMED = 1
    EXPIRED = 2
    FINISHED = 3