
/**
 * REST API helper functions for NCI Lost & Found.
 * Version 0.4 - Svelte and FastAPI integration.
 */

// Read the backend address from the environment configuration.
// Use the local FastAPI server if no address is configured.
const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');


/**
 * Send an HTTP request to the FastAPI backend.
 *
 * @param {string} path - API endpoint to call.
 * @param {object} options - HTTP method, body and headers.
 * @returns {Promise<any>} Parsed JSON response or null for HTTP 204.
 */
async function request(path, options = {}) {

  // Send the request with JSON headers.
  const response = await fetch(`${API_URL}${path}`, {...options, headers: {'Content-Type': 'application/json', ...(options.headers || {})}});

  // Handle unsuccessful HTTP responses.
  if (!response.ok) {
    let message = `Request failed (${response.status})`;

    try {
      // Read the validation or error message from FastAPI.
      const body = await response.json();

      message = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail || body);

    } catch {
      // Keep the original HTTP error if JSON is unavailable.
    }

    throw new Error(message);
  }

  // DELETE returns HTTP 204 without JSON content.
  if (response.status === 204) {
    return null;
  }

  // Convert the JSON response into a JavaScript object.
  return response.json();
}


/**
 * Retrieve all reports or filter by lost/found category.
 *
 * @param {string} category - Optional category filter.
 */
export function getItems(category = '') {

  const query = category ? `?category=${encodeURIComponent(category)}` : '';

  return request(`/items${query}`);
}


/**
 * Create a new lost or found report.
 *
 * @param {object} item - Report information from the form.
 */
export function createItem(item) {

  return request('/items', {method: 'POST', body: JSON.stringify(item)});
}


/**
 * Update an existing report using its ID.
 *
 * @param {number} id - ID of the report to update.
 * @param {object} item - Updated report information.
 */
export function updateItem(id, item) {

  return request(`/items/${id}`, {method: 'PUT', body: JSON.stringify(item)});
}


/**
 * Delete an existing report using its ID.
 *
 * @param {number} id - ID of the report to delete.
 */
export function deleteItem(id) {

  return request(`/items/${id}`, {method: 'DELETE'});
}
