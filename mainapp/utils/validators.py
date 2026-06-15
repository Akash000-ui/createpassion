import os
from django.core.exceptions import ValidationError


ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
MAX_IMAGE_SIZE_MB = 5


def validate_image_file(file):
    """Validate uploaded image: extension and size."""
    if not file:
        return
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f'Invalid file type. Allowed: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
        )
    max_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if file.size > max_bytes:
        raise ValidationError(f'File size must not exceed {MAX_IMAGE_SIZE_MB} MB.')


def validate_kyc_image(file):
    """Validate KYC document image: jpg/jpeg/png only, max 1 MB. Returns error string or None."""
    if not file:
        return None
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        return 'Invalid format. Allowed: JPEG, JPG, PNG.'
    if file.size > 1 * 1024 * 1024:
        return 'File size must not exceed 1 MB.'
    return None


def validate_mobile(mobile):
    """Return True if mobile is a valid 10-digit Indian number."""
    mobile = str(mobile).strip()
    return mobile.isdigit() and len(mobile) == 10


def validate_pincode(pincode):
    """Return True if pincode is a valid 6-digit Indian pincode."""
    pincode = str(pincode).strip()
    return pincode.isdigit() and len(pincode) == 6


def validate_pan(pan):
    """Basic PAN format check: AAAAA9999A"""
    import re
    return bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', str(pan).upper()))


def validate_ifsc(ifsc):
    """Basic IFSC format check: 4 letters + 0 + 6 alphanumeric"""
    import re
    return bool(re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', str(ifsc).upper()))
