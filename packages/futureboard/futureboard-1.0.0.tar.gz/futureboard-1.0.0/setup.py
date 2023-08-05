# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['futureboard', 'futureboard.forms']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0', 'pydantic>=1.7.3,<2.0.0', 'snap-html>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'futureboard',
    'version': '1.0.0',
    'description': '',
    'long_description': "# futureboard\n\na robust html to image engine build on top of playwright\n\n## Futureboard_builder Quickstart \n```python\n#install html2image package first!\nfrom futureboard.futureboard_builder import FutureboardBuilder\n\nfutureboard_builder = FutureboardBuilder()\nfutureboard_congratulation = futureboard_builder.create('congratulation')\nfutureboard_job = futureboard_builder.create('job')\n\n#Read from file\nfutureboard_job.generate_from_file(file='web/congrats_empoyer.html', save_as='congrats_employer.png')\n\n#Create job image with option\n#available option for job template:\n# job: str ='พนักงานเติมน้ำมันหน้าลานจอดรถ',\n# company: str ='บริษัท เอเชีย เอ็นจีเนียริ่ง',\n# location: str ='อโศก/กรุงเทพ',\n# salary: str ='30,000 บาท',\n# background_color: str ='#e3c3d7',\n# background_image: str ='job_thumbnail.png',\n# logo_url_image: str ='https://via.placeholder.com/300'\nfutureboard_job.generate(save_as='job.png', future_board_option={\n    'company': 'Something Company',\n    'salary': '100,000 บาท'\n})\n\n#Create congrat image with option\n#available option for congrat template:\n# company: str ='บริษัท เอเชีย เอ็นจีเนียริ่ง',\n# text: str ='สนใจสนทนากับพี่',\n# background_color: str ='#e3c3d7',\n# background_image: str ='congrats.png',\n# logo_url_image: str ='https://via.placeholder.com/300'\nfutureboard_congratulation.generate(save_as='cong.png', future_board_option={\n    'company': 'บริษัท กสิกร ซอฟต์',\n    'logo_url_image': 'https://res-4.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco/ll9dkelmfnghuthajcrb'\n})\n\n```",
    'author': 'Nutchanon Ninyawee',
    'author_email': 'nutchanon@codustry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sakuguru/futureboard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
