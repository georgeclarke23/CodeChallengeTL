def close_sessions(context):
    """Close all sessions in the context"""
    context.close_sessions()
    context.debug("CloseSessions", "All session are closed")
