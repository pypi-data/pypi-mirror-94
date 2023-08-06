# Copyright 2021 http://www.thingsintouch.com
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'RFID Attendance System RAS2',
    'version': '12.0.1.0.13',
    'category': 'Human Resources',
    'website': 'https://github.com/thingsintouch/things_attendance/tree/12.0',
    'author': 'thingsintouch.com',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance_rfid',
    ],
    'data': [
        'views/hr_employee_view.xml',
        'wizard/add_singleton.xml',
        'views/res_config_settings_views.xml',
    ],
}
