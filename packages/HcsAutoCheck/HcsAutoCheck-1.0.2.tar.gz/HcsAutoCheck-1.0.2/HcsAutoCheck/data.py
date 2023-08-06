area_data = (
    ('서울', '서울시', '서울교육청', '서울시교육청', '서울특별시','서울특별시교육청'),
    ('부산', '부산광역시', '부산시', '부산교육청', '부산광역시교육청'),
    ('대구', '대구광역시', '대구시', '대구교육청', '대구광역시교육청'),
    ('인천', '인천광역시', '인천시', '인천교육청', '인천광역시교육청'),
    ('광주', '광주광역시', '광주시', '광주교육청', '광주광역시교육청'),
    ('대전', '대전광역시', '대전시', '대전교육청', '대전광역시교육청'),
    ('울산', '울산광역시', '울산시', '울산교육청', '울산광역시교육청'),
    ('세종', '세종특별시', '세종시', '세종교육청', '세종특별자치시', '세종특별자치시교육청'),
    (),
    ('경기', '경기도', '경기교육청', '경기도교육청'),
    ('강원', '강원도', '강원교육청', '강원도교육청'),
    ('충북', '충청북도', '충북교육청', '충청북도교육청'),
    ('충남', '충청남도', '충남교육청', '충청남도교육청'),
    ('전북', '전라북도', '전북교육청', '전라북도교육청'),
    ('전남', '전라남도', '전남교육청', '전라남도교육청'),
    ('경북', '경상북도', '경북교육청', '경상북도교육청'),
    ('경남', '경상남도', '경남교육청', '경상남도교육청'),
    ('제주', '제주도', '제주특별자치시', '제주교육청', '제주도교육청', '제주특별자치시교육청', '제주특별자치도'),
)

area_data_url_code = ('sen', 'pen', 'dge', 'ice', 'gen', 'dje', 'use', 'sje', None, 'goe', 'kwe', 'cbe', 'cne', 'jbe', 'jne', 'gbe', 'gne', 'jje')

level_data = (
    ('유치원', '유', '유치'),
    ('초등학교', '초', '초등'),
    ('중학교', '중', '중등'),
    ('고등학교', '고', '고등'),
    ('특수학교', '특', '특수', '특별'),
)

def get_area(area_name: str):
    for area_list in area_data:
        for area in area_list:
            if area_name == area:
                index = area_data.index(area_list)
                if index + 1 < 10:
                    area_code = '0' + str(index + 1)
                else:
                    area_code = str(index + 1)
                return (area_code, area_data_url_code[index])

def get_level(level_name: str):
    for level_list in level_data:
        for level in level_list:
            if level_name == level:
                index = level_data.index(level_list)
                return str(index + 1)