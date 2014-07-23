# v7.0 - Beta.
{
    "name": "Pentaho res.partner report sample",
    "description": """
Titile of pentaho res.partner report sample
===========================================
This is a sample of a pentaho report using a custom wizard. 
The main modifications you should do are:
* report/res_partner.prpt --> your custom report
* report/report_data.xml --> everywhere you find the '<!-- MOD -->'' tag
* wizard/report_prompt.py --> everywhere you find the '# MOD' tag
* wizard/report_prompt.xml --> everywhere you find the '<!-- MOD -->'' tag
* Mod dependencies, name, description in this file
    """,
    "version": "0.1",
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar',
    "depends": ["pentaho_reports"],
    "category": "Reporting subsystems",
    "data": [
            'wizard/report_prompt.xml',
            'report/report_data.xml',
             ],
    "installable": True,
    "active": False
}
