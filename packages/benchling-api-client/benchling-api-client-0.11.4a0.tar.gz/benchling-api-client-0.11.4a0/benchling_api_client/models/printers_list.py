from typing import Any, Dict, List

import attr

from ..models.printer import Printer


@attr.s(auto_attribs=True)
class PrintersList:
    """  """

    label_printers: List[Printer]

    def to_dict(self) -> Dict[str, Any]:
        label_printers = []
        for label_printers_item_data in self.label_printers:
            label_printers_item = label_printers_item_data.to_dict()

            label_printers.append(label_printers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labelPrinters": label_printers,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "PrintersList":
        d = src_dict.copy()
        label_printers = []
        _label_printers = d.pop("labelPrinters")
        for label_printers_item_data in _label_printers:
            label_printers_item = Printer.from_dict(label_printers_item_data)

            label_printers.append(label_printers_item)

        printers_list = PrintersList(
            label_printers=label_printers,
        )

        return printers_list
