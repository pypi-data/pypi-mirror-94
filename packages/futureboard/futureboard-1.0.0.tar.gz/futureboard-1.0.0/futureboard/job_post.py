from pydantic import Field

from futureboard.base import FormModel
from futureboard.colors_utils import generate_random_pastel_hex
from futureboard.forms import job_thumbnail


class JobPost(FormModel):
    __form__ = job_thumbnail

    position: str
    company_name: str
    location: str
    salary: str

    logo_url: str
    bg_color: str = Field(default_factory=generate_random_pastel_hex)


if __name__ == '__main__':
    job = JobPost(
        position="p",
        company_name="c",
        location="p",
        salary="1 b",

        logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/LINE_logo.svg/300px-LINE_logo.svg.png",
        bg_color=generate_random_pastel_hex()
    )
    job.generate_image_sync()