def execute(action):
    """The executor takes an action and gives it the context"""

    def wrapped_action(context):
        try:
            action(context)
        except Exception as exc_info:
            if not context.is_error:
                context.set_error(exc_info)
            raise

    return wrapped_action
