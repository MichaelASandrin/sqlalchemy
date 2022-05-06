from __future__ import annotations

import operator
from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

from ..sql import roles
from ..sql._typing import _HasClauseElement
from ..sql.elements import ColumnElement
from ..util.typing import Protocol
from ..util.typing import TypeGuard

if TYPE_CHECKING:
    from .attributes import AttributeImpl
    from .attributes import CollectionAttributeImpl
    from .attributes import HasCollectionAdapter
    from .attributes import QueryableAttribute
    from .base import PassiveFlag
    from .decl_api import registry as _registry_type
    from .descriptor_props import _CompositeClassProto
    from .interfaces import InspectionAttr
    from .interfaces import MapperProperty
    from .interfaces import UserDefinedOption
    from .mapper import Mapper
    from .relationships import Relationship
    from .state import InstanceState
    from .util import AliasedClass
    from .util import AliasedInsp
    from ..sql._typing import _CE
    from ..sql.base import ExecutableOption

_T = TypeVar("_T", bound=Any)


_T_co = TypeVar("_T_co", bound=Any, covariant=True)

# I would have preferred this were bound=object however it seems
# to not travel in all situations when defined in that way.
_O = TypeVar("_O", bound=Any)
"""The 'ORM mapped object' type.

"""

_OO = TypeVar("_OO", bound=object)
"""The 'ORM mapped object, that's definitely object' type.

"""


if TYPE_CHECKING:
    _RegistryType = _registry_type

_InternalEntityType = Union["Mapper[_T]", "AliasedInsp[_T]"]

_ExternalEntityType = Union[Type[_T], "AliasedClass[_T]"]

_EntityType = Union[
    Type[_T], "AliasedClass[_T]", "Mapper[_T]", "AliasedInsp[_T]"
]


_ClassDict = Mapping[str, Any]
_InstanceDict = Dict[str, Any]

_IdentityKeyType = Tuple[Type[_T], Tuple[Any, ...], Optional[Any]]

_ORMColumnExprArgument = Union[
    ColumnElement[_T],
    _HasClauseElement,
    roles.ExpressionElementRole[_T],
]


_ORMCOLEXPR = TypeVar("_ORMCOLEXPR", bound=ColumnElement[Any])


class _ORMAdapterProto(Protocol):
    """protocol for the :class:`.AliasedInsp._orm_adapt_element` method
    which is a synonym for :class:`.AliasedInsp._adapt_element`.


    """

    def __call__(self, obj: _CE, key: Optional[str] = None) -> _CE:
        ...


class _LoaderCallable(Protocol):
    def __call__(self, state: InstanceState[Any], passive: PassiveFlag) -> Any:
        ...


def is_user_defined_option(
    opt: ExecutableOption,
) -> TypeGuard[UserDefinedOption]:
    return not opt._is_core and opt._is_user_defined  # type: ignore


def is_composite_class(obj: Any) -> TypeGuard[_CompositeClassProto]:
    return hasattr(obj, "__composite_values__")


if TYPE_CHECKING:

    def insp_is_mapper_property(obj: Any) -> TypeGuard[MapperProperty[Any]]:
        ...

    def insp_is_mapper(obj: Any) -> TypeGuard[Mapper[Any]]:
        ...

    def insp_is_aliased_class(obj: Any) -> TypeGuard[AliasedInsp[Any]]:
        ...

    def insp_is_attribute(
        obj: InspectionAttr,
    ) -> TypeGuard[QueryableAttribute[Any]]:
        ...

    def attr_is_internal_proxy(
        obj: InspectionAttr,
    ) -> TypeGuard[QueryableAttribute[Any]]:
        ...

    def prop_is_relationship(
        prop: MapperProperty[Any],
    ) -> TypeGuard[Relationship[Any]]:
        ...

    def is_collection_impl(
        impl: AttributeImpl,
    ) -> TypeGuard[CollectionAttributeImpl]:
        ...

    def is_has_collection_adapter(
        impl: AttributeImpl,
    ) -> TypeGuard[HasCollectionAdapter]:
        ...

else:
    insp_is_mapper_property = operator.attrgetter("is_property")
    insp_is_mapper = operator.attrgetter("is_mapper")
    insp_is_aliased_class = operator.attrgetter("is_aliased_class")
    insp_is_attribute = operator.attrgetter("is_attribute")
    attr_is_internal_proxy = operator.attrgetter("_is_internal_proxy")
    is_collection_impl = operator.attrgetter("collection")
    prop_is_relationship = operator.attrgetter("_is_relationship")
    is_has_collection_adapter = operator.attrgetter(
        "_is_has_collection_adapter"
    )
