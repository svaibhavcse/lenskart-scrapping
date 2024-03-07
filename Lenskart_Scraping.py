import requests as req
import json
import pandas as pd 
from azure.storage.blob import ContainerClient

# Initialize lists to store data
product_ids = []
brand_names = []
colors = []
occasions = []
sizes = []
widths = []
model_names = []
market_prices = []
lenskart_prices = []
offer_names = []
quantities = []
search_product_names = []
classifications = []
avg_ratings = []
total_ratings = []
purchase_counts = []
wishlist_counts = []
suited_for=[]
response_pages=[]

print("Start")

#Fetching the page once to get the number of products
print("Fetching once to get the number of pages")
fetch=req.get("https://api-gateway.juno.lenskart.com/v2/products/category/3363?page-size=10&page=0")
fetched_data= fetch.json()
print("Total number of products:",fetched_data['result']['num_of_products'])


#Diving the num_of_products with 1000 to find the number of pages
num_of_pages=int((int(fetched_data['result']['num_of_products'])/1000)+1)
print("Total number of pages:",num_of_pages)


# Loop through multiple pages of API response
for page_num in range(num_of_pages):
    # Fetch data from the API
    print("Fetching response from page",page_num+1)
    response = req.get(f"https://api-gateway.juno.lenskart.com/v2/products/category/3363?page-size=1000&page={page_num}")
    data = response.json()

    # Extract product information from the API response
    if int(data['result']['num_of_products'])!=0:

        #Appending each page response in to an array
        response_pages.append(data)

        for product in data['result']['product_list']:
            # Extracting and appending product details to respective lists
            product_ids.append(product['id'])
            brand_names.append(product['brand_name'] )
            colors.append(product['color'] if 'color' in product else 'No color available')
            occasions.append(product['occasion'] if 'occasion' in product else 'Any occasion')
            suited_for.append(product['suited_for'] if 'suited_for' in product else 'Any age group')
            sizes.append(product['size'] if 'size' in product else 'No size')
            widths.append(product['width'] if 'width' in product else '')
            model_names.append(product['model_name'] if 'model_name' in product else '')
            market_prices.append(product['prices'][0]['price'] if 'prices' in product and len(product['prices']) > 0 else '')
            lenskart_prices.append(product['prices'][1]['price'] if 'prices' in product and len(product['prices']) > 1 else '')
            offer_names.append(product['offerName'] if 'offerName' in product else 'No offer')
            quantities.append(product['qty'] if 'qty' in product else '')
            search_product_names.append(product['searchProductName'] if 'searchProductName' in product else 'No search keywords')
            classifications.append(product['classification'] if 'classification' in product else '')
            avg_ratings.append(product['avgRating'] if 'avgRating' in product else '')
            total_ratings.append(product['totalNoOfRatings'] if 'totalNoOfRatings' in product else 0)
            purchase_counts.append(product['purchaseCount'] if 'purchaseCount' in product else '')
            wishlist_counts.append(product['wishlistCount'] if 'wishlistCount' in product else '')
    else:
        print("No prodcuts in page",page_num+1)

# Save data to a JSON file
print("Saving all responses to json file")
with open("products_data.json", "a") as json_file:
            json.dump(response_pages,json_file)
print("Saved responses inside json file")

# Create a DataFrame from the collected data
df = pd.DataFrame({
    'id': product_ids,
    'Brand_Name': brand_names,
    'Color': colors,
    'Occasion': occasions,
    'Size': sizes,
    'Width': widths,
    'Model_Name': model_names,
    'Market_Price': market_prices,
    'Lenskart_Price': lenskart_prices,
    'Offer_Name': offer_names,
    'Quantity': quantities,
    'Suited_For':suited_for,
    'Search_Product Name': search_product_names,
    'Classification': classifications,
    'Average_Ratings': avg_ratings,
    'Total_No_of_Ratings': total_ratings,
    'Purchase_Count': purchase_counts,
    'Wishlist_Count': wishlist_counts
})
print("DataFrame created")

# Write DataFrame to a CSV file
csv_file = 'products_dataframe.csv'
print("Writing to CSV file")
df.to_csv(csv_file, index=False)

#Storing the output csv inside azure blob
cntion_string ="enter connecting string"
print("Writing to azure storage blob")
container_client = ContainerClient.from_connection_string(conn_str=cntion_string, container_name="lenskartdata/Source")
with open("products_dataframe.csv", "rb") as data:
    container_client.upload_blob(name="products.csv", data=data)

print("Completed")