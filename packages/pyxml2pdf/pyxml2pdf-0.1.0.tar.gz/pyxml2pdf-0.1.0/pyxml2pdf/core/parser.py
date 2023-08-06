""":py:mod:`pyxml2pdf.core.parser` is the interface between xml input and table"""

__all__ = ["Parser"]

import warnings
from typing import List

from reportlab.platypus.flowables import KeepTogether  # type: ignore

from pyxml2pdf.core.events import Event
from pyxml2pdf.tables.builder import TableBuilder


class Parser:
    """XML parser to extract all interesting information from xml input

    :param elements: cells to populate the Parser
    """

    _elements: List[KeepTogether]
    _table_manager: TableBuilder

    def __init__(self, elements: List[KeepTogether]):
        self._elements = elements
        self._table_manager = TableBuilder()

    def collect_xml_data(self, events):
        """Traverse the parsed xml data and gather collected event data

        The collected xml data then is passed to the table_manager and all arranged
        data is return.

        :param List[Event] events: a list of the items from which the texts shall be
            extracted into a nicely formatted table
        :returns: list of all table rows containing the relevant
            event data
        :rtype: List[KeepTogether]
        """
        if events:
            for event in events:
                self._table_manager.distribute_event(Event(event))
            subtable_elements = self._table_manager.collect_subtables()
            self._elements.extend(
                [
                    KeepTogether(subtable_element)
                    for subtable_element in subtable_elements
                ]
            )
            return self._elements
        else:
            warnings.warn("There were no items to print.", RuntimeWarning)
