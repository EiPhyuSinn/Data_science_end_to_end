import asyncio
from playwright.async_api import async_playwright
import json

BASE_URL = "https://propertiesinyangon.com/rent/"

async def scrape_page(page, scraped_ids):
    await page.wait_for_selector(".mh-property", timeout=10000)
    
    listings = await page.query_selector_all(".mh-property")
    
    results = []
    for item in listings:
        try:
            # Get property ID first to check for duplicates
            pid_elem = None
            all_spans = await item.query_selector_all("span.mh-estate-vertical__more-info")
            for span in all_spans:
                text = await span.inner_text()
                if "Property ID:" in text:
                    pid_elem = span
                    break
            
            pid = await pid_elem.inner_text() if pid_elem else None
            if pid:
                pid = pid.replace("Property ID:", "").strip()
            
            # Skip if already scraped
            if pid in scraped_ids:
                continue
            
            # Add to scraped IDs
            scraped_ids.add(pid)
            
            title_elem = await item.query_selector("h3.mh-estate-vertical__heading a")
            title = await title_elem.inner_text() if title_elem else None
            
            price_elem = await item.query_selector(".mh-estate-vertical__primary > div")
            price = await price_elem.inner_text() if price_elem else None
            
            details = {}
            
            prop_type_elem = await item.query_selector(".mh-estate-vertical__more-info.mh-attribute__property-type")
            prop_type = await prop_type_elem.inner_text() if prop_type_elem else None
            if prop_type:
                prop_type = prop_type.replace("Property type:", "").strip()
                details["property_type"] = prop_type
            
            township_elem = await item.query_selector(".mh-estate-vertical__more-info.mh-attribute__townships")
            township = await township_elem.inner_text() if township_elem else None
            if township:
                township = township.replace("Township:", "").strip()
                details["township"] = township
            
            bedrooms_elem = await item.query_selector(".mh-estate-vertical__more-info.mh-attribute__bedrooms")
            bedrooms = await bedrooms_elem.inner_text() if bedrooms_elem else None
            if bedrooms:
                bedrooms = bedrooms.replace("Bedrooms:", "").strip()
                details["bedrooms"] = bedrooms
            
            size_elem = await item.query_selector(".mh-estate-vertical__more-info.mh-attribute__property-size")
            size = await size_elem.inner_text() if size_elem else None
            if size:
                size = size.replace("Property size:", "").strip()
                details["property_size"] = size
            
            results.append({
                "title": title.strip() if title else None,
                "price": price.strip() if price else None,
                "property_id": pid,
                "details": details,
            })
            
        except Exception as e:
            print(f"Error scraping item: {e}")
            continue
    
    return results, scraped_ids


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("Opening page...")
        await page.goto(BASE_URL, timeout=60000)
        
        await page.wait_for_selector(".mh-search", timeout=10000)
        
        print("Scrolling to load initial items...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)
        
        await page.evaluate("window.scrollTo(0, 500)")
        await page.wait_for_timeout(3000)
        
        all_data = []
        scraped_ids = set()  # Track scraped property IDs
        i = 1
        
        while True:
            print(f"\n--- Page {i} ---")
            
            try:
                await page.wait_for_selector(".mh-property", timeout=10000)
            except:
                print("No properties found on this page")
                break
            
            properties, scraped_ids = await scrape_page(page, scraped_ids)
            all_data.extend(properties)
            print(f"Collected {len(properties)} new properties on this page")
            print(f"Total collected so far: {len(all_data)}")
            
            load_more_btn = await page.query_selector(".mh-search__more button")
            
            if not load_more_btn:
                print("No 'Load more' button found.")
                break
            
            print("Clicking 'Load more'...")
            try:
                await load_more_btn.scroll_into_view_if_needed()
                await load_more_btn.click()
                
                await page.wait_for_timeout(3000)
                
                await page.evaluate("window.scrollBy(0, 300)")
                await page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"Error clicking load more: {e}")
                break
            
            i += 1
        
        print(f"\n=== SCRAPING COMPLETE ===")
        print(f"Total unique properties collected: {len(all_data)}")

        with open("properties.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print(f"\nData saved to properties.json")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())