from typing import Optional

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema

@attr.s(auto_attribs=True, kw_only=True)
class Integration:
  integration_id: Optional[str] = None
  unique_id: Optional[str] = None
  name: Optional[str] = None
  owner_name: Optional[str] = None
  picture: Optional[str] = None
  region: Optional[str] = None
  connection_url: Optional[str] = None
  port: Optional[int] = None
  user: Optional[str] = None
  password: Optional[str] = None
  deleted: Optional[bool] = None

class IntegrationSchema(AttrsSchema):
  class Meta:
    target = Integration
    register_as_scheme = True