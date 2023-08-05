# futureboard

a robust html to image engine build on top of playwright

## Futureboard_builder Quickstart 
```python
#install html2image package first!
from futureboard.futureboard_builder import FutureboardBuilder

futureboard_builder = FutureboardBuilder()
futureboard_congratulation = futureboard_builder.create('congratulation')
futureboard_job = futureboard_builder.create('job')

#Read from file
futureboard_job.generate_from_file(file='web/congrats_empoyer.html', save_as='congrats_employer.png')

#Create job image with option
#available option for job template:
# job: str ='พนักงานเติมน้ำมันหน้าลานจอดรถ',
# company: str ='บริษัท เอเชีย เอ็นจีเนียริ่ง',
# location: str ='อโศก/กรุงเทพ',
# salary: str ='30,000 บาท',
# background_color: str ='#e3c3d7',
# background_image: str ='job_thumbnail.png',
# logo_url_image: str ='https://via.placeholder.com/300'
futureboard_job.generate(save_as='job.png', future_board_option={
    'company': 'Something Company',
    'salary': '100,000 บาท'
})

#Create congrat image with option
#available option for congrat template:
# company: str ='บริษัท เอเชีย เอ็นจีเนียริ่ง',
# text: str ='สนใจสนทนากับพี่',
# background_color: str ='#e3c3d7',
# background_image: str ='congrats.png',
# logo_url_image: str ='https://via.placeholder.com/300'
futureboard_congratulation.generate(save_as='cong.png', future_board_option={
    'company': 'บริษัท กสิกร ซอฟต์',
    'logo_url_image': 'https://res-4.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco/ll9dkelmfnghuthajcrb'
})

```