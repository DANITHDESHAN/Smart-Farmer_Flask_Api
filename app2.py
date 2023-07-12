from flask import Flask, jsonify, request
import joblib
import json
import numpy as np
import pandas as pd

app = Flask(__name__)


####### Yeild Prediction #########
model = joblib.load('yeild2.joblib')

@app.route('/api/yeildpredict', methods=['GET'])
def yeildpredict():
    # Get the input data from the query parameters
    input_data = request.args.get('input_data')

    if input_data is None:
        return jsonify({'error': 'No input data provided'})

    try:
        input_data = json.loads(input_data)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid input data format'})

    # Prepare input data for prediction
    encoded_data = []
    
        # Add 'Area' feature
    area = input_data.get('Area', '')
    encoded_data.append(area)

    # Define the column lists
    district_columns = ['district_Colombo', 'district_Monaragala', 'district_Rathnapura', 'district_ampara', 'district_anuradhapura',
                        'district_badulla', 'district_batticaloa', 'district_galle', 'district_gampaha',
                        'district_hambantota', 'district_jaffna', 'district_kalutara', 'district_kandy', 'district_kegalle',
                        'district_kilinochchi', 'district_kurunegala', 'district_mannar', 'district_matale', 'district_matara',
                        'district_mullaitivu', 'district_nuwaraEliya', 'district_polonnaruwa', 'district_puttalam',
                        'district_ratnapura', 'district_trincomalee', 'district_vavuniya']

    crop_columns = ['Crop_banana', 'Crop_beetroot', 'Crop_brinjal', 'Crop_carrot', 'Crop_cinnamon', 'Crop_coconut', 'Crop_coffee',
                    'Crop_corn', 'Crop_cucumber', 'Crop_greenchilli', 'Crop_mango', 'Crop_mungbean', 'Crop_orange', 'Crop_papaya',
                    'Crop_pepper', 'Crop_pomegranate', 'Crop_potato', 'Crop_rice', 'Crop_tea', 'Crop_watermelon', 'Crop_yard long bean']

    season_columns = ['Season_maha', 'Season_whole year', 'Season_yala']

    # Perform one-hot encoding on the fly
    for feature in district_columns + crop_columns + season_columns:
        value = input_data.get(feature, '')  # Get feature value from input data
        encoded_values = [int(value == 1)]  # One-hot encode the value (assuming 1 is the value)

        encoded_data.extend(encoded_values)

    # Perform prediction
    features = np.array(encoded_data).reshape(1, -1)
    pred_value = model.predict(features)

    # Print the prediction result
    print('Prediction_Yeild:', pred_value)

    # Return the prediction as a JSON response
    return jsonify({'predictions_yeild': pred_value.tolist()})



if __name__ == '__main__':
    app.run(host='192.168.8.100', port=5002, debug=True)

