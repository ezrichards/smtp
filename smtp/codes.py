# SMTP Server Reply Codes (see RFC 5321 4.2.3)

# 2yz Positive Completion
SYSTEM_STATUS = (211, 'System status, or system help reply')
HELP = (214, 'Help message')
SERVICE_READY = (220, 'Service ready')
SERVICE_CLOSING = (221, 'Service closing transmission channel')
QUIT = (240, 'QUIT')
REQUESTED_MAIL_ACTION_OK = (250, 'Requested mail action okay, completed')

# 5yz Permanent Negative Completion (Errors)
SYNTAX_ERROR_COMMAND = (500, 'Syntax error, command unrecognized') # can include command line too long
SYNTAX_ERROR = (501, 'Syntax error in parameters or arguments')
COMMAND_NOT_IMPLEMENTED = (502, 'Command not implemented')
BAD_SEQUENCE = (503, 'Bad sequence of commands')
PARAMETER_NOT_IMPLEMENTED = (504, 'Command parameter not implemented')
