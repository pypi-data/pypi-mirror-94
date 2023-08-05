from circle.resources.abstract import (
    CreateableAPIResource,
    RetrievableAPIResource
)


class Wire(CreateableAPIResource, RetrievableAPIResource):

    OBJECT_NAME = "banks.wires"
