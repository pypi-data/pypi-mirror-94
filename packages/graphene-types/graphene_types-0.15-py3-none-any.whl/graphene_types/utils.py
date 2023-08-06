from typing import Any, TypeVar
from graphene import ObjectType


def patch_object_type() -> None:
    """
    Patches `graphene.ObjectType` to make it indexable at runtime. This is necessary for it be
    generic at typechecking time.
    """

    ObjectTypeMetaclass = type(ObjectType)

    C = TypeVar("C")

    def __getitem__(cls: C, _: Any) -> C:
        return cls

    ObjectTypeMetaclass.__getitem__ = __getitem__  # type: ignore
