import time


def retry_execute(action, retries=3, wait=10):
    def wrapped_action(context):
        retry = 0
        is_complete = False
        while (not is_complete) and (retry <= retries):
            if retry > 0:
                context.rollback_state()
                context.debug(
                    "Retry_executor",
                    "Retrying ... wait for {}".format(wait),
                )
                time.sleep(wait)

            context.snapshot_state()
            try:
                action(context)
            except Exception as e:
                context.set_error(e)

            is_complete = not context.is_error
            retry += 1

        if not context.is_error:
            return
        else:
            raise context.errors[-1]

    return wrapped_action
