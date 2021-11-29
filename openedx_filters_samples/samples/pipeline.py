"""
Filters steps exemplifying how to:
    - Modify filter input
    - No operation
    - Halt process
"""
from openedx_filters import PipelineStep
from openedx_filters.learning.auth import PreRegisterFilter, PreLoginFilter
from openedx_filters.learning.enrollment import PreEnrollmentFilter


class ModifyUsernameBeforeRegistration(PipelineStep):
    """
    Modify user's username appending 'edunext'.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_test_plugin.pipeline.ModifyUsernameBeforeRegistration"
                ]
            }
        }
    """
    def run(self, form_data):
        username = f"{form_data.get('username')}-edunext"
        form_data["username"] = username
        return {
            "form_data": form_data,
        }


class ModifyUserProfileBeforeLogin(PipelineStep):
    """
    Add previous_login field to the user's profile.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_test_plugin.pipeline.ModifyUserProfileBeforeLogin"
                ]
            }
        }
    """
    def run(self, user):
        user.profile.set_meta({"previous_login": str(user.last_login)})
        return {"user": user}

class ModifyModeBeforeEnrollment(PipelineStep):
    """
    Change enrollment mode to 'honor'.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_test_plugin.pipeline.ModifyModeBeforeEnrollment"
                ]
            }
        }
    """
    def run(self, user, course_key, mode):
        return {
            "mode": "honor",
        }


class NoopFilter(PipelineStep):
    """
    No operation filter step. Continuous without any modification.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_test_plugin.pipeline.NoopFilter"
                ]
            }
        }
    """

    def run(self, **kwargs):
        return {}


class StopEnrollment(PipelineStep):
    """
    Stop enrollment process raising PreventEnrollment exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_test_plugin.pipeline.StopEnrollment"
                ]
            }
        }
    """

    def run(self, user, course_key, mode):
        raise PreEnrollmentFilter.PreventEnrollment("You can't enroll on this course.")


class StopRegister(PipelineStep):
    """
    Stop registration process raising PreventRegister exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_test_plugin.pipeline.StopRegister"
                ]
            }
        }
    """

    def run(self, form_data):
        raise PreRegisterFilter.PreventRegister("You can't register on this site.", status_code=403)


class StopLogin(PipelineStep):
    """
    Stop login process raising PreventLogin exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_test_plugin.pipeline.StopLogin"
                ]
            }
        }
    """

    def run(self, user):
        raise PreLoginFilter.PreventLogin("You can't login on this site.")
