from flask import Flask, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity, get_jwt


app = Flask(__name__)

load_dotenv()
jwt = JWTManager(app)

# Initialize Supabase client
# SUPABASE_URL = os.getenv('SUPABASE_URL')
# SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_URL="https://ldenrcqttxxnhernzyph.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkZW5yY3F0dHh4bmhlcm56eXBoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NTI1NTcsImV4cCI6MjAyODQyODU1N30.WCkmIB1k2l2Syap8jo6-vRvH1mLqI8rJhfFqSobFUmY"
SECRET_KEY="cloudcomputing"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Load your secret key from environment variables
app.config['SECRET_KEY'] = SECRET_KEY


# Function to check if the user is an admin
def checkAdmin(user_id, jwt_payload):
    if jwt_payload.get('is_admin',False) != True:
        return False
    return True


@app.route('/orders', methods=['GET'])
@jwt_required()
def get_order_history():

    # Get user ID from the request or session 
    user_id = get_jwt_identity()
    # print("user_id",user_id)
    jwt_payload = get_jwt()
    # print("jwt_payload",jwt_payload)
    # print(jwt_payload.get('is_admin',False))

    if checkAdmin(user_id, jwt_payload) != True:
        return jsonify({'message': 'You are not authorized to access this resource'}), 403
       
    try:
        # Retrieve order history for the specified user from the 'Orders' table
        response, count = supabase.table('Orders').select("*").eq('User_ID', user_id).execute()
        # print(response)

        if 'error' in response:
            error_message = response['error']['message']
            return jsonify({'message': f'Failed to fetch order history: {error_message}'}), 500

        orders = response[1]
        return jsonify({'orders': orders}), 200

    except Exception as e:
        return jsonify({'message': f'Failed to fetch order history nkjnkjjk: {str(e)}'}), 500



# allow users to track their orders
@app.route('/orders/<int:order_id>', methods=['GET'])
def track_order(order_id):

    # ! TODO make sure to check that the user is the owner of the order or an admin
    try:
        # Retrieve the order details for the specified OrderID
        response, count = supabase.table('Orders').select("*").eq('OrderID', order_id).execute()

        if "error" in response:
            error_message = response['error']['message']
            return jsonify({'message': f'Failed to track order: {error_message}'}), 404  # Use 404 for not found
        

        if response[1] == []:
            return jsonify({'message': 'Order not found'}), 404
        
        print("response",response)

        order = response[1][0]
        return jsonify({'order': order}), 200

    except Exception as e:
        return jsonify({'message': f'Failed to track order: {str(e)}'}), 500


@app.route('/placeOrder', methods=['POST'])
@jwt_required()
def place_order():
    data = request.get_json()
    # user_id = data.get('UserID')

    user_id = get_jwt_identity()
    # ! TODO : Add validation for the order data before inserting into the database (eg check for qty)
    # add the user ID to the order data
    data['User_ID'] = user_id

    # print("data",data)
    
    try:
        # Insert the new order into the 'Orders' table
        response, count = supabase.table('Orders').insert(data).execute()

        # print("response",response)
        if "error" in response:
            error_message = response['error']['message']
            return jsonify({'message': f'Failed to place order: {error_message}'}), 400  # Use 400 for bad request

        new_order = response[1][0]
        return jsonify({'message': 'Order placed successfully', 'order': new_order}), 201

    except Exception as e:
        return jsonify({'message': f'Failed to place order: {str(e)}'}), 500



@app.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.get_json()

    # Get user ID from the JWT token's identity
    user_id = get_jwt_identity()
    jwt_payload = get_jwt()

    # add user ID to the order data
    data['User_ID'] = user_id   

    # Check if the user is an admin
    if not checkAdmin(user_id, jwt_payload):
        return jsonify({'message': 'You are not authorized to perform this action'}), 403

    try:
        # Update the order with the specified OrderID
        response, count = supabase.table('Orders').update(data).eq('OrderID', order_id).execute()

        if response[1] == []:
            return jsonify({'message': 'Order not found'}), 404

        updated_order = response[1][0]
        return jsonify({'message': 'Order updated successfully', 'order': updated_order}), 200

    except Exception as e:
        return jsonify({'message': f'Failed to update order: {str(e)}'}), 500


@app.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def cancel_order(order_id):
    # Get user ID from the JWT token's identity
    user_id = get_jwt_identity()
    jwt_payload = get_jwt()

    # Check if the user is an admin
    if not checkAdmin(user_id, jwt_payload):
        return jsonify({'message': 'You are not authorized to perform this action'}), 403

    try:
        # Delete the order with the specified OrderID
        response, count = supabase.table('Orders').delete().eq('OrderID', order_id).execute()

        if count == 0:
            return jsonify({'message': 'Order not found'}), 404

        return jsonify({'message': 'Order canceled successfully'}), 200

    except Exception as e:
        return jsonify({'message': f'Failed to cancel order: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
