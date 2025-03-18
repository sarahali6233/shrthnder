"""
macOS-specific configuration settings.
"""

# Feature flags
USE_OPTIMIZED_INPUT = False  # Set to True to use the optimized implementation

# Performance tuning
PASTE_DELAY = 0.01  # Delay in seconds for paste operations
DELETE_BATCH_SIZE = 10  # Maximum number of characters to delete in one batch

# Fallback settings
MAX_RETRY_ATTEMPTS = 3  # Number of times to retry an operation before falling back
FALLBACK_DELAY = 0.02  # Delay to use when falling back to original implementation 