import requests
import json

from django.utils import timezone
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import JobChange


def execute_jobchange(job_change):
    """
    Execute a JobChange.

    We dynamically retrieve the model and the object based on the PK UUID. These operations may fail if the model has
    been renamed / deleted or if the object no longer exists. In this case, we try to find the cause as precisely as
    possible and we change the status to FATAL_ERROR.

    If all goes well, we will then push the modification to the remote application to its API. The structure of the
    JSON is :

        {
            'id' : <the ID of the JobChange, for debugging purpose>,
            'type' <the type of change : CREATE_OR_UPDATE or DELETE>,
            'model' <the model of the change : 'Member' or 'Unit' or ...>
            'uuid' : <the object's UUID PK changing>',
            'data': {
                '<field 1>': <value 1>,
                '<field 2>': <value 2>,
                ...
            }
        }

    The field "inactive" is not the one of the Model. We use the field "applications_active" to detect if the object
    must be active or inactive in the remote application and we set the "inactive" field according to that.

    The fields "applications_active", "password" of 'Member' model, 'applications_access' of 'Member' model and 'user'
    of 'Member' model are never sent.

    If the remote application correctly processes the request, an HTTP 200 code is returned with the following JSON
    content :

        {
            'success': 'true'
        }

    If the request was successful (network, authentication, etc ...) but the remote application refuses to update the
    object, an HTTP 200 code is returned with the following JSON content :

        {
            'success': 'false',
            'error': <error description>
        }

    :param job_change: the job change
    :type job_change: JobChange
    :return True if success, else False
    :rtype bool
    """
    if job_change.status not in (JobChange.STATUS.WAITING,
                                 JobChange.STATUS.WAITING_AFTER_ERROR,
                                 JobChange.STATUS.FATAL_ERROR):
        raise RuntimeError(f'JobChange #{job_change.pk} doesn\'t have the correct status')

    object_fields = None

    error = None

    try:
        try:
            model = apps.get_model(app_label='centralhub', model_name=job_change.target_model)

            target_obj = None
            try:
                target_obj = model.objects.get(pk=job_change.target_uuid)
            except ObjectDoesNotExist:
                error = 'UUID_NOT_FOUND'
            try:
                object_fields = json.loads(serializers.serialize('json', [target_obj]))[0]['fields']

                # We remove the "inactive" flag and the "applications_active" for the client (see juste after)
                field_inactive = object_fields.pop('inactive', None)
                object_fields.pop('applications_active', None)

                # For the member, we remove the user FK, the password hash and the application_access
                if job_change.target_model == 'Member':
                    object_fields.pop('user', None)
                    object_fields.pop('password', None)
                    object_fields.pop('applications_access', None)
                    object_fields['user_access'] = target_obj.applications_access.filter(id=job_change.application.pk).\
                                                       count() == 1

                # Depending of the application, we set the "inactive" to True or False
                is_inactive = field_inactive or \
                              target_obj.applications_active.filter(id=job_change.application.pk).count() == 0
                object_fields['inactive'] = is_inactive

            except AttributeError:
                error = 'JSON_MANIPULATION_FAILED'
        except LookupError:
            error = 'MODEL_NOT_FOUND'
    except Exception as e:
        error = f'ERROR_UNKNOW__{str(e).upper()}'

    if object_fields is None:
        error = 'TARGET_OBJECT_NOT_FOUND_BUT_ERROR_UNKNOWN'

    job_change.last_operation_date_time = timezone.now()

    if error:
        job_change.status = JobChange.STATUS.FATAL_ERROR
        job_change.last_operation_result = error

        job_change.save()

        return False

    json_payload = {
        'id': job_change.pk,
        'type': job_change.change_type,
        'model': job_change.target_model,
        'uuid': str(job_change.target_uuid),
        'data': object_fields
    }

    headers = {
        'Authorization': f'Api-Key {job_change.application.api_token_key}',
    }

    try:
        resp = requests.post(url=job_change.application.api_endpoint_base,
                             verify=settings.API_ENDPOINTS_CA,
                             json=json_payload, headers=headers)

        resp.raise_for_status()

        json_resp = json.loads(resp.content)

        if 'success' in json_resp and json_resp['success']:
            job_change.status = JobChange.STATUS.DONE
            job_change.last_operation_result = None
        else:
            if 'success' not in json_resp or 'error' not in json_resp:
                error = 'INVALID_RESPONSE'
            else:
                error = json_resp['error']

            job_change.status = JobChange.STATUS.WAITING_AFTER_ERROR
            job_change.last_operation_result = error

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        job_change.status = JobChange.STATUS.WAITING_AFTER_ERROR
        job_change.last_operation_result = str(e).upper()

    job_change.save()

    return job_change.status == JobChange.STATUS.DONE
