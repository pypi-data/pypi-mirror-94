class DocumentException(BaseException):
    def __init__(self, message):
        self.message = message


class DocumentDoesntExist(DocumentException):
    def __init__(self):
        self.message = "Document not found."


class DuplicateError(DocumentException):
    def __init__(self):
        self.message = "Duplicate error. Unique constrait failed."


class NotFoundError(DocumentException):
    def __init__(self):
        self.message = "Specified document doesn't exist."


class UnknownModelField(DocumentException):
    def __init__(self, field_name):
        self.message = f"Unknown fields {field_name} are present in document."


class RequiredFieldMissing(DocumentException):
    def __init__(self, field_name):
        self.message = f"Field {field_name} required by model is missing."


class WrongValueType(DocumentException):
    def __init__(self, field_name):
        self.message = f"Value provided for fields {field_name} value have wrong type."


class RelationNotSet(DocumentException):
    def __init__(self):
        self.message = "Relation type is missing for related field."


class PrimaryKeyNotInSyncedFields(DocumentException):
    def __init__(self):
        self.message = (
            "For sync to work primary key should be present in synced fields."
        )


class FieldIsNotJsonEncodable(DocumentException):
    def __init__(self):
        self.message = "Field is not json encodable please change your model."


class WrongModelFieldType(DocumentException):
    def __init__(self, extra_message=None):
        self.message = (
            f"Unknown field type provided for relation. {extra_message or ''}"
        )
