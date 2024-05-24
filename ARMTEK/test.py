from requests import Session
import json

import winsound

from armtek_config import Config
from main import Armtek_Parts_Information

req_sess: Session = Session()

test_result = Armtek_Parts_Information(original_part_number='19260034S', session=req_sess, config=Config(req_sess))

with open('test_result.json', "w", encoding='utf-8') as file:
    json.dump(test_result.return_result(), file, indent=4)
    print('mission completed')
    frequency = 1000  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
print(test_result)
