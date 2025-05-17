from enum import Enum


class TicketStatus(Enum):
    UNREDEEMED = 0
    REDEEMED = 1
    FINISHED = 2