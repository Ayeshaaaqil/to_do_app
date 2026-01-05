# Data Model: Phase II Todo Web Application

## Entity: User

**Description**: Represents an authenticated user with credentials and account information

**Fields**:
- `id` (UUID/Integer): Unique identifier for the user
- `email` (String): User's email address (unique, required)
- `name` (String): User's display name (optional)
- `hashed_password` (String): Hashed password for authentication
- `created_at` (DateTime): Timestamp when the user account was created
- `updated_at` (DateTime): Timestamp when the user account was last updated
- `is_active` (Boolean): Whether the user account is active

**Relationships**:
- One-to-many with Todo (one user can have many todos)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (length, complexity)
- Name must not exceed 100 characters if provided

## Entity: Todo

**Description**: Represents a task with title, description, completion status, and association to a user

**Fields**:
- `id` (UUID/Integer): Unique identifier for the todo
- `title` (String): Title of the todo item (required)
- `description` (String): Detailed description of the todo (optional)
- `is_completed` (Boolean): Whether the todo is completed (default: false)
- `user_id` (UUID/Integer): Foreign key linking to the user who owns this todo
- `created_at` (DateTime): Timestamp when the todo was created
- `updated_at` (DateTime): Timestamp when the todo was last updated

**Relationships**:
- Many-to-one with User (many todos belong to one user)

**Validation Rules**:
- Title must not be empty
- Title must not exceed 200 characters
- Description must not exceed 1000 characters if provided
- User_id must reference an existing user
- A todo cannot be marked as completed if it has already been deleted

## Entity: Authentication Session (Implicit)

**Description**: Represents the authenticated state of a user during their session (handled by Better Auth)

**Fields**:
- `session_token` (String): Unique token for the session
- `user_id` (UUID/Integer): Reference to the authenticated user
- `expires_at` (DateTime): Expiration time of the session
- `created_at` (DateTime): When the session was created

**Notes**:
- This entity is primarily managed by Better Auth
- Implementation details will follow Better Auth's session management patterns
- The application will validate session tokens on protected endpoints

## State Transitions

### Todo State Transitions
- **Created**: When a new todo is added (is_completed = false)
- **Updated**: When the todo details are modified (title, description)
- **Completed**: When the todo is marked as complete (is_completed = true)
- **Reopened**: When a completed todo is marked as incomplete (is_completed = false)
- **Deleted**: When the todo is removed (soft delete or hard delete)

### User State Transitions
- **Registered**: When a new user signs up
- **Activated**: When a user's account is active and can access the system
- **Deactivated**: When a user's account is temporarily disabled
- **Deleted**: When a user account is removed (if supported)

## Data Ownership Rules

1. Each todo must be associated with exactly one user
2. Users can only access, modify, or delete their own todos
3. The system must enforce data ownership at the API level
4. Database queries must always filter by the authenticated user's ID
5. Attempting to access another user's data should result in a 404 (Not Found) or 403 (Forbidden) error