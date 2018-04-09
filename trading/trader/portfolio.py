import logging
import pprint

from config.cst import *


class Portfolio:
    def __init__(self, config, trader):
        self.config = config
        self.portfolio = self.config["simulator"]["starting_portfolio"]
        self.logger = logging.getLogger("Portfolio")
        self.trader = trader
        self.exchange = self.trader.get_exchange()

    def get_currency_portfolio(self, currency):
        if currency in self.portfolio:
            return self.portfolio[currency]
        else:
            self.portfolio[currency] = 0
            return self.portfolio[currency]

    def update_portfolio(self, order):
        currency, market = order.get_currency_and_market()

        # update currency
        if currency in self.portfolio:
            if order.get_side() == TradeOrderSide.BUY:
                self.portfolio[currency] += order.get_filled_quantity()
            else:
                self.portfolio[currency] -= order.get_filled_quantity()
        else:
            self.portfolio[currency] = order.get_filled_quantity()

        # update market
        if market in self.portfolio:
            if order.get_side() == TradeOrderSide.BUY:
                self.portfolio[market] -= (order.get_filled_quantity() * order.get_filled_price()) - order.get_total_fees()
            else:
                self.portfolio[market] += (order.get_filled_quantity() * order.get_filled_price()) - order.get_total_fees()
        else:
            self.portfolio[market] = (-order.get_filled_quantity() * order.get_filled_price()) - order.get_total_fees()

        # Only for log purpose
        if order.get_side() == TradeOrderSide.BUY:
            currency_portfolio_num = "+" + str(order.get_filled_quantity())
            market_portfolio_num = "-" + str(self.portfolio[market])
        else:
            currency_portfolio_num = "-" + str(order.get_filled_quantity())
            market_portfolio_num = "+" + str(self.portfolio[market])

        self.logger.debug("Portfolio updated | " + currency + " " + currency_portfolio_num
                          + " | " + market + " " + market_portfolio_num
                          + " | " + "Current Portfolio : " + pprint.pformat(self.portfolio))