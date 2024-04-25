from flask import Flask, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity, get_jwt
app = Flask(__name__)
jwt = JWTManager(app)
load_dotenv()

# Initialize Supabase client
# SUPABASE_URL = os.getenv('SUPABASE_URL')
# SUPABASE_KEY = os.getenv('SUPABASE_KEY')
# SECRET_KEY=os.getenv('SECRET_KEY')
SUPABASE_URL="https://ldenrcqttxxnhernzyph.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkZW5yY3F0dHh4bmhlcm56eXBoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NTI1NTcsImV4cCI6MjAyODQyODU1N30.WCkmIB1k2l2Syap8jo6-vRvH1mLqI8rJhfFqSobFUmY"
SECRET_KEY="cloudcomputing"
app.config['SECRET_KEY']=SECRET_KEY
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def checkAdmin(user_id, jwt_payload):
    if jwt_payload.get('is_admin',False) != True:
        return False
    return True

@app.route('/add', methods=['POST'])
@jwt_required()
def warehouse():
    user_id = get_jwt_identity()
    jwt_payload = get_jwt()
    data = request.get_json()
    if checkAdmin(user_id, jwt_payload) != True:
        return jsonify({'message': 'You are not authorized to access this resource'}), 403
    try:
        product_response, product_count=supabase.table('Products').insert(data).execute()
        if 'error' in product_response:
            error_message = product_response['error']['message']
            return jsonify({'message': f'Failed to add product: {error_message}'}), 500

        return jsonify({'message': 'Product added successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/delete', methods=['POST'])
@jwt_required()
def delete_product():
    data = request.get_json()
    user_id = get_jwt_identity()
    jwt_payload = get_jwt()
    if checkAdmin(user_id, jwt_payload) != True:
        return jsonify({'message': 'You are not authorized to access this resource'}), 403
    try:
        product_name = data.get('Product')
        product_response, product_count = supabase.table('Products').select("*").eq('Name', product_name).execute()
        if 'error' in product_response:
            error_message = product_response['error']['message']
            return jsonify({'message': f'Failed to retrieve product details: {error_message}'}), 500
        if len(product_response[1]) == 0:
            return jsonify({'message': 'Product not found'}), 404

        delete_response, delete_count = supabase.table('Products').delete().eq('Name', product_name).execute()

        if 'error' in delete_response:
            error_message = delete_response['error']['message']
            return jsonify({'message': f'Failed to delete product: {error_message}'}), 500

        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



@app.route('/edit', methods=['POST'])
@jwt_required()
def edit_product():
    data = request.get_json()
    user_id = get_jwt_identity()
    jwt_payload = get_jwt()
    if checkAdmin(user_id, jwt_payload) != True:
        return jsonify({'message': 'You are not authorized to access this resource'}), 403
    try:
        product_id = data.get('Id')
        product_name=data.get('Name')
        new_product_data = {
            'Name': data.get('Name'),
            'Price': data.get('Price'),
            'Quantity': data.get('Quantity')
        }

        product_response, product_count = supabase.table('Products').select("*").eq('id', product_id).execute()

        if 'error' in product_response:
            error_message = product_response['error']['message']
            return jsonify({'message': f'Failed to retrieve product details: {error_message}'}), 500

        if len(product_response[1]) == 0:
            return jsonify({'message': 'Product not found'}), 404

        update_response, update_count = supabase.table('Products').update(new_product_data).eq('id', product_id).execute()

        if 'error' in update_response:
            error_message = update_response['error']['message']
            return jsonify({'message': f'Failed to update product details: {error_message}'}), 500

        return jsonify({'message': 'Product updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
@app.route('/search', methods=['POST'])
def search_product():
    data = request.get_json()
    product_name = data.get('Name')

    try:
        response, count = supabase.table('Products').select("Name, Price, Quantity").eq('Name', product_name).execute()

        if 'error' in response:
            error_message = response['error']['message']
            return jsonify({'message': f'Failed to search for product: {error_message}'}), 500

        if count == 0:
            return jsonify({'message': 'Product is unavailable'}), 404

        if response and len(response) > 1 and response[1]:
            product_data = response[1][0]  
            return jsonify({
                'product_name': product_data['Name'],
                'price': product_data['Price'],
                'quantity': product_data['Quantity']
            }), 200
        else:
            return jsonify({'message':'No product found'}), 500

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
@app.route('/view', methods=['GET'])
def view_products():
    try:
        response, count = supabase.table('Products').select("Name, Price, Quantity").execute()

        if 'error' in response:
            error_message = response['error']['message']
            return jsonify({'message': f'Failed to retrieve products: {error_message}'}), 500

        products_list = []
        if response and len(response) > 1 and response[1]:
            for product_data in response[1]:
                product_details = {
                    'Name': product_data['Name'],
                    'Price': product_data['Price'],
                    'Quantity': product_data['Quantity']
                }
                products_list.append(product_details)
        if len(products_list)==0:
            return jsonify({'message':'No products are currently available'})
        else:
            return jsonify({'products': products_list}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
