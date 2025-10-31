from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic_model.user_input import UserInput

from model.predict import predict_output, MODEL_VERSION, model

from pydantic_model import validate_output

# to run code ->    uvicorn app:app --reload 

#  pip install scikit-learn==1.6.1
# pip install panda
# import the ml model

# -? transfer to model/predict.py
# with open('model/model.pkl', 'rb') as f:  # rb read binary
#     model = pickle.load(f)

# # MLFlow sai ata hai original model versioning k liye
# MODEL_VERSION = "1.0.0"

app = FastAPI()



# pydantic model to validate incoming data
# transfer to pydantic_model folder

# human readable       
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}

# machine readable   
# verify that your API service is running correctly. 
#  aws services like load balancers, kubernative ,auto-scaling groups, and monitoring tools often use health check endpoints to determine the status of your application.
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict', response_model=validate_output.PredictionResponse)
def predict_premium(data: UserInput):

    user_input ={
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:

        prediction = predict_output(user_input)

        return JSONResponse(status_code=200, content={'response': prediction})
    
    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))




