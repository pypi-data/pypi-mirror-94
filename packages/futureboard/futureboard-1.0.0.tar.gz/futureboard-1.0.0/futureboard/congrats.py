from pydantic import Field

from futureboard.base import FormModel
from futureboard.colors_utils import generate_random_pastel_hex
from futureboard.forms import congrats_employee, congrats_employer


class EmployeeCongrats(FormModel):
    __form__ = congrats_employee
    company_name: str

    logo_url: str
    bg_color: str = Field(default_factory=generate_random_pastel_hex)


class EmployerCongrats(FormModel):
    __form__ = congrats_employer

    job_seeker_name: str

    logo_url: str
    bg_color: str = Field(default_factory=generate_random_pastel_hex)