import { API_URLS } from '../config/api';

export const fetchWithService = async (path: string, service: 'BACKEND' | 'MUSIC_SERVICE', options: RequestInit = {}) => {
  const url = `${API_URLS[service]}${path}`;
  return fetch(url, options);
};