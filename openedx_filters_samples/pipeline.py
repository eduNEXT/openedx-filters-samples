"""
Filters steps illustrating how to modify the application behavior by using pipeline steps.

Pipeline steps are used to modify the behavior of the application by altering the
input data or stopping the process. The pipeline steps are executed in the order
they are defined in the configuration OPEN_EDX_FILTERS_CONFIG for each filter type.

This file contains examples of pipeline steps that modify the behavior of the application,
such as stopping the enrollment process, modifying the user's profile, or changing the
certificate mode before rendering.

These use cases are illustrative and can be adapted to your specific needs.
"""

from django.http import HttpResponse
from opaque_keys.edx.keys import CourseKey
from openedx_filters import PipelineStep
from openedx_filters.learning.filters import (
    AccountSettingsRenderStarted,
    CertificateCreationRequested,
    CertificateRenderStarted,
    CohortAssignmentRequested,
    CohortChangeRequested,
    CourseAboutRenderStarted,
    CourseEnrollmentStarted,
    CourseUnenrollmentStarted,
    StudentLoginRequested,
    StudentRegistrationRequested,
)


class ModifyUsernameBeforeRegistration(PipelineStep):
    """
    Modify user's username appending 'modified' to the original username before registration.

    By modifying the username before registration, now the username will be saved with '-modified' appended to it.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
        "org.openedx.learning.student.registration.requested.v1": {
            "fail_silently": false,
            "pipeline": [
                "openedx_filters_samples.pipeline.ModifyUsernameBeforeRegistration"
            ]
        }
    }
    """

    def run_filter(
        self, form_data, *args, **kwargs
    ):
        """
        Modify the username before registration.

        Arguments:
            form_data (QueryDict): The form data containing the user's registration information.
        """
        username = f"{form_data.get('username')}-modified"
        form_data["username"] = username
        return {
            "form_data": form_data,
        }


class ModifyUserProfileBeforeLogin(PipelineStep):
    """
    Add previous_login field to the user's profile before login.

    By modifying the user's profile before login, now the user's profile will have a previous_login field
    with the value of the user's last login.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
        "org.openedx.learning.student.login.requested.v1": {
            "fail_silently": false,
            "pipeline": [
                "openedx_filters_samples.pipeline.ModifyUserProfileBeforeLogin"
            ]
        }
    }
    """

    def run_filter(self, user, *args, **kwargs):
        """
        Modify the user's profile before login.

        Arguments:
            user (User): The user logging in.
        """
        user.profile.set_meta({"previous_login": str(user.last_login)})
        user.profile.save()
        return {"user": user}


class ModifyModeBeforeEnrollment(PipelineStep):
    """
    Change enrollment mode to 'honor' before enrollment in all cases.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
        "org.openedx.learning.course.enrollment.started.v1": {
            "fail_silently": false,
            "pipeline": [
                "openedx_filters_samples.pipeline.ModifyModeBeforeEnrollment"
            ]
        }
    }
    """

    def run_filter(
        self, user, course_key, mode, *args, **kwargs
    ):
        """
        Change the enrollment mode to 'honor' before enrollment.

        Arguments:
            user (User): The user enrolling in the course.
            course_key (CourseKey): The course key for the course.
            mode (str): The mode of the enrollment.
        """
        return {
            "mode": "honor",
        }


class ModifyCertificateModeBeforeCreation(PipelineStep):
    """
    Change certificate mode from 'honor' to 'no-id-professional' before certificate creation.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.creation.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.ModifyCertificateModeBeforeCreation"
                ]
            }
        }
    """

    def run_filter(
        self, user, course_id, mode, status, *args, **kwargs
    ):
        """
        Change the certificate mode from 'honor' to 'no-id-professional' before certificate creation.

        Arguments:
            user (User): The user requesting the certificate.
            course_id (str): The course id for the course.
            mode (str): The mode of the certificate.
            status (str): The status of the certificate.
        """
        if mode == "honor":
            return {
                "mode": "no-id-professional",
            }
        return {}


class ModifyContextBeforeRender(PipelineStep):
    """
    Modify template context before rendering the certificate.

    By modifying the context before rendering the certificate, now the context will have a context_modified field
    that can be used in the template to check if the context was modified.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.ModifyContextBeforeRender"
                ]
            }
        }
    """

    def run_filter(self, context, *args, **kwargs):
        """
        Modify the context before rendering the certificate.

        Arguments:
            context (dict): The context data for the certificate
        """
        context["context_modified"] = True
        return {
            "context": context,
        }


class ModifyUserProfileBeforeUnenrollment(PipelineStep):
    """
    Add unenrolled_from field to the user's profile before un-enrollment.

    By modifying the user's profile before un-enrollment, now the user's profile will have an unenrolled_from field
    with the value of the course from which the user is un-enrolling.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.unenrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.pipeline.ModifyUserProfileBeforeUnenrollment"
                ]
            }
        }
    """

    def run_filter(
        self, enrollment, *args, **kwargs
    ):
        """
        Modify the user's profile before un-enrollment.

        Arguments:
            enrollment (CourseEnrollment): The enrollment being un-enrolled.
        """
        enrollment.user.profile.set_meta({"unenrolled_from": str(enrollment.course_id)})
        enrollment.user.profile.save()
        return {}


class ModifyUserProfileBeforeCohortChange(PipelineStep):
    """
    Add cohort_info field to the user's profile before cohort change or assignment.

    By modifying the user's profile before cohort change or assignment, now the user's profile will have a cohort_info
    field with the value of the course user group from which the user is changing cohorts or being assigned to a cohort.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.cohort.change.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.pipeline.ModifyUserProfileBeforeCohortChange"
                ]
            }
        }
    """

    def run_filter(
        self, current_membership, target_cohort, *args, **kwargs
    ):
        """
        Modify the user's profile before cohort change or assignment.

        Arguments:
            current_membership (CourseUserGroupMembership): The current membership of the user.
            target_cohort (CourseUserGroup): The target cohort to which the user is changing cohorts or being assigned.
        """
        user = current_membership.user
        user.profile.set_meta(
            {
                "cohort_info": f"Changed from Cohort {str(current_membership.course_user_group)} to Cohort {str(target_cohort)}"  # pylint: disable=line-too-long
            }
        )
        user.profile.save()
        return {}


class ModifyUpdatesFromCourse(PipelineStep):
    """
    Modify any update from the course by changing the content to a simple message.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.ModifyUpdatesFromCourse"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):
        """
        Modify the course updates content to a simple message.

        Arguments:
            context (dict): The context data for the course about page.
            template_name (str): The template name for the course about page.
        """
        update_message = context["update_message_fragment"]
        if update_message:
            update_message.content = "<p>This is a simple message</p>"
        return {
            "context": context,
            template_name: template_name,
        }


class RenderCustomCertificateStep(PipelineStep):
    """
    Modify the certificate rendering process by creating a custom template.

    By creating a custom certificate template, now the certificate will be rendered using the custom template.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.RenderCustomCertificateStep"
                ]
            }
        }
    """

    def run_filter(self, context, custom_template):
        """
        Get or create a new custom template to render instead of the original.

        Arguments:
            context (dict): The context data for the certificate.
            custom_template (str): The custom template to render.
        """
        course_key = CourseKey.from_string(context["course_id"])
        custom_template = self._get_or_create_custom_template(
            mode="honor", course_key=course_key
        )
        return {"custom_template": custom_template}

    def _get_or_create_custom_template(
        self, org_id=None, mode=None, course_key=None, language=None
    ):
        """
        Create a custom certificate template entry in the database.

        Arguments:
            org_id (str): The organization id for the certificate.
            mode (str): The mode of the certificate.
            course_key (CourseKey): The course key for the course.
            language (str): The language of the certificate.

        Returns:
            CertificateTemplate: The custom certificate template.

        WARNING: This method is for demonstration purposes only. It is not recommended to import
        models directly from the platform code. This is done here to demonstrate how to create
        a custom certificate template entry in the database.
        """
        from lms.djangoapps.certificates.models import (  # pylint: disable=import-error, import-outside-toplevel
            CertificateTemplate,
        )

        template_html = """
            <%namespace name='static' file='static_content.html'/>
            <html>
            <body>
                lang: ${LANGUAGE_CODE}
                course name: ${accomplishment_copy_course_name}
                mode: ${course_mode}
                ${accomplishment_copy_course_description}
                ${twitter_url}
                <img class="custom-logo" src="test-logo.png" />
            </body>
            </html>
        """
        template = CertificateTemplate.objects.filter(course_key=course_key)
        if bool(template):
            return template.first()

        template = CertificateTemplate(
            name="custom template",
            template=template_html,
            organization_id=org_id,
            course_key=course_key,
            mode=mode,
            is_active=True,
            language=language,
        )
        template.save()
        return template


class NoopFilter(PipelineStep):
    """
    Noop filter that does nothing.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
        "org.openedx.learning.course.enrollment.started.v1": {
            "fail_silently": false,
            "pipeline": [
                "openedx_filters_samples.pipeline.NoopFilter"
            ]
        }
    }
    """

    def run_filter(self, *args, **kwargs):
        """Return an empty dictionary without any modifications to the input data."""
        return {}


class StopCertificateCreation(PipelineStep):
    """
    Stop certificate generation process raising PreventCertificateCreation exception.

    By raising PreventCertificateCreation exception, the certificate generation process will be stopped in all cases.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
        "org.openedx.learning.certificate.creation.requested.v1": {
            "fail_silently": false,
            "pipeline": [
                "openedx_filters_samples.pipeline.StopCertificateCreation"
            ]
        }
    }
    """

    def run_filter(
        self, user, course_key, mode, status, grade, generation_mode
    ):
        """
        Raise PreventCertificateCreation exception to stop the certificate generation in all cases.

        Arguments:
            user (User): The user requesting the certificate.
            course_key (CourseKey): The course key for the course.
            mode (str): The mode of the certificate.
            status (str): The status of the certificate.
            grade (str): The grade of the certificate.
            generation_mode (str): The generation mode of the certificate.
        """
        raise CertificateCreationRequested.PreventCertificateCreation(
            "You can't generate a certificate from this site."
        )


class StopEnrollment(PipelineStep):
    """
    Stop enrollment process raising PreventEnrollment exception.

    By raising PreventEnrollment exception, the enrollment process will be stopped in all cases.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.pipeline.StopEnrollment"
                ]
            }
        }
    """

    def run_filter(self, enrollment, *args, **kwargs):
        """
        Raise PreventEnrollment exception to stop the enrollment process in all cases.

        Arguments:
            enrollment (CourseEnrollment): The enrollment being processed.
        """
        raise CourseEnrollmentStarted.PreventEnrollment(
            "You can't enroll on this course."
        )


class StopRegister(PipelineStep):
    """
    Stop registration process raising PreventRegister exception.

    By raising PreventRegister exception, the registration process will be stopped in all cases by raising a 403 error.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.registration.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.pipeline.StopRegister"
                ]
            }
        }
    """

    def run_filter(self, form_data, *args, **kwargs):
        """
        Raise PreventRegister exception to stop the registration process in all cases.

        Arguments:
            form_data (QueryDict): The form data containing the user's registration information.
        """
        raise StudentRegistrationRequested.PreventRegistration(
            "You can't register on this site.", status_code=403
        )


class StopLogin(PipelineStep):
    """
    Stop login process raising PreventLogin exception in all cases.

    By raising PreventLogin exception, the login process will be stopped in all cases by raising an
    error code.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.pipeline.StopLogin"
                ]
            }
        }
    """

    def run_filter(self, user, *args, **kwargs):
        """
        Raise PreventLogin exception to stop the login process in all cases.

        Arguments:
            user (User): The user trying to login.
        """
        raise StudentLoginRequested.PreventLogin(
            "You can't login on this site.",
            redirect_to="",
            error_code="pre-register-login-forbidden",
        )


class StopUnenrollment(PipelineStep):
    """
    Stop un-enrollment process raising StopUnenrollment exception.

    By raising StopUnenrollment exception, the un-enrollment from a course will be stopped in all cases.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course.unenrollment.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.pipeline.StopUnenrollment"
                ]
            }
        }
    """

    def run_filter(
        self, enrollment, *args, **kwargs
    ):
        """
        Raise PreventUnenrollment exception to stop the un-enrollment process in all cases.

        Arguments:
            enrollment (CourseEnrollment): The enrollment being un-enrolled.
        """
        raise CourseUnenrollmentStarted.PreventUnenrollment(
            "You can't un-enroll from this site."
        )


class RenderAlternativeCertificate(PipelineStep):
    """
    Render alternative certificate raising RenderAlternativeInvalidCertificate exception.

    By raising RenderAlternativeInvalidCertificate exception, the certificate generation process will be stopped
    and an alternative certificate will be rendered. In this case, the default invalid certificate template will be
    rendered.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.creation.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.RenderAlternativeCertificate"
                ]
            }
        }
    """

    def run_filter(
        self, context, custom_template, *args, **kwargs
    ):
        """
        Raise RenderAlternativeInvalidCertificate exception to alter the certificate generation process.

        Arguments:
            context (dict): The context data for the certificate.
            custom_template (str): The custom template to render.
        """
        raise CertificateRenderStarted.RenderAlternativeInvalidCertificate(
            "You can't generate a certificate from this site.",
        )


class RenderCustomResponseCertificate(PipelineStep):
    """
    Alter the certificate generation process by rendering a custom response.

    By raising RenderCustomResponse exception, the certificate generation process will be stopped and a custom response
    will be rendered instead of the certificate.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.creation.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.RenderCustomResponseCertificate"
                ]
            }
        }
    """

    def run_filter(
        self, context, custom_template, *args, **kwargs
    ):
        """
        Raise RenderCustomResponse exception to alter the certificate generation process.

        Arguments:
            context (dict): The context data for the certificate.
            custom_template (str): The custom template to render.
        """
        response = HttpResponse("Here's the text of the web page.")
        raise CertificateRenderStarted.RenderCustomResponse(
            "You can't generate a certificate from this site.",
            response=response,
        )


class RedirectToCustomCertificate(PipelineStep):
    """
    Redirect to custom certificate page.

    By raising RedirectToPage exception, the certificate generation process will be stopped and the user will be
    redirected to a custom certificate page or any other URL.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.RenderCustomCertificateStep"
                ]
            }
        }
    """

    def run_filter(self, context, custom_template):
        """
        Raise RedirectToPage exception to redirect the user to a custom certificate page.

        Arguments:
            context (dict): The context data for the certificate.
            custom_template (str): The custom template to render.
        """
        raise CertificateRenderStarted.RedirectToPage(
            "You can't generate a certificate from this site, redirecting to the correct location.",
            redirect_to="https://certificate.pdf",
        )


class RenderResponseCourseAbout(PipelineStep):
    """
    Alter the course about render process by rendering a custom response.

    By raising RenderCustomResponse exception, the course about render process will be stopped and a custom response
    will be rendered instead of the course about page. In this case, the response will be a simple HttpResponse.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.RenderResponseCourseAbout"
                ]
            }
        }
    """

    def run_filter(
        self, context, custom_template, *args, **kwargs
    ):
        """
        Raise RenderCustomResponse exception to alter the course about render process.

        When raising the exception, this filter uses a redirect_to field handled by
        the course about view that redirects to the URL indicated.

        Arguments:
            context (dict): The context data for the course about page.
            custom_template (str): The custom template to render.
        """
        response = HttpResponse("Here's the text of the web page.")

        raise CourseAboutRenderStarted.RenderCustomResponse(
            "You can't access this courses home page, redirecting to the correct location.",
            response=response,
        )


class RenderAlternativeCourseAbout(PipelineStep):
    """
    Alter course about render by raising RenderAlternativeCourseAbout exception.

    By raising RenderAlternativeCourseAbout exception, the course about render process will be stopped and an
    alternative course about page will be rendered. In this case, the default 404 course about template will be
    rendered.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.RenderAlternativeCourseAbout"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):
        """
        Render alternative course about page raising RenderAlternativeCourseAbout exception.

        When raising the exception, this filter uses a redirect_to field handled by
        the course about view that redirects to the URL indicated.

        Arguments:
            context (dict): The context data for the course about page.
            template_name (str): The template name for the course about page.
        """
        raise CourseAboutRenderStarted.RenderInvalidCourseAbout(
            "You can't view this course.",
            course_about_template="static_templates/404.html",
            template_context=context,
        )


class RedirectCustomCourseAbout(PipelineStep):
    """
    Redirect to custom course about page.

    By raising RedirectToPage exception, the course about render process will be stopped and the user will be
    redirected to a custom course about page or any other URL.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.RedirectCustomCourseAbout"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):
        """
        Redirect to custom course about page raising RedirectToPage exception.

        Arguments:
            context (dict): The context data for the course about page.
            template_name (str): The template name for the course about page.
        """
        raise CourseAboutRenderStarted.RedirectToPage(
            "You can't access this courses about page, redirecting to the correct location.",
            redirect_to="https://custom-course-about.com",
        )


class StopCohortChange(PipelineStep):
    """
    Stop cohort change by raising PreventCohortChange exception.

    By raising PreventCohortChange exception, the cohort change of a student will be stopped in all cases.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.cohort.change.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.StopCohortChange"
                ]
            }
        }
    """

    def run_filter(
        self, current_membership, target_cohort, *args, **kwargs
    ):
        """
        Raise PreventCohortChange exception to stop the cohort change process in all cases.

        Arguments:
            current_membership (CourseUserGroupMembership): The current membership of the user.
            target_cohort (CourseUserGroup): The target cohort to which the user is changing cohorts.
        """
        raise CohortChangeRequested.PreventCohortChange("You can't change cohorts.")


class StopCohortAssignment(PipelineStep):
    """
    Stop cohort assignment for a student by raising PreventCohortAssignment exception.

    By raising PreventCohortAssignment exception, the cohort assignment process will be stopped in all cases.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.cohort.assignment.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.pipeline.StopCohortAssignment"
                ]
            }
        }
    """

    def run_filter(
        self, user, target_cohort, *args, **kwargs
    ):
        """
        Raise PreventCohortAssignment exception to stop the cohort assignment process in all cases.

        Arguments:
            user (User): The user being assigned to a cohort.
            target_cohort (CourseUserGroup): The target cohort to which the user is being assigned.
        """
        raise CohortAssignmentRequested.PreventCohortAssignment(
            "You can't assign this user to that cohorts."
        )


class StopAccountSettingsRender(PipelineStep):
    """
    Alter the account settings render process by raising RedirectToPage exception.

    By raising RedirectToPage exception, the account settings render process will be stopped and the user will be
    redirected to a custom page or any other URL.

    Example usage:

    >>> "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.student.settings.render.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filters_samples.pipeline.StopAccountSettingsRender"
                ]
            }
        },
    """

    def run_filter(self, context, *args, **kwargs):
        """
        Raise RedirectToPage exception to stop the account settings render process.

        Arguments:
            context (dict): The context data for the account settings.
        """
        raise AccountSettingsRenderStarted.RedirectToPage(
            "You can't access to account settings.",
            redirect_to="https://custom-account-settings.com",
        )
