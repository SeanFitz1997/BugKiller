from typing import Any, Dict, Optional

from arrow import Arrow
from pydantic.fields import ModelField
from pydantic.schema import field_schema

from bug_killer_utils.dates import try_parse_arrow


class ArrowType(Arrow):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Arrow:
        return try_parse_arrow(value)

    @classmethod
    def __modify_schema__(cls, schema: Dict[str, Any], field: Optional[ModelField]):
        """ Change the type of arrow to str when generating the schema """
        # Create copy of existing field,
        # change the data type to str, and then delete __modify_schema__ to prevent recursion
        field_copy = ModelField(
            name=field.name,
            type_=str,
            class_validators=field.class_validators,
            model_config=field.model_config,
            default=field.default,
            default_factory=field.default_factory,
            required=field.required,
            alias=field.alias,
            field_info=field.field_info
        )
        override_schema, _, _ = field_schema(field_copy, model_name_map={})

        schema.update(override_schema)
