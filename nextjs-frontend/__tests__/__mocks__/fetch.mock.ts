/**
 * Fetch API mock for testing API calls without backend dependencies.
 *
 * This mock intercepts all fetch requests and returns configurable responses.
 * Use this in unit tests to avoid making actual network calls.
 *
 * Usage in tests:
 * ```typescript
 * import { mockFetchResponse, mockFetchError } from '@/__mocks__/fetch';
 *
 * // Mock successful response
 * global.fetch = jest.fn().mockResolvedValue(mockFetchResponse({ data: 'test' }));
 *
 * // Mock error response
 * global.fetch = jest.fn().mockRejectedValue(mockFetchError(400, 'Bad Request'));
 * ```
 */

export interface MockFetchResponseInit {
  status?: number;
  statusText?: string;
  headers?: Record<string, string>;
}

/**
 * Create a mock fetch Response object
 */
export function mockFetchResponse(
  data: any,
  init: MockFetchResponseInit = {}
): Response {
  const { status = 200, statusText = 'OK', headers = {} } = init;

  return {
    ok: status >= 200 && status < 300,
    status,
    statusText,
    headers: new Headers(headers),
    json: async () => data,
    text: async () => JSON.stringify(data),
    blob: async () => new Blob([JSON.stringify(data)]),
    arrayBuffer: async () => new TextEncoder().encode(JSON.stringify(data)).buffer,
    clone: () => mockFetchResponse(data, init),
    body: null,
    bodyUsed: false,
  } as Response;
}

/**
 * Create a mock fetch error
 */
export function mockFetchError(
  status = 500,
  message = 'Internal Server Error'
): Error {
  const error = new Error(message);
  (error as any).status = status;
  return error;
}

/**
 * Reset fetch mock
 */
export function resetFetchMock(): void {
  if (global.fetch) {
    jest.clearAllMocks();
  }
}

/**
 * Setup fetch mock with default responses
 */
export function setupFetchMock(): void {
  global.fetch = jest.fn();
}

export default { mockFetchResponse, mockFetchError, resetFetchMock, setupFetchMock };
