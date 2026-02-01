/**
 * Custom test render utilities for React Testing Library.
 *
 * This module provides custom render functions that wrap components
 * with necessary providers (Theme, Auth, etc.) for consistent testing.
 *
 * Usage:
 * ```typescript
 * import { render, screen } from '@/test-utils';
 *
 * test('renders component', () => {
 *   render(<MyComponent />);
 *   expect(screen.getByText('Hello')).toBeInTheDocument();
 * });
 * ```
 */

import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';

/**
 * Custom render function that wraps components with providers
 *
 * Add providers here as needed (e.g., AuthProvider, ThemeProvider, etc.)
 */
export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  function AllTheProviders({ children }: { children: React.ReactNode }) {
    // Add providers here as your application grows
    // Example:
    // return (
    //   <AuthProvider>
    //     <ThemeProvider>
    //       {children}
    //     </ThemeProvider>
    //   </AuthProvider>
    // );
    return <>{children}</>;
  }

  return render(ui, { wrapper: AllTheProviders, ...options });
}

/**
 * Re-export everything from React Testing Library
 */
export * from '@testing-library/react';

/**
 * Re-export screen for convenience
 */
export { screen } from '@testing-library/react';

/**
 * Default render function (alias for renderWithProviders)
 */
export const render = renderWithProviders;
