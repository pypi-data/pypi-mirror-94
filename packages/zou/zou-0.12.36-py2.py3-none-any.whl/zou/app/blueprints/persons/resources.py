import datetime

from flask import abort
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from zou.app.services import persons_service, user_service, time_spents_service
from zou.app.utils import auth, permissions, csv_utils
from zou.app.services.exception import WrongDateFormatException

from zou.app import config


class NewPersonResource(Resource):
    """
    Create a new user in the database. Set "default" as password.
    User role can be set but only admins can create admin users.
    """

    @jwt_required
    def post(self):
        permissions.check_admin_permissions()
        data = self.get_arguments()

        if persons_service.is_user_limit_reached():
            return {
                "error": True,
                "message": "User limit reached.",
                "limit": config.USER_LIMIT,
            }, 400
        else:
            person = persons_service.create_person(
                data["email"],
                auth.encrypt_password("default"),
                data["first_name"],
                data["last_name"],
                data["phone"],
                role=data["role"],
                desktop_login=data["desktop_login"],
            )
        return person, 201

    def get_arguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "email", help="The email is required.", required=True
        )
        parser.add_argument(
            "first_name", help="The first name is required.", required=True
        )
        parser.add_argument("last_name", default="")
        parser.add_argument("phone", default="")
        parser.add_argument("role", default="user")
        parser.add_argument("desktop_login", default="")
        args = parser.parse_args()
        return args


class DesktopLoginsResource(Resource):
    """
    Allow to create and retrieve desktop login logs. Desktop login logs can only
    be created by current user.
    """

    @jwt_required
    def get(self, person_id):
        current_user = persons_service.get_current_user()
        if (
            current_user["id"] != person_id
            and not permissions.has_manager_permissions()
        ):
            raise permissions.PermissionDenied

        persons_service.get_person(person_id)
        return persons_service.get_desktop_login_logs(person_id)

    @jwt_required
    def post(self, person_id):
        arguments = self.get_arguments()

        current_user = persons_service.get_current_user()
        if (
            current_user["id"] != person_id
            and not permissions.has_admin_permissions()
        ):
            raise permissions.PermissionDenied

        desktop_login_log = persons_service.create_desktop_login_logs(
            person_id, arguments["date"]
        )

        return desktop_login_log, 201

    def get_arguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument("date", default=datetime.datetime.now())
        return parser.parse_args()


class PresenceLogsResource(Resource):
    """
    Return a csv file containing the presence logs based on a daily basis.
    """

    @jwt_required
    def get(self, month_date):
        permissions.check_admin_permissions()
        date = datetime.datetime.strptime(month_date, "%Y-%m")
        presence_logs = persons_service.get_presence_logs(date.year, date.month)
        return csv_utils.build_csv_response(presence_logs)


class TimeSpentsResource(Resource):
    """
    Get time spents for given person and date.
    """

    @jwt_required
    def get(self, person_id, date):
        permissions.check_admin_permissions()
        try:
            return time_spents_service.get_time_spents(person_id, date)
        except WrongDateFormatException:
            abort(404)


class PersonYearTimeSpentsResource(Resource):
    """
    Get aggregated time spents for given person and year.
    """

    @jwt_required
    def get(self, person_id, year):
        user_service.check_person_access(person_id)
        try:
            return time_spents_service.get_year_time_spents(person_id, year)
        except WrongDateFormatException:
            abort(404)


class PersonMonthTimeSpentsResource(Resource):
    """
    Get aggregated time spents for given person and month.
    """

    @jwt_required
    def get(self, person_id, year, month):
        user_service.check_person_access(person_id)
        try:
            return time_spents_service.get_month_time_spents(
                person_id, year, month
            )
        except WrongDateFormatException:
            abort(404)


class PersonWeekTimeSpentsResource(Resource):
    """
    Get aggregated time spents for given person and week.
    """

    @jwt_required
    def get(self, person_id, year, week):
        user_service.check_person_access(person_id)
        try:
            return time_spents_service.get_week_time_spents(
                person_id, year, week
            )
        except WrongDateFormatException:
            abort(404)


class PersonDayTimeSpentsResource(Resource):
    """
    Get aggregated time spents for given person and day.
    """

    @jwt_required
    def get(self, person_id, year, month, day):
        user_service.check_person_access(person_id)
        try:
            return time_spents_service.get_day_time_spents(
                person_id, year, month, day
            )
        except WrongDateFormatException:
            abort(404)


class TimeSpentMonthResource(Resource):
    """
    Return a table giving time spent by user and by day for given year and
    month.
    """

    @jwt_required
    def get(self, year, month):
        if permissions.has_admin_permissions():
            return time_spents_service.get_day_table(year, month)
        else:
            current_user = persons_service.get_current_user()
            return time_spents_service.get_day_table(
                year, month, person_id=current_user["id"]
            )


class TimeSpentYearsResource(Resource):
    """
    Return a table giving time spent by user and by month for given year.
    """

    @jwt_required
    def get(self):
        if permissions.has_admin_permissions():
            return time_spents_service.get_year_table()
        else:
            current_user = persons_service.get_current_user()
            return time_spents_service.get_year_table(
                person_id=current_user["id"]
            )


class TimeSpentMonthsResource(Resource):
    """
    Return a table giving time spent by user and by month for given year.
    """

    @jwt_required
    def get(self, year):
        if permissions.has_admin_permissions():
            return time_spents_service.get_month_table(year)
        else:
            current_user = persons_service.get_current_user()
            return time_spents_service.get_month_table(
                year,
                person_id=current_user["id"]
            )


class TimeSpentWeekResource(Resource):
    """
    Return a table giving time spent by user and by week for given year.
    """

    @jwt_required
    def get(self, year):
        if permissions.has_admin_permissions():
            return time_spents_service.get_week_table(year)
        else:
            current_user = persons_service.get_current_user()
            return time_spents_service.get_week_table(
                year,
                person_id=current_user["id"]
            )


class InvitePersonResource(Resource):
    """
    Sends an email to given person to invite him/her to connect to Kitsu
    """

    @jwt_required
    def get(self, person_id):
        permissions.check_admin_permissions()
        persons_service.invite_person(person_id)
        return {"success": True, "message": "Email sent"}
