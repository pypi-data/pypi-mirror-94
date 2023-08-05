import typing

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from mdocument.document import MDocument

__all__ = ["MDocumentAsyncIOClient"]


class WrongQueryType(BaseException):
    pass


class MDocumentAsyncIOClient(AsyncIOMotorClient):
    def __getattr__(self, item):
        result = super().__getattr__(item)
        result.__class__ = MDocumentAsyncIOMotorDatabase
        return result


class MDocumentAsyncIOMotorDatabase(AsyncIOMotorDatabase):
    def __getattr__(self, item):
        result = super().__getattr__(item)
        result.__class__ = MDocumentAsyncIOMotorCollection
        return result


class MDocumentAsyncIOMotorCollection(AsyncIOMotorCollection):
    async def find_one(self, document_query: "MDocument", *args, **kwargs):
        """Finds one document and returns it with provided type."""

        if not isinstance(document_query, MDocument):
            raise WrongQueryType()

        result = await super().find_one(document_query.__document__, **kwargs)
        if result is not None:
            return document_query.__class__(result)
        return None

    async def find(self, document_query: "MDocument", *args, **kwargs):
        """Finds multiple documents and returns them with provided type."""

        if not isinstance(document_query, MDocument):
            raise WrongQueryType()

        result = []
        async for document in super().find(
            document_query.__document__, *args, **kwargs
        ):
            result.append(document_query.__class__(document))
        return result

    async def insert_one(self, document, *args, **kwargs):
        """Inserts one document to database."""

        if not isinstance(document, MDocument):
            raise WrongQueryType()

        return await super().insert_one(document.__document__, *args, **kwargs)

    async def insert_many(self, documents: typing.List[MDocument], *args, **kwargs):
        """Inserts multiple documents to database."""

        for document in documents:
            if not isinstance(document, MDocument):
                raise WrongQueryType()

        return await super().insert_many(
            [document.__document__ for document in documents], *args, **kwargs
        )

    async def update_one(self, document: MDocument, *args, **kwargs):
        """Updates one document in database. Also updates related documents."""

        await super().update_one(document.__document__, *args, **kwargs)
        await document._update_related(client=self)

    async def update_many(self, documents: typing.List[MDocument], *args, **kwargs):
        """Updates multiple documents in database. Also updates related documents."""

        result = await super().update_many(
            [document.__document__ for document in documents], *args, **kwargs
        )
        for document in documents:
            await document._update_related(client=self)
        return result

    async def delete_one(self, document: MDocument, *args, **kwargs):
        """Deletes one document in database. Also updates related documents."""

        result = await super().delete_one(document.__document__, *args, **kwargs)
        await document._delete_related(client=self)
        return result

    async def delete_many(self, documents: typing.List[MDocument], *args, **kwargs):
        """Deletes multiple documents in database. Also updates related documents."""

        result = await super().delete_many(
            [document.__document__ for document in documents], *args, **kwargs
        )
        for document in documents:
            await document._delete_related(client=self)
        return result
