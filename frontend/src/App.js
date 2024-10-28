import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState({ temperature: null, humidity: null });

  useEffect(() => {
    // Função para buscar dados da API FastAPI
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/data");
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Erro ao buscar dados da API:", error);
      }
    };

    // Atualizar dados a cada 5 segundos
    const interval = setInterval(fetchData, 1000);
    fetchData(); // Chama a primeira vez para não esperar 5s
    return () => clearInterval(interval); // Limpa o intervalo ao desmontar o componente
  }, []);

  return (
    <div className="App">
      <h1 style={{fontSize: "72px", textAlign: "center"}}>Monitoramento de Temperatura da Máquina Coladeira de Borda!</h1>
      <p style={{fontSize: "96px", textAlign: "center"}}>Temperatura: {data.temperature !== null ? `${data.temperature} °C` : "Carregando..."}</p>
      {/* <p>Umidade: {data.humidity !== null ? `${data.humidity} %` : "Carregando..."}</p> */}
    </div>
  );
}

export default App;
