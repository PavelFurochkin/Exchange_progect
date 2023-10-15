# from http.server import BaseHTTPRequestHandler
# from Router.router import PathRouter

from Controller.base_controller import BaseController
from DAO.DAO import CurrenciesDAO


class ExchangeRate(BaseController):
    def __init__(self, handler):
        super().__init__(handler),
        self.dao = CurrenciesDAO()

    def do_GET(self):
        pass
        # params = PathRouter.determine_path_params(BaseHTTPRequestHandler.path)
        # response = self.dao.get_exchange_rate_by_code(params[0], params[1])
        # self.send(200, response)
        # self.dao.close()

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass