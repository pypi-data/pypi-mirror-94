from typing import Optional

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema


@attr.s(auto_attribs=True, kw_only=True)
class PostCommentSummary:
    person_name: str = attr.ib()
    post_comment_count: Optional[int] = None
    post_like_count: Optional[int] = None
    post_url: Optional[str] = []


class PostCommentSummarySchema(AttrsSchema):
    class Meta:
        target = PostCommentSummary
        register_as_scheme = True
