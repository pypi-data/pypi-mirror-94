# Library Imports
import os
import sys
import math
import colorsys
from dataclasses import dataclass
import unittest
import doctest
import pandas as pd
import numpy as np
from IPython.core.display import display
from IPython.core.display import clear_output
from ipywidgets import widgets
import plotly
import plotly.callbacks
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from typing import List, Tuple, Callable, Any, Sequence, Dict, Optional
import traitlets
from pyqstrat.pq_utils import bootstrap_ci, np_bucket, get_child_logger

# Local Imports
ROOT_DIR = os.path.join(sys.path[0])
sys.path.insert(1, ROOT_DIR)

# Constants and Globals
_logger = get_child_logger(__name__)

DEFAULT_PLOTLY_COLORS = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                         'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                         'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                         'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                         'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

LineDataType = Tuple[str, 
                     pd.DataFrame, 
                     Dict[Any, pd.DataFrame]]
    
DimensionFilterType = Callable[[
    pd.DataFrame,
    str,
    List[Tuple[str, Any]]],
    np.ndarray]

DataFilterType = Callable[[
    pd.DataFrame,
    List[Tuple[str, Any]]],
    pd.DataFrame]

StatFuncType = Callable[[pd.DataFrame, str, str, str], List[LineDataType]]

DetailDisplayType = Callable[[
    widgets.Widget, 
    pd.DataFrame],
    None]


PlotFuncType = Callable[[str, str, List[LineDataType]], List[widgets.Widget]]

DataFrameTransformFuncType = Callable[[pd.DataFrame], pd.DataFrame]

SeriesTransformFuncType = Callable[[pd.Series], pd.Series]

DisplayFormFuncType = Callable[[Sequence[widgets.Widget]], None]

UpdateFormFuncType = Callable[[int], None]

CreateSelectionWidgetsFunctype = Callable[[Dict[str, str], Dict[str, str], UpdateFormFuncType], Dict[str, Any]]


def percentile_buckets(a: np.ndarray, n=10):
    return np_bucket(a, np.nanpercentile(a, np.arange(0, 100, int(round(100 / n)))))


def display_form(form_widgets: Sequence[widgets.Widget]) -> None:
    clear_output()
    box_layout = widgets.Layout(
        display='flex',
        flex_flow='column',
        align_items='stretch',
        border='solid',
        width='100%')
    box = widgets.Box(children=list(form_widgets), layout=box_layout)
    display(box)
    
    
class SimpleTransform:
    '''
    Initial transformation of data.  For example, you might add columns that are quantiles of other columns
    '''
    def __init__(self, transforms: List[Tuple[str, str, SeriesTransformFuncType]] = None) -> None:
        self.transforms = [] if transforms is None else transforms
        
    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        for (colname, new_colname, func) in self.transforms:
            data[new_colname] = func(data[colname])
        return data
    

def simple_dimension_filter(data: pd.DataFrame, dim_name: str, selected_values: List[Tuple[str, Any]]) -> np.ndarray:
    '''
    Produces a list to put into a dropdown for selecting a dimension value
    '''
    mask = np.full(len(data), True)
    for name, value in selected_values:
        if value == 'All': continue
        mask &= (data[name] == value)
    values = np.unique(data[mask][dim_name].values)  # will sort values before returning them
    return ['All'] + values.tolist()
    
    
def simple_data_filter(data: pd.DataFrame, selected_values: List[Tuple[str, Any]]) -> pd.DataFrame:
    '''
    Filters a dataframe based on the selected values
    '''
    mask = np.full(len(data), True)
    for name, value in selected_values:
        if value == 'All': continue
        mask &= (data[name] == value)
    return data[mask]
    
    
class MeanWithCI:
    '''
    Computes mean (or median) and optionally confidence intervals for plotting
    '''
    def __init__(self, mean_func: Callable[[np.ndarray], np.ndarray] = np.nanmean, ci_level: int = 0) -> None:  # type: ignore
        '''
        Args:
            mean: The function to compute ci for
            ci_level: Set to 0 for no confidence intervals, or the level you want.
                For example, set to 95 to compute a 95% confidence interval. Default 0
        '''
        self.mean_func = mean_func
        self.ci_level = ci_level
        
    def __call__(self, filtered_data: pd.DataFrame, xcol: str, ycol: str, zcol: str) -> List[LineDataType]:
        '''
        For each unique value of x and z, compute mean (and optionally ci) of y.
        Return:
            x, y data for plotting lines of the mean of y versus x for each z and the data used to compute the mean
        '''
        zvals = np.unique(filtered_data[zcol])
        cols = [col for col in filtered_data.columns if col not in [xcol, ycol, zcol]]
        df = filtered_data[[xcol, ycol, zcol] + cols]
        ret = []
        columns = [xcol, ycol] if not self.ci_level else [xcol, ycol, f'ci_d_{self.ci_level}', f'ci_u_{self.ci_level}']
        for zvalue in zvals:
            df = filtered_data[filtered_data[zcol] == zvalue]
            plt_data: List[Any] = []
            for x, yseries in df.groupby(xcol)[ycol]:
                y = yseries.values
                mean = self.mean_func(y)
                if self.ci_level:
                    ci_up, ci_down = bootstrap_ci(y, ci_level=self.ci_level / 100)
                    plt_data.append((x, mean, ci_down, ci_up))
                else:
                    plt_data.append((x, mean))
            line = pd.DataFrame.from_records(plt_data, columns=columns)
            ret.append((zvalue, line, df))
        return ret
    
    
class SimpleDetailTable:
    '''
    Displays a pandas DataFrame under a plot that contains the data used to compute a statistic of y for each x, y pair
    '''
    
    def __init__(self, 
                 colnames: Optional[List[str]] = None, 
                 float_format: str = '{:.4g}', 
                 min_rows: int = 100, 
                 copy_to_clipboard: bool = True) -> None:
        '''
        Args:
            colnames: List of column names to display. If None we display all columns. Default None
            float_format: Format for each floating point column. Default {:.4g}
            min_rows: Do not truncate the display of the table before this many rows. Default 100
            copy_to_clipboard: If set, we copy the dataframe to the clipboard. On linux, you must install xclip for this to work
       '''
        self.colnames = colnames
        self.float_format = float_format
        self.min_rows = min_rows
        self.copy_to_clipboard = True
        
    def __call__(self, detail_widget: widgets.Widget, data: pd.DataFrame) -> None:
        '''
        Args:
            detail_widget: The widget to display the data in
            data: The dataframe to display
        '''
        if self.float_format:
            orig_float_format = pd.options.display.float_format
            pd.options.display.float_format = (self.float_format).format
        
        if self.min_rows:
            orig_min_rows = pd.options.display.min_rows
            pd.options.display.min_rows = self.min_rows
            
        with detail_widget:
            clear_output()
            if self.colnames: data = data[self.colnames]
            data = data.reset_index(drop=True)
            display(data)
            if self.copy_to_clipboard: data.to_clipboard(index=False)
                
        if self.float_format: pd.options.display.float_format = orig_float_format
        if self.min_rows: pd.options.display.min_rows = orig_min_rows
            
            
def create_selection_dropdowns(dims: Dict[str, str], labels: Dict[str, str], update_form_func: UpdateFormFuncType) -> Dict[str, Any]:
    '''
    Create a list of selection widgets
    '''
    selection_widgets: Dict[str, widgets.Widget] = {}
    for name in dims.keys():
        label = labels[name] if name in labels else name
        widget = widgets.Dropdown(description=label, style={'description_width': 'initial'})
        selection_widgets[name] = widget
        
    for widget in selection_widgets.values():
        widget.observe(lambda x: on_widgets_updated(x, update_form_func, selection_widgets), names='value')

    return selection_widgets


def on_widgets_updated(change: traitlets.utils.bunch.Bunch, update_form_func, selection_widgets: Dict[str, widgets.Widget]) -> None:
    '''
    Callback called by plotly when widgets are updated by the user.
    '''
    owner = change['owner']
    widgets = list(selection_widgets.values())
    owner_idx = widgets.index(owner)
    update_form_func(owner_idx)
            
            
@dataclass
class LineConfig:
    color: Optional[str] = None
    thickness: float = math.nan
    secondary_y: bool = False
    marker_mode: str = 'lines+markers'
    show_detail: bool = True
        
        
def _plotly_color_to_rgb(plotly_color: str) -> Tuple[int, int, int]:
    '''
    Convert plotly color which is a string into r, g, b values
    >>> assert _plotly_color_to_rgb('rgb(31, 119, 180)') == (31, 119, 180)
    '''
    plotly_color = plotly_color.replace('rgb(', '').replace(')', '')
    s = plotly_color.split(',')
    r, g, b = int(s[0]), int(s[1]), int(s[2])
    return r, g, b

        
def _lighten_color(r: int, g: int, b: int) -> Tuple[int, int, int]:
    '''
    Lighten color so we can show confidence intervals in a lighter shade than the line itself
    We convert to hls and increase lightness and decrease saturation
    >>> assert _lighten_color(31, 119, 180) == (102, 168, 214)
    '''
    hls = colorsys.rgb_to_hls(r, g, b)
    light_hls = (hls[0], hls[1] * 1.5, hls[2] * 0.5)
    rgb = colorsys.hls_to_rgb(*light_hls)
    rgb = (int(round(rgb[0])), int(round(rgb[1])), int(round(rgb[2])))
    return rgb
    
        
class LineGraphWithDetailDisplay:
    '''
    Draws line graphs and also includes a detail pane.
    When you click on a point on the line graph, the detail pane shows the data used to compute that point.
    '''
    
    def __init__(self, 
                 display_detail_func: DetailDisplayType = SimpleDetailTable(), 
                 line_configs: Dict[str, LineConfig] = {}, 
                 title: str = None, 
                 hovertemplate: str = None) -> None:
        '''
        Args:
            display_detail_func: A function that displays the data on the detail pane. Default SimpleDetailTable
            line_configs: Configuration of each line. The key in this dict is the zvalue for that line.  Default {}
            title: Title of the graph. Default None
            hovertemplate: What to display when we hover over a point on the graph.  See plotly hovertemplate
        '''
        self.display_detail_func = display_detail_func
        self.line_configs = line_configs
        self.title = title
        self.hovertemplate = hovertemplate
        self.default_line_config = LineConfig()
        self.detail_data: Dict[Any, pd.DataFrame] = {}
        self.xcol = ''
        self.zvalues: Dict[int, Any] = {}  # trace index by zvalue
 
    def __call__(self, xaxis_title: str, yaxis_title: str, line_data: List[LineDataType]) -> List[widgets.Widget]:
        '''
        Draw the plot and also set it up so if you click on a point, we display the data used to compute that point.
        Args:
            line_data: The zvalue, plot data, and detail data for each line to draw. The plot data must have 
                x as the first column and y as the second column
         Return:
            A list of widgets to draw.  In this case, a figure widget and a output widget which contains the detail display
        '''
        if not len(line_data): return []
        self.detail_data.clear()
        secondary_y = any([lc.secondary_y for lc in self.line_configs.values()])
        
        fig_widget = go.FigureWidget(make_subplots(specs=[[{"secondary_y": secondary_y}]]))
        detail_widget = widgets.Output()
        
        trace_num = 0

        for line_num, (zvalue, line_df, _detail_data) in enumerate(line_data):
            x = line_df.iloc[:, 0].values
            self.xcol = line_df.columns[0]
            y = line_df.iloc[:, 1].values
            self.detail_data[zvalue] = _detail_data
            line_config = self.line_configs[zvalue] if zvalue in self.line_configs else self.default_line_config
            marker_mode = line_config.marker_mode
            color = line_config.color if line_config.color else DEFAULT_PLOTLY_COLORS[line_num]
            
            hovertemplate = self.hovertemplate
            customdata = None
            
            if hovertemplate is None:
                unique, counts = np.unique(_detail_data[self.xcol].values, return_counts=True)
                customdata = counts[np.searchsorted(unique, x)]
                hovertemplate = 'N: %{customdata}'  # number of entries used to compute each x
                hovertemplate += f' Series: {zvalue} {xaxis_title}: ' + '%{x:.4g} ' + f'{yaxis_title}: ' + '%{y:.4g}'
                
            trace = go.Scatter(
                x=x,
                y=y,
                customdata=customdata,
                mode=marker_mode,
                name=str(zvalue),
                line=dict(color=color),
                hovertemplate=hovertemplate              
            )
           
            self.zvalues[trace_num] = zvalue
 
            fig_widget.add_trace(trace, secondary_y=line_config.secondary_y)
            if line_config.show_detail:
                fig_widget.data[trace_num].on_click(self._on_graph_click, append=True)
            trace_num += 1

            if len(line_df.columns) > 2:  # x, y, ci up and ci down 
                fill_color = _plotly_color_to_rgb(color)
                fill_color = _lighten_color(*fill_color)
                # we set transparency to 0.5 so we can see lines under the ci fill
                fill_color_str = f'rgba({fill_color[0]},{fill_color[1]},{fill_color[2]},0.5)'
                ci_down = line_df.iloc[:, 2].values
                ci_up = line_df.iloc[:, 3].values
                ci_trace = go.Scatter(
                    x=np.concatenate([x, x[::-1]]),  # x, then x reversed
                    y=np.concatenate([ci_up, ci_down[::-1]]),  # upper, then lower reversed
                    fill='toself',
                    fillcolor=fill_color_str,
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip",
                    showlegend=False)
            
                fig_widget.add_trace(ci_trace, secondary_y=line_config.secondary_y)
                trace_num += 1
            
        fig_widget.update_layout(title=self.title, xaxis_title=xaxis_title)
        fig_widget.update_layout(yaxis_title=yaxis_title)
        if secondary_y:
            fig_widget.update_yaxes(title_text=yaxis_title, secondary_y=True)
            
        self.fig_widget = fig_widget
        self.detail_widget = detail_widget
        self.line_data = line_data
                        
        return [self.fig_widget, self.detail_widget]
    
    def _on_graph_click(self, 
                        trace: go.Trace, 
                        points: plotly.callbacks.Points, 
                        selector: plotly.callbacks.InputDeviceState) -> None:
        '''
        Callback called by plotly when you click on a point on the graph.
        When you click on a point, we display the dataframe with the data we used to compute that point.
        '''
        if not len(points.xs): return
        trace_idx = points.trace_index
        zvalue = self.zvalues[trace_idx]
        _detail_data = self.detail_data[zvalue]
        _detail_data = _detail_data[_detail_data[self.xcol].values == points.xs[0]]
        self.display_detail_func(self.detail_widget, _detail_data)


class InteractivePlot:
    '''
    Creates a multidimensional interactive plot off a dataframe.
    '''
    def __init__(self,
                 data: pd.DataFrame,
                 labels: Dict[str, str] = None,
                 transform_func: DataFrameTransformFuncType = SimpleTransform(),
                 create_selection_widgets_func: CreateSelectionWidgetsFunctype = create_selection_dropdowns,
                 dim_filter_func: DimensionFilterType = simple_dimension_filter,
                 data_filter_func: DataFilterType = simple_data_filter,
                 stat_func: StatFuncType = MeanWithCI(),
                 plot_func: PlotFuncType = LineGraphWithDetailDisplay(),
                 display_form_func: DisplayFormFuncType = display_form) -> None:
        '''
        Args:
            data: The pandas dataframe to use for plotting
            labels: A dict where column names from the dataframe are mapped to user friendly labels. For any column names
                not found as keys in this dict, we use the column name as the label. Default None
            dim_filter_func: A function that generates the values of a dimension based on other dimensions. For example, if 
                the user chooses "Put Option" in a put/call dropdown, the valid strikes could change in a Strike 
                dropdown that follows. Default simple_dimension_filter
            data_filter_func: A function that filters the data to plot. For example, if the user chooses "Put Option" in a put/call dropdown,
                we could filter the dataframe to only include put options. Default simple_data_filter
            stat_func: Once we have filtered the data, we may need to plot some statistics, such as mean and confidence intervals.
                In this function, we compute these statistics. Default MeanWithCI()
            plot_func: A function that plots the data.  This could also display detail data used to compute the statistics associated
                with each data point.
            display_form_func: A function that displays the form given a list of plotly widgets (including the graph widget)
        '''
        self.data = transform_func(data)
        self.create_selection_widgets_func = create_selection_widgets_func
        if labels is None: labels = {}
        self.labels = labels
        self.dim_filter_func = dim_filter_func
        self.data_filter_func = data_filter_func
        self.stat_func = stat_func
        self.plot_func = plot_func
        self.display_form_func = display_form_func
        self.selection_widgets: Dict[str, Any] = {}
        
    def create_pivot(self, xcol: str, ycol: str, zcol: str, dimensions: Dict[str, Any]) -> None:
        '''
        Create the initial pivot
        Args:
            xcol: Column name to use as the x axis in the DataFrame
            ycol: Column name to use as the y axis in the DataFrame
            zcol: Column name to use for z-values. Each zvalue can be used for a different trace within this plot. For example, a column
                called "option_type" could contain the values "American", "European", "Bermudan" and we could plot the data for each type
                in a separate trace
            dimensions: The column names used for filter dimensions. For example, we may want to filter by days to expiration and put/call
                The key the column name and the value is the initial value for that column. For example, in a 
                dropdown for Put/Call we may want "Put" to be the initial value set in the dropdown.  Set to None if you 
                don't care what initial value is chosen.
        '''
        self.xlabel = xcol if xcol not in self.labels else self.labels[xcol]
        self.ylabel = ycol if ycol not in self.labels else self.labels[ycol]
        self.zcol = zcol
        self.xcol = xcol
        self.ycol = ycol
        self.selection_widgets = self.create_selection_widgets_func(dimensions, self.labels, self.update)
        self.update()
        
    def update(self, owner_idx: int = -1) -> None:
        '''
        Redraw the form using the values of all widgets above and including the one with index owner_idx.
        If owner_idx is -1, we redraw everything.
        '''
        select_conditions = [(name, widget.value) for name, widget in self.selection_widgets.items()]
        if owner_idx == -1:
            dim_select_conditions = []
        else:
            dim_select_conditions = select_conditions[:owner_idx + 1]  # for selecting lower widget options, use value of widgets above 
        
        for name in list(self.selection_widgets.keys())[owner_idx + 1:]:
            widget = self.selection_widgets[name]
            widget_options = self.dim_filter_func(self.data, name, dim_select_conditions)
            _logger.debug(f'setting values: {widget_options} on widget: {name}')
            widget.options = self.dim_filter_func(self.data, name, dim_select_conditions)
            
        if owner_idx == -1: return
                         
        filtered_data = self.data_filter_func(self.data, select_conditions)
        lines = self.stat_func(filtered_data, self.xcol, self.ycol, self.zcol)
        plot_widgets = self.plot_func(self.xlabel, self.ylabel, lines)
        self.display_form_func(list(self.selection_widgets.values()) + plot_widgets)

        
# unit tests
class TestInteractivePlot(unittest.TestCase):
    def test_interactive_plot(self):
        np.random.seed(0)
        size = 1000
        
        dte = np.random.randint(5, 10, size)
        put_call = np.random.choice(['put', 'call'], size)
        year = np.random.choice([2018, 2019, 2020, 2021], size)
        delta = np.random.uniform(0, 0.5, size)
        delta = np.where(put_call == 'call', delta, -delta)
        premium = np.abs(delta * 10) * dte + np.random.normal(size=size) * dte / 10
        data = pd.DataFrame({'dte': dte, 'put_call': put_call, 'year': year, 'delta': delta, 'premium': premium})
        
        labels = {'premium': 'Premium $', 'year': 'Year', 'dte': 'Days to Expiry', 'delta_rnd': 'Delta'}
        secy_line_config = LineConfig(secondary_y=True)
        
        ip = InteractivePlot(data, 
                             labels, 
                             transform_func=self.transform,
                             stat_func=MeanWithCI(ci_level=95),
                             plot_func=LineGraphWithDetailDisplay(line_configs={'put': secy_line_config}))
        
        ip.create_pivot('delta_rnd', 'premium', 'put_call', dimensions={'year': 2018, 'dte': None})
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        data['delta_rnd'] = percentile_buckets(np.abs(data.delta), 10)
        return data
    
      
if __name__ == '__main__':
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print('done')
