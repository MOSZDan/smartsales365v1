"""
Custom validators for user inputs to enhance security.
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_no_special_chars_in_name(value):
    """
    Validate that name doesn't contain potentially dangerous characters.
    """
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", value):
        raise ValidationError(
            _('Name can only contain letters, spaces, hyphens, and apostrophes.'),
            code='invalid_name'
        )


def validate_email_domain(value):
    """
    Validate email domain is not from a disposable email provider.
    This is a basic implementation - consider using a library like
    'disposable-email-domains' for production.
    """
    disposable_domains = [
        'tempmail.com', 'guerrillamail.com', '10minutemail.com',
        'mailinator.com', 'trashmail.com', 'throwaway.email'
    ]

    domain = value.split('@')[-1].lower()
    if domain in disposable_domains:
        raise ValidationError(
            _('Please use a permanent email address.'),
            code='disposable_email'
        )


def validate_password_strength(password):
    """
    Additional password strength validation beyond Django's defaults.
    """
    if len(password) < 8:
        raise ValidationError(
            _('Password must be at least 8 characters long.'),
            code='password_too_short'
        )

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            _('Password must contain at least one uppercase letter.'),
            code='password_no_upper'
        )

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            _('Password must contain at least one lowercase letter.'),
            code='password_no_lower'
        )

    # Check for at least one digit
    if not re.search(r'\d', password):
        raise ValidationError(
            _('Password must contain at least one number.'),
            code='password_no_digit'
        )

    # Check for common patterns
    common_patterns = ['123456', 'password', 'qwerty', 'abc123']
    if any(pattern in password.lower() for pattern in common_patterns):
        raise ValidationError(
            _('Password contains a common pattern. Please choose a stronger password.'),
            code='password_too_common'
        )


def validate_image_file_extension(value):
    """
    Validate uploaded image file extensions.
    """
    import os
    from django.conf import settings

    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.gif', '.webp'])

    if ext not in allowed_extensions:
        raise ValidationError(
            _(f'File extension {ext} is not allowed. Allowed extensions: {", ".join(allowed_extensions)}'),
            code='invalid_extension'
        )


def validate_image_file_size(value):
    """
    Validate uploaded image file size.
    """
    from django.conf import settings

    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5242880)  # 5MB default

    if value.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(
            _(f'File size exceeds maximum allowed size of {max_size_mb}MB.'),
            code='file_too_large'
        )


def sanitize_html_input(value):
    """
    Remove potentially dangerous HTML tags and attributes.
    For production, consider using libraries like 'bleach' or 'html-sanitizer'.
    """
    import re

    # Remove script tags
    value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.DOTALL | re.IGNORECASE)

    # Remove on* event handlers
    value = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', value, flags=re.IGNORECASE)

    # Remove javascript: protocol
    value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)

    return value.strip()
