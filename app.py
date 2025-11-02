from playwright.sync_api import sync_playwright
import re

def get_facebook_post_id(post_url):
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Go to the post URL
            page.goto(post_url)
            # Wait for the page to load
            page.wait_for_timeout(5000)

            # Get the final URL after any redirects
            final_url = page.url

            # Try to find the post ID in the URL using regex
            # This pattern matches common Facebook post ID formats in URLs
            patterns = [
                r'(?<=story_fbid=)(\d+)',
                r'(?<=posts/)(\d+)',
                r'(?:/|%2F)(\d+)(?:%3F|\?|$)'
            ]

            post_id = None
            for pattern in patterns:
                match = re.search(pattern, final_url)
                if match:
                    post_id = match.group(1)
                    break

            browser.close()
            return post_id

        except Exception as e:
            print(f"An error occurred: {e}")
            browser.close()
            return None

# Example usage
post_id = get_facebook_post_id("https://www.facebook.com/share/p/1C8EEGCHWy/")
print(f"Extracted Post ID: {post_id}")
