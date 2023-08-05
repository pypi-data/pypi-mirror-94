from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('futureboard', 'forms'),
    autoescape=select_autoescape(['html', 'xml'])
)

job_thumbnail = env.get_template('job_thumbnail.jinja2')
congrats_employer = env.get_template('congrats_employer.jinja2')
congrats_employee = env.get_template('congrats_employee.jinja2')