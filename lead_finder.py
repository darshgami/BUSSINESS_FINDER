import asyncio
import os
import re
import argparse
import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def clean_text(text):
    if text:
        return re.sub(r'\s+', ' ', text).strip()
    return ""

async def scrape_google_maps_leads(city: str, search_query: str, output_name: str):
    print("\n" + "="*60)
    print(f"🚀 Initializing Google Maps Lead Finder...")
    print(f"🌆 Target City: {city}")
    print(f"🔍 Search Query: {search_query} in {city}")
    print(f"🎯 Filter Criteria: Rating >= 3.5 AND No Website Built")
    print("="*60 + "\n")

    async with async_playwright() as p:
        # Launch browser in background
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Format Google Maps Search URL
        formatted_query = f"{search_query} in {city}".replace(" ", "+")
        maps_url = f"https://www.google.com/maps/search/{formatted_query}"
        
        await page.goto(maps_url, wait_until="domcontentloaded")
        await asyncio.sleep(5)
        
        print("⏳ Scanning Google Maps rows (Scrolling down)...")
        
        # Scroll the left results panel to load more businesses
        results_panel_selector = "div[role='feed']"
        try:
            for _ in range(12):  # 12 scrolls to load enough listings
                await page.locator(results_panel_selector).evaluate("el => el.scrollBy(0, 1500);")
                await asyncio.sleep(1.5)
        except Exception:
            print("⚠️ Reached end of maps feed or panel layout finished.")

        # Extract page content
        html_content = await page.content()
        await browser.close()
        
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        cards = soup.select("div[class*='Nv2y3c'], div.m67q6c, div.bJzme")
        if not cards:
            cards = soup.find_all("div", role="article")

        leads_pool = []
        
        for card in cards:
            try:
                # 1. Extract Business Name
                name_node = card.find(["div", "span", "a"], class_=lambda x: x and ('qbf1Pd' in x or 'fontHeadlineSmall' in x))
                name = await clean_text(name_node.get_text()) if name_node else ""
                
                if not name or len(name) < 2:
                    continue
                
                # 2. Extract Rating
                rating_node = card.find("span", class_=lambda x: x and ('MW4etd' in x or 'rating' in x))
                rating_text = rating_node.get_text().strip() if rating_node else "0"
                
                try:
                    rating = float(rating_text)
                except ValueError:
                    rating = 0.0
                    
                # 3. Website Check (CRITICAL FILTER)
                website_node = card.find("a", attrs={"data-value": "Website"}) or card.find("a", class_=lambda x: x and 'l97Zg' in x)
                has_website = "Yes" if website_node else "No"
                
                # 4. Extract Address / Phone Info Text
                meta_nodes = card.find_all("div", class_=lambda x: x and 'W4CHMc' in x)
                address_info = "Local Area, " + city
                if meta_nodes:
                    address_info = await clean_text(", ".join([m.get_text() for m in meta_nodes]))

                # 🔥 STRICT FILTERING (No Website & Rating >= 3.5)
                if has_website == "No" and rating >= 3.5:
                    leads_pool.append({
                        "Business Name": name,
                        "City": city,
                        "Google Rating": rating,
                        "Address / Contact Info": address_info
                    })
                    print(f"   ✔️ Lead Found: [{name}] | Rating: {rating}")
                    
            except Exception:
                continue

        # Save data to CSV
        if leads_pool:
            df = pd.DataFrame(leads_pool)
            df.drop_duplicates(subset=["Business Name"], inplace=True)
            
            final_csv = output_name if output_name.endswith('.csv') else f"{output_name}.csv"
            df.to_csv(final_csv, index=False, encoding='utf-8-sig')
            
            print("\n" + "="*60)
            print("🎉 Clean Lead Extraction Operation Finished!")
            print(f"📊 Total High-Rating (No Website) Leads Saved: {len(df)}")
            print(f"📁 Extracted CSV Saved Location: {os.path.abspath(final_csv)}")
            print("="*60)
        else:
            print("\n⚠️ No leads matched your criteria (Rating >= 3.5 & No Website) in this batch.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Maps Web-Less Lead Generator")
    parser.add_argument("--city", required=True, help="Enter the target city (e.g., Rajkot)")
    parser.add_argument("--query", required=True, help="Enter search term (e.g., 'manufacturers' or 'hotels')")
    parser.add_argument("--output", default="potential_leads.csv", help="Output CSV filename")
    
    args = parser.parse_args()
    
    asyncio.run(scrape_google_maps_leads(args.city, args.query, args.output))