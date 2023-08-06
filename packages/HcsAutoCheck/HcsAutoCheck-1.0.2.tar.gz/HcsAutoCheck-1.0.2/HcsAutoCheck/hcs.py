class Hcs:
    import requests
    from . import data, encrypt

    def __init__(self, name: str, birth: str, area: str, school: str, level: str, password: str):
        self.name = name
        self.birth = birth
        self.area = area
        self.school = school
        self.level = level
        self.password = password

    def run(self):
        area = self.data.get_area(self.area)
        if area == None:
            return {'type': 'error', 'message': 'NOT_EXIST_AREA'}
        
        level = self.data.get_level(self.level)
        if level == None:
            return {'type': 'error', 'message': 'NOT_EXIST_LEVEL'}

        response = self.requests.get('https://hcs.eduro.go.kr/v2/searchSchool', params={
            'lctnScCode': area[0],
            'schulCrseScCode': level,
            'orgName': self.school,
        })

        json = response.json()

        if 'isError' in json:
            return {'type': 'error', 'message': 'UNKNOWN'}

        if len(json['schulList']) == 0:
            return {'type': 'error', 'message': 'NOT_EXIST_SCHOOL'}

        school = json['schulList'][0]['orgCode']

        name = self.encrypt.encrypt(self.name)
        birth = self.encrypt.encrypt(self.birth)

        response = self.requests.post(f'https://{area[1]}hcs.eduro.go.kr/v2/findUser', json={
            'orgCode': school,
            'name': name,
            'birthday': birth,
        })

        json = response.json()

        if 'isError' in json:
            return {'type': 'error', 'message': 'WRONG_NAME_OR_BIRTH'}

        token = json['token']

        password = self.encrypt.encrypt(self.password)

        response = self.requests.post(f'https://{area[1]}hcs.eduro.go.kr/v2/validatePassword', headers={'Authorization': token}, json={
            'password': password
        })

        if 'isError' in json:
            return {'type': 'error', 'message': 'WRONG_PASSWORD'}

        token = response.json()

        response = self.requests.post(f'https://{area[1]}hcs.eduro.go.kr/registerServey', headers={'Authorization': token}, json={
            'rspns01': '1',
            'rspns02': '1',
            'rspns00': 'Y',
            'upperToken': token,
            'upperUserNameEncpt': 'HcsAutoCheck',
        })

        json = response.json()

        if 'isError' in json:
            return {'type': 'error', 'message': 'UNKNOWN'}

        return {'type': 'success', 'message': json['registerDtm']}