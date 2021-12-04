# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .notifications import NotificationMethod, SingleNotificationMethod, BulkNotificationMethod
from part.test_part import BaseNotificationIntegrationTest


class NotificationTests(BaseNotificationIntegrationTest):

    def test_NotificationMethod(self):
        """ensure the implementation requirements are tested"""

        class FalseNotificationMethod(NotificationMethod):
            METHOD_NAME = 'FalseNotification'

        class AnotherFalseNotificationMethod(NotificationMethod):
            METHOD_NAME = 'AnotherFalseNotification'

            def send(self):
                """a comment so we do not need a pass"""

        class NoNameNotificationMethod(NotificationMethod):
            pass

        # no send / send bulk
        with self.assertRaises(NotImplementedError):
            FalseNotificationMethod('', '', '', '', )

        # no gathering
        with self.assertRaises(NotImplementedError):
            AnotherFalseNotificationMethod('', '', '', '', )

        # no METHOD_NAME
        with self.assertRaises(NotImplementedError):
            NoNameNotificationMethod('', '', '', '', )

    def test_SingleNotificationMethod(self):
        """ensure the implementation requirements are tested"""
        print('TESTING SingleNotificationMethod')

        class WrongImplementation(SingleNotificationMethod):
            METHOD_NAME = 'WrongImplementation1'

            def setup(self):
                print('running setup on WrongImplementation')
                return super().setup()

        with self.assertRaises(NotImplementedError):
            self._notification_run()

    def test_BulkNotificationMethod(self):
        """ensure the implementation requirements are tested"""
        print('TESTING BulkNotificationMethod')

        class WrongImplementation(BulkNotificationMethod):
            METHOD_NAME = 'WrongImplementation2'

            def setup(self):
                print('running setup on WrongImplementation')
                return super().setup()

        with self.assertRaises(NotImplementedError):
            self._notification_run()


# A integration test for notifications is provided in test_part.PartNotificationTest
