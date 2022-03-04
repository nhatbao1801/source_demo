from rest_framework.request import Request

from models.document import Document
from main.serializers.document_serializer import DocumentSerializer, DocumentVersionSerializer


def h_push_document(request: Request, description: str, obj_str: str, obj_id: int) -> list:
    """
    Args:
        request (Request): The request
        description (str): description of the document
        obj_str (str): name of the model label
        obj_id (int): id of the model
    Returns:
        list: a list of strings representing the header columns

    Raises:
        ValueError: if obj_str not a string
        ValueError: if obj_id not a integer
        Exception: The ``Raised`` section is a list of all exceptions
            that are relevant to  the interface.
    """
    if not isinstance(obj_str, str):
        raise ValueError('obj must be a string')
    if not isinstance(obj_id, int):
        raise ValueError('obj_id must be an integer')

    document_ids = []
    if request.FILES.getlist('documents'):
        for doc in request.FILES.getlist('documents'):
            document_serializer = DocumentSerializer(
                data={
                    obj_str: obj_id,
                    'name': doc.name, 'doc_file': doc,
                    'description': description or 'hSpaces document',
                    'created_by': request.user.id
                })
            if document_serializer.is_valid():
                document_serializer.save()
                document_ids.append(document_serializer.data['id'])

                # push document version
                document_version_serializer = DocumentVersionSerializer(
                    data={
                        'document': Document.objects.get(id=document_serializer.data['id'])
                    }
                )
                if document_version_serializer.is_valid():
                    document_version_serializer.save()
            else:
                raise Exception('Error while saving document')
        return document_ids
    return document_ids
