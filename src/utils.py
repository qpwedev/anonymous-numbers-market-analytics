import asyncio
from typing import Optional


class RetryError(Exception):
    pass


def async_retry(
    retry_on_exception: Optional[callable] = None,
    stop_max_attempt_number: Optional[int] = None,
    wait_fixed: Optional[float] = None,
    return_on_error: Optional[callable] = None,
):
    def wrap(f):
        async def wrapped_f(*args, **kwargs):
            attempt_number = 1
            actual_exception = None
            while True:
                try:
                    return await f(*args, **kwargs)
                except Exception as e:
                    if retry_on_exception and not retry_on_exception(e):
                        if return_on_error:
                            return return_on_error()

                        raise e
                    else:
                        actual_exception = e

                    if stop_max_attempt_number and stop_max_attempt_number <= attempt_number:
                        if return_on_error:
                            return return_on_error()

                        if actual_exception:
                            raise actual_exception

                        raise RetryError(f'{stop_max_attempt_number} attempts error')

                if wait_fixed:
                    await asyncio.sleep(wait_fixed)

                attempt_number += 1

        return wrapped_f

    return wrap
