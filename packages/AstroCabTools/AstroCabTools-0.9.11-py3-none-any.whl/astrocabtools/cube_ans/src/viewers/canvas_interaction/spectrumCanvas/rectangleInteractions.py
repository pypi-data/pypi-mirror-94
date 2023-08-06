# This Copyright is paste from https://gist.github.com/t20100/e5a9ba1196101e618883
# /*##########################################################################
#
# Copyright (c) 2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
import numpy
import weakref

from pubsub import pub

import matplotlib.pyplot as _plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from .panOnClick import PanOnClick


class RectangleInteractions(PanOnClick):
    """Class providing pan & zoom interaction to a matplotlib Figure.
    Left button for pan and zoom on wheel.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(RectangleInteractions, self).__init__(figure, scale_factor=1.1)
        self._add_connection_rectangle('button_press_event', self._on_mouse_press)
        self._add_connection_rectangle('button_release_event', self._on_mouse_release)
        self._add_connection_rectangle('motion_notify_event', self._on_mouse_motion)

        self._pressed_button = None  # To store active button
        self._axes = None  # To store x and y axes concerned by interaction
        self._event = None  # To store reference event during interaction



    def update_current_rectangle(self, ax, curr_event, past_event):
        """Create the rectangle with the width stablished from initial click
        and current position of the mouse
        :param AXIS ax: axis where the rectangle is gonna be drawed or it's width modified
        :param EVENT curr_event: data from the current position of the mouse of the motion event
        :param EVENT past_event: data from the initial position where a click has been done
        """
        print(type(ax), type(curr_event), type(past_event))
        try:

            #If current click does not goes to the limit (which would cause to return None)
            if curr_event.xdata != None:
                #If rectangle creation goes from left to right
                if curr_event.xdata < past_event.xdata:

                    #If the rectangle has not been created
                    if not isinstance(self._rectangle_interactions, Rectangle):

                        self._rectangle_interactions = Rectangle([curr_event.xdata, ax.get_ylim()[0]*0.9 ],
                                            abs(past_event.xdata - curr_event.xdata), ax.get_ylim()[1]*1.1, color='blue', alpha = 0.3)

                        self._rectangleStats.direction = -1
                        ax.add_patch(self._rectangle_interactions)

                    #If it has been created and goes from left to right
                    elif isinstance(self._rectangle_interactions, Rectangle) and self._rectangleStats.direction == -1:
                        self._rectangle_interactions.set_x(curr_event.xdata)
                        self._rectangle_interactions.set_width(abs(past_event.xdata - curr_event.xdata))

                    #If it has been created but changed direction from right-left to left-right
                    elif self._rectangleStats.direction == 1:
                        self._rectangleStats.direction = -1
                        self._rectangle_interactions.set_x(curr_event.xdata)
                        self._rectangle_interactions.set_width(abs(past_event.xdata - curr_event.xdata))

                #If rectangle creation goes from right to left
                else:

                    if not isinstance(self._rectangle_interactions, Rectangle):
                        self._rectangle_interactions = Rectangle([past_event.xdata, ax.get_ylim()[0]*0.9],
                                            abs(past_event.xdata - curr_event.xdata), ax.get_ylim()[1]*1.1, color='blue', alpha = 0.3)

                        self._rectangleStats.direction = 1
                        ax.add_patch(self._rectangle_interactions)
                    elif isinstance(self._rectangle_interactions, Rectangle) and self._rectangleStats.direction == 1:
                        self._rectangle_interactions.set_x(past_event.xdata)
                        self._rectangle_interactions.set_width(abs(past_event.xdata - curr_event.xdata))
                    elif self._rectangleStats.direction == -1:
                        self._rectangleStats.direction = 1
                        self._rectangle_interactions.set_x(past_event.xdata)
                        self._rectangle_interactions.set_width(abs(past_event.xdata - curr_event.xdata))
        except Exception as e:
            pass

    def _rectangle(self, event):
        """Execute function based on the name of it"""
        if event.name == 'button_press_event':  # begin pan
            self._original_event = event
            self._event = event

        elif event.name == 'button_release_event':  # end pan
            self._event = None

        elif event.name == 'motion_notify_event':  # pan
            if self._event is None:
                return

            if event.x != self._event.x:
                for ax in self._axes[0]:
                    self.update_current_rectangle(ax, event, self._original_event)

            if event.x != self._event.x:
                self._draw()

            self._event = event

    def _on_mouse_press(self, event):
        """Set axes values based on point selected"""
        if self._pressed_button is not None:
            return  # Discard event if a button is already pressed

        x_axes = set()
        y_axes = set()
        for ax in self.figure.axes:
            #Simmilar to event.inaxis = axis
            if ax.contains(event)[0]:
                x_axes.add(ax)
                y_axes.add(ax)
                self._axes = x_axes, y_axes
                self._pressed_button = event.button
                if self._pressed_button == 1:  # pan
                    self._rectangle(event)

    def _on_mouse_release(self, event):
        if self._pressed_button == 1:  # pan
            self._rectangle(event)

        self._pressed_button = None

    def _on_mouse_motion(self, event):
        if self._pressed_button == 1:  # pan
            self._rectangle(event)
