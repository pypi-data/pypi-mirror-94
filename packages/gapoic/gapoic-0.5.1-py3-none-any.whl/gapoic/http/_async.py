from asyncio import iscoroutinefunction
from pydantic import BaseModel, ValidationError
from .base import AbstractRequest

try:
    from logzero import logger
except ImportError:
    import logging as logger


class Request(AbstractRequest):
    async def get(self, **params):
        try:
            if hasattr(self, "Params"):
                params = self.Params(**params).dict()

            headers = self.headers.dict()
            request_cfg = {"params": params, "headers": headers}

            async with self._cl.get(self.url, **request_cfg) as resp:
                if resp.status != 200:
                    msg = "Url=%s, API call unsuccesful => %s"
                    text = await resp.text()
                    logger.error(msg, self.url, text)
                    return self.on_failure(resp)

                json = await resp.json()

                if iscoroutinefunction(self.on_success):
                    return await self.on_success(json)

                return self.on_success(json)

        except ValidationError as err:
            logger.error("Url=%s, Invalid query-param: %s", self.url, err)
            return self.on_error(err)

        except Exception as err:
            logger.error("Url=%s, API call error: %s", self.url, err)
            return self.on_error(err)

    def on_failure(self, response):
        pass

    def on_error(self, error):
        pass

    def on_success(self, json_data):
        if hasattr(self, "Response"):
            return self.Response(**json_data)

        if hasattr(self, "response"):
            return self.response(**json_data)

        return json_data
