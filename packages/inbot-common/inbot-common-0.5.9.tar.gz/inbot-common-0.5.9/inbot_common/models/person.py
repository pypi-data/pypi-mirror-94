from typing import Optional, List

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema


@attr.s(auto_attribs=True, kw_only=True)
class PersonSummary:
    id: str = attr.ib()
    name: str = attr.ib()
    profile_url: str = attr.ib()
    headline: Optional[str] = None
    job_titles: List[str] = attr.ib(factory=list)
    company_names: List[str] = attr.ib(factory=list)
    company_urls: List[str] = attr.ib(factory=list)
    description: Optional[str] = None
    location: Optional[str] = None

class PersonSummarySchema(AttrsSchema):
    class Meta:
        target = PersonSummary
        register_as_scheme = True
