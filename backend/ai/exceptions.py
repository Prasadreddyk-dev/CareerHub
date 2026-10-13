class AIServiceError(Exception):
    status_code = 502
    code = "ai_error"
    message = "The AI service failed."

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class AINotConfiguredError(AIServiceError):
    status_code = 503
    code = "ai_not_configured"
    message = "AI analysis is not configured on this server."


class AITimeoutError(AIServiceError):
    status_code = 504
    code = "ai_timeout"
    message = "The AI service timed out. Please try again."


class AIRateLimitError(AIServiceError):
    status_code = 429
    code = "ai_rate_limited"
    message = "The AI service is rate limited. Please try again later."


class AIProviderError(AIServiceError):
    status_code = 502
    code = "ai_provider_error"
    message = "The AI provider returned an error."


class AIInvalidResponseError(AIServiceError):
    status_code = 502
    code = "ai_invalid_response"
    message = "The AI returned an unusable response."