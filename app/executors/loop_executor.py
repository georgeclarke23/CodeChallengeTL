def loop_execute(actions):
    """The loop executor takes an all executable actions and gives it the context"""

    def wrapped_actions(context):
        for action in actions:
            try:
                action(context)
            except Exception as e:
                if not context.is_error:
                    context.set_error(e)
                raise

    return wrapped_actions
