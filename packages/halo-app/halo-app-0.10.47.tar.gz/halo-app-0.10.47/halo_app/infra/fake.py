from halo_app.app.event import AbsHaloEvent
from halo_app.classes import AbsBaseClass
from halo_app.domain.repository import AbsRepository
from halo_app.app.uow import AbsUnitOfWork

class FakeRepository(AbsRepository):

    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product):
        self._products.add(product)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def _get_by_batchref(self, batchref):
        return next((
            p for p in self._products for b in p.batches
            if b.reference == batchref
        ), None)


class FakeUnitOfWork(AbsUnitOfWork):

    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakePublisher(AbsBaseClass):
    def publish(self,channel, event: AbsHaloEvent):
        #logging.info('publishing: channel=%s, event=%s', channel, event)
        pass