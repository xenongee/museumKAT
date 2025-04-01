from models import Stands
from lib.ListPrepare import ListPrepare


class StandsMenu:
    standslist = ListPrepare(Stands.query.order_by(Stands.stand_id), 'stand_id')
    standslist = standslist.get_list()
