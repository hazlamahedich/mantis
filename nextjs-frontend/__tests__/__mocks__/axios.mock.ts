/**
 * Axios mock for testing API calls without backend dependencies.
 *
 * This mock intercepts all axios requests and returns configurable responses.
 * Use this in unit tests to avoid making actual network calls.
 *
 * Usage in tests:
 * ```typescript
 * import axios from 'axios';
 * import { mockAxiosResponse, mockAxiosError } from '@/__mocks__/axios';
 *
 * // Mock successful response
 * jest.spyOn(axios, 'get').mockResolvedValue(mockAxiosResponse({ data: 'test' }));
 *
 * // Mock error response
 * jest.spyOn(axios, 'post').mockRejectedValue(mockAxiosError(400, 'Bad Request'));
 * ```
 */

import { AxiosError, InternalAxiosRequestConfig, AxiosResponse } from "axios";

/**
 * Create a mock Axios response
 */
export function mockAxiosResponse<T = unknown>(
  data: T,
  status = 200,
  statusText = "OK",
): AxiosResponse<T> {
  return {
    data,
    status,
    statusText,
    headers: {},
    config: {} as InternalAxiosRequestConfig,
  };
}

/**
 * Create a mock Axios error
 */
export function mockAxiosError(
  status = 500,
  message = "Internal Server Error",
  code?: string,
): AxiosError {
  const error = new AxiosError(message);
  error.status = status;
  error.code = code;
  return error;
}

/**
 * Reset all axios mocks
 */
export function resetAxiosMocks(): void {
  jest.clearAllMocks();
}

/**
 * Default mock implementations
 */
export const axiosMocks = {
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  patch: jest.fn(),
};

export default axiosMocks;
