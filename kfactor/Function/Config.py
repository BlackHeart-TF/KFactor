class Config:
    _config = {}

    @staticmethod
    def get(key, default=None):
        return Config._config.get(key, default)

    @staticmethod
    def set(key, value):
        Config._config[key] = value

    @staticmethod
    def get_all():
        return Config._config
    
    @staticmethod
    def load(config:dict):
        Config._config = config

