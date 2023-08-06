import numpy as np
import pandas as pd
import types
import sys
from collections import defaultdict
from pprint import pformat
import math

from pyqstrat.evaluator import compute_return_metrics, display_return_metrics, plot_return_metrics
from pyqstrat.account import Account
from pyqstrat.pq_types import ContractGroup, Contract, Order, Trade, ReasonCode, MarketOrder
from pyqstrat.plot import TimeSeries, trade_sets_by_reason_code, Subplot, Plot, LinePlotAttributes, FilledLinePlotAttributes
from pyqstrat.pq_utils import series_to_array, str2date, strtup2date
from types import SimpleNamespace
import matplotlib as mpl
from typing import Sequence, Callable, Any, Mapping, Union, Tuple, Optional, Dict, List

StrategyContextType = SimpleNamespace

PriceFunctionType = Callable[[Contract, np.ndarray, int, StrategyContextType], float]

IndicatorType = Union[np.ndarray, 
                      pd.Series,
                      Callable[[ContractGroup, np.ndarray, SimpleNamespace, StrategyContextType], np.ndarray]]

SignalType = Callable[[ContractGroup, np.ndarray, SimpleNamespace, SimpleNamespace, StrategyContextType], np.ndarray]

RuleType = Callable[
    [ContractGroup, 
     int, 
     np.ndarray, 
     SimpleNamespace, 
     np.ndarray, 
     Account, 
     StrategyContextType],
    Sequence[Order]]

MarketSimulatorType = Callable[
    [Sequence[Order], 
     int, 
     np.ndarray, 
     Dict[ContractGroup, SimpleNamespace], 
     Dict[ContractGroup, SimpleNamespace], 
     SimpleNamespace],
    Sequence[Trade]]

DateRangeType = Union[Tuple[str, str], Tuple[np.datetime64, np.datetime64]]

# Placeholder for orders to create later
OrderTupType = Tuple[RuleType, ContractGroup, Dict[str, Any]]

PlotPropertiesType = Mapping[str, Mapping[str, Any]]


def _get_time_series_list(timestamps: np.ndarray, 
                          names: Sequence[str], 
                          values: SimpleNamespace, 
                          properties: Optional[PlotPropertiesType]) -> List[TimeSeries]:
    '''
    For plotting, create a list of TimeSeries objects from the arrays in the values object
    '''
    ts_list = []
    for name in names:
        line_type: Optional[str] = None
        color: Optional[str] = None
        if properties is not None and name in properties:
            if 'line_type' in properties[name]: line_type = properties[name]['line_type']
            if 'color' in properties[name]: color = properties[name]['color']
        y = getattr(values, name)
        if not len(y): continue
        if y.dtype.type in [np.str_, np.object_, np.datetime64]: continue
        attrib = LinePlotAttributes(line_type=line_type, color=color)
        ts = TimeSeries(name, timestamps, y, display_attributes=attrib)
        ts_list.append(ts)
    return ts_list


class Strategy:
    def __init__(self, 
                 timestamps: np.ndarray,
                 contract_groups: Sequence[ContractGroup],
                 price_function: PriceFunctionType,
                 starting_equity: float = 1.0e6, 
                 pnl_calc_time: int = 15 * 60 + 1,
                 trade_lag: int = 0,
                 run_final_calc: bool = True, 
                 strategy_context: StrategyContextType = None) -> None:
        '''
        Args:
            timestamps (np.array of np.datetime64): The "heartbeat" of the strategy.  We will evaluate trading rules and 
                simulate the market at these times.
            contract_groups: The contract groups we will potentially trade.
            price_function: A function that returns the price of a contract at a given timestamp
            starting_equity: Starting equity in Strategy currency.  Default 1.e6
            pnl_calc_time: Time of day used to calculate PNL.  Default 15 * 60 (3 pm)
            trade_lag: Number of bars you want between the order and the trade.  For example, if you think it will take
                5 seconds to place your order in the market, and your bar size is 1 second, set this to 5.  Set this to 0 if you
                want to execute your trade at the same time as you place the order, for example, if you have daily bars.  Default 0.
            run_final_calc: If set, calculates unrealized pnl and net pnl as well as realized pnl when strategy is done.
                If you don't need unrealized pnl, turn this off for faster run time. Default True
            strategy_context: A storage class where you can store key / value pairs relevant to this strategy.
                For example, you may have a pre-computed table of correlations that you use in the indicator or trade rule functions.  
                If not set, the __init__ function will create an empty member strategy_context object that you can access.
        '''
        self.name = 'main'  # Set by portfolio when running multiple strategies
        self.timestamps = timestamps
        assert(len(contract_groups) and isinstance(contract_groups[0], ContractGroup))
        self.contract_groups = contract_groups
        if strategy_context is None: strategy_context = types.SimpleNamespace()
        self.strategy_context = strategy_context
        self.account = Account(contract_groups, timestamps, price_function, strategy_context, starting_equity, pnl_calc_time)
        assert trade_lag >= 0, f'trade_lag cannot be negative: {trade_lag}'
        self.trade_lag = trade_lag
        self.run_final_calc = run_final_calc
        self.indicators: Dict[str, IndicatorType] = {}
        self.signals: Dict[str, SignalType] = {}
        self.signal_values: Dict[ContractGroup, SimpleNamespace] = defaultdict(types.SimpleNamespace)
        self.rule_names: List[str] = []
        self.rules: Dict[str, RuleType] = {}
        self.position_filters: Dict[str, Optional[str]] = {}
        self.rule_signals: Dict[str, Tuple[str, Sequence]] = {}
        self.market_sims: List[MarketSimulatorType] = []
        self._trades: List[Trade] = []
        self._orders: List[Order] = []
        self._open_orders: Dict[int, List[Order]] = defaultdict(list)
        self.indicator_deps: Dict[str, List[str]] = {}
        self.indicator_cgroups: Dict[str, List[ContractGroup]] = {}
        self.indicator_values: Dict[ContractGroup, SimpleNamespace] = defaultdict(types.SimpleNamespace)
        self.signal_indicator_deps: Dict[str, List[str]] = {}
        self.signal_deps: Dict[str, List[str]] = {}
        self.signal_cgroups: Dict[str, List[ContractGroup]] = {}
        self.trades_iter: List[List] = [[] for x in range(len(timestamps))]  # For debugging, we don't really need this as a member variable
        
    def add_indicator(self, 
                      name: str, 
                      indicator: IndicatorType, 
                      contract_groups: Sequence[ContractGroup] = None, 
                      depends_on: Sequence[str] = None) -> None:
        '''
        Args:
            name: Name of the indicator
            indicator:  A function that takes strategy timestamps and other indicators and returns a numpy array
              containing indicator values.  The return array must have the same length as the timestamps object.
              Can also be a numpy array or a pandas Series in which case we just store the values.
            contract_groups: Contract groups that this indicator applies to.  If not set, it applies to all contract groups. Default None.
            depends_on: Names of other indicators that we need to compute this indicator. Default None.
        '''
        self.indicators[name] = indicator
        self.indicator_deps[name] = [] if depends_on is None else list(depends_on)
        if contract_groups is None: contract_groups = self.contract_groups
        if isinstance(indicator, np.ndarray) or isinstance(indicator, pd.Series):
            indicator_values = series_to_array(indicator)
            for contract_group in contract_groups:
                setattr(self.indicator_values[contract_group], name, indicator_values)
        self.indicator_cgroups[name] = list(contract_groups)
        
    def add_signal(self,
                   name: str,
                   signal_function: SignalType,
                   contract_groups: Sequence[ContractGroup] = None,
                   depends_on_indicators: Sequence[str] = None,
                   depends_on_signals: Sequence[str] = None) -> None:
        '''
        Args:
            name (str): Name of the signal
            signal_function (function):  A function that takes timestamps and a dictionary of indicator value arrays and 
                returns a numpy array
                containing signal values.  The return array must have the same length as the input timestamps
            contract_groups (list of :obj:`ContractGroup`, optional): Contract groups that this signal applies to.  
                If not set, it applies to all contract groups.  Default None.
            depends_on_indicators (list of str, optional): Names of indicators that we need to compute this signal. Default None.
            depends_on_signals (list of str, optional): Names of other signals that we need to compute this signal. Default None.
        '''
        self.signals[name] = signal_function
        self.signal_indicator_deps[name] = [] if depends_on_indicators is None else list(depends_on_indicators)
        self.signal_deps[name] = [] if depends_on_signals is None else list(depends_on_signals)
        if contract_groups is None: contract_groups = self.contract_groups
        self.signal_cgroups[name] = list(contract_groups)
        
    def add_rule(self, 
                 name: str, 
                 rule_function: RuleType, 
                 signal_name: str, 
                 sig_true_values: Sequence = None, 
                 position_filter: str = None) -> None:
        '''Add a trading rule.  Trading rules are guaranteed to run in the order in which you add them.  For example, if you set trade_lag to 0,
               and want to exit positions and re-enter new ones in the same bar, make sure you add the exit rule before you add the entry rule to the 
               strategy.
        
        Args:
            name: Name of the trading rule
            rule_function: A trading rule function that returns a list of Orders
            signal_name: The strategy will call the trading rule function when the signal with this name matches sig_true_values
            sig_true_values: If the signal value at a bar is equal to one of these values, 
                the Strategy will call the trading rule function.  Default [TRUE]
            position_filter: Can be "zero", "nonzero" or None.  Zero rules are only triggered when the corresponding contract positions are 0
                Nonzero rules are only triggered when the corresponding contract positions are non-zero.  
                If not set, we don't look at position before triggering the rule. Default None
        '''
        
        if sig_true_values is None: sig_true_values = [True]
            
        if name in self.rule_names:
            raise Exception(f'Rule {name} already exists')
        # Rules should be run in order
        self.rule_names.append(name)
        self.rule_signals[name] = (signal_name, sig_true_values)
        self.rules[name] = rule_function
        if position_filter is not None:
            assert(position_filter in ['zero', 'nonzero'])
        self.position_filters[name] = position_filter
        
    def add_market_sim(self, market_sim_function: MarketSimulatorType) -> None:
        '''Add a market simulator.  A market simulator is a function that takes orders as input and returns trades.'''
        self.market_sims.append(market_sim_function)
        
    def run_indicators(self, 
                       indicator_names: Sequence[str] = None, 
                       contract_groups: Sequence[ContractGroup] = None, 
                       clear_all: bool = False) -> None:
        '''Calculate values of the indicators specified and store them.
        
        Args:
            indicator_names: List of indicator names.  If None (default) run all indicators
            contract_groups: Contract group to run this indicator for.  If None (default), we run it for all contract groups.
            clear_all: If set, clears all indicator values before running.  Default False.
        '''
        
        if indicator_names is None: indicator_names = list(self.indicators.keys())
        if contract_groups is None: contract_groups = self.contract_groups
            
        if clear_all: self.indicator_values = defaultdict(types.SimpleNamespace)
            
        ind_names = []
            
        for ind_name, cgroup_list in self.indicator_cgroups.items():
            if len(set(contract_groups).intersection(cgroup_list)): ind_names.append(ind_name)
                
        indicator_names = list(set(ind_names).intersection(indicator_names))
         
        for cgroup in contract_groups:
            cgroup_ind_namespace = self.indicator_values[cgroup]
            for indicator_name in indicator_names:
                # First run all parents
                parent_names = self.indicator_deps[indicator_name]
                for parent_name in parent_names:
                    if cgroup in self.indicator_values and hasattr(cgroup_ind_namespace, parent_name): continue
                    self.run_indicators([parent_name], [cgroup])
                    
                # Now run the actual indicator
                if cgroup in self.indicator_values and hasattr(cgroup_ind_namespace, indicator_name): continue
                indicator_function = self.indicators[indicator_name]
                     
                parent_values = types.SimpleNamespace()

                for parent_name in parent_names:
                    setattr(parent_values, parent_name, getattr(cgroup_ind_namespace, parent_name))
                    
                if isinstance(indicator_function, np.ndarray) or isinstance(indicator_function, pd.Series):
                    indicator_values = indicator_function
                else:
                    indicator_values = indicator_function(cgroup, self.timestamps, parent_values, self.strategy_context)

                setattr(cgroup_ind_namespace, indicator_name, series_to_array(indicator_values))
                
    def run_signals(self, 
                    signal_names: Sequence[str] = None, 
                    contract_groups: Sequence[ContractGroup] = None, 
                    clear_all: bool = False) -> None:
        '''Calculate values of the signals specified and store them.
        
        Args:
            signal_names: List of signal names.  If None (default) run all signals
            contract_groups: Contract groups to run this signal for. If None (default), we run it for all contract groups.
            clear_all: If set, clears all signal values before running.  Default False.
        '''
        if signal_names is None: signal_names = list(self.signals.keys())
        if contract_groups is None: contract_groups = self.contract_groups
            
        if clear_all: self.signal_values = defaultdict(types.SimpleNamespace)
            
        sig_names = []
        
        for sig_name, cgroup_list in self.signal_cgroups.items():
            if len(set(contract_groups).intersection(cgroup_list)): 
                sig_names.append(sig_name)
                
        signal_names = list(set(sig_names).intersection(signal_names))
        
        for cgroup in contract_groups:
            for signal_name in signal_names:
                if cgroup not in self.signal_cgroups[signal_name]: continue
                # First run all parent signals
                parent_names = self.signal_deps[signal_name]
                for parent_name in parent_names:
                    if cgroup in self.signal_values and hasattr(self.signal_values[cgroup], parent_name): continue
                    self.run_signals([parent_name], [cgroup])
                # Now run the actual signal
                if cgroup in self.signal_values and hasattr(self.signal_values[cgroup], signal_name): continue
                signal_function = self.signals[signal_name]
                parent_values = types.SimpleNamespace()
                for parent_name in parent_names:
                    sig_vals = getattr(self.signal_values[cgroup], parent_name)
                    setattr(parent_values, parent_name, sig_vals)
                    
                # Get indicators needed for this signal
                indicator_values = types.SimpleNamespace()
                for indicator_name in self.signal_indicator_deps[signal_name]:
                    setattr(indicator_values, indicator_name, getattr(self.indicator_values[cgroup], indicator_name))
                    
                signal_output = signal_function(cgroup, self.timestamps, indicator_values, parent_values, self.strategy_context)
                setattr(self.signal_values[cgroup], signal_name, series_to_array(signal_output))

    def _generate_order_iterations(self, 
                                   rule_names: Sequence[str] = None, 
                                   contract_groups: Sequence[ContractGroup] = None, 
                                   start_date: np.datetime64 = None, 
                                   end_date: np.datetime64 = None) -> None:
        '''
        >>> class MockStrat:
        ...    def __init__(self):
        ...        self.timestamps = timestamps
        ...        self.account = self
        ...        self.rules = {'rule_a': rule_a, 'rule_b': rule_b}
        ...        self.market_sims = {ibm: market_sim_ibm, aapl: market_sim_aapl}
        ...        self.rule_signals = {'rule_a': ('sig_a', [1]), 'rule_b': ('sig_b', [1, -1])}
        ...        self.signal_values = {ibm: types.SimpleNamespace(sig_a=np.array([0., 1., 1.]), 
        ...                                                   sig_b = np.array([0., 0., 0.]) ),
        ...                               aapl: types.SimpleNamespace(sig_a=np.array([0., 0., 0.]), 
        ...                                                    sig_b=np.array([0., -1., -1])
        ...                                                   )}
        ...        self.signal_cgroups = {'sig_a': [ibm, aapl], 'sig_b': [ibm, aapl]}
        ...        self.indicator_values = {ibm: types.SimpleNamespace(), aapl: types.SimpleNamespace()}
        >>>
        >>> def market_sim_aapl(): pass
        >>> def market_sim_ibm(): pass
        >>> def rule_a(): pass
        >>> def rule_b(): pass
        >>> timestamps = np.array(['2018-01-01', '2018-01-02', '2018-01-03'], dtype = 'M8[D]')
        >>> rule_names = ['rule_a', 'rule_b']
        >>> ContractGroup.clear()
        >>> ibm = ContractGroup.create('IBM')
        >>> aapl = ContractGroup.create('AAPL')
        >>> contract_groups = [ibm, aapl]
        >>> start_date = np.datetime64('2018-01-01')
        >>> end_date = np.datetime64('2018-02-05')
        >>> strategy = MockStrat()
        >>> Strategy._generate_order_iterations(strategy, rule_names, contract_groups, start_date, end_date)
        >>> orders_iter = strategy.orders_iter
        >>> assert(len(orders_iter[0]) == 0)
        >>> assert(len(orders_iter[1]) == 2)
        >>> assert(orders_iter[1][0][1] == ibm)
        >>> assert(orders_iter[1][1][1] == aapl)
        >>> assert(len(orders_iter[2]) == 0)
        '''
        start_date, end_date = str2date(start_date), str2date(end_date)
        if rule_names is None: rule_names = self.rule_names
        if contract_groups is None: contract_groups = self.contract_groups

        num_timestamps = len(self.timestamps)
        
        # List of lists, i -> list of order tuple
        orders_iter: List[List[OrderTupType]] = [[] for x in range(num_timestamps)]

        for rule_name in rule_names:
            rule_function = self.rules[rule_name]
            for cgroup in contract_groups:
                signal_name, sig_true_values = self.rule_signals[rule_name]
                if cgroup not in self.signal_cgroups[signal_name]:
                    # We don't need to call this rule for this contract group
                    continue
                sig_values = getattr(self.signal_values[cgroup], signal_name)
                timestamps = self.timestamps

                null_value = False if sig_values.dtype == np.dtype('bool') else np.nan
                
                if start_date is not None:
                    start_idx: int = np.searchsorted(timestamps, start_date)  # type: ignore
                    sig_values[0:start_idx] = null_value
                    
                if end_date is not None:
                    end_idx: int = np.searchsorted(timestamps, end_date)  # type: ignore
                    sig_values[end_idx:] = null_value

                indices = np.nonzero(np.isin(sig_values[:num_timestamps], sig_true_values))[0]
                
                # Don't run rules on last index since we cannot fill any orders
                if len(indices) and indices[-1] == len(sig_values) - 1: indices = indices[:-1] 
                indicator_values = self.indicator_values[cgroup]
                iteration_params = {'indicator_values': indicator_values, 'signal_values': sig_values, 'rule_name': rule_name}
                for idx in indices: orders_iter[idx].append((rule_function, cgroup, iteration_params))

        self.orders_iter = orders_iter
    
    def run_rules(self, 
                  rule_names: Sequence[str] = None, 
                  contract_groups: Sequence[ContractGroup] = None, 
                  start_date: np.datetime64 = None,
                  end_date: np.datetime64 = None) -> None:
        '''
        Run trading rules.
        
        Args:
            rule_names: List of rule names.  If None (default) run all rules
            contract_groups: Contract groups to run this rule for.  If None (default), we run it for all contract groups.
            start_date: Run rules starting from this date. Default None 
            end_date: Don't run rules after this date.  Default None
        '''
        start_date, end_date = str2date(start_date), str2date(end_date)
        self._generate_order_iterations(rule_names, contract_groups, start_date, end_date)
        
        # Now we know which rules, contract groups need to be applied for each iteration, go through each iteration and apply them
        # in the same order they were added to the strategy
        for i in range(len(self.orders_iter)):
            self._run_iteration(i)
            
        if self.run_final_calc:
            self.account.calc(self.timestamps[-1])
        
    def _run_iteration(self, i: int) -> None:
        
        self._sim_market(i)
        # Treat all orders as IOC, i.e. if the order was not executed, then its cancelled.
        self._open_orders[i] = []
        
        rules = self.orders_iter[i]
        
        for (rule_function, contract_group, params) in rules:
            orders = self._get_orders(i, rule_function, contract_group, params)
            self._orders += orders
            self._open_orders[i + self.trade_lag] += orders
            # If the lag is 0, then run rules one by one, and after each rule, run market sim to generate trades and update
            # positions.  For example, if we have a rule to exit a position and enter a new one, we should make sure 
            # positions are updated after the first rule before running the second rule.  If the lag is not 0, 
            # run all rules and collect the orders, we don't need to run market sim after each rule
            if self.trade_lag == 0: self._sim_market(i)
        # If we failed to fully execute any orders in this iteration, add them to the next iteration so we get another chance to execute
        open_orders = self._open_orders.get(i)
        if open_orders is not None and len(open_orders):
            self._open_orders[i + 1] += open_orders
            
    def run(self) -> None:
        self.run_indicators()
        self.run_signals()
        self.run_rules()
        
    def _get_orders(self, idx: int, rule_function: RuleType, contract_group: ContractGroup, params: Dict[str, Any]) -> Sequence[Order]:
        try:
            indicator_values, signal_values, rule_name = params['indicator_values'], params['signal_values'], params['rule_name']
            position_filter = self.position_filters[rule_name]
            if position_filter is not None:
                curr_pos = self.account.position(contract_group, self.timestamps[idx])
                if position_filter == 'zero' and not math.isclose(curr_pos, 0): return []
                if position_filter == 'nonzero' and math.isclose(curr_pos, 0): return []
            orders = rule_function(contract_group, idx, self.timestamps, indicator_values, signal_values, self.account,
                                   self.strategy_context)
        except Exception as e:
            raise type(e)(
                f'Exception: {str(e)} at rule: {type(rule_function)} contract_group: {contract_group} index: {idx}'
            ).with_traceback(sys.exc_info()[2])
        return orders
        
    def _sim_market(self, i: int) -> None:
        '''
        Go through all open orders and run market simulators to generate a list of trades and return any orders that were not filled.
        '''
        open_orders = self._open_orders.get(i)
        if open_orders is None or len(open_orders) == 0: return
            
        for market_sim_function in self.market_sims:
            try:
                trades = market_sim_function(open_orders, i, self.timestamps, self.indicator_values, self.signal_values, self.strategy_context)
                if len(trades): self.account.add_trades(trades)
                self._trades += trades
            except Exception as e:
                raise type(e)(f'Exception: {str(e)} at index: {i} function: {market_sim_function}').with_traceback(sys.exc_info()[2])
            
        self._open_orders[i] = [order for order in open_orders if order.status != 'filled']
            
    def df_data(self, 
                contract_groups: Sequence[ContractGroup] = None, 
                add_pnl: bool = True, 
                start_date: Union[str, np.datetime64] = None, 
                end_date: Union[str, np.datetime64] = None) -> pd.DataFrame:
        '''
        Add indicators and signals to end of market data and return as a pandas dataframe.
        
        Args:
            contract_groups (list of:obj:`ContractGroup`, optional): list of contract groups to include.  All if set to None (default)
            add_pnl: If True (default), include P&L columns in dataframe
            start_date: string or numpy datetime64. Default None
            end_date: string or numpy datetime64: Default None
        '''
        start_date, end_date = str2date(start_date), str2date(end_date)
        if contract_groups is None: contract_groups = self.contract_groups
            
        timestamps = self.timestamps
        
        if start_date: timestamps = timestamps[timestamps >= start_date]
        if end_date: timestamps = timestamps[timestamps <= end_date]
            
        dfs = []
             
        for contract_group in contract_groups:
            df = pd.DataFrame({'timestamp': self.timestamps})
            if add_pnl: 
                df_pnl = self.df_pnl(contract_group)
 
            indicator_values = self.indicator_values[contract_group]
            
            for k in sorted(indicator_values.__dict__):
                name = k
                # Avoid name collisions
                if name in df.columns: name = name + '.ind'
                df.insert(len(df.columns), name, getattr(indicator_values, k))

            signal_values = self.signal_values[contract_group]

            for k in sorted(signal_values.__dict__):
                name = k
                if name in df.columns: name = name + '.sig'
                df.insert(len(df.columns), name, getattr(signal_values, k))
                
            if add_pnl: df = pd.merge(df, df_pnl, on=['timestamp'], how='left')
            # Add counter column for debugging
            df.insert(len(df.columns), 'i', np.arange(len(df)))
            
            dfs.append(df)
            
        return pd.concat(dfs)
    
    def trades(self, 
               contract_group: ContractGroup = None, 
               start_date: np.datetime64 = None, 
               end_date: np.datetime64 = None) -> Sequence[Trade]:
        '''Returns a list of trades with the given contract group and with trade date between (and including) start date 
            and end date if they are specified.
            If contract_group is None trades for all contract_groups are returned'''
        start_date, end_date = str2date(start_date), str2date(end_date)
        return self.account.trades(contract_group, start_date, end_date)
    
    def df_trades(self, 
                  contract_group: ContractGroup = None, 
                  start_date: np.datetime64 = None, 
                  end_date: np.datetime64 = None) -> pd.DataFrame:
        '''Returns a dataframe with data from trades with the given contract group and with trade date between (and including)
            start date and end date
            if they are specified. If contract_group is None trades for all contract_groups are returned'''
        start_date, end_date = str2date(start_date), str2date(end_date)
        return self.account.df_trades(contract_group, start_date, end_date)
    
    def orders(self, 
               contract_group: ContractGroup = None, 
               start_date: Union[np.datetime64, str] = None, 
               end_date: Union[np.datetime64, str] = None) -> Sequence[Order]:
        '''Returns a list of orders with the given contract group and with order date between (and including) start date and 
            end date if they are specified.
            If contract_group is None orders for all contract_groups are returned'''
        orders: List[Order] = []
        start_date, end_date = str2date(start_date), str2date(end_date)
        if contract_group is None:
            orders += [order for order in self._orders if (
                start_date is None or order.timestamp >= start_date) and (end_date is None or order.timestamp <= end_date)]
        else:
            for contract in contract_group.contracts:
                orders += [order for order in self._orders if (contract is None or order.contract == contract) and (
                    start_date is None or order.timestamp >= start_date) and (end_date is None or order.timestamp <= end_date)]
        return orders
    
    def df_orders(self, contract_group=None, start_date=None, end_date=None) -> pd.DataFrame:
        '''Returns a dataframe with data from orders with the given contract group and with order date between (and including) 
            start date and end date
            if they are specified. If contract_group is None orders for all contract_groups are returned'''
        start_date, end_date = str2date(start_date), str2date(end_date)
        orders = self.orders(contract_group, start_date, end_date)
        order_records = [(order.contract.symbol, type(order).__name__, order.timestamp, order.qty, 
                          order.reason_code, 
                          (str(order.properties.__dict__) if order.properties.__dict__ else ''),
                          (str(order.contract.properties.__dict__) if order.contract.properties.__dict__ else '')) for order in orders]
        df_orders = pd.DataFrame.from_records(order_records,
                                              columns=['symbol', 'type', 'timestamp', 'qty', 'reason_code', 'order_props', 'contract_props'])
        return df_orders
   
    def df_pnl(self, contract_group=None) -> pd.DataFrame:
        '''Returns a dataframe with P&L columns.  If contract group is set to None (default), sums up P&L across all contract groups'''
        return self.account.df_account_pnl(contract_group)
    
    def df_returns(self, 
                   contract_group: ContractGroup = None,
                   sampling_frequency: str = 'D') -> pd.DataFrame:
        '''Return a dataframe of returns and equity indexed by date.
        
        Args:
            contract_group: The contract group to get returns for.  
                If set to None (default), we return the sum of PNL for all contract groups
            sampling_frequency: Downsampling frequency.  Default is None.  See pandas frequency strings for possible values
        '''
        pnl = self.df_pnl(contract_group)[['timestamp', 'net_pnl', 'equity']]

        pnl.equity = pnl.equity.ffill()
        pnl = pnl.set_index('timestamp').resample(sampling_frequency).last().reset_index()
        pnl = pnl.dropna(subset=['equity'])
        pnl['ret'] = pnl.equity.pct_change()
        return pnl
    
    def plot(self, 
             contract_groups: Sequence[ContractGroup] = None, 
             primary_indicators: Sequence[str] = None,
             primary_indicators_dual_axis: Sequence[str] = None,
             secondary_indicators: Sequence[str] = None,
             secondary_indicators_dual_axis: Sequence[str] = None,
             indicator_properties: PlotPropertiesType = None,
             signals: Sequence[str] = None,
             signal_properties: PlotPropertiesType = None, 
             pnl_columns: Sequence[str] = None, 
             title: str = None, 
             figsize: Tuple[int, int] = (20, 15), 
             _date_range: DateRangeType = None, 
             date_format: str = None, 
             sampling_frequency: str = None, 
             trade_marker_properties: PlotPropertiesType = None, 
             hspace: float = 0.15) -> None:
        
        '''
        Plot indicators, signals, trades, position, pnl
        
        Args:
            contract_groups: Contract groups to plot or None (default) for all contract groups. 
            primary indicators: List of indicators to plot in the main indicator section. Default None (plot everything)
            primary indicators: List of indicators to plot in the secondary indicator section. Default None (don't plot anything)
            indicator_properties: If set, we use the line color, line type indicated for the given indicators
            signals: Signals to plot.  Default None (plot everything).
            plot_equity: If set, we plot the equity curve.  Default is True
            title: Title of plot. Default None
            figsize: Figure size.  Default (20, 15)
            date_range: Used to restrict the date range of the graph. Default None
            date_format: Date format for tick labels on x axis.  If set to None (default), will be selected based on date range. 
                See matplotlib date format strings
            sampling_frequency: Downsampling frequency.  The graph may get too busy if you have too many bars of data, 
                so you may want to downsample before plotting.  See pandas frequency strings for possible values. Default None.
            trade_marker_properties: A dictionary of order reason code -> marker shape, marker size, marker color for plotting trades
                with different reason codes. By default we use the dictionary from the :obj:`ReasonCode` class
            hspace: Height (vertical) space between subplots.  Default is 0.15
        '''
        date_range = strtup2date(_date_range)
        if contract_groups is None: contract_groups = self.contract_groups
        if isinstance(contract_groups, ContractGroup): contract_groups = [contract_groups]
        if pnl_columns is None: pnl_columns = ['equity']
        
        for contract_group in contract_groups:
            primary_indicator_names = [ind_name for ind_name in self.indicator_values[contract_group].__dict__
                                       if hasattr(self.indicator_values[contract_group], ind_name)]
            if primary_indicators:
                primary_indicator_names = list(set(primary_indicator_names).intersection(primary_indicators))
            secondary_indicator_names: List[str] = []
            if secondary_indicators:
                secondary_indicator_names = list(secondary_indicators)
            signal_names = [sig_name for sig_name in self.signals.keys() if hasattr(self.signal_values[contract_group], sig_name)]
            if signals:
                signal_names = list(set(signal_names).intersection(signals))
 
            primary_indicator_list = _get_time_series_list(self.timestamps, primary_indicator_names, 
                                                           self.indicator_values[contract_group], indicator_properties)
            secondary_indicator_list = _get_time_series_list(self.timestamps, secondary_indicator_names, 
                                                             self.indicator_values[contract_group], indicator_properties)
            signal_list = _get_time_series_list(self.timestamps, signal_names, self.signal_values[contract_group], signal_properties)
            df_pnl_ = self.df_pnl(contract_group)
            pnl_list = [TimeSeries(pnl_column, 
                                   timestamps=df_pnl_.timestamp.values, 
                                   values=df_pnl_[pnl_column].values) for pnl_column in pnl_columns]
            
            trades = [trade for trade in self._trades if trade.order.contract.contract_group == contract_group]
            if trade_marker_properties:
                trade_sets = trade_sets_by_reason_code(trades, trade_marker_properties, remove_missing_properties=True)
            else:
                trade_sets = trade_sets_by_reason_code(trades)
                
            primary_indicator_subplot = Subplot(
                primary_indicator_list + trade_sets,  # type: ignore # mypy does not allow adding heterogeneous lists
                secondary_y=primary_indicators_dual_axis,
                height_ratio=0.5, 
                ylabel='Primary Indicators')
 
            if len(secondary_indicator_list):
                secondary_indicator_subplot = Subplot(secondary_indicator_list, 
                                                      secondary_y=secondary_indicators_dual_axis,
                                                      height_ratio=0.5, 
                                                      ylabel='Secondary Indicators')
            signal_subplot = Subplot(signal_list, ylabel='Signals', height_ratio=0.167)
            pnl_subplot = Subplot(pnl_list, ylabel='Equity', height_ratio=0.167, log_y=True, y_tick_format='${x:,.0f}')
            position = df_pnl_.position.values
            disp_attribs = FilledLinePlotAttributes()
            pos_subplot = Subplot(
                [TimeSeries('position', timestamps=df_pnl_.timestamp, values=position, display_attributes=disp_attribs)], 
                ylabel='Position', height_ratio=0.167)
            
            title_full = title
            if len(contract_groups) > 1:
                if title is None: title = ''
                title_full = f'{title} {contract_group.name}'
                
            plot_list = []
            if len(primary_indicator_list): plot_list.append(primary_indicator_subplot)
            if len(secondary_indicator_list): plot_list.append(secondary_indicator_subplot)
            if len(signal_list): plot_list.append(signal_subplot)
            if len(position): plot_list.append(pos_subplot)
            if len(pnl_list): plot_list.append(pnl_subplot)
            
            if not len(plot_list): return
                
            plot = Plot(plot_list, 
                        figsize=figsize, 
                        date_range=date_range, 
                        date_format=date_format, 
                        sampling_frequency=sampling_frequency, 
                        title=title_full, 
                        hspace=hspace)
            plot.draw()
            
    def evaluate_returns(self, 
                         contract_group: ContractGroup = None, 
                         plot: bool = True, 
                         display_summary: bool = True, 
                         float_precision: int = 4, 
                         return_metrics: bool = False) -> Optional[Mapping]:
        '''Returns a dictionary of common return metrics.
        
        Args:
            contract_group (:obj:`ContractGroup`, optional): Contract group to evaluate or None (default) for all contract groups
            plot (bool): If set to True, display plots of equity, drawdowns and returns.  Default False
            float_precision (float, optional): Number of significant figures to show in returns.  Default 4
            return_metrics (bool, optional): If set, we return the computed metrics as a dictionary
        '''
        returns = self.df_returns(contract_group)
        ev = compute_return_metrics(returns.timestamp.values, returns.ret.values, self.account.starting_equity)
        if display_summary:
            display_return_metrics(ev.metrics(), float_precision=float_precision)
        if plot: 
            plot_return_metrics(ev.metrics())
        if return_metrics:
            return ev.metrics()
        return None
    
    def plot_returns(self, contract_group: ContractGroup = None) -> Optional[Tuple[mpl.figure.Figure, mpl.axes.Axes]]:
        '''Display plots of equity, drawdowns and returns for the given contract group or for all contract groups if contract_group 
            is None (default)'''
        if contract_group is None:
            returns = self.df_returns()
        else:
            returns = self.df_returns(contract_group)

        ev = compute_return_metrics(returns.timestamp.values, returns.ret.values, self.account.starting_equity)
        return plot_return_metrics(ev.metrics())
       
    def __repr__(self):
        return f'{pformat(self.indicators)} {pformat(self.rules)} {pformat(self.account)}'
    

def test_strategy() -> Strategy:
    import math
    import numpy as np
    import pandas as pd
    import os
    from types import SimpleNamespace
    from pyqstrat.pq_types import Contract, ContractGroup, Trade

    try:
        # If we are running from unit tests
        ko_file_path = os.path.dirname(os.path.realpath(__file__)) + '/notebooks/support/coke_15_min_prices.csv.gz'
        pep_file_path = os.path.dirname(os.path.realpath(__file__)) + '/notebooks/support/pepsi_15_min_prices.csv.gz' 
    except NameError:
        ko_file_path = '../notebooks/support/coke_15_min_prices.csv.gz'
        pep_file_path = '../notebooks/support/pepsi_15_min_prices.csv.gz'

    ko_prices = pd.read_csv(ko_file_path)
    pep_prices = pd.read_csv(pep_file_path)

    ko_prices['timestamp'] = pd.to_datetime(ko_prices.date)
    pep_prices['timestamp'] = pd.to_datetime(pep_prices.date)
    
    end_time = '2019-01-30 12:00'
    
    ko_prices = ko_prices.query(f'timestamp <= "{end_time}"')
    pep_prices = pep_prices.query(f'timestamp <= "{end_time}"')

    timestamps = ko_prices.timestamp.values
    
    ratio = ko_prices.c / pep_prices.c
    
    def zscore_indicator(contract_group: ContractGroup, 
                         timestamps: np.ndarray, 
                         indicators: SimpleNamespace,
                         strategy_context: StrategyContextType) -> np.ndarray:  # simple moving average
        ratio = indicators.ratio
        r = pd.Series(ratio).rolling(window=130)
        mean = r.mean()
        std = r.std(ddof=0)
        zscore = (ratio - mean) / std
        zscore = np.nan_to_num(zscore)
        return zscore
    
    def pair_strategy_signal(contract_group: ContractGroup,
                             timestamps: np.ndarray,
                             indicators: SimpleNamespace, 
                             parent_signals: SimpleNamespace,
                             strategy_context: StrategyContextType) -> np.ndarray: 
        # We don't need any indicators since the zscore is already part of the market data
        zscore = indicators.zscore
        signal = np.where(zscore > 1, 2, 0)
        signal = np.where(zscore < -1, -2, signal)
        signal = np.where((zscore > 0.5) & (zscore < 1), 1, signal)
        signal = np.where((zscore < -0.5) & (zscore > -1), -1, signal)
        if contract_group.name == 'PEP': signal = -1. * signal
        return signal
    
    def pair_entry_rule(contract_group: ContractGroup,
                        i: int,
                        timestamps: np.ndarray,
                        indicators: SimpleNamespace,
                        signal: np.ndarray,
                        account: Account,
                        strategy_context: StrategyContextType) -> Sequence[Order]:
        timestamp = timestamps[i]
        assert(math.isclose(account.position(contract_group, timestamp), 0))
        signal_value = signal[i]
        risk_percent = 0.1

        orders = []
        
        symbol = contract_group.name
        contract = contract_group.get_contract(symbol)
        if contract is None: contract = Contract.create(symbol, contract_group=contract_group)
        
        curr_equity = account.equity(timestamp)
        order_qty = np.round(curr_equity * risk_percent / indicators.c[i] * np.sign(signal_value))
        print(f'order_qty: {order_qty} curr_equity: {curr_equity} timestamp: {timestamp}'
              f' risk_percent: {risk_percent} indicator: {indicators.c[i]} signal_value: {signal_value}')
        reason_code = ReasonCode.ENTER_LONG if order_qty > 0 else ReasonCode.ENTER_SHORT
        orders.append(MarketOrder(contract, timestamp, order_qty, reason_code=reason_code))
        return orders
            
    def pair_exit_rule(contract_group: ContractGroup,
                       i: int,
                       timestamps: np.ndarray,
                       indicators: SimpleNamespace,
                       signal: np.ndarray,
                       account: Account,
                       strategy_context: StrategyContextType) -> Sequence[Order]:
        timestamp = timestamps[i]
        curr_pos = account.position(contract_group, timestamp)
        assert(not math.isclose(curr_pos, 0))
        signal_value = signal[i]
        orders = []
        symbol = contract_group.name
        contract = contract_group.get_contract(symbol)
        if contract is None: contract = Contract.create(symbol, contract_group=contract_group)
        if (curr_pos > 0 and signal_value == -1) or (curr_pos < 0 and signal_value == 1):
            order_qty = -curr_pos
            reason_code = ReasonCode.EXIT_LONG if order_qty < 0 else ReasonCode.EXIT_SHORT
            orders.append(MarketOrder(contract, timestamp, order_qty, reason_code=reason_code))
        return orders

    def market_simulator(orders: Sequence[Order],
                         i: int,
                         timestamps: np.ndarray,
                         indicators: Dict[ContractGroup, SimpleNamespace],
                         signals: Dict[ContractGroup, SimpleNamespace],
                         strategy_context: StrategyContextType) -> Sequence[Trade]:
        trades = []

        timestamp = timestamps[i]

        for order in orders:
            trade_price = np.nan
            
            cgroup = order.contract.contract_group
            ind = indicators[cgroup]
            
            o, h, l = ind.o[i], ind.h[i], ind.l[i]  # noqa: E741  # l is ambiguous

            assert isinstance(order, MarketOrder), f'Unexpected order type: {order}'
            trade_price = 0.5 * (o + h) if order.qty > 0 else 0.5 * (o + l)

            if np.isnan(trade_price): continue

            trade = Trade(order.contract, order, timestamp, order.qty, trade_price, commission=0, fee=0)
            order.status = 'filled'
            print(f'trade: {trade}')

            trades.append(trade)

        return trades
    
    def get_price(contract: Contract, timestamps: np.ndarray, i: int, strategy_context: StrategyContextType) -> float:
        if contract.symbol == 'KO':
            return strategy_context.ko_price[i]
        elif contract.symbol == 'PEP':
            return strategy_context.pep_price[i]
        raise Exception(f'Unknown contract: {contract}')
        
    Contract.clear()
    ContractGroup.clear()
        
    ko_contract_group = ContractGroup.create('KO')
    pep_contract_group = ContractGroup.create('PEP')

    strategy_context = SimpleNamespace(ko_price=ko_prices.c.values, pep_price=pep_prices.c.values)

    strategy = Strategy(timestamps, [ko_contract_group, pep_contract_group], get_price, trade_lag=1, strategy_context=strategy_context)
    for tup in [(ko_contract_group, ko_prices), (pep_contract_group, pep_prices)]:
        for column in ['o', 'h', 'l', 'c']:
            strategy.add_indicator(column, tup[1][column], contract_groups=[tup[0]])
    strategy.add_indicator('ratio', ratio)
    strategy.add_indicator('zscore', zscore_indicator, depends_on=['ratio'])

    strategy.add_signal('pair_strategy_signal', pair_strategy_signal, depends_on_indicators=['zscore'])

    # ask pqstrat to call our trading rule when the signal has one of the values [-2, -1, 1, 2]
    strategy.add_rule('pair_entry_rule', pair_entry_rule, 
                      signal_name='pair_strategy_signal', sig_true_values=[-2, 2], position_filter='zero')
    
    strategy.add_rule('pair_exit_rule', pair_exit_rule, 
                      signal_name='pair_strategy_signal', sig_true_values=[-1, 1], position_filter='nonzero')
    
    strategy.add_market_sim(market_simulator)
    
    strategy.run_indicators()
    strategy.run_signals()
    strategy.run_rules()

    metrics = strategy.evaluate_returns(plot=False, display_summary=False, return_metrics=True)
    assert metrics is not None
    assert(round(metrics['gmean'], 6) == -0.062878)
    assert(round(metrics['sharpe'], 4) == -9.7079)  # -7.2709)
    assert(round(metrics['mdd_pct'], 6) == 0.002574)  # -0.002841)
    return strategy
    

if __name__ == "__main__":
    strategy = test_strategy()
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
