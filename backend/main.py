from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# Configurar CORS para permitir o frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    temperature: float
    # humidity: float

async def fetch_sensor_data():
    temperature_url = "http://192.168.0.2:4001/aasServer/shells/heaterAAS/aas/submodels/temperatureSensor/submodel/submodelElements/currentTemperature/value"
    # humidity_url = "http://192.168.0.2:4001/aasServer/shells/heaterAAS/aas/submodels/humiditySensor/submodel/submodelElements/currentHumidity/value"
    
    try:
        async with httpx.AsyncClient() as client:
            temperature_response = await client.get(temperature_url)
            # humidity_response = await client.get(humidity_url)
            
            # Verificar se ambas as respostas foram bem-sucedidas
            temperature_response.raise_for_status()
            # humidity_response.raise_for_status()

            # Extrair os dados como texto e converter para float
            temperature = float(temperature_response.text)
            # humidity = float(humidity_response.text)

            return {
                "temperature": temperature,
                # "humidity": humidity
            }

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        # Log do erro para depuração
        print(f"Failed to fetch data: {e}")
        raise HTTPException(status_code=500, detail="Erro ao chamar sensor/unidade tal")

@app.get("/data", response_model=SensorData)
async def get_sensor_data():
    data = await fetch_sensor_data()
    return SensorData(**data)
