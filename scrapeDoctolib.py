from playwright.sync_api import sync_playwright, expect


def llm_decision(options):
    """
    Placeholder decision function.
    You can replace this with your LLM integration to choose the correct option.
    For now, it simply selects the first available option.
    """
    return 0


def run(playwright, llm_decision=llm_decision, url_start=None):
    """
    This function navigates through the Doctolib website to find the time slot page.
    :param playwright:
    :return : url of the time slot page or None if not found.
    """
    browser = playwright.chromium.launch(headless=True)
    # headless=False for debugging
    page = browser.new_page()

    # Navigate to the clinique starting page and wait until network activity quiets down.
    if url_start is None:
        url_start = "https://www.doctolib.fr/cabinet-medical/paris/maison-abeille-chirurgie-dermatologique-medecine-dermo-esthetique/booking/specialities?bookingFunnelSource=profile"
    page.goto(url_start, wait_until="networkidle")

    max_steps = 5  # Limit to avoid an infinite loop if something goes wrong.

    for step in range(max_steps):
        # Use a locator to detect the time slot page by checking for time slot buttons.
        time_slot_locator = page.locator('button[class*="availabilities-slot"]')
        # If at least one matching button is found, we consider it the time choosing page.
        if time_slot_locator.count() > 0:
            # Wait for the time slot element to be visible (if present, this will wait up to 3 seconds).
            print("Time slot page reached!")
            print("Final URL:", page.url)
            page.screenshot(path="example.png")
            return page.url

        # Locate the specialty options (the clickable buttons with white French text).
        specialty_locator = page.locator('li[role="button"][data-test$="-list-item"]')

        # Get the text content of all available options.
        options = specialty_locator.all_text_contents()
        if not options:
            print("No specialty options found on this page. Exiting navigation.")
            # If no options are found, take a screenshot and exit.
            page.screenshot(path="example.png")
            break

        print(f"Step {step}: Found options: {options}")

        # Decide which option to click (replace this logic with your actual decision function as needed).
        selected_index = llm_decision(options)

        # Click the chosen option using the nth locator.
        specialty_locator.nth(selected_index).click()

        # Wait for the page to load new content.
        page.wait_for_load_state("networkidle")
    else:
        print("Did not reach the time slot page within the allowed steps.")
        # If we reach here, we didn't find the time slot page. Take a screenshot and exit.
        page.screenshot(path="example.png")

    browser.close()


def main(llm_decision=llm_decision, url_start=None):
    with sync_playwright() as playwright:
        # This function is called to run the main logic of the script.
        # It initializes the Playwright context and calls the run function.
        # You can pass a custom URL to start from if needed.
        # Otherwise, it defaults to the specified clinique URL.
        # The llm_decision function is used to decide which option to click.
        # This is where you can integrate your LLM decision-making logic.
        run(playwright, llm_decision=llm_decision, url_start=None)


if __name__ == "__main__":
    main(llm_decision=llm_decision, url_start=None)