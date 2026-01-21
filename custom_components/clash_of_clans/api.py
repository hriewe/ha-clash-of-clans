import aiohttp

API_BASE = "https://api.clashofclans.com/v1"


class ClashOfClansApi:
    def __init__(self, token):
        self._headers = {
            "Authorization": f"Bearer {token}"
        }

    async def _get(self, endpoint):
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(endpoint) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def get_player(self, tag):
        tag = tag.replace("#", "%23")
        return await self._get(f"{API_BASE}/players/{tag}")

    async def get_current_war(self, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")
        return await self._get(
            f"{API_BASE}/clans/{clan_tag}/currentwar"
        )