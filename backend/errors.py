class PetAppError(Exception):
    """Classe base para todas as exceções de domínio do projeto."""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ExternalServiceError(PetAppError):
    """Exceção para falhas ao se comunicar ou processar APIs de serviços externos (ex: OpenRouter)."""
    def __init__(self, message="Falha de comunicação ou processamento no serviço de Inteligência Artificial.", status_code=502):
        super().__init__(message, status_code)


class DatabaseIntegrationError(PetAppError):
    """Exceção para falhas de persistência ou de comunicação com o Supabase."""
    def __init__(self, message="Falha ao integrar dados ou conectar com o serviço de banco de dados.", status_code=503):
        super().__init__(message, status_code)