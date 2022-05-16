"""
Unit tests for task management
"""

from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django_q.models import Schedule

import InvenTree.tasks
from common.models import InvenTreeSetting


class ScheduledTaskTests(TestCase):
    """
    Unit tests for scheduled tasks
    """

    def get_tasks(self, name):

        return Schedule.objects.filter(func=name)

    def test_add_task(self):
        """
        Ensure that duplicate tasks cannot be added.
        """

        task = 'InvenTree.tasks.heartbeat'

        self.assertEqual(self.get_tasks(task).count(), 0)

        InvenTree.tasks.schedule_task(task, schedule_type=Schedule.MINUTES, minutes=10)

        self.assertEqual(self.get_tasks(task).count(), 1)

        t = Schedule.objects.get(func=task)

        self.assertEqual(t.minutes, 10)

        # Attempt to schedule the same task again
        InvenTree.tasks.schedule_task(task, schedule_type=Schedule.MINUTES, minutes=5)
        self.assertEqual(self.get_tasks(task).count(), 1)

        # But the 'minutes' should have been updated
        t = Schedule.objects.get(func=task)
        self.assertEqual(t.minutes, 5)


class InvenTreeTaskTests(TestCase):
    """Unit tests for tasks"""

    def test_task_hearbeat(self):
        """Test the task heartbeat"""
        InvenTree.tasks.offload_task(InvenTree.tasks.heartbeat)

    def test_task_delete_successful_tasks(self):
        """Test the task delete_successful_tasks"""
        from django_q.models import Success

        Success.objects.create(
            name='abc',
            func='abc',
            started=timezone.now() - timedelta(days=31)
        )
        InvenTree.tasks.offload_task(InvenTree.tasks.delete_successful_tasks)
        threshold = timezone.now() - timedelta(days=30)
        results = Success.objects.filter(
            started__lte=threshold
        )
        self.assertEqual(len(results, 0))

    def test_task_delete_old_error_logs(self):
        """Test the task delete_old_error_logs"""
        InvenTree.tasks.offload_task(InvenTree.tasks.delete_old_error_logs)

    def test_task_check_for_updates(self):
        """Test the task check_for_updates"""
        # Check that setting should be empty
        self.assertEqual(InvenTreeSetting.get_setting('INVENTREE_LATEST_VERSION'), '')

        # Get new version
        InvenTree.tasks.offload_task(InvenTree.tasks.check_for_updates)

        # Check that setting is not empty
        response = InvenTreeSetting.get_setting('INVENTREE_LATEST_VERSION')
        self.assertNotEqual(response, '')
        self.assertTrue(bool(response))
