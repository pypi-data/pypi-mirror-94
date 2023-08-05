import typing

from mdocument import exceptions


class Synced:
    """Placeholder for identifying synced fields and models."""

    @classmethod
    def cut_data(cls, document):
        """Cuts document to only needed fields or single field value."""

        result = {
            key: value for key, value in document.items() if key in cls.Model.fields()
        }
        cls.Model.validate(result)
        return result


class Field:
    """Basic field."""

    SENSITIVE_PLACEHOLDER = "***hidden***"

    def __init__(
        self,
        field_type: typing.Type,
        default: typing.Any = None,
        optional: bool = False,
        sensitive: bool = False,
        relation: typing.Type["Relation"] = None,
        unique: bool = False,
    ):
        self.type = field_type
        self.default = default
        self.optional = optional
        self.sensitive = sensitive
        self.relation = relation
        self.unique = unique
        self.model = None
        self.name = None

        if isinstance(field_type, Field):
            raise exceptions.WrongModelFieldType()

    @property
    def is_related(self):
        from mdocument.document import MDocument

        return isinstance(self.type, Field) or issubclass(self.type, MDocument)

    @property
    def is_primary(self):
        if self.model is not None:
            return self.model.__primary_key__ == self.name
        return False

    def to_dict(self):
        return {
            "type": self.type,
            "default": self.default,
            "optional": self.optional,
            "sensitive": self.sensitive,
            "relation": self.relation,
        }

    def __repr__(self):
        return f"Field({self.to_dict()}) "

    def validate(self, value):
        """Validates that provided value matches field type."""

        return isinstance(value, self.type)

    def connect_to_model(self, model: typing.Type["Model"], name: str):
        """Saves field model relation."""

        self.model = model
        self.name = name


class FieldSynced(Field):
    """Field where its value is a copy of a specified document. Made for performance."""

    type: type

    def __init__(
        self,
        document_cls: typing.Type["MDocument"],
        optional: bool = False,
        relation: typing.Type["Relation"] = None,
        unique: bool = False,
        sync_fields: typing.List[str] = None,
    ):
        super().__init__(
            None,
            optional=optional,
            relation=relation,
            unique=unique,
        )
        self.type = type(
            f"SyncFields{document_cls.__name__}",
            (document_cls, Synced),
            {
                "Model": type(
                    f"SyncModel{document_cls.Model.__name__}",
                    (document_cls.Model, Synced),
                    {
                        field_name: field
                        for field_name, field in document_cls.Model.fields().items()
                        if field_name in sync_fields
                    },
                ),
                "__parent_cls__": document_cls,
            },
        )
        self.sync_fields = sync_fields

    def validate(self, value):
        """Validates that value matches Document model."""

        self.type.Model.validate(value)
        return True


class FieldRelated(Field):
    """Field where its value is a primary key value of a specific document."""

    type: typing.Type["MDocument"]

    def __init__(
        self,
        document_cls: typing.Type["MDocument"],
        optional: bool = False,
        relation: typing.Type["Relation"] = None,
        unique: bool = False,
    ):
        super().__init__(
            None,
            optional=optional,
            relation=relation,
            unique=unique,
        )
        self.type = getattr(document_cls.Model, document_cls.Model.__primary_key__)

    def validate(self, value):
        """Validates that value matches related documents primary key type."""

        return isinstance(value, self.type.type)
