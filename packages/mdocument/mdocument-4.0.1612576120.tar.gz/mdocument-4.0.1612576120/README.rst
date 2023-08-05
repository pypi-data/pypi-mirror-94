MDocument
=========

|pipeline status| |coverage report| |pypi link|

.. |pipeline status| image:: https://git.yurzs.dev/yurzs/mdocument/badges/master/pipeline.svg
   :target: https://git.yurzs.dev/yurzs/mdocument/-/commits/master

.. |coverage report| image:: https://git.yurzs.dev/yurzs/mdocument/badges/master/coverage.svg
   :target: https://git.yurzs.dev/yurzs/mdocument/-/commits/master

.. |pypi link| image:: https://badge.fury.io/py/mdocument.svg
   :target: https://pypi.org/project/mdocument

.. |code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |imports: isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
   :target: https://pycqa.github.io/isort

.. role:: strike
    :class: strike

MDocument is a simple ORM for MongoDB with addition of relations.

Usage
-----

There are two ways of using mdocument:
1. Specify database, colleciton and client in class.
2. Use modified mongo motor client.

Specifying document parameters in class
---------------------------------------

.. code-block:: python

    import asyncio

    import motor.motor_asyncio

    from mdocument import MDocument, relations, model

    client = motor.motor_asyncio.AsyncIOMotorClient()

    class Video(MDocument):
        __collection__ = "videos"
        __database__ = "mdocument"
        __client__ = client

        class Model(MDocument.Model):
            title = model.Field(str)
            views_count = model.Field(int)
            public_id = model.Field(str, unique=True)

    class Comment(MDocument):
        __collection__ = "comments"
        __database__ = "mdocument"
        __client__ = client

        class Model(MDocument.Model):
            text = model.Field(str)
            video = model.FieldSync(Video, relation=relations.RelationOneToMany, synced_fields=["_id", "title"])


    async def main():
        video = await Video.create({"title": "Test"})

        comment1 = await Comment.create(
            video=video._id,
            message="First!",
        )

        comment2 = await Comment.create(
            video=video._id,
            message="Second!"
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Now we can easily access our comments using our related documents

TODO: REWRITE DOCUMENTATION!
