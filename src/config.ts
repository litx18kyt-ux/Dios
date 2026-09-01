export const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (window.location.hostname.includes('github.dev') || window.location.hostname.includes('localhost') 
    ? '/api' 
    : 'https://dios-cbo-bot.onrender.com/api');
