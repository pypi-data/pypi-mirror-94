from typing import Any, Dict, Union

import attr

from ..models.sample_group_samples import SampleGroupSamples
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class SampleGroup:
    """ Represents a sample group that is an input to a request. A sample group is a set of samples upon which work in the request should be done. """

    id: str
    samples: Union[Unset, SampleGroupSamples] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        samples: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.samples, Unset):
            samples = self.samples.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if samples is not UNSET:
            field_dict["samples"] = samples

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SampleGroup":
        d = src_dict.copy()
        id = d.pop("id")

        samples: Union[Unset, SampleGroupSamples] = UNSET
        _samples = d.pop("samples", UNSET)
        if not isinstance(_samples, Unset):
            samples = SampleGroupSamples.from_dict(_samples)

        sample_group = SampleGroup(
            id=id,
            samples=samples,
        )

        return sample_group
