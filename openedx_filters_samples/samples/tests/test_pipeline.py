"""
Test cases for Open edX Filters steps samples.
"""
from datetime import datetime
from unittest.mock import MagicMock

from django.test import TestCase, override_settings
from opaque_keys.edx.keys import CourseKey
from openedx_filters.learning.filters import (
    CourseEnrollmentStarted,
    StudentLoginRequested,
    StudentRegistrationRequested,
)


class SampleStepsTestCase(TestCase):
    """
    Samples steps test cases.
    """

    def setUp(self):
        super().setUp()
        self.user = MagicMock(username="test_username", last_login=datetime.now())
        self.registration_form = {
            "username": "test_username",
        }
        self.course_key = CourseKey.from_string("course-v1:Demo+DemoX+Demo_Course")

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyUsernameBeforeRegistration"
                ]
            }
        }
    )
    def test_modify_username(self):
        """
        Test that the user's username is modified before registration.
        """
        expected_result = {
            "username": "test_username-modified"
        }

        result = StudentRegistrationRequested.run_filter(form_data=self.registration_form)

        self.assertDictEqual(expected_result, result)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopRegister"
                ]
            }
        }
    )
    def test_stop_registration(self):
        """
        Test that the user's registration stops.
        """
        with self.assertRaises(StudentRegistrationRequested.PreventRegistration):
            StudentRegistrationRequested.run_filter(form_data=self.registration_form)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyUserProfileBeforeLogin"
                ]
            }
        }
    )
    def test_modify_user_profile(self):
        """
        Test that the user's username is modified before registration.
        """
        user = StudentLoginRequested.run_filter(user=self.user)

        user.profile.set_meta.assert_called_once_with(
            {
                "previous_login": str(self.user.last_login),
            }
        )

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopLogin"
                ]
            }
        }
    )
    def test_stop_login(self):
        """
        Test that the user's login stops.
        """
        with self.assertRaises(StudentLoginRequested.PreventLogin):
            StudentLoginRequested.run_filter(user=self.user)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyModeBeforeEnrollment"
                ]
            }
        }
    )
    def test_modify_enrollment_mode(self):
        """
        Test that the enrollment mode is modified before the enrollment process.
        """
        expected_result = (
            self.user,
            self.course_key,
            "honor",
        )

        result = CourseEnrollmentStarted.run_filter(
            user=self.user, course_key=self.course_key, mode="audit",
        )

        self.assertTupleEqual(expected_result, result)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopEnrollment"
                ]
            }
        }
    )
    def test_stop_enrollment(self):
        """
        Test that the user's enrollment stops.
        """
        with self.assertRaises(CourseEnrollmentStarted.PreventEnrollment):
            CourseEnrollmentStarted.run_filter(
                user=self.user, course_key=self.course_key, mode="audit",
            )
