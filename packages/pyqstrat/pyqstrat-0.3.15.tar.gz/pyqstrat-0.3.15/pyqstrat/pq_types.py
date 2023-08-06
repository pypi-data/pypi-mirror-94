import pandas as pd
import numpy as np
import types
import math
import datetime
from dataclasses import dataclass
from types import SimpleNamespace
from typing import MutableSet, Mapping, Optional, Union, Any


class ContractGroup:
    '''A way to group contracts for figuring out which indicators, rules and signals to apply to a contract and for PNL reporting'''

    _group_names: MutableSet = set()
    name: str
    contracts: MutableSet['Contract']
    contracts_by_symbol: Mapping[str, 'Contract']
    
    @staticmethod
    def clear() -> None:
        '''
        When running Python interactively you may create a ContractGroup with a given name multiple times because you don't restart Python 
        therefore global variables are not cleared.  This function clears global ContractGroups
        '''
        ContractGroup._group_names = set()
        
    @staticmethod
    def create(name) -> 'ContractGroup':
        '''
         Args:
            name (str): Name of the group
        '''
        if name in ContractGroup._group_names:
            raise Exception(f'Contract group: {name} already exists')
        ContractGroup._group_names.add(name)
        contract_group = ContractGroup()
        contract_group.name = name
        contract_group.contracts = set()
        contract_group.contracts_by_symbol = {}
        return contract_group
        
    def add_contract(self, contract):
        self.contracts.add(contract)
        self.contracts_by_symbol[contract.symbol] = contract
        
    def get_contract(self, symbol):
        return self.contracts_by_symbol.get(symbol)
        
    def __repr__(self):
        return self.name


class Contract:
    _symbol_names: MutableSet[str] = set()
    symbol: str
    expiry: Optional[np.datetime64]
    multiplier: float
    properties: SimpleNamespace
    contract_group: ContractGroup
        
    contracts_by_symbol: Mapping[str, 'Contract']

    '''A contract such as a stock, option or a future that can be traded'''
    @staticmethod
    def create(symbol: str, contract_group: ContractGroup, expiry: Optional[Union[np.datetime64, datetime.datetime]] = None, multiplier: float = 1., 
               properties: Optional[SimpleNamespace] = None) -> 'Contract':
        '''
        Args:
            symbol: A unique string reprenting this contract. e.g IBM or ESH9
            contract_group: We sometimes need to group contracts for calculating PNL, for example, you may have a strategy
                which has 3 legs, a long option, a short option and a future or equity used to hedge delta.  In this case, you will be trading
                different symbols over time as options and futures expire, but you may want to track PNL for each leg using a contract group for each leg.
                So you could create contract groups 'Long Option', 'Short Option' and 'Hedge' and assign contracts to these.
            expiry: In the case of a future or option, the date and time when the 
                contract expires.  For equities and other non expiring contracts, set this to None.  Default None.
            multiplier: If the market price convention is per unit, and the unit is not the same as contract size, 
                set the multiplier here. For example, for E-mini contracts, each contract is 50 units and the price is per unit, 
                so multiplier would be 50.  Default 1
            properties: Any data you want to store with this contract.
                For example, you may want to store option strike.  Default None
        '''
        assert(isinstance(symbol, str) and len(symbol) > 0)
        if symbol in Contract._symbol_names:
            raise Exception(f'Contract with symbol: {symbol} already exists')
        Contract._symbol_names.add(symbol)

        assert(multiplier > 0)

        contract = Contract()
        contract.symbol = symbol
        
        assert(expiry is None or isinstance(expiry, datetime.datetime) or isinstance(expiry, np.datetime64))
        
        if expiry is not None and isinstance(expiry, datetime.datetime):
            expiry = np.datetime64(expiry)
            
        contract.expiry = expiry
        contract.multiplier = multiplier
        
        if properties is None:
            properties = types.SimpleNamespace()
        contract.properties = properties
        
        contract_group.add_contract(contract)
        contract.contract_group = contract_group
        return contract
    
    @staticmethod
    def clear() -> None:
        '''
        When running Python interactively you may create a Contract with a given symbol multiple times because you don't restart Python 
        therefore global variables are not cleared.  This function clears global Contracts
        '''
        Contract._symbol_names = set()
   
    def __repr__(self) -> str:
        return f'{self.symbol}' + (f' {self.multiplier}' if self.multiplier != 1 else '') + (
            f' expiry: {self.expiry.astype(datetime.datetime):%Y-%m-%d %H:%M:%S}' if self.expiry is not None else '') + (
            f' group: {self.contract_group.name}' if self.contract_group else '') + (
            f' {self.properties.__dict__}' if self.properties.__dict__ else '')
    

@dataclass
class Price:
    '''
    >>> price = Price(datetime.datetime(2020, 1, 1), 15.25, 15.75, 189, 300)
    >>> print(price)
    15.25@189/15.75@300
    >>> price.properties = SimpleNamespace(delta = -0.3)
    >>> price.valid = False
    >>> print(price)
    15.25@189/15.75@300 delta: -0.3 invalid
    >>> print(price.mid())
    15.5
    '''
    timestamp: datetime.datetime
    bid: float
    ask: float
    bid_size: int
    ask_size: int
    valid: bool = True
    properties: Optional[SimpleNamespace] = None
        
    @staticmethod
    def invalid() -> 'Price':
        return Price(datetime.datetime(datetime.MINYEAR, 1, 1),
                     bid=math.nan, 
                     ask=math.nan, 
                     bid_size=-1, 
                     ask_size=-1, 
                     valid=False)
        
    def mid(self) -> float:
        return 0.5 * (self.bid + self.ask)
    
    def vw_mid(self) -> float:
        '''
        Volume weighted mid
        >>> price = Price(datetime.datetime(2020, 1, 1), 15.25, 15.75, 189, 300)
        >>> print(f'{price.vw_mid():.4f}')
        15.4433
        >>> price.bid_size = 0
        >>> price.ask_size = 0
        >>> assert math.isnan(price.vw_mid())
        '''
        if self.bid_size + self.ask_size == 0: return math.nan
        return (self.bid * self.ask_size + self.ask * self.bid_size) / (self.bid_size + self.ask_size)
    
    def set_property(self, name: str, value: Any) -> None:
        if self.properties is None:
            self.properties = SimpleNamespace()
        setattr(self.properties, name, value)
    
    def spread(self) -> float:
        if self.ask < self.bid: return math.nan
        return self.ask - self.bid
        
    def __repr__(self) -> str:
        msg = f'{self.bid:.2f}@{self.bid_size}/{self.ask:.2f}@{self.ask_size}'
        if self.properties:
            for k, v in self.properties.__dict__.items():
                if isinstance(v, (np.floating, float)):
                    msg += f' {k}: {v:.5g}'
                else:
                    msg += f' {k}: {v}'
        if not self.valid:
            msg += ' invalid'
        return msg


class OrderStatus:
    '''
    Enum for order status
    '''
    OPEN = 'open'
    FILLED = 'filled'
    

class ReasonCode:
    '''A class containing constants for predefined order reason codes. Prefer these predefined reason codes if they suit
    the reason you are creating your order.  Otherwise, use your own string.
    '''
    ENTER_LONG = 'enter long'
    ENTER_SHORT = 'enter short'
    EXIT_LONG = 'exit long'
    EXIT_SHORT = 'exit short'
    BACKTEST_END = 'backtest end'
    ROLL_FUTURE = 'roll future'
    NONE = 'none'
    
    # Used for plotting trades
    MARKER_PROPERTIES = {
        ENTER_LONG: {'symbol': 'P', 'color': 'blue', 'size': 50},
        ENTER_SHORT: {'symbol': 'P', 'color': 'red', 'size': 50},
        EXIT_LONG: {'symbol': 'X', 'color': 'blue', 'size': 50},
        EXIT_SHORT: {'symbol': 'X', 'color': 'red', 'size': 50},
        ROLL_FUTURE: {'symbol': '>', 'color': 'green', 'size': 50},
        BACKTEST_END: {'symbol': '*', 'color': 'green', 'size': 50},
        NONE: {'symbol': 'o', 'color': 'green', 'size': 50}
    }
    

class Order:
    def __init__(self):
        self.contract: Contract = None
        self.timestamp: np.datetime64 = None
        self.qty: float = math.nan
        self.reason_code: str = None
        self.properties: SimpleNamespace = None
        self.status: str = None


class MarketOrder(Order):
    def __init__(self, contract: Contract, 
                 timestamp: np.datetime64, 
                 qty: float, 
                 reason_code: str = ReasonCode.NONE, 
                 properties: SimpleNamespace = None, 
                 status: str = 'open') -> None:
        '''
        Args:
            contract: The contract this order is for
            timestamp: Time the order was placed
            qty:  Number of contracts or shares.  Use a negative quantity for sell orders
            reason_code: The reason this order was created.
                Prefer a predefined constant from the ReasonCode class if it matches your reason for creating this order.
                Default None
            properties: Any order specific data we want to store.  Default None
            status: Status of the order, "open", "filled", etc. Default "open"
        '''
        self.contract = contract
        self.timestamp = timestamp
        if not np.isfinite(qty) or math.isclose(qty, 0): raise Exception(f'order qty must be finite and nonzero: {qty}')
        self.qty = qty
        self.reason_code = reason_code
        self.status = status
        if properties is None: properties = types.SimpleNamespace()
        self.properties = properties
        
    def __repr__(self):
        timestamp = pd.Timestamp(self.timestamp).to_pydatetime()
        return f'{self.contract.symbol} {timestamp:%Y-%m-%d %H:%M:%S} qty: {self.qty}' + (
            '' if self.reason_code == ReasonCode.NONE else f' {self.reason_code}') + (
            '' if not self.properties.__dict__ else f' {self.properties}') + (
            f' {self.status}')
            

class LimitOrder(Order):
    def __init__(self, 
                 contract: Contract,
                 timestamp: np.datetime64,
                 qty: float,
                 limit_price: float,
                 reason_code: str = ReasonCode.NONE,
                 properties: SimpleNamespace = None,
                 status: str = 'open') -> None:
        '''
        Args:
            contract: The contract this order is for
            timestamp: Time the order was placed
            qty:  Number of contracts or shares.  Use a negative quantity for sell orders
            limit_price: Limit price (float)
            reason_code: The reason this order was created.
                Prefer a predefined constant from the ReasonCode class if it matches your reason for creating this order.
                Default None
            properties: Any order specific data we want to store.  Default None
            status: Status of the order, "open", "filled", etc. (default "open")
        '''
        self.contract = contract
        self.timestamp = timestamp
        if not np.isfinite(qty) or math.isclose(qty, 0): raise Exception(f'order qty must be finite and nonzero: {qty}')
        self.qty = qty
        self.reason_code = reason_code
        self.limit_price = limit_price
        if properties is None: properties = types.SimpleNamespace()
        self.properties = properties
        self.properties.limit_price = self.limit_price
        self.status = status
        
    def __repr__(self) -> str:
        timestamp = pd.Timestamp(self.timestamp).to_pydatetime()
        return f'{self.contract.symbol} {timestamp:%Y-%m-%d %H:%M:%S} qty: {self.qty} lmt_prc: {self.limit_price}' + (
            '' if self.reason_code == ReasonCode.NONE else f' {self.reason_code}') + (
            '' if not self.properties.__dict__ else f' {self.properties}') + (
            f' {self.status}')
    

class RollOrder(Order):
    '''A roll order is used to roll a future from one series to the next.  It represents a sell of one future and the buying of another future.'''
    def __init__(self, 
                 contract: Contract, 
                 timestamp: np.datetime64,
                 close_qty: float,
                 reopen_qty: float,
                 reason_code: str = ReasonCode.ROLL_FUTURE,
                 properties: SimpleNamespace = None, 
                 status: str = 'open') -> None:
        '''
        Args:
            contract: The contract this order is for
            timestamp: Time the order was placed
            close_qty: Quantity of the future you are rolling
            reopen_qty: Quantity of the future you are rolling to
            reason_code: The reason this order was created.
                Prefer a predefined constant from the ReasonCode class if it matches your reason for creating this order.
                Default None
            properties: Any order specific data we want to store.  Default None
            status: Status of the order, "open", "filled", etc. (default "open")
        '''
        self.contract = contract
        self.timestamp = timestamp
        if not np.isfinite(close_qty) or math.isclose(close_qty, 0) or not np.isfinite(reopen_qty) or math.isclose(reopen_qty, 0):
            raise Exception(f'order quantities must be non-zero and finite: {close_qty} {reopen_qty}')
        self.close_qty = close_qty
        self.reopen_qty = reopen_qty
        self.reason_code = reason_code
        self.qty = close_qty  # For display purposes when we print varying order types
        if properties is None: properties = types.SimpleNamespace()
        self.properties = properties
        self.properties.close_qty = self.close_qty
        self.properties.reopen_qty = self.reopen_qty
        self.status = status
        
    def __repr__(self) -> str:
        timestamp = pd.Timestamp(self.timestamp).to_pydatetime()
        return f'{self.contract.symbol} {timestamp:%Y-%m-%d %H:%M:%S} close_qty: {self.close_qty} reopen_qty: {self.reopen_qty}' + (
            '' if self.reason_code == ReasonCode.NONE else f' {self.reason_code}') + '' if not self.properties.__dict__ else f' {self.properties}' + (
            f' {self.status}')

  
class StopLimitOrder(Order):
    '''Used for stop loss or stop limit orders.  The order is triggered when price goes above or below trigger price, depending on whether this is a short
      or long order.  Becomes either a market or limit order at that point, depending on whether you set the limit price or not.
    '''
    def __init__(self, 
                 contract: Contract,
                 timestamp: np.datetime64,
                 qty: float,
                 trigger_price: float,
                 limit_price: float = np.nan,
                 reason_code: str = ReasonCode.NONE, 
                 properties: SimpleNamespace = None,
                 status: str = 'open') -> None:
        '''
        Args:
            contract: The contract this order is for
            timestamp: Time the order was placed
            qty:  Number of contracts or shares.  Use a negative quantity for sell orders
            trigger_price: Order becomes a market or limit order if price crosses trigger_price.
            limit_price: If not set (default), order becomes a market order when price crosses trigger price.  
                Otherwise it becomes a limit order.  Default np.nan
            reason_code: The reason this order was created.
                Prefer a predefined constant from the ReasonCode class if it matches your reason for creating this order.
                Default None
            properties: Any order specific data we want to store.  Default None
            status: Status of the order, "open", "filled", etc. (default "open")
        '''      
        self.contract = contract
        self.timestamp = timestamp
        if not np.isfinite(qty) or math.isclose(qty, 0): raise Exception(f'order qty must be finite and nonzero: {qty}')
        self.qty = qty
        self.trigger_price = trigger_price
        self.limit_price = limit_price
        self.reason_code = reason_code
        self.triggered = False
        if properties is None: properties = types.SimpleNamespace()
        self.properties = properties
        self.properties.trigger_price = trigger_price
        self.properties.limit_price = limit_price
        self.status = status
        
    def __repr__(self) -> str:
        timestamp = pd.Timestamp(self.timestamp).to_pydatetime()
        return f'{self.contract.symbol} {timestamp:%Y-%m-%d %H:%M:%S} qty: {self.qty} trigger_prc: {self.trigger_price} limit_prc: {self.limit_price}' + (
            '' if self.reason_code == ReasonCode.NONE else f' {self.reason_code}') + ('' if not self.properties.__dict__ else f' {self.properties}') + (
            f' {self.status}')
    

class Trade:
    def __init__(self, contract: Contract,
                 order: Order,
                 timestamp: np.datetime64, 
                 qty: float, 
                 price: float, 
                 fee: float = 0., 
                 commission: float = 0., 
                 properties: Optional[SimpleNamespace] = None) -> None:
        '''
        Args:
            contract: The contract we traded
            order: A reference to the order that created this trade. Default None
            timestamp: Trade execution datetime
            qty: Number of contracts or shares filled
            price: Trade price
            fee: Fees paid to brokers or others. Default 0
            commision: Commission paid to brokers or others. Default 0
            properties: Any data you want to store with this contract.
                For example, you may want to store bid / ask prices at time of trade.  Default None
        '''
        assert(isinstance(contract, Contract))
        assert(isinstance(order, Order))
        assert(np.isfinite(qty))
        assert(np.isfinite(price))
        assert(np.isfinite(fee))
        assert(np.isfinite(commission))
        assert(isinstance(timestamp, np.datetime64))
        
        self.contract = contract
        self.order = order
        self.timestamp = timestamp
        self.qty = qty
        self.price = price
        self.fee = fee
        self.commission = commission
        
        if properties is None:
            properties = types.SimpleNamespace()
        self.properties = properties
        
    def __repr__(self) -> str:
        '''
        >>> Contract.clear()
        >>> ContractGroup.clear()
        >>> contract = Contract.create('IBM', contract_group = ContractGroup.create('IBM'))
        >>> order = MarketOrder(contract, np.datetime64('2019-01-01T14:59'), 100)
        >>> print(Trade(contract, order, np.datetime64('2019-01-01 15:00'), 100, 10.2130000, 0.01))
        IBM 2019-01-01 15:00:00 qty: 100 prc: 10.213 fee: 0.01 order: IBM 2019-01-01 14:59:00 qty: 100 open
        '''
        timestamp = pd.Timestamp(self.timestamp).to_pydatetime()
        fee = f' fee: {self.fee:.6g}' if self.fee else ''
        commission = f' commission: {self.commission:.6g}' if self.commission else ''
        return f'{self.contract.symbol}' + (
            f' {self.contract.properties.__dict__}' if self.contract.properties.__dict__ else '') + (
            f' {timestamp:%Y-%m-%d %H:%M:%S} qty: {self.qty} prc: {self.price:.6g}{fee}{commission} order: {self.order}') + (
            f' {self.properties.__dict__}' if self.properties.__dict__ else '')
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
