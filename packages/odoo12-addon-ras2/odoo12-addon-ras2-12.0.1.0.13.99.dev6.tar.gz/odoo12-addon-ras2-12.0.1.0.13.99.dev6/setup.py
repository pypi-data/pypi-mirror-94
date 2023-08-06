import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'depends_override': {
            'hr_attendance_rfid': 'odoo12-addon-hr-attendance-rfid==12.0.1.1.0.99.dev1',
            'gate': 'odoo12-addon-gate==12.0.1.0.1'
        }
    }
)