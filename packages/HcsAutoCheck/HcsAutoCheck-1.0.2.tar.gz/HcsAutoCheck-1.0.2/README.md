# HcsAutoCheck
파이썬 자가진단 자동화

## Install
```shell
pip install HcsAutoCheck
```

## Example
```python
import HcsAutoCheck

hcs = HcsAutoCheck.Hcs('이름', '생년월일', '지역', '학교', '학교종류', '비밀번호')
result = hcs.run()

if result['type'] == 'error':
    print('Error: ' + result['message'])
else:
    print('Time: ' + result['message'])
```