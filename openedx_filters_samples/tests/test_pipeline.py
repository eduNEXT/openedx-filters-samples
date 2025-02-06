"""
Test cases for some Open edX Filters steps samples to illustrate how to use them.

Not all steps are tested here, but you can use these test cases as a reference to implement your own tests.
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
    Test suite for the sample steps of Open edX Filters:

    - ModifyUsernameBeforeRegistration
    - StopRegister
    - ModifyUserProfileBeforeLogin
    - StopLogin
    - ModifyModeBeforeEnrollment
    - StopEnrollment
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
                    "openedx_filters_samples.pipeline.ModifyUsernameBeforeRegistration"
                ],
            }
        }
    )
    def test_modify_username(self):
        """
        Test that the user's username is modified before registration.

        Expected behavior:
        - The username is modified from "test_username" to "test_username-modified
        """
        expected_result = {"username": "test_username-modified"}

        result = StudentRegistrationRequested.run_filter(
            form_data=self.registration_form
        )

        self.assertDictEqual(expected_result, result)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_filters_samples.pipeline.StopRegister"],
            }
        }
    )
    def test_stop_registration(self):
        """
        Test that the user's registration stops when the registration is requested.

        Expected behavior:
        - The registration process is stopped with the exception `StudentRegistrationRequested.PreventRegistration`.
        """
        with self.assertRaises(StudentRegistrationRequested.PreventRegistration):
            StudentRegistrationRequested.run_filter(form_data=self.registration_form)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.ModifyUserProfileBeforeLogin"
                ],
            }
        }
    )
    def test_modify_user_profile(self):
        """
        Test that the user's username is modified before registration.

        Expected behavior:
        - The user's profile meta is updated with the previous login date.
        """
        user = StudentLoginRequested.run_filter(user=self.user)

        user.profile.set_meta.assert_called_once_with(
            {
                "last_login": str(self.user.last_login),
            }
        )

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_filters_samples.pipeline.StopLogin"],
            }
        }
    )
    def test_stop_login(self):
        """
        Test that the user's login stops when the login is requested.

        Expected behavior:
        - The login process is stopped with the exception `StudentLoginRequested.PreventLogin`.
        """
        with self.assertRaises(StudentLoginRequested.PreventLogin):
            StudentLoginRequested.run_filter(user=self.user)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.ModifyModeBeforeEnrollment"
                ],
            }
        }
    )
    def test_modify_enrollment_mode(self):
        """
        Test that the enrollment mode is modified when the enrollment is started.

        Expected behavior:
        - The enrollment mode is modified from "audit" to "honor".
        """
        expected_result = (
            self.user,
            self.course_key,
            "honor",
        )

        result = CourseEnrollmentStarted.run_filter(
            user=self.user,
            course_key=self.course_key,
            mode="audit",
        )

        self.assertTupleEqual(expected_result, result)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_filters_samples.pipeline.StopEnrollment"],
            }
        }
    )
    def test_stop_enrollment(self):
        """
        Test that the user's enrollment stops the enrollment is started.

        Expected behavior:
        - The enrollment process is stopped with the exception `CourseEnrollmentStarted.PreventEnrollment`.
        """
        with self.assertRaises(CourseEnrollmentStarted.PreventEnrollment):
            CourseEnrollmentStarted.run_filter(
                user=self.user,
                course_key=self.course_key,
                mode="audit",
            )
