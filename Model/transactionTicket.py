from typing import List
from Model.itemType import ItemType
from Model.reviewFilm import ReviewFilm
from Model.showing import Showing
from Model.ticket import Ticket
from Model.ticketStatus import TicketStatus
from Model.transaction import Transaction


class TransactionTicket(Transaction):
    def __init__(self, id, tickets:List[Ticket], nominal, memberId = 0, ticketStatus:TicketStatus = TicketStatus.UNREDEEMED, review:ReviewFilm = None, showing:Showing = None):
        super().__init__(id, nominal, ItemType.MOVIE, memberId)
        self.tickets:List[Ticket] = tickets
        self.ticketStatus:TicketStatus
        self.review:ReviewFilm = review
        self.showing = showing

    def get_showing(self):
        return self.showing

    def set_showing(self, value):
        self.showing = value

    def get_review(self):
        return self.review

    def set_review(self, value):
        self.review = value
    
    def get_tickets(self):
        return self.tickets

    def set_tickets(self, tickets):
        self.tickets = tickets
    
    def get_ticketStatus(self):
        return self.ticketStatus
    
    def set_ticketStatus(self, status:TicketStatus):
        self.ticketStatus = status

