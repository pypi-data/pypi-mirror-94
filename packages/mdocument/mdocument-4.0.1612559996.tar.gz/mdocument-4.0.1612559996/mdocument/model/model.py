import copy
import types
import typing

import bson
import pymongo

from mdocument import exceptions
from mdocument.model.field import Field, FieldRelated, FieldSynced, Synced
from mdocument.model.index import Index


class Model:
    """Document model. Should be JSON serializable.

    All class fields that are not a part of model but are needed
    for internals should be named with first underscore.

    Document model should be set in Document class with `Model` name.
    """

    _id = Field(bson.ObjectId)
    __primary_key__ = "_id"
    __relations__ = []
    __indexes__ = set()
    __document_cls__ = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if not issubclass(cls, Synced):
            for parent_field, value in cls._get_parent_fields().items():
                setattr(cls, parent_field, copy.deepcopy(value))
        for field_name, field in cls.__dict__.items():
            if not isinstance(field, (types.MethodType, classmethod)):
                if not field_name.startswith("_"):
                    if not isinstance(field, Field):
                        raise Exception(
                            f"Model field {field_name} should be Field type."
                        )
                if isinstance(field, Field):
                    field.connect_to_model(cls, field_name)
                    if field.is_related:
                        field.relation.register(field, field)
                    if field.unique:
                        cls.add_index(
                            Index(((field.name, pymongo.ASCENDING),), unique=True)
                        )

    @classmethod
    def _get_parent_fields(cls):
        fields = {}
        for parent in cls.__bases__:
            if issubclass(parent, Model):
                fields.update(parent._get_parent_fields())
                for field, field_type in parent.__dict__.items():
                    if isinstance(field_type, Field):
                        fields[field] = field_type
        return fields

    @classmethod
    def fields(cls) -> typing.Dict[str, "Field"]:
        fields = {}
        for field, field_type in cls.__dict__.items():
            if isinstance(field_type, Field):
                fields[field] = field_type
        return fields

    @classmethod
    def fields_dict(cls):
        result = {}
        for field, model_field in cls.fields().items():
            result[field] = model_field.to_dict()
        return result

    @classmethod
    def pop_optional_none(cls, query: dict):
        """Pops optional fields with None values."""

        for key, value in query.copy().items():
            field = getattr(cls, key)
            if field.optional and value is None:
                query.pop(key)
        return query

    @classmethod
    def validate(cls, document: typing.Union["MDocument", dict], pre_insert=False):
        """Validates that fields are present and have correct types."""

        from mdocument.document import MDocument

        if isinstance(document, MDocument):
            doc = document.__document__
        elif isinstance(document, dict):
            doc = document
        else:
            raise exceptions.WrongValueType(
                "Wrong value type provided for model validation."
            )

        if set(doc).difference(cls.fields()):
            raise exceptions.UnknownModelField(set(cls.fields()).difference(doc))
        for field_name, field in cls.fields().items():
            doc_field_value = doc.get(field_name)
            if doc_field_value is None and not field.optional:
                if field.is_primary and pre_insert:
                    continue
                raise exceptions.RequiredFieldMissing(field_name)
            elif doc_field_value is None and field.optional:
                continue
            elif doc.get(field_name):
                if not field.validate(doc_field_value):
                    raise exceptions.WrongValueType(field_name)
            getattr(cls, f"{field_name}_validate", lambda v: True)(doc_field_value)

    def __repr__(self):
        return f"{self.__document_cls__.__name__}Model({self.fields_dict()})"

    @classmethod
    def add_index(cls, index: Index):
        """Adds Index to model indexes."""

        return cls.__indexes__.add(index)

    @classmethod
    def add_relation(cls, relation: "Relation"):
        """Adds relation to global set of models relations."""

        Model.__relations__.append(relation)
