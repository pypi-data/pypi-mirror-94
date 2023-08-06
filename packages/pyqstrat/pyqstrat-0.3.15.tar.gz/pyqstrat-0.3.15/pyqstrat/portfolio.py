import pandas as pd
import numpy as np
from functools import reduce
from pyqstrat.evaluator import compute_return_metrics, display_return_metrics, plot_return_metrics
from pyqstrat.strategy import Strategy
from pyqstrat.pq_utils import str2date

from typing import Sequence, MutableMapping, Mapping, Tuple, Optional


class Portfolio:
    '''A portfolio contains one or more strategies that run concurrently so you can test running strategies that are uncorrelated together.'''
    def __init__(self, name: str = 'main') -> None:
        '''Args:
            name: String used for displaying this portfolio
        '''
        self.name = name
        self.strategies: MutableMapping[str, Strategy] = {}
        
    def add_strategy(self, name: str, strategy: Strategy) -> None:
        '''
        Args:
            name: Name of the strategy
            strategy: Strategy instance
        '''
        self.strategies[name] = strategy
        strategy.name = name
        
    def run_indicators(self, strategy_names: Sequence[str] = None) -> None:
        '''Compute indicators for the strategies specified
        
        Args:
            strategy_names: By default this is set to None and we use all strategies.
        '''
        if strategy_names is None: strategy_names = list(self.strategies.keys())
        if len(strategy_names) == 0: raise Exception('a portfolio must have at least one strategy')
        for name in strategy_names: self.strategies[name].run_indicators()
                
    def run_signals(self, strategy_names: Sequence[str] = None) -> None:
        '''Compute signals for the strategies specified.  Must be called after run_indicators
        
        Args:
            strategy_names: By default this is set to None and we use all strategies.
        '''
        if strategy_names is None: strategy_names = list(self.strategies.keys())
        if len(strategy_names) == 0: raise Exception('a portfolio must have at least one strategy')
        for name in strategy_names: self.strategies[name].run_signals()
            
    def _generate_order_iterations(self, 
                                   strategies: Sequence[Strategy], 
                                   start_date: Optional[np.datetime64], 
                                   end_date: Optional[np.datetime64]) -> Tuple[np.ndarray, Sequence[Tuple[Strategy, np.ndarray]]]:
        '''
        >>> class Strategy:
        ...    def __init__(self, num): 
        ...        self.timestamps = [
        ...            np.array(['2018-01-01', '2018-01-02', '2018-01-03'], dtype='M8[D]'),
        ...            np.array(['2018-01-02', '2018-01-03', '2018-01-04'], dtype='M8[D]')][num]
        ...        self.num = num
        ...    def _generate_order_iterations(self, start_date, end_date):
        ...        pass
        ...    def __repr__(self):
        ...        return f'{self.num}'
        >>> all_timestamps, orders_iter = Portfolio._generate_order_iterations(None, [Strategy(0), Strategy(1)], None, None)
        >>> assert(all(all_timestamps == np.array(['2018-01-01', '2018-01-02', '2018-01-03','2018-01-04'], dtype = 'M8[D]')))
        >>> assert(all(orders_iter[0][1] == np.array([0, 1, 2, 3])))
        >>> assert(all(orders_iter[1][1] == np.array([0, 0, 1, 2])))
        '''
        if strategies is None: strategies = self.strategies.values
            
        timestamps_list = [strategy.timestamps for strategy in strategies]
        
        all_timestamps = np.array(reduce(np.union1d, timestamps_list))
        
        if start_date is not None:
            all_timestamps = all_timestamps[(all_timestamps >= start_date)]
        if end_date is not None:
            all_timestamps = all_timestamps[(all_timestamps <= end_date)]
        
        iterations = []
        
        for strategy in strategies:
            indices = np.searchsorted(strategy.timestamps, all_timestamps)
            iterations.append((strategy, indices))
            strategy._generate_order_iterations(start_date=start_date, end_date=end_date)
            
        return all_timestamps, iterations
                
    def run_rules(self, strategy_names: Sequence[str] = None, start_date: np.datetime64 = None, end_date: np.datetime64 = None) -> None:
        '''Run rules for the strategies specified.  Must be called after run_indicators and run_signals.  
          See run function for argument descriptions
        '''
        start_date, end_date = str2date(start_date), str2date(end_date)
        if strategy_names is None: strategy_names = list(self.strategies.keys())
        if len(strategy_names) == 0: raise Exception('a portfolio must have at least one strategy')

        strategies = [self.strategies[key] for key in strategy_names]
        
        min_date = min([strategy.timestamps[0] for strategy in strategies])
        if start_date: min_date = max(min_date, start_date)
        max_date = max([strategy.timestamps[-1] for strategy in strategies])
        if end_date: max_date = min(max_date, end_date)
            
        all_timestamps, iterations = self._generate_order_iterations(strategies, start_date, end_date)
        
        for i, timestamp in enumerate(all_timestamps):
            for (strategy, indices) in iterations:
                # index into strategy timestamps
                idx = indices[i]
                if idx != len(strategy.timestamps) and strategy.timestamps[idx] == timestamp:
                    strategy._run_iteration(idx)
                    
        # Make sure we calc to the end for each strategy
        for strategy in strategies:
            strategy.account.calc(strategy.timestamps[-1])
                
    def run(self, strategy_names: Sequence[str] = None, start_date: np.datetime64 = None, end_date: np.datetime64 = None) -> None:
        '''
        Run indicators, signals and rules.
        
        Args:
            strategy_names: A list of strategy names.  By default this is set to None and we use all strategies.
            start_date: Run rules starting from this date.  
              Sometimes we have a few strategies in a portfolio that need different lead times before they are ready to trade
              so you can set this so they are all ready by this date.  Default None
            end_date: Don't run rules after this date.  Default None
         '''
        start_date, end_date = str2date(start_date), str2date(end_date)
        self.run_indicators()
        self.run_signals()
        self.run_rules(strategy_names, start_date, end_date)
        
    def df_returns(self, sampling_frequency: str = 'D', strategy_names: Sequence[str] = None) -> pd.DataFrame:
        '''
        Return dataframe containing equity and returns with a date index.  Equity and returns are combined from all strategies passed in.
        
        Args:
            sampling_frequency: Date frequency for rows.  Default 'D' for daily so we will have one row per day
            strategy_names: By default this is set to None and we use all strategies.
        '''
        if strategy_names is None: strategy_names = list(self.strategies.keys())
        if len(strategy_names) == 0: raise Exception('portfolio must have at least one strategy')
        equity_list = []
        for name in strategy_names:
            equity = self.strategies[name].df_returns(sampling_frequency=sampling_frequency)[['timestamp', 'equity']]
            equity.columns = ['timestamp', name]
            equity = equity.set_index('timestamp')
            equity_list.append(equity)
        df = pd.concat(equity_list, axis=1)
        df['equity'] = df.sum(axis=1)
        df['ret'] = df.equity.pct_change()
        return df.reset_index()
        
    def evaluate_returns(self, 
                         sampling_frequency: str = 'D', 
                         strategy_names: Sequence[str] = None, 
                         plot: bool = True, 
                         float_precision: int = 4) -> Mapping:
        '''Returns a dictionary of common return metrics.
        
        Args:
            sampling_frequency: Date frequency.  Default 'D' for daily so we downsample to daily returns before computing metrics
            strategy_names: By default this is set to None and we use all strategies.
            plot: If set to True, display plots of equity, drawdowns and returns.  Default False
            float_precision: Number of significant figures to show in returns.  Default 4
        '''
        returns = self.df_returns(sampling_frequency, strategy_names)
        ev = compute_return_metrics(returns.timestamp.values, returns.ret.values, returns.equity.values[0])
        display_return_metrics(ev.metrics(), float_precision=float_precision)
        if plot: plot_return_metrics(ev.metrics())
        return ev.metrics()
    
    def plot(self, 
             sampling_frequency: str = 'D', 
             strategy_names: Sequence[str] = None) -> None:
        '''Display plots of equity, drawdowns and returns
        
        Args:
            sampling_frequency: Date frequency.  Default 'D' for daily so we downsample to daily returns before computing metrics
            strategy_names: A list of strategy names.  By default this is set to None and we use all strategies.
        '''
        returns = self.df_returns(sampling_frequency, strategy_names)
        timestamps = returns.timestamp.values
        ev = compute_return_metrics(timestamps, returns.ret.values, returns.equity.values[0])
        plot_return_metrics(ev.metrics())
        
    def __repr__(self) -> str:
        return f'{self.name} {self.strategies.keys()}'
    

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
