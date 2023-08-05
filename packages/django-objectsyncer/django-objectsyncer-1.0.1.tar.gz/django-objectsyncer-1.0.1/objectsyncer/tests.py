import uuid

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Application, JobChange, VersioningFakeClass


class BaseTestCase(TestCase):
    def __init__(self, *args):
        super().__init__(*args)

        self.app_counter = 0
        self.fake_counter = 0

    def setUp(self):
        """
        Preparation before a test :

          - creating a user
        """

        # On créé un utilisateur
        self.current_user = User.objects.create_user("myusername", "email@domain.tld", "mypassword")

    def create_application(self, name=None, api_endpoint_base='', api_token_key='', inactive=False, save=True):
        """
        Create an application

        :param name: the name of the application, default is "App<id>"
        :type name: str or None
        :param api_endpoint_base: the API endpoint base
        :tyoe api_endpoint_base: str
        :param api_token_key: the API token key
        :param api_token_key: str
        :param inactive: set the app as inactive
        :type inactive: bool
        :param save: persist the app
        :type save: bool
        :return the app
        :rtype Application
        """
        self.app_counter += 1

        app_name = f'app{self.app_counter}' if name is None else name
        app = Application(name=app_name, api_endpoint_base='', api_token_key='', inactive=inactive)

        if save:
            app.save()

        return app

    def create_versioningfake(self, code=None, name=None,inactive=False, save=True):
        """
        Create a versioning fake class

        :param code: the code, default is "1000+<id>"
        :param code: str
        :param name: the name, default is "fake<id>"
        :param inactive: set the unit as inactive
        :type inactive: bool
        :param save: persist the unit
        :type save: bool
        :return the unit
        :rtype Unit
        """
        self.fake_counter += 1

        unit_code = str(1000 + self.fake_counter) if code is None else code
        unit_name = f'unit{self.fake_counter}' if name is None else name

        o = VersioningFakeClass(code=unit_code, name=unit_name, inactive=inactive)

        if save:
            o.save()

        return o


class JobChangeTest(BaseTestCase):
    def test_without_application(self):
        """
        Test creating JobChange without application
        """
        # Without application, no JobChange must be created
        JobChange.create('Unit', uuid.uuid4())
        self.assertEqual(0, JobChange.objects.all().count())

    def test_with_one_application(self):
        """
        Test creating JobChange with 1 application
        """

        # One application
        app1 = self.create_application()

        test_uuid = uuid.uuid4()
        JobChange.create('Unit', test_uuid)

        self.assertEqual(JobChange.objects.filter(target_model='Unit', target_uuid=test_uuid).count(), 1)

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid)

        self.assertEqual(JobChange.CHANGE_TYPES.CREATE_OR_UPDATE, jc_db1.change_type)
        self.assertEqual(app1, jc_db1.application)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db1.status)
        self.assertIsNone(jc_db1.last_operation_date_time)
        self.assertIsNone(jc_db1.last_operation_result)

        # Test delete
        test_uuid2 = uuid.uuid4()
        JobChange.create('Unit', test_uuid2, change_type=JobChange.CHANGE_TYPES.DELETE)

        self.assertEqual(JobChange.objects.filter(target_model='Unit', target_uuid=test_uuid2).count(), 1)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid2)

        self.assertEqual(JobChange.CHANGE_TYPES.DELETE, jc_db2.change_type)
        self.assertEqual(app1, jc_db2.application)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db2.status)
        self.assertIsNone(jc_db2.last_operation_date_time)
        self.assertIsNone(jc_db2.last_operation_result)

    def test_with_two_application(self):
        """
        Test creating JobChange with 2 application
        """

        # Two application
        app1 = self.create_application()
        app2 = self.create_application()

        test_uuid = uuid.uuid4()
        JobChange.create('Unit', test_uuid)

        self.assertEqual(JobChange.objects.filter(target_model='Unit', target_uuid=test_uuid).count(), 2)

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app1)
        self.assertEqual(JobChange.CHANGE_TYPES.CREATE_OR_UPDATE, jc_db1.change_type)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db1.status)
        self.assertIsNone(jc_db1.last_operation_date_time)
        self.assertIsNone(jc_db1.last_operation_result)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app2)
        self.assertEqual(JobChange.CHANGE_TYPES.CREATE_OR_UPDATE, jc_db2.change_type)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db2.status)
        self.assertIsNone(jc_db2.last_operation_date_time)
        self.assertIsNone(jc_db2.last_operation_result)

    def test_with_two_application_with_one_onhold(self):
        """
        Test creating JobChange with 2 application : one active and one inactive
        """

        # Two application
        app1 = self.create_application()
        app2 = self.create_application(inactive=True)

        test_uuid = uuid.uuid4()
        JobChange.create('Unit', test_uuid)

        self.assertEqual(JobChange.objects.filter(target_model='Unit', target_uuid=test_uuid).count(), 2)

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app1)
        self.assertEqual(JobChange.CHANGE_TYPES.CREATE_OR_UPDATE, jc_db1.change_type)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db1.status)
        self.assertIsNone(jc_db1.last_operation_date_time)
        self.assertIsNone(jc_db1.last_operation_result)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app2)
        self.assertEqual(JobChange.CHANGE_TYPES.CREATE_OR_UPDATE, jc_db2.change_type)
        self.assertEqual(JobChange.STATUS.ON_HOLD, jc_db2.status)
        self.assertIsNone(jc_db2.last_operation_date_time)
        self.assertIsNone(jc_db2.last_operation_result)

    def test_with_multiple_changes_on_same_object(self):
        """
        Test multiple changes on the same object
        """
        app1 = self.create_application()

        # Same status
        test_uuid = uuid.uuid4()
        JobChange.create('Unit', test_uuid)
        JobChange.create('Unit', test_uuid)

        self.assertEqual(JobChange.objects.filter(target_model='Unit', target_uuid=test_uuid).count(), 1)

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app1)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db1.status)

        # Add one app
        app2 = self.create_application(inactive=True)

        JobChange.create('Unit', test_uuid)

        self.assertEqual(JobChange.objects.filter(target_model='Unit', target_uuid=test_uuid).count(), 2)

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app1)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db1.status)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app2)
        self.assertEqual(JobChange.STATUS.ON_HOLD, jc_db2.status)

        # Change one status to done
        jc_db1.status = JobChange.STATUS.DONE
        jc_db1.save()

        JobChange.create('Unit', test_uuid)

        self.assertEqual(JobChange.objects.filter(target_model='Unit', target_uuid=test_uuid).count(), 3)

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, status=JobChange.STATUS.DONE,
                                       application=app1)
        self.assertEqual(JobChange.STATUS.DONE, jc_db1.status)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, status=JobChange.STATUS.ON_HOLD,
                                       application=app2)
        self.assertEqual(JobChange.STATUS.ON_HOLD, jc_db2.status)

        jc_db3 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, status=JobChange.STATUS.WAITING,
                                       application=app1)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db3.status)

    def test_when_delete_application(self):
        """
        Test when deleting an application
        """
        app1 = self.create_application()
        app2 = self.create_application()

        JobChange.create('Unit', uuid.uuid4())
        JobChange.create('Unit', uuid.uuid4())
        JobChange.create('Unit', uuid.uuid4())
        JobChange.create('Unit', uuid.uuid4())
        JobChange.create('Unit', uuid.uuid4())

        self.assertEqual(10, JobChange.objects.filter(target_model='Unit').count())

        app1.delete()

        self.assertEqual(5, JobChange.objects.filter(target_model='Unit').count())
        self.assertEqual(5, JobChange.objects.filter(target_model='Unit', application=app2).count())

    def test_when_changing_application_to_inactive(self):
        """
        Test when changing an application to inactive
        """
        app1 = self.create_application()
        app2 = self.create_application()

        test_uuid = uuid.uuid4()
        JobChange.create('Unit', test_uuid)

        self.assertEqual(2, JobChange.objects.filter(target_model='Unit', status=JobChange.STATUS.WAITING).count())

        app1.inactive = True
        app1.save()

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app1)
        self.assertEqual(JobChange.STATUS.ON_HOLD, jc_db1.status)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app2)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db2.status)

        # Clear all
        JobChange.objects.all().delete()

        JobChange.create('Unit', test_uuid)
        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app1)
        jc_db1.status = JobChange.STATUS.DONE
        jc_db1.save()

        app1.inactive = True
        app1.save()

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app1)
        self.assertEqual(JobChange.STATUS.DONE, jc_db1.status)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid, application=app2)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db2.status)

    def test_when_changing_application_to_active(self):
        """
        Test when changing an application to inactive
        """
        app1 = self.create_application(inactive=True)

        JobChange.create('Unit', uuid.uuid4())
        JobChange.create('Unit', uuid.uuid4())

        self.assertEqual(2, JobChange.objects.filter(target_model='Unit', status=JobChange.STATUS.ON_HOLD).count())

        app1.inactive = False
        app1.save()

        self.assertEqual(2, JobChange.objects.filter(target_model='Unit', status=JobChange.STATUS.WAITING).count())

        # Clear all
        JobChange.objects.all().delete()

        app1.inactive = True
        app1.save()

        test_uuid1 = uuid.uuid4()
        JobChange.create('Unit', test_uuid1)

        test_uuid2 = uuid.uuid4()
        JobChange.create('Unit', test_uuid2)

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid1)
        jc_db1.status = JobChange.STATUS.DONE
        jc_db1.save()

        app1.inactive = False
        app1.save()

        jc_db1 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid1)
        self.assertEqual(JobChange.STATUS.DONE, jc_db1.status)

        jc_db2 = JobChange.objects.get(target_model='Unit', target_uuid=test_uuid2)
        self.assertEqual(JobChange.STATUS.WAITING, jc_db2.status)


class TrackingAndVersioningBaseModelTest(BaseTestCase):
    """
    TrackingAndVersioningBaseModel tests

    The class cannot be tested alone because of Meta abstract = True. We use a fake model for testing purpose only.
    """
    def test_version(self):
        """
        Test the version
        """
        o = self.create_versioningfake()

        self.assertEqual(1, o.version)

        o.name = "change1"
        self.assertEqual(1, o.version)

        o.save()
        self.assertEqual(2, o.version)

        o.name = "change2"
        o.name = "change2bis"
        self.assertEqual(2, o.version)

        o.save()
        self.assertEqual(3, o.version)

    def test_last_edition(self):
        """
        Test the last edition timestamp
        """
        o = self.create_versioningfake()
        self.assertEqual(0, (o.last_edition - o.creation).total_seconds())

        o.name = "change1"
        self.assertEqual(0, (o.last_edition - o.creation).total_seconds())

        now = timezone.now()
        o.save()
        self.assertTrue((o.last_edition - now).total_seconds() < 1.0)

    def test_last_inactive(self):
        """
        Test the inactive
        """
        app1 = self.create_application()
        app2 = self.create_application()
        app3 = self.create_application()

        o = self.create_versioningfake()
        o.applications_active.add(app1)
        o.applications_active.add(app2)
        o.applications_active.add(app3)

        o.save()
        self.assertEqual(3, o.applications_active.all().count())

        o.inactive = True
        self.assertEqual(3, o.applications_active.all().count())

        o.save()
        self.assertEqual(0, o.applications_active.all().count())
