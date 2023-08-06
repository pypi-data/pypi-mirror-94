# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashDataTable(Component):
    """A DashDataTable component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- containerClassName (string; optional): Container className
- containerStyle (dict; optional): Container style
- currentPage (number; optional): Current page
- currentRowsPerPage (number; optional): Current rows per page
- currentClickedRow (boolean | number | string | dict | list; optional): Current clicked row
- currentDoubleClickedRow (boolean | number | string | dict | list; optional): Current double clicked row
- currentSelectedRows (list of boolean | number | string | dict | lists; optional): Current row selected
- currentSorting (dict; optional): Current sorting
- title (string; optional): Table title
- columns (list of dicts; required): Column definitions
- data (list of dicts; optional): Row data
- keyField (string; optional): Key field the id that uniquely identifies the row
- striped (boolean; optional): Stripe odd rows
- highlightOnHover (boolean; optional): Highlight rows on hover
- pointerOnHover (boolean; optional): Point icon on hover
- className (string; optional): Table className
- style (dict; optional): Style
- responsive (boolean; optional): Horizontally scrollable
- disabled (boolean; optional): Disable the table section
- overflowY (boolean; optional): if a table is responsive, items such as 
layovers/menus/dropdowns will be clipped 
on the last row(s)
- overflowYOffset (string; optional): Used with overflowY
- dense (boolean; optional): compact the rows
- noTableHead (boolean; optional): Hides the sort columns
- persistTableHead (boolean; optional): Show the table head event when progressPending is true
- direction (string; optional): Direction
- selectableRows (boolean; optional): Selectable rows
- selectableRowsVisibleOnly (boolean; optional): Select only visible rows
matters for pagination.
If this option is not set to
true it will select all 
rows specified in data also
those now shown
- selectableRowsHighlight (boolean; optional): Highlight selected rows
- selectableRowsNoSelectAll (boolean; optional): Show select all icon
- sortServer (boolean; optional): Disables internal sorting
- expandableRows (boolean; optional): Make rows expandable
- expandOnRowClicked (boolean; optional): Expand rows on click
- expandOnRowDoubleClicked (boolean; optional): Expand rows on double click
- expandableRowsHideExpander (boolean; optional): Hide expander button
- defaultSortField (string; optional): Default pre sorting
- defaultSortAsc (boolean; optional): Default pre sorting direction
- pagination (boolean; default True): Enable pagination
- paginationServer (boolean; optional): Use server side pagination
- paginationDefaultPage (number; optional): Start page
- paginationPerPage (number; optional): Rows per page
- paginationRowsPerPageOptions (list of numbers; optional): Row per page options
- paginationTotalRows (number; optional): Total rows when using serverside pagination
- noHeader (boolean; optional): No table header
- fixedHeader (boolean; optional): Fixed header
- fixedHeaderScrollHeight (string; optional): Fixed header scroll height"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, containerClassName=Component.UNDEFINED, containerStyle=Component.UNDEFINED, currentPage=Component.UNDEFINED, currentRowsPerPage=Component.UNDEFINED, currentClickedRow=Component.UNDEFINED, currentDoubleClickedRow=Component.UNDEFINED, currentSelectedRows=Component.UNDEFINED, currentSorting=Component.UNDEFINED, title=Component.UNDEFINED, columns=Component.REQUIRED, data=Component.UNDEFINED, keyField=Component.UNDEFINED, striped=Component.UNDEFINED, highlightOnHover=Component.UNDEFINED, pointerOnHover=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, responsive=Component.UNDEFINED, disabled=Component.UNDEFINED, overflowY=Component.UNDEFINED, overflowYOffset=Component.UNDEFINED, dense=Component.UNDEFINED, noTableHead=Component.UNDEFINED, persistTableHead=Component.UNDEFINED, direction=Component.UNDEFINED, selectableRows=Component.UNDEFINED, selectableRowsVisibleOnly=Component.UNDEFINED, selectableRowsHighlight=Component.UNDEFINED, selectableRowsNoSelectAll=Component.UNDEFINED, sortServer=Component.UNDEFINED, expandableRows=Component.UNDEFINED, expandOnRowClicked=Component.UNDEFINED, expandOnRowDoubleClicked=Component.UNDEFINED, expandableRowsHideExpander=Component.UNDEFINED, defaultSortField=Component.UNDEFINED, defaultSortAsc=Component.UNDEFINED, pagination=Component.UNDEFINED, paginationServer=Component.UNDEFINED, paginationDefaultPage=Component.UNDEFINED, paginationPerPage=Component.UNDEFINED, paginationRowsPerPageOptions=Component.UNDEFINED, paginationTotalRows=Component.UNDEFINED, noHeader=Component.UNDEFINED, fixedHeader=Component.UNDEFINED, fixedHeaderScrollHeight=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'containerClassName', 'containerStyle', 'currentPage', 'currentRowsPerPage', 'currentClickedRow', 'currentDoubleClickedRow', 'currentSelectedRows', 'currentSorting', 'title', 'columns', 'data', 'keyField', 'striped', 'highlightOnHover', 'pointerOnHover', 'className', 'style', 'responsive', 'disabled', 'overflowY', 'overflowYOffset', 'dense', 'noTableHead', 'persistTableHead', 'direction', 'selectableRows', 'selectableRowsVisibleOnly', 'selectableRowsHighlight', 'selectableRowsNoSelectAll', 'sortServer', 'expandableRows', 'expandOnRowClicked', 'expandOnRowDoubleClicked', 'expandableRowsHideExpander', 'defaultSortField', 'defaultSortAsc', 'pagination', 'paginationServer', 'paginationDefaultPage', 'paginationPerPage', 'paginationRowsPerPageOptions', 'paginationTotalRows', 'noHeader', 'fixedHeader', 'fixedHeaderScrollHeight']
        self._type = 'DashDataTable'
        self._namespace = 'dash_data_table'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'containerClassName', 'containerStyle', 'currentPage', 'currentRowsPerPage', 'currentClickedRow', 'currentDoubleClickedRow', 'currentSelectedRows', 'currentSorting', 'title', 'columns', 'data', 'keyField', 'striped', 'highlightOnHover', 'pointerOnHover', 'className', 'style', 'responsive', 'disabled', 'overflowY', 'overflowYOffset', 'dense', 'noTableHead', 'persistTableHead', 'direction', 'selectableRows', 'selectableRowsVisibleOnly', 'selectableRowsHighlight', 'selectableRowsNoSelectAll', 'sortServer', 'expandableRows', 'expandOnRowClicked', 'expandOnRowDoubleClicked', 'expandableRowsHideExpander', 'defaultSortField', 'defaultSortAsc', 'pagination', 'paginationServer', 'paginationDefaultPage', 'paginationPerPage', 'paginationRowsPerPageOptions', 'paginationTotalRows', 'noHeader', 'fixedHeader', 'fixedHeaderScrollHeight']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['columns']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashDataTable, self).__init__(**args)
