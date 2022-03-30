"""
Filters steps exemplifying how to:
    - Modify filter input
    - No operation
    - Halt process
"""
from django.http import HttpResponse
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
    def run_filter(self, user, course_key, mode, status, grade, generation_mode, *args, **kwargs):  # pylint: disable=arguments-differ
        raise CertificateCreationRequested.PreventCertificateCreation(
            "You can't generate a certificate from this site."
        )


class RenderResponseCourseAbout(PipelineStep):
    """
    Stop course about render raising RenderCustomResponse exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.RenderResponseCourseAbout"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """
        Pipeline step that redirects to the course survey.

        When raising RedirectCourseHomePage, this filter uses a redirect_to field handled by
        the course home view that redirects to the URL indicated.
        """
        response = HttpResponse("Here's the text of the web page.")

        raise CourseAboutRenderStarted.RenderCustomResponse(
            "You can't access this courses home page, redirecting to the correct location.",
            response=response,
        )


class RenderAlternativeCourseAbout(PipelineStep):
    """
    Stop course about render raising RenderCustomResponse exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.RenderAlternativeCourseAbout"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """
        Pipeline step that renders a custom template.

        When raising RedirectCourseHomePage, this filter uses a redirect_to field handled by
        the course home view that redirects to the URL indicated.
        """
        raise CourseAboutRenderStarted.RenderAlternativeCourseAbout(
            "You can't view this course.",
            course_about_template='custom-course-about-template.html',
            template_context=context,
        )



class RedirectCustomCourseAbout(PipelineStep):
    """
    Redirect to custom course about.

    Example usage:

    Add the following configurations to your configuration file:

            "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.RedirectCustomCourseAbout"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """
        Pipeline step that redirects to the course survey.

        When raising RedirectCourseAboutPage, this filter uses a redirect_to field handled by
        the course about view that redirects to that URL.
        """
        raise CourseAboutRenderStarted.RedirectToPage(
            "You can't access this courses about page, redirecting to the correct location.",
            redirect_to="https://custom-course-about.com",
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


class ModifyUpdatesFromCourse(PipelineStep):
    """
    Modifies any update from course when rendering the home page.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.ModifyUpdatesFromCourse"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """Pipeline that modifies any update messages."""
        update_message = context["update_message_fragment"]
        if update_message:
            update_message.content = "<p>This is a simple message</p>"
        return {
            "context": context, template_name: template_name,
        }



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
            dashboard_template="static_templates/server-error.html",
            template_context=context,
        )


class RedirectFromDashboard(PipelineStep):
    """
    Stop dashboard render raising RedirectDashboardPage exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.dashboard.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.RedirectFromDashboard"
                ]
            }
        }
    """
    def run_filter(self, context, template_name, *args, **kwargs):  # pylint: disable=arguments-differ
        raise DashboardRenderStarted.RedirectDashboardPage(
            "You can't see this site's dashboard, redirecting to the correct location.",
            redirect_to="https://custom-lms-dashboard.com",
        )

class FilterEnrollmentDashboard(PipelineStep):
    """
    Filter enrollment list by a condition.
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """
        Pipeline steps that changes certificate mode from honor to no-id-professional.

        Example usage:

        Add the following configurations to your configuration file:

            "OPEN_EDX_FILTERS_CONFIG": {
                "org.openedx.learning.dashboard.render.started.v1": {
                    "fail_silently": False,
                    "pipeline": [
                        "openedx_filters_samples.samples.pipeline.FilterEnrollmentDashboard"
                    ]
                }
            }
        """
        context["course_enrollments"] = [
            course for course in context["course_enrollments"] if course.course_id.org != "edX"
        ]
        return {
            "context": context, template_name: template_name,
        }


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


class RenderCustomCertificateStep(PipelineStep):
    """
    Step that modifies the certificate rendering process by creating a custom template.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.RenderCustomCertificateStep"
                ]
            }
        }
    """

    def run_filter(self, context, custom_template):  # pylint: disable=arguments-differ
        """
        Pipeline steps that gets or creates a new custom template to render instead
        of the original.
        """
        from opaque_keys.edx.keys import CourseKey

        course_key = CourseKey.from_string(context["course_id"])
        custom_template = self._get_or_create_custom_template(mode='honor', course_key=course_key)
        return {"custom_template": custom_template}

    def _get_or_create_custom_template(self, org_id=None, mode=None, course_key=None, language=None):
        """
        Creates a custom certificate template entry in DB.
        """
        from lms.djangoapps.certificates.models import CertificateTemplate

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
            name='custom template',
            template=template_html,
            organization_id=org_id,
            course_key=course_key,
            mode=mode,
            is_active=True,
            language=language
        )
        template.save()
        return template


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


class StaffViewCourseAbout(PipelineStep):
    """
    Give to student staff view in course about.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.course_about.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StaffViewCourseAbout"
                ]
            }
        }
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """Pipeline that gives staff view to the current user."""
        context["staff_access"] = True
        context["studio_url"] = "http://studio.com"
        return {
            "context": context, template_name: template_name,
        }


class RedirectToCustomCertificate(PipelineStep):
    """
    Redirect to custom certificate.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.RenderCustomCertificateStep"
                ]
            }
        }
    """

    def run_filter(self, context, custom_template):  # pylint: disable=arguments-differ
        """Pipeline step that redirects before rendering the certificate."""
        raise CertificateRenderStarted.RedirectCertificateRender(
            "You can't generate a certificate from this site, redirecting to the correct location.",
            redirect_to="https://certificate.pdf",
        )
