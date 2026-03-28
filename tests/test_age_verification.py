import time
import pytest
from pages.age_verification_page import AgeVerificationPage

#Test for age exactly 18y/o, 20, 40 - positive - parameterise for all positives
@pytest.mark.parametrize("dob", [
    "07-11-2007",  # Exactly 18 years old (boundary)
    "06-11-2007",  # Just over 18
    "01-01-2000",  # Clearly over 18
])
def test_age_verification_valid(driver, dob):
    """BVA: Verify access is granted for users aged 18 or older."""
    driver.get("https://grocerymate.masterschool.com/store")
    age_verification_page = AgeVerificationPage(driver)

    age_verification_page.handle_age_verification(dob)
    popup_text = age_verification_page.get_popup_text()

    assert "You are of age" in popup_text, f"Expected 'You are of age' for DOB: {dob}"


#test for underage - negative include no date or false date
@pytest.mark.parametrize("dob", [
    "",  # empty date field (boundary)
    "XX-XX-XXXX", # invalid date entry
    "09-11-2007",  # Just under 18
    "01-01-2020",  # Clearly under 18
])
def test_age_verification_invalid(driver, dob):
    """BVA: Verify access is not granted for users aged 18 or under or invalid or empty date field."""
    driver.get("https://grocerymate.masterschool.com/store")
    age_verification_page = AgeVerificationPage(driver)

    age_verification_page.handle_age_verification(dob)
    popup_text = age_verification_page.get_popup_text()

    assert "You are underage" in popup_text, f"Expected 'You are underage' for DOB: {dob}"
