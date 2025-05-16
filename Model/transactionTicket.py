from typing import List
from Model.itemType import ItemType
from Model.ticket import Ticket
from Model.transaction import Transaction


class TransactionTicket(Transaction):
    def __init__(self, id, tickets:List[Ticket], nominal, itemType = ItemType.MOVIE, memberId = 0):
        super().__init__(id, nominal, itemType, memberId)
        self.tickets:List[Ticket] = tickets
