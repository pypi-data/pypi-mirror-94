from enum import Enum


class EnvName(Enum):
    STAGING = "staging"
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"



def is_production(*, environment: str) -> bool:
    return environment == EnvName.PRODUCTION.value


def is_staging(*, environment: str) -> bool:
    return environment == EnvName.STAGING.value


def is_testing(*, environment: str) -> bool:
    return environment == EnvName.TESTING.value


def is_development(*, environment: str) -> bool:
    return environment == EnvName.DEVELOPMENT.value


