#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Vidar Tonaas Fauske.
# Distributed under the terms of the Modified BSD License.

"""
Time picker widget
"""

from ipywidgets import ValueWidget, register
from traitlets import Unicode, Bool, Union, Enum, CFloat, validate, TraitError
from ipywidgets.widgets.widget_description import DescriptionWidget

from .base_widget import BaseWidget
from .trait_types import Time, time_serialization


@register
class TimePicker(BaseWidget, DescriptionWidget, ValueWidget):
    """
    Display a widget for picking times.

    Parameters
    ----------

    value: datetime.time
        The current value of the widget.

    disabled: bool
        Whether to disable user changes.

    min: datetime.time
        The lower allowed time bound

    max: datetime.time
        The upper allowed time bound

    step: float | 'any'
        The time step to use for the picker, in seconds, or "any"

    Examples
    --------

    >>> import datetime
    >>> import ipydatetime
    >>> time_pick = ipydatetime.TimePicker()
    >>> time_pick.value = datetime.time(12, 34, 3)
    """

    value = Time(None, allow_none=True).tag(sync=True, **time_serialization)
    disabled = Bool(False, help="Enable or disable user changes.").tag(sync=True)

    min = Time(None, allow_none=True).tag(sync=True, **time_serialization)
    max = Time(None, allow_none=True).tag(sync=True, **time_serialization)
    step = Union(
        (CFloat(60), Enum("any")),
        help='The time step to use for the picker, in seconds, or "any".',
    ).tag(sync=True)

    @validate("value")
    def _validate_value(self, proposal):
        """Cap and floor value"""
        value = proposal["value"]
        if self.min and self.min > value:
            value = max(value, self.min)
        if self.max and self.max < value:
            value = min(value, self.max)
        return value

    @validate("min")
    def _validate_min(self, proposal):
        """Enforce min <= value <= max"""
        min = proposal["value"]
        if self.max and min > self.max:
            raise TraitError("Setting min > max")
        if self.value and min > self.value:
            self.value = min
        return min

    @validate("max")
    def _validate_max(self, proposal):
        """Enforce min <= value <= max"""
        max = proposal["value"]
        if self.min and max < self.min:
            raise TraitError("setting max < min")
        if self.value and max < self.value:
            self.value = max
        return max

    _view_name = Unicode("TimeView").tag(sync=True)
    _model_name = Unicode("TimeModel").tag(sync=True)
