# SRN POST - Unique SRN Reference Number Implementation

## Overview
This implementation provides automatic generation of unique 4-digit SRN Reference numbers for the SRN POST doctype in the ISRO CMS system.

## Features
- **Automatic Generation**: SRN Reference numbers are automatically generated when creating a new SRN POST document
- **Uniqueness**: Ensures all generated numbers are unique across the system
- **4-Digit Format**: Generates numbers between 1000-9999
- **Client-Side Preview**: Shows a preview number when opening a new document
- **Server-Side Validation**: Final unique number is generated and validated on the server

## Files Created
1. **srn_post.py** - Main Python class with generation logic
2. **srn_post.js** - Client-side JavaScript for UI interactions
3. **srn_post.json** - DocType definition with proper field configuration
4. **test_srn_post.py** - Unit tests for the implementation
5. **__init__.py** - Python module initialization

## How It Works

### Server-Side (Python)
- `generate_unique_srn_ref_no()`: Generates a unique 4-digit number
- Uses random generation with fallback to sequential numbering
- Checks database for existing numbers to ensure uniqueness
- Automatically called during document validation and before save

### Client-Side (JavaScript)
- Shows a preview number when creating a new document
- Provides a "Generate SRN Ref No" button for manual generation
- Validates input to ensure 4-digit format
- Calls server-side method to get the final unique number

### Database Integration
- The `srn_ref_no` field is marked as unique in the database
- Uses Frappe's built-in validation to prevent duplicate entries
- Automatically handles database constraints

## Usage
1. Open the SRN POST doctype
2. A preview SRN Reference number will be automatically filled
3. Click "Generate SRN Ref No" button to get the final unique number
4. Save the document - the unique number will be automatically assigned

## Testing
The implementation includes comprehensive tests that verify:
- Number generation within the correct range (1000-9999)
- Uniqueness of generated numbers
- Proper handling of existing numbers
- Client-side validation

## Error Handling
- Prevents infinite loops during number generation
- Falls back to sequential numbering if random generation fails
- Validates input format on both client and server side
- Provides user-friendly error messages

## Security
- Server-side validation ensures data integrity
- Whitelisted methods for client-server communication
- Proper permission checks for document access
