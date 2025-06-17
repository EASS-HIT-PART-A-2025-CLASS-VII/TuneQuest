const API_CONFIG = {
    BACKEND_PORT: import.meta.env.BACKEND_PORT || '8000',
    MUSIC_SERVICE_PORT: import.meta.env.MUSIC_SERVICE_PORT || '8001',
    API_BASE_URL: import.meta.env.API_BASE_URL || 'http://localhost',
    MUSIC_SERVICE_BASE_URL: import.meta.env.MUSIC_SERVICE_BASE_URL || 'http://localhost'
};

export const API_URLS = {
    BACKEND: `${API_CONFIG.API_BASE_URL}:${API_CONFIG.BACKEND_PORT}`,
    MUSIC_SERVICE: `${API_CONFIG.MUSIC_SERVICE_BASE_URL}:${API_CONFIG.MUSIC_SERVICE_PORT}`
};