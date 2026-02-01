# Multi-Tenancy Frontend Integration Guide

This guide explains how the frontend should integrate with the Mantis multi-tenancy system using PostgreSQL Row-Level Security (RLS).

## Overview

The Mantis platform uses **database-level tenant isolation** via PostgreSQL RLS. The frontend does not need to manually filter data by tenant - all queries are automatically scoped to the user's tenant by the database.

## Key Concepts

### What the Frontend Needs to Know

1. **Automatic Data Isolation**: All API responses are already filtered by tenant. The frontend receives only data belonging to the user's tenant.

2. **JWT Token Contains `tenant_id`**: The JWT token includes a `tenant_id` claim that identifies which tenant the user belongs to.

3. **No Manual Filtering Required**: The frontend should NOT add `tenant_id` to API requests or filter responses manually.

## JWT Token Structure

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "email_verified": true,
  "tenant_id": "tenant-uuid",
  "iss": "http://localhost:8080/realms/mantis",
  "aud": "mantis-frontend",
  "exp": 1234567890,
  "iat": 1234567890
}
```

## API Response Examples

### User Profile (Includes `tenant_id`)

```typescript
// GET /users/me
{
  "id": "user-uuid",
  "email": "user@example.com",
  "is_active": true,
  "is_verified": true,
  "tenant_id": "tenant-uuid",  // Included for display purposes
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Items List (Automatically Filtered by Tenant)

```typescript
// GET /items/?page=1&size=10
{
  "items": [
    {
      "id": "item-uuid-1",
      "name": "Item 1",
      "description": "Description",
      "tenant_id": "tenant-uuid",  // Matches user's tenant_id
      "user_id": "user-uuid"
    },
    {
      "id": "item-uuid-2",
      "name": "Item 2",
      "description": "Description",
      "tenant_id": "tenant-uuid",  // All items have same tenant_id
      "user_id": "user-uuid"
    }
  ],
  "total": 2,
  "page": 1,
  "size": 10
}
```

## Frontend Implementation Guide

### 1. Display Tenant Information

Show the tenant name or ID in the user profile/dashboard:

```typescript
// Example: Display tenant info in user profile
function UserProfile({ user }: { user: User }) {
  return (
    <div>
      <h2>{user.email}</h2>
      <p>Tenant ID: {user.tenant_id}</p>
      {/* Optionally fetch and display tenant name */}
    </div>
  );
}
```

### 2. API Client Configuration

The frontend API client should:

1. Include the JWT `Authorization` header with all requests
2. NOT include `tenant_id` in query parameters or request body
3. Trust the backend to return correctly filtered data

```typescript
// Example API client configuration
const apiClient = createClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    // The JWT token contains tenant_id
    // Backend extracts it and sets database context
    Authorization: `Bearer ${token}`,
  },
});

// DO NOT do this (unnecessary):
const items = await apiClient.get('/items', {
  params: { tenant_id: user.tenant_id }  // ❌ WRONG
});

// DO this instead:
const items = await apiClient.get('/items');  // ✅ CORRECT
```

### 3. Authentication Flow

When a user logs in:

1. Frontend receives JWT token from Keycloak
2. Token is stored (e.g., in httpOnly cookie or localStorage)
3. All subsequent API requests include this token
4. Backend extracts `tenant_id` from token and sets database context
5. All queries automatically scoped to that tenant

```typescript
// Example: Login flow
async function login(credentials: LoginCredentials) {
  const response = await fetch('/auth/jwt/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });

  const { access_token } = await response.json();

  // Store token for future requests
  sessionStorage.setItem('token', access_token);

  // Token contains tenant_id - backend will use it
  return await fetchCurrentUser();
}
```

## Dashboard Display Recommendations

### Show Tenant Context

Display tenant information in the UI so users understand their context:

```typescript
// Example: Dashboard header
function DashboardHeader({ user }: { user: User }) {
  return (
    <header>
      <h1>Mantis Dashboard</h1>
      <div className="tenant-badge">
        <span>Tenant: {user.tenant_id}</span>
      </div>
    </header>
  );
}
```

### Tenant-Specific Branding (Optional)

If tenants have custom branding:

```typescript
// Fetch tenant details and apply theme
async function loadTenantTheme(tenantId: string) {
  const tenant = await apiClient.get(`/tenants/${tenantId}`);
  applyTheme(tenant.branding);
}
```

## Common Patterns

### List Views

```typescript
// Items list - automatically filtered by tenant
function ItemsList() {
  const { data } = useSWR('/items', fetcher);

  return (
    <ul>
      {data?.items.map(item => (
        <li key={item.id}>
          {item.name} {/* All items belong to user's tenant */}
        </li>
      ))}
    </ul>
  );
}
```

### Create Operations

```typescript
// Create item - tenant_id automatically set by backend
function CreateItemForm() {
  const handleSubmit = async (data: ItemCreate) => {
    // DO NOT include tenant_id in request
    await apiClient.post('/items', {
      name: data.name,
      description: data.description,
      // tenant_id is automatically set from authenticated user
    });
  };
}
```

## Security Notes

1. **Never Trust Client-Side `tenant_id`**: Always use the `tenant_id` from the JWT token validated by the backend.

2. **No Manual Filtering**: The frontend should not filter data by `tenant_id` - this is done at the database level.

3. **Display Only**: The `tenant_id` in API responses is for display purposes only. Do not use it for filtering or access control decisions.

## Troubleshooting

### Seeing Data from Other Tenants?

This should never happen with RLS enabled. If you see data from other tenants:

1. Check that JWT token is being sent with requests
2. Verify backend tenant middleware is running
3. Check database RLS policies are enabled

### Empty Results When Data Should Exist?

1. Verify user's `tenant_id` in JWT matches data's `tenant_id`
2. Check backend logs for tenant context errors
3. Ensure RLS policies are correctly configured

## API Reference

### User Endpoints

| Endpoint | Response Includes Tenant Info? |
|----------|-------------------------------|
| `GET /users/me` | Yes: `tenant_id` field |
| `GET /users/{id}` | Yes: `tenant_id` field |

### Data Endpoints

All data endpoints (`/items`, etc.) return objects with `tenant_id` field for display purposes, but data is automatically filtered by the backend.

## Questions?

Contact the backend team for questions about multi-tenancy implementation.
