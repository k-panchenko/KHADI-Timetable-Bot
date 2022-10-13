from typing import Union

import aiohttp


class KHADIClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self._base_url = base_url
        self._timeout = timeout

    async def get_timetable_from_server(self, faculty_id: Union[str, int], course: Union[str, int],
                                        group_id: Union[str, int]) -> bytes:
        cookies = {
            '_csrf-frontend': 'e16d6c209f84adf52830964505c618b84dfe86306507d39ef0fdb9e85af0e4a0a%3A2%3A%7Bi%3A0%3Bs%3A1'
                              '4%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228mQLvU7KmkT1uQ5r1LvhFvZsFs9LHMqk%22%3B%7D'
        }

        params = {
            'type': '0',
        }

        data = {
            '_csrf-frontend': 'l547P68_3nvb_4rM2P-KQQVi5-DkWUT4YfIiC_0XK-uv'
                              '82pz2WrpMLaU3v2trr8zNC6RiKIvHosngRtHtVpagA==',
            'TimeTableForm[facultyId]': faculty_id,  # 3
            'TimeTableForm[course]': course,  # 1
            'TimeTableForm[groupId]': group_id,  # 1046
        }

        async with aiohttp.ClientSession(self._base_url, cookies=cookies) as session:
            async with session.get('/time-table/group', data=data, params=params, timeout=self._timeout) as response:
                return await response.read()

    async def get_details(self, data_r1: str, data_r2: str) -> bytes:
        params = {
            'r1': data_r1,
            'r2': data_r2
        }

        headers = {
            'X-Requested-With': 'XMLHttpRequest'
        }

        async with aiohttp.ClientSession(self._base_url, headers=headers) as session:
            async with session.get('/time-table/show-ads', params=params, timeout=self._timeout) as response:
                return await response.read()
