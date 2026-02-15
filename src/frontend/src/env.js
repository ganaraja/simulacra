/**
 * Environment config. In tests this module is replaced by env.test.js so Jest does not need import.meta.
 */
export function getApiBase() {
  if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE != null) {
    return import.meta.env.VITE_API_BASE;
  }
  return '';
}
