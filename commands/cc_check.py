from telegram import Update
from telegram.ext import CallbackContext
import re
from datetime import datetime


# Luhn Algorithm for Credit Card Validation
def validate_luhn(card_number):
    card_number = card_number.replace(" ", "")
    reverse_digits = card_number[::-1]
    total = 0

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Double every second digit
            n *= 2
            if n > 9:  # If result is two digits, subtract 9
                n -= 9
        total += n
    return total % 10 == 0


# Check if Expiry Date is Valid
def validate_expiry_date(expiry_date):
    try:
        expiry = datetime.strptime(expiry_date, "%m/%y")
        return expiry > datetime.now()
    except ValueError:
        return False


# Validate CVV
def validate_cvv(cvv, card_type):
    if card_type.lower() in ['amex']:  # AMEX has 4-digit CVV
        return bool(re.fullmatch(r"\d{4}", cvv))
    else:  # Visa, MasterCard, etc. have 3-digit CVV
        return bool(re.fullmatch(r"\d{3}", cvv))


# Detect Card Type Based on BIN (IIN ranges)
def detect_card_type(card_number):
    card_number = card_number.replace(" ", "")
    if card_number.startswith(('4',)):  # Visa
        return "Visa"
    elif card_number.startswith(('5',)):  # MasterCard
        return "MasterCard"
    elif card_number.startswith(('34', '37')):  # AMEX
        return "American Express"
    elif card_number.startswith(('6',)):  # Discover
        return "Discover"
    else:
        return "Unknown"


# Check 3DSecure (VBV or Non-VBV)
def check_3ds_secure(card_number):
    # Mock logic to determine 3DSecure status
    secure_bins = ["401288", "511111"]  # Example secure BINs
    return card_number[:6] in secure_bins


# Main Mass CC Checker Handler Function
def handle_cccheck(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text(
            "Please provide card details in the format: `/cccheck <card_number_1> <expiry_date_1> <cvv_1> / <card_number_2> <expiry_date_2> <cvv_2> ...`")
        return

    results = []

    for arg in context.args:
        card_details = arg.split(",")  # Assume each input is comma-separated
        if len(card_details) != 3:
            results.append(f"Invalid format for {arg}, please use: <card_number>,<expiry_date>,<cvv>")
            continue

        card_number, expiry_date, cvv = card_details

        # Validate the card details
        card_type = detect_card_type(card_number)
        is_luhn_valid = validate_luhn(card_number)
        is_expiry_valid = validate_expiry_date(expiry_date)
        is_cvv_valid = validate_cvv(cvv, card_type)
        is_3ds_secure = check_3ds_secure(card_number)

        # Prepare the validation result for this card
        result = (
            f"Card Type: {card_type}\n"
            f"Luhn Valid: {'Yes' if is_luhn_valid else 'No'}\n"
            f"Expiry Valid: {'Yes' if is_expiry_valid else 'No'}\n"
            f"CVV Valid: {'Yes' if is_cvv_valid else 'No'}\n"
            f"3DSecure (VBV/Non-VBV): {'Yes' if is_3ds_secure else 'No'}\n"
            f"Overall Valid: {'Yes' if (is_luhn_valid and is_expiry_valid and is_cvv_valid) else 'No'}\n"
        )

        results.append(result)

    # Send the result back to the user
    update.message.reply_text("\n\n".join(results))