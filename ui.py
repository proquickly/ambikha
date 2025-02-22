from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Purchase Product</title>
    </head>
    <body>
        <h1>Purchase Product</h1>
        <form action="/submit_purchase" method="post">
            <!-- Home Page -->

            <!-- Purchase Option -->
            <fieldset>
                <legend>Option</legend>
                <label for="purchase_option">Select option:</label>
                <select id="purchase_option" name="purchase_option">
                    <option value="purchase">Purchase product</option>
                    <option value="account">Check account</option>
                </select>
            </fieldset>

            <!-- Search Screen -->

            <!-- Search for Product -->
            <fieldset>
                <legend>Search for Product</legend>
                <label for="search_product">Enter the product you want:</label>
                <input type="text" id="search_product" name="search_product">
            </fieldset>

            <!-- Add to Cart -->
            <fieldset>
                <legend>Add to Cart</legend>
                <label for="add_to_cart">quantity:</label>
                <input type="text" id="add_to_cart" name="add_to_cart">
            </fieldset>

            <!-- Order Product -->
            <fieldset>
                <legend>Order Product</legend>
                <label for="order_product">Order the product:</label>
                <input type="text" id="order_product" name="order_product">
            </fieldset>

            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    ''')

@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    purchase_option = request.form.get('purchase_option')
    search_product = request.form.get('search_product')
    add_to_cart = request.form.get('add_to_cart')
    order_product = request.form.get('order_product')

    # Process the form data here
    # For now, just print the data to the console
    print(f"Purchase Option: {purchase_option}")
    print(f"Search Product: {search_product}")
    print(f"Add to Cart: {add_to_cart}")
    print(f"Order Product: {order_product}")

    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)