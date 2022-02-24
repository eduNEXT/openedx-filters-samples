"""
Filters steps exemplifying how to:
    - Modify filter input
    - No operation
    - Halt process
"""
from openedx_filters import PipelineStep
from openedx_filters.learning.filters import (
    CertificateCreationRequested,
    CertificateRenderStarted,
    CohortChangeRequested,
    CourseAboutRenderStarted,
    CourseEnrollmentStarted,
    CourseHomeRenderStarted,
    CourseUnenrollmentStarted,
    DashboardRenderStarted,
    StudentLoginRequested,
    StudentRegistrationRequested,
)


class ModifyUsernameBeforeRegistration(PipelineStep):
    """
    Modify user's username appending 'modified'.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyUsernameBeforeRegistration"
                ]
            }
        }
    """
    def run_filter(self, form_data, *args, **kwargs):  # pylint: disable=arguments-differ
        username = f"{form_data.get('username')}-modified"
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
                    "openedx_filters_samples.samples.pipeline.ModifyUserProfileBeforeLogin"
                ]
            }
        }
    """
    def run_filter(self, user, *args, **kwargs):  # pylint: disable=arguments-differ
        user.profile.set_meta({"previous_login": str(user.last_login)})
        user.profile.save()
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
                    "openedx_filters_samples.samples.pipeline.ModifyModeBeforeEnrollment"
                ]
            }
        }
    """
    def run_filter(self, user, course_key, mode, *args, **kwargs):  # pylint: disable=arguments-differ, unused-argument
        return {
            "mode": "honor",
        }


class ModifyCertificateModeBeforeCreation(PipelineStep):
    """
    Change certificate mode from 'honor' to 'no-id-professional'.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.creation.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyCertificateModeBeforeCreation"
                ]
            }
        }
    """
    def run_filter(self, user, course_id, mode, status, *args, **kwargs):  # pylint: disable=arguments-differ, unused-argument
        if mode == 'honor':
            return {
                'mode': 'no-id-professional',
            }
        return {}


class ModifyContextBeforeRender(PipelineStep):
    """
    Modify template context before rendering.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyContextBeforeRender"
                ]
            }
        }
    """
    def run_filter(self, context, *args, **kwargs):  # pylint: disable=arguments-differ
        context['context_modified'] = True
        return {
            'context': context,
        }


class ModifyUserProfileBeforeUnenrollment(PipelineStep):
    """
    Add unenrolled_from field to the user's profile.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.unenrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyUserProfileBeforeUnenrollment"
                ]
            }
        }
    """
    def run_filter(self, enrollment, *args, **kwargs):  # pylint: disable=arguments-differ
        enrollment.user.profile.set_meta({"unenrolled_from": str(enrollment.course_id)})
        enrollment.user.profile.save()
        return {}


class ModifyUserProfileBeforeCohortChange(PipelineStep):
    """
    Add cohort_info field to the user's profile.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.cohort.change.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyUserProfileBeforeCohortChange"
                ]
            }
        }
    """
    def run_filter(self, current_membership, target_cohort, *args, **kwargs):  # pylint: disable=arguments-differ
        user = current_membership.user
        user.profile.set_meta(
            {
                "cohort_info": f"Changed from Cohort {str(current_membership.course_user_group)} to Cohort {str(target_cohort)}"
            }
        )
        user.profile.save()
        return {}


class NoopFilter(PipelineStep):
    """
    No operation filter step. Continuous without any modification.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.NoopFilter"
                ]
            }
        }
    """

    def run_filter(self, *args, **kwargs):
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
                    "openedx_filters_samples.samples.pipeline.StopEnrollment"
                ]
            }
        }
    """

    def run_filter(self, *args, **kwargs):  # pylint: disable=arguments-differ
        raise CourseEnrollmentStarted.PreventEnrollment("You can't enroll on this course.")


class StopRegister(PipelineStep):
    """
    Stop registration process raising PreventRegister exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopRegister"
                ]
            }
        }
    """

    def run_filter(self, *args, **kwargs):  # pylint: disable=arguments-differ
        raise StudentRegistrationRequested.PreventRegistration("You can't register on this site.", status_code=403)


class StopLogin(PipelineStep):
    """
    Stop login process raising PreventLogin exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopLogin"
                ]
            }
        }
    """

    def run_filter(self, user, *args, **kwargs):  # pylint: disable=arguments-differ
        raise StudentLoginRequested.PreventLogin(
            "You can't login on this site.", redirect_to="", error_code="pre-register-login-forbidden"
        )


class StopUnenrollment(PipelineStep):
    """
    Stop un-enrollment process raising StopUnenrollment exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.unenrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopUnenrollment"
                ]
            }
        }
    """
    def run_filter(self, enrollment, *args, **kwargs):  # pylint: disable=arguments-differ
        raise CourseUnenrollmentStarted.PreventUnenrollment(
            "You can't un-enroll from this site."
        )


class StopCertificateCreation(PipelineStep):
    """
    Stop certificate generation process raising PreventCertificateCreation exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.creation.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopCertificateCreation"
                ]
            }
        }
    """
    def run_filter(self, user, course_id, mode, status, *args, **kwargs):  # pylint: disable=arguments-differ
        raise CertificateCreationRequested.PreventCertificateCreation(
            "You can't generate a certificate from this site."
        )


class StopCourseAboutRendering(PipelineStep):
    """
    Stop course about render raising PreventCourseAboutRender exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopCourseAboutRendering"
                ]
            }
        }
    """
    def run_filter(self, context, template_name, *args, **kwargs):  # pylint: disable=arguments-differ
        template_context = {}
        raise CourseAboutRenderStarted.PreventCourseAboutRender(
            "You can't view this course.",
            course_about_template='courseware/custom_course_about_alternative.html',
            template_context=context,
        )


class StopCourseHomeRendering(PipelineStep):
    """
    Stop course home render raising StopCourseHomeRendering exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_home.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopCourseHomeRendering"
                ]
            }
        }
    """
    def run_filter(self, context, template_name, *args, **kwargs):  # pylint: disable=arguments-differ
        raise CourseHomeRenderStarted.PreventCourseHomeRender(
            "You can't view this course.",
            course_home_template='course_experience/custom-course-home-fragment.html',
            template_context=context,
        )


class StopDashboardRender(PipelineStep):
    """
    Stop dashboard render raising PreventDashboardRender exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.dashboard.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopDashboardRender"
                ]
            }
        }
    """
    def run_filter(self, context, template_name, *args, **kwargs):  # pylint: disable=arguments-differ
        raise DashboardRenderStarted.PreventDashboardRender(
            "You can't access the dashboard right now.",
            dashboard_template='custom-dashboard-template.html',
            template_context=context,
        )


class StopCertificateRender(PipelineStep):
    """
    Stop certificate render raising PreventCertificateRender exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopCertificateRender"
                ]
            }
        }
    """
    def run_filter(self, context, custom_template, *args, **kwargs):  # pylint: disable=arguments-differ
        raise CertificateRenderStarted.PreventCertificateRender(
            "You can't view this certificate.",
            invalid_cert_path="custom.invalid.cert.template.path",
        )


class StopCohortChange(PipelineStep):
    """
    Stop cohort change process raising PreventCohortChange exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.cohort.change.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopCohortChange"
                ]
            }
        }
    """
    def run_filter(self, current_membership, target_cohort, *args, **kwargs):  # pylint: disable=arguments-differ
        raise CohortChangeRequested.PreventCohortChange("You can't change cohorts.")
