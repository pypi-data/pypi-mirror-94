import sys
import uuid

from django.db import models
from django.db.models import Q
from django.db.models.signals import m2m_changed
from django.utils import timezone
from model_utils import Choices, FieldTracker
from django.dispatch import receiver
from django.conf import settings


if settings.OBJECTSYNCER_ROLE == 'SERVER':

    #
    # Applications
    #

    class Application(models.Model):
        """
        An application is a remote webapp that expose an API endpoint to receive push notifications.
        """

        """
        The name of the application
        """
        name = models.CharField(max_length=250)

        """
        Base of the API endpoint
        """
        api_endpoint_base = models.CharField(max_length=500)

        """
        API token key
        """
        api_token_key = models.CharField(max_length=250)

        """
        Is inactive
        """
        inactive = models.BooleanField(default=False)

        """
        Tracker
        """
        tracker = FieldTracker()

        def save(self, *args, **kwargs):
            """
            Save. In case of change(s) :

                - 1 is added to the version
                - the last_edition is now
                - a JobChange is created by application
            """
            is_inactive_changed = 'inactive' in self.tracker.changed()

            super().save(*args, **kwargs)

            if is_inactive_changed:
                new_status = JobChange.STATUS.ON_HOLD if self.inactive else JobChange.STATUS.WAITING

                JobChange.objects.filter(Q(application=self) &
                                         ~Q(status=JobChange.STATUS.DONE)).update(status=new_status)

        def __str__(self):
            s = self.name

            if self.inactive:
                s += ' (inactive)'

            return s

    #
    # JobChange
    #

    class JobChange(models.Model):
        """
        A JobChange represents the change of a object (designed by its UUID) for a specific model.

        There is one JobChange per application. There is only one JobChange "pending" per targeted object.

        The JobChange can have 2 types:
            - CREATE_OR_UPDATE : we do not differentiate between the two, the application must either create the object if
                                 it is new, or update it
            - DELETE : the application have to delete the record

        Each JobChange has one of the following statuses:
            - WAITING : pending execution this is the initial status at creation
            - ON_HOLD : changes related to inactive applications
            - WAITING_AFTER_ERROR : the push failed and the request is pending to try again
            - DONE : the change has been applied
        """

        CHANGE_TYPES = Choices('CREATE_OR_UPDATE', 'DELETE')

        STATUS = Choices('WAITING', 'ON_HOLD', 'WAITING_AFTER_ERROR', 'DONE', 'FATAL_ERROR')

        """
        The application
        """
        application = models.ForeignKey(Application, models.CASCADE)

        """
        Date and time of the change request 
        """
        request_date_time = models.DateTimeField(auto_now_add=True)

        """
        Change type
        """
        change_type = models.CharField(max_length=25, choices=CHANGE_TYPES)

        """
        Model to update
        """
        target_model = models.CharField(max_length=50)

        """
        Target UUID object
        """
        target_uuid = models.CharField(max_length=36)

        """
        Status
        """
        status = models.CharField(max_length=25, choices=STATUS)

        """
        Last operation date and time
        """
        last_operation_date_time = models.DateTimeField(blank=True, null=True)

        """
        Last operation result
        """
        last_operation_result = models.TextField(blank=True, null=True)

        def __str__(self):
            return f'[{self.application.name}] {self.target_model} {self.target_uuid} : {self.status}'

        @staticmethod
        def create(target_model, target_uuid, change_type=CHANGE_TYPES.CREATE_OR_UPDATE):
            """"
            Create a new JobChange.

            All previous unfinished JobChanges targeting the same object are deleted to be replaced by this one.
            """
            previous_jc = JobChange.objects.filter(Q(target_model=target_model) &
                                                   Q(target_uuid=target_uuid) &
                                                   ~Q(status=JobChange.STATUS.DONE))
            previous_jc.delete()

            for application in Application.objects.all():
                jc = JobChange()
                jc.application = application
                jc.change_type = change_type
                jc.target_model = target_model
                jc.target_uuid = target_uuid

                if not application.inactive:
                    jc.status = JobChange.STATUS.WAITING
                else:
                    jc.status = JobChange.STATUS.ON_HOLD

                jc.save()


#
# UUID base model
#

class VersioningBaseModel(models.Model):
    """
    The versioning base model have the following fields :

        - a UUID (version 4), unique for this model
        - a version, starting at 1
        - a creation datetime
        - a last edition datetime
        - a inactive flag
    """

    """
    UUID
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)

    """
    Version
    """
    version = models.IntegerField(default=1)

    """
    Date and time of creation
    """
    creation = models.DateTimeField(auto_now_add=True)

    """
    Date and time of last edition
    """
    last_edition = models.DateTimeField(auto_now_add=True)

    """
    Is inactive
    """
    inactive = models.BooleanField(default=False)

    class Meta:
        abstract = True


if settings.OBJECTSYNCER_ROLE == 'SERVER':
    class TrackingAndVersioningBaseModel(VersioningBaseModel):
        """
        The tracking and versioning base model have the following field added to the fields of VersioningBaseModel.

            - a active state by applications

        If the inactive flag is set, all applications active states are removed.

        Note that each sub class must have the following field :
            - tracker = FieldTracker()
        """

        """
        Applications active status
        """
        applications_active = models.ManyToManyField(Application, blank=True)

        def save(self, *args, **kwargs):
            """
            Save. In case of change(s) :

                - 1 is added to the version
                - the last_edition is now
                - a JobChange is created by application
            """
            have_changed = len(self.tracker.changed()) > 0
            is_new = self._state.adding

            if have_changed:
                if 'inactive' in self.tracker.changed() and self.inactive:
                    print(self.applications_active.clear())
                    # Doesn't work fixme todo

                self.version += 1
                self.last_edition = timezone.now()

            super().save(*args, **kwargs)

            if is_new or have_changed:
                JobChange.create(self.__class__.__name__, self.uuid)

        def delete(self, *args, **kwargs):
            """
            Delete : generate a JobChange by application
            """
            old_uuid = self.uuid

            super().delete(*args, **kwargs)

            JobChange.create(self.__class__.__name__, old_uuid, change_type=JobChange.CHANGE_TYPES.DELETE)

        class Meta:
            abstract = True


    @receiver(m2m_changed, sender=TrackingAndVersioningBaseModel.applications_active.through)
    def trackingandversioningbasemodel_application_active_changed(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        JobChange.create(instance.__class__.__name__, instance.uuid)


    # For test perupose only
    if settings.DEBUG:
        class VersioningFakeClass(TrackingAndVersioningBaseModel):
            """
            A code
            """
            code = models.CharField(max_length=20)

            """
            A name 
            """
            name = models.CharField(max_length=250)

            """
            Tracker
            """
            tracker = FieldTracker()
