from rest_framework.request import Request

from hStartup.serializers.hstartup_document_serializer import HStartupDocumentSerializer


def push_document_hstartup_tool(request: Request, description=None, obj_str=None, obj_id=None) -> list:
    if not isinstance(obj_str, str):
        raise ValueError('obj must be a string')
    if not isinstance(obj_id, int):
        raise ValueError('obj_id must be an integer')

    document_ids = []
    if request.FILES.getlist('documents'):
        for doc in request.FILES.getlist('documents'):
            document_serializer = HStartupDocumentSerializer(
                data={
                    obj_str: obj_id,
                    'name': doc.name, 'url': doc,
                    'description': description or 'Hstartup document',
                    'created_by': request.user.id
                })
            if document_serializer.is_valid():
                document_serializer.save()
                document_ids.append(document_serializer.data['id'])
            else:
                raise Exception('Error while saving document')
        return document_ids
    return document_ids
