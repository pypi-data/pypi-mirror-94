import sys

from django.core.management.base import BaseCommand
from django.db.models import Q

from centralhub.models import JobChange
from objectsyncer.utils_srv import execute_jobchange


class Command(BaseCommand):
    """
    Help
    """
    help = 'Push JobChanges to remote applications'

    def add_arguments(self, parser):
        """
        The arguments of the command.

        By default, all WAITING jobs are executed.

        The "--retryfail" argument is used to add jobs that are pending after at least one failed attempt.

        The "--retryfatal" argument allows you to add the jobs which have the status FATAL_ERROR.

        :param parser:
        """
        parser.add_argument('--retryfail', action="store_true", help='Retry failed jobs')
        parser.add_argument('--retryfatal', action="store_true", help='Retry fatal jobs')
        parser.add_argument('--verbose', action="store_true", help='Verbose mode')

    def handle(self, *args, **kwargs):
        retry_fail = kwargs['retryfail']
        retry_fatal = kwargs['retryfatal']
        verbose = kwargs['verbose']

        q_filter = Q(status=JobChange.STATUS.WAITING)

        if retry_fail:
            q_filter.add(Q(status=JobChange.STATUS.WAITING_AFTER_ERROR), Q.OR)

        if retry_fatal:
            q_filter.add(Q(status=JobChange.STATUS.FATAL_ERROR), Q.OR)

        job_changes = JobChange.objects.filter(q_filter)

        if verbose:
            sys.stdout.write(f'{len(job_changes)} job(s) found\n')

        counter_success = 0
        counter_failed = 0

        for job_change in JobChange.objects.filter(q_filter):
            try:
                if execute_jobchange(job_change):
                    if verbose:
                        sys.stdout.write(f'Job #{job_change.pk} successfully pushed\n')

                    counter_success += 1
                else:
                    job_change.refresh_from_db()
                    sys.stderr.write(f'Job #{job_change.pk} failed with error {job_change.last_operation_result}\n')

                    counter_failed += 1
            except Exception as e:
                sys.stderr.write(f'Job #{job_change.pk} failed with an unforeseen error : {e}\n')

                counter_failed += 1

        if verbose:
            sys.stdout.write(f'{counter_success}/{len(job_changes)} job(s) successfully pushed\n')

        if counter_failed > 0:
            sys.stderr.write(f'{counter_success}/{len(job_changes)} job(s) failed\n')

