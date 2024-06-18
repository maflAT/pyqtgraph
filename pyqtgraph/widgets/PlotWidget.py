"""
PlotWidget.py -  Convenience class--GraphicsView widget displaying a single PlotItem
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more information.
"""
from typing import TYPE_CHECKING
from ..graphicsItems.PlotItem import PlotItem
from ..Qt import QtCore, QtWidgets
from .GraphicsView import GraphicsView

__all__ = ['PlotWidget']
class PlotWidget(GraphicsView):
    
    # signals wrapped from PlotItem / ViewBox
    sigRangeChanged = QtCore.Signal(object, object)
    sigTransformChanged = QtCore.Signal(object)
    
    """
    :class:`GraphicsView <pyqtgraph.GraphicsView>` widget with a single 
    :class:`PlotItem <pyqtgraph.PlotItem>` inside.
    
    The following methods are wrapped directly from PlotItem: 
    :func:`addItem <pyqtgraph.PlotItem.addItem>`, 
    :func:`removeItem <pyqtgraph.PlotItem.removeItem>`, 
    :func:`clear <pyqtgraph.PlotItem.clear>`, 
    :func:`setAxisItems <pyqtgraph.PlotItem.setAxisItems>`,
    :func:`setXRange <pyqtgraph.ViewBox.setXRange>`,
    :func:`setYRange <pyqtgraph.ViewBox.setYRange>`,
    :func:`setRange <pyqtgraph.ViewBox.setRange>`,
    :func:`autoRange <pyqtgraph.ViewBox.autoRange>`,
    :func:`setXLink <pyqtgraph.ViewBox.setXLink>`,
    :func:`setYLink <pyqtgraph.ViewBox.setYLink>`,
    :func:`viewRect <pyqtgraph.ViewBox.viewRect>`,
    :func:`setMouseEnabled <pyqtgraph.ViewBox.setMouseEnabled>`,
    :func:`enableAutoRange <pyqtgraph.ViewBox.enableAutoRange>`,
    :func:`disableAutoRange <pyqtgraph.ViewBox.disableAutoRange>`,
    :func:`setAspectLocked <pyqtgraph.ViewBox.setAspectLocked>`,
    :func:`setLimits <pyqtgraph.ViewBox.setLimits>`,
    :func:`register <pyqtgraph.ViewBox.register>`,
    :func:`unregister <pyqtgraph.ViewBox.unregister>`
    
    
    For all 
    other methods, use :func:`getPlotItem <pyqtgraph.PlotWidget.getPlotItem>`.
    """
    def __init__(self, parent=None, background='default', plotItem=None, **kargs):
        ## start by instantiating the plotItem attribute in order to avoid recursive 
        ## calls of PlotWidget.__getattr__ - which access self.plotItem!
        self.plotItem = None
        """When initializing PlotWidget, *parent* and *background* are passed to 
        :func:`GraphicsWidget.__init__() <pyqtgraph.GraphicsWidget.__init__>`
        and all others are passed
        to :func:`PlotItem.__init__() <pyqtgraph.PlotItem.__init__>`."""
        GraphicsView.__init__(self, parent, background=background)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.enableMouse(False)
        if plotItem is None:
            self.plotItem = PlotItem(**kargs)
        else:
            self.plotItem = plotItem
        self.setCentralItem(self.plotItem)
        ## Explicitly wrap methods from plotItem
        ## NOTE: If you change this list, update the documentation above as well.
        for m in ['addItem', 'removeItem', 'autoRange', 'clear', 'setAxisItems', 'setXRange', 
                  'setYRange', 'setRange', 'setAspectLocked', 'setMouseEnabled', 
                  'setXLink', 'setYLink', 'enableAutoRange', 'disableAutoRange', 
                  'setLimits', 'register', 'unregister', 'viewRect']:
            setattr(self, m, getattr(self.plotItem, m))
        #QtCore.QObject.connect(self.plotItem, QtCore.SIGNAL('viewChanged'), self.viewChanged)
        self.plotItem.sigRangeChanged.connect(self.viewRangeChanged)

    # -------------------------------------------------------------------------------- #
    #                           Wrapped Methods from PlotItem                          #
    # -------------------------------------------------------------------------------- #
    if TYPE_CHECKING:
        def addItem(self, item, *args, **kargs):
            """
            Add a graphics item to the view box. 
            If the item has plot data (:class:`PlotDataItem <pyqtgraph.PlotDataItem>` , 
            :class:`~pyqtgraph.PlotCurveItem` , :class:`~pyqtgraph.ScatterPlotItem` ), 
            it may be included in analysis performed by the PlotItem.
            """
        def removeItem(self, item):
            """
            Remove an item from the PlotItem's :class:`~pyqtgraph.ViewBox`.
            """
        def clear(self):
            """
            Remove all items from the PlotItem's :class:`~pyqtgraph.ViewBox`.
            """
        def setAxisItems(self, axisItems=None):
            """
            Place axis items as given by `axisItems`. Initializes non-existing axis items.
            
            ==============  ==========================================================================================
            **Arguments:**
            *axisItems*     Optional dictionary instructing the PlotItem to use pre-constructed items
                            for its axes. The dict keys must be axis names ('left', 'bottom', 'right', 'top')
                            and the values must be instances of AxisItem (or at least compatible with AxisItem).
            ==============  ==========================================================================================
            """

    # ------------------------- Wrapped Methods from ViewBox ------------------------- #
        def autoRange(self, padding=None, items=None, item=None):
            """
            Set the range of the view box to make all children visible.
            Note that this is not the same as enableAutoRange, which causes the view to
            automatically auto-range whenever its contents are changed.

            ==============  =============================================================
            **Arguments:**
            padding         The fraction of the total data range to add on to the final
                            visible range. By default, this value is set between the 
                            default padding and 0.1 depending on the size of the ViewBox.
            items           If specified, this is a list of items to consider when
                            determining the visible range.
            ==============  =============================================================
            """
        def setXRange(self, min, max, padding=None, update=True):
            """
            Set the visible X range of the view to [*min*, *max*].
            The *padding* argument causes the range to be set larger by the fraction specified.
            (by default, this value is between the default padding and 0.1 depending on the size of the ViewBox)
            """
        def setYRange(self, min, max, padding=None, update=True):
            """
            Set the visible Y range of the view to [*min*, *max*].
            The *padding* argument causes the range to be set larger by the fraction specified.
            (by default, this value is between the default padding and 0.1 depending on the size of the ViewBox)
            """
        def setRange(self, rect=None, xRange=None, yRange=None, padding=None, update=True, disableAutoRange=True):
            """
            Set the visible range of the ViewBox.
            Must specify at least one of *rect*, *xRange*, or *yRange*.

            ================== =====================================================================
            **Arguments:**
            *rect*             (QRectF) The full range that should be visible in the view box.
            *xRange*           (min,max) The range that should be visible along the x-axis.
            *yRange*           (min,max) The range that should be visible along the y-axis.
            *padding*          (float) Expand the view by a fraction of the requested range.
                            By default, this value is set between the default padding value
                            and 0.1 depending on the size of the ViewBox.
            *update*           (bool) If True, update the range of the ViewBox immediately.
                            Otherwise, the update is deferred until before the next render.
            *disableAutoRange* (bool) If True, auto-ranging is diabled. Otherwise, it is left
                            unchanged.
            ================== =====================================================================

            """
        def setAspectLocked(self, lock=True, ratio=1):
            """
            If the aspect ratio is locked, view scaling must always preserve the aspect ratio.
            By default, the ratio is set to 1; x and y both have the same scaling.
            This ratio can be overridden (xScale/yScale), or use None to lock in the current ratio.
            """
        def setMouseEnabled(self, x=None, y=None):
            """
            Set whether each axis is enabled for mouse interaction. *x*, *y* arguments must be True or False.
            This allows the user to pan/scale one axis of the view while leaving the other axis unchanged.
            """
        def setXLink(self, view):
            """Link this view's X axis to another view. (see LinkView)"""
        def setYLink(self, view):
            """Link this view's Y axis to another view. (see LinkView)"""
        def enableAutoRange(self, axis=None, enable=True, x=None, y=None):
            """
            Enable (or disable) auto-range for *axis*, which may be ViewBox.XAxis, ViewBox.YAxis, or ViewBox.XYAxes for both
            (if *axis* is omitted, both axes will be changed).
            When enabled, the axis will automatically rescale when items are added/removed or change their shape.
            The argument *enable* may optionally be a float (0.0-1.0) which indicates the fraction of the data that should
            be visible (this only works with items implementing a dataBounds method, such as PlotDataItem).
            """
        def disableAutoRange(self, axis=None):
            """Disables auto-range. (See enableAutoRange)"""
        def setLimits(self, **kwds):
            """
            Set limits that constrain the possible view ranges.

            **Panning limits**. The following arguments define the region within the
            viewbox coordinate system that may be accessed by panning the view.

            =========== ============================================================
            xMin        Minimum allowed x-axis value
            xMax        Maximum allowed x-axis value
            yMin        Minimum allowed y-axis value
            yMax        Maximum allowed y-axis value
            =========== ============================================================

            **Scaling limits**. These arguments prevent the view being zoomed in or
            out too far.

            =========== ============================================================
            minXRange   Minimum allowed left-to-right span across the view.
            maxXRange   Maximum allowed left-to-right span across the view.
            minYRange   Minimum allowed top-to-bottom span across the view.
            maxYRange   Maximum allowed top-to-bottom span across the view.
            =========== ============================================================

            Added in version 0.9.9
            """
        def register(self, name):
            """
            Add this ViewBox to the registered list of views.

            This allows users to manually link the axes of any other ViewBox to
            this one. The specified *name* will appear in the drop-down lists for
            axis linking in the context menus of all other views.

            The same can be accomplished by initializing the ViewBox with the *name* attribute.
            """
        def unregister(self):
            """
            Remove this ViewBox from the list of linkable views. (see :func:`register() <pyqtgraph.ViewBox.register>`)
            """
        def viewRect(self):
            """Return a QRectF bounding the region visible within the ViewBox"""

            
    # -------------------------------------------------------------------------------- #
    def close(self):
        self.plotItem.close()
        self.plotItem = None
        #self.scene().clear()
        #self.mPlotItem.close()
        self.setParent(None)
        super(PlotWidget, self).close()

    def __getattr__(self, attr):  ## implicitly wrap methods from plotItem
        if hasattr(self.plotItem, attr):
            m = getattr(self.plotItem, attr)
            if hasattr(m, '__call__'):
                return m
        raise AttributeError(attr)
    
    if TYPE_CHECKING:
        def setLabel(self, axis, text=None, units=None, unitPrefix=None, **args):
            """
            Sets the label for an axis. Basic HTML formatting is allowed.
            
            ==============  =================================================================
            **Arguments:**
            axis            must be one of 'left', 'bottom', 'right', or 'top'
            text            text to display along the axis. HTML allowed.
            units           units to display after the title. If units are given,
                            then an SI prefix will be automatically appended
                            and the axis values will be scaled accordingly.
                            (ie, use 'V' instead of 'mV'; 'm' will be added automatically)
            ==============  =================================================================
            """
    
    def viewRangeChanged(self, view, range):
        #self.emit(QtCore.SIGNAL('viewChanged'), *args)
        self.sigRangeChanged.emit(self, range)

    def widgetGroupInterface(self):
        return (None, PlotWidget.saveState, PlotWidget.restoreState)

    def saveState(self):
        return self.plotItem.saveState()
        
    def restoreState(self, state):
        return self.plotItem.restoreState(state)
        
    def getPlotItem(self):
        """Return the PlotItem contained within."""
        return self.plotItem
