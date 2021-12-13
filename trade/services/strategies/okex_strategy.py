from ..okex.okex_dto import OkexDTO
from ..okex.okex_service import OkexService

class OkexStrategy(OkexService):

    def __init__(self, dto:OkexDTO):
        self.dto = dto
        super().__init__(dto)

    def get_current_balance(self):
        return super().get_current_balance()


okex_st = OkexStrategy()
okex_st.get_current_balance()