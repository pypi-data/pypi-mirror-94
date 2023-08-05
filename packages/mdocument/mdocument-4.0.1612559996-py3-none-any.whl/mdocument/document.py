import copy

import pymongo.errors
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from mdocument import exceptions, model


class MetaDocument(type):
    __client__: AsyncIOMotorClient
    __collection__: str
    __database__: str

    @property
    def collection(cls) -> AsyncIOMotorCollection:
        return cls.database[cls.__collection__]

    @property
    def client(cls) -> AsyncIOMotorClient:
        return cls.__client__

    @property
    def database(cls) -> AsyncIOMotorDatabase:
        return cls.client[cls.__database__]

    def _with_patched_client(cls, client):
        cls_copy = copy.deepcopy(cls)
        cls_copy.__client__ = client
        return cls_copy


class MDocument(metaclass=MetaDocument):
    __document__: dict
    __original_document__: dict

    NotFoundError = exceptions.NotFoundError
    DuplicateError = exceptions.DuplicateError

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.__class__.collection

    @property
    def client(self) -> AsyncIOMotorClient:
        return self.__class__.client

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self.__class__.database

    def __init__(self, doc):
        self.__document__ = doc
        self.__original_document__ = copy.deepcopy(doc)
        for key, value in doc.items():
            setattr(self, key, value)

    def __getitem__(self, item):
        return self.__document__[item]

    def __setitem__(self, key, value):
        self.__document__[key] = value

    def __getattr__(self, item):
        try:
            model_field = getattr(self.Model, item, None)
            if model_field:
                if model_field.sensitive:
                    return model.Field.SENSITIVE_PLACEHOLDER
                else:
                    return self.__document__[item]
            else:
                if isinstance(self.__class__.__dict__.get(item), property):
                    return super().__getattribute__(item)
                raise AttributeError(item)
        except KeyError:
            raise AttributeError(item) from None

    def __setattr__(self, key, value):
        if key.startswith("_") and key not in self.Model.fields():
            return super().__setattr__(key, value)
        if key in self.__class__.Model.fields():
            field_type = getattr(self.__class__.Model, key).type
            if isinstance(field_type, model.Field):
                field_type = field_type.type
            if issubclass(field_type, MDocument) and isinstance(value, dict):
                field_type.Model.validate(value)
                self.__document__[key] = value
                super().__setattr__(key, field_type(value))
            elif not isinstance(value, field_type):
                raise exceptions.WrongValueType(key)
            else:
                self.__document__[key] = value
        else:
            raise exceptions.UnknownModelField(key)

    def __eq__(self, other):
        if isinstance(other, MDocument):
            return self.__document__ == other.__document__
        elif isinstance(other, dict):
            return self.__document__ == other
        return False

    def __repr__(self):

        formatted = {
            field_name: field_value
            if not getattr(self.Model, field_name).sensitive
            else model.Field.SENSITIVE_PLACEHOLDER
            for field_name, field_value in self.__document__.items()
        }
        return f"{self.__class__.__name__}({formatted})"

    def __init_subclass__(cls, **kwargs):
        cls.Model.__document_cls__ = cls
        if getattr(cls, "__client__", None):
            if cls.collection and cls.database:
                for index in cls.Model.__indexes__:
                    cls.client.delegate[cls.__database__][
                        cls.__collection__
                    ].create_index(index.keys, **index.kwargs)

    @classmethod
    async def create(cls, *args, **kwargs):
        """Creates new document."""

        query = args[0]
        cls.Model.validate(query, pre_insert=True)
        cls.Model.pop_optional_none(query)
        try:
            await cls.collection.insert_one(*args, **kwargs)
        except pymongo.errors.DuplicateKeyError:
            raise cls.DuplicateError()
        return cls(query)

    @classmethod
    async def one(cls, query: dict, required: bool = True):
        """Finds one document."""

        result = await cls.collection.find_one(query)
        if result is None and required:
            raise cls.NotFoundError()
        elif not result:
            return
        else:
            return cls(result)

    @classmethod
    async def many(cls, query: dict, required: bool = False, session=None):
        """Finds multiple documents."""

        documents = []
        async for doc in cls.collection.find(query, session=session):
            documents.append(cls(doc))
        if not documents and required:
            raise cls.NotFoundError()
        return documents

    async def _update_related(self, client=None, session=None):
        """Updates related documents."""

        for relation in model.Model.__relations__:
            if issubclass(relation.parent_document_cls, self.__class__) and issubclass(
                relation.parent_document_cls, model.field.Synced
            ):
                await relation.update(
                    client or self.__class__.__client__, self, session=session
                )
            if isinstance(self, relation.parent_model):
                await relation.update(
                    client or self.__class__.__client__, self, session=session
                )

    async def _delete_related(self, client=None, session=None):
        """Deletes related documents."""

        for relation in model.Model.__relations__:
            if issubclass(relation.parent_document_cls, self.__class__) and issubclass(
                relation.parent_document_cls, model.field.Synced
            ):
                await relation.delete(
                    client or self.__class__.__client__, self, session=session
                )
            if isinstance(self, relation.parent_model):
                await relation.delete(
                    client or self.__class__.__client__, self, session=session
                )

    async def save(self, session=None):
        """Saves current document to database."""

        updated_doc = copy.deepcopy(self.__document__)
        updated_doc.pop(self.__class__.Model.__primary_key__)
        await self.collection.update_one(
            {
                self.Model.__primary_key__: self.__original_document__[
                    self.Model.__primary_key__
                ],
            },
            {"$set": updated_doc},
            session=session,
        )
        await self._update_related(session=session)

    @classmethod
    async def find(cls, query, **kwargs):
        """Finds multiple document. Returns async generator."""

        async for doc in cls.collection.find(query, **kwargs):
            yield cls(doc)

    async def delete(self, session=None):
        """Deletes document."""

        await self.collection.delete_one(
            {self.Model.__primary_key__: self[self.Model.__primary_key__]},
            session=session,
        )
        await self._delete_related(session=session)
        await self._update_related(session=session)

    def items(self):
        return self.__document__.items()
