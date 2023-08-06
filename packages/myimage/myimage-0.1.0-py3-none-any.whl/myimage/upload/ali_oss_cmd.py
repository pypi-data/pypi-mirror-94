import sys
import os
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, p)
from myimage.upload.ali_oss import AliOss


"""
test command:
# single img test
/Users/mark/PycharmProjects/mark_scripts/venv/bin/python /Users/mark/PycharmProjects/mark_scripts/myimage/ali_oss_upload_terminal.py /Users/mark/Pictures/xx.jpg

# multi imgs test
/Users/mark/PycharmProjects/mark_scripts/venv/bin/python /Users/mark/PycharmProjects/mark_scripts/myimage/ali_oss_upload_terminal.py  /Users/mark/Pictures/xx.jpg /Users/mark/Pictures/xx.jpg  
"""

if __name__ == '__main__':
    ali_oss = AliOss()
    results = ali_oss.upload_multi_imgs(sys.argv[1:])
    for result in results:
        print(result["url"])
