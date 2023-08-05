from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status


class RestAPIJobChangePushHandler:
    """
    JobChangePush handler for the REST API.
    """

    def __init__(self, app_label, supported_models):
        """
        Constructor.

        The supported models are provided as a list.

        :param app_label: the app label where we must search for the models
        :type app_label: str
        :param supported_models: the supported models
        :type supported_models: list(str)
        """
        self.app_label = app_label
        self.supported_models = supported_models
        self.pre_save_hooks = {}

    def add_pre_save_hooks(self, model_name, hook_function):
        """
        Add a pre-save hook function for the provided model name.

        More than one hook function is supported.
        """
        if not callable(hook_function):
            raise ValueError(f'{hook_function} is not callable')

        self.pre_save_hooks.setdefault(model_name, []).append(hook_function)

    def process(self, data):
        """
        Process the request.data.

        rest_framework.response.Response with json content and a HTTP status code is returned :
            - "success" can be False or True

        :param data: the request.data
        :rtype rest_framework.response.Response
        """
        try:
            object_uuid = data['uuid']
            model_name = data['model']
            type = data['type']
        except KeyError:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        if model_name not in self.supported_models:
            return Response({'success': True}, status=status.HTTP_202_ACCEPTED)

        try:
            model = apps.get_model(self.app_label, model_name)
        except LookupError:
            return Response({'success': False}, status=status.HTTP_417_EXPECTATION_FAILED)

        obj = None

        try:
            obj = model.objects.get(uuid=object_uuid)
        except ObjectDoesNotExist:
            pass

        if type == 'DELETE':
            if obj:
                return Response({'success': False}, status=status.HTTP_304_NOT_MODIFIED)
            else:
                return Response({'success': True}, status=status.HTTP_304_NOT_MODIFIED)
        elif type == 'CREATE_OR_UPDATE':
            new_object = obj is None
            if new_object:
                obj = model(uuid=object_uuid)

            for field in data['data']:
                setattr(obj, field, data['data'][field])

            if model_name in self.pre_save_hooks:
                for hook in self.pre_save_hooks[model_name]:
                    obj = hook(new_object=new_object, obj=obj, data=data['data'])

            try:
                obj.save()
                return Response({'success': True}, status=status.HTTP_200_OK)
            except:
                return Response({'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
