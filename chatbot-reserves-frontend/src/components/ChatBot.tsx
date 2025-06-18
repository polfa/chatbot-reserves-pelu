// src/components/ChatBot.tsx
import { useState } from "react";
import axios from "axios";

const ChatBot = () => {
  const [step, setStep] = useState(0);
  const [clientName, setClientName] = useState("");
  const [service, setService] = useState("");
  const [dateTime, setDateTime] = useState("");
  const [duration, setDuration] = useState(30);
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const res = await axios.post("http://localhost:8000/reserva", {
        client_name: clientName,
        service,
        iso_datetime: dateTime,
        duration_minutes: duration,
      });
      setResponse("Reserva creada amb èxit ✅");
    } catch (error) {
      setResponse("Error al fer la reserva ❌");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto" }}>
      <h2>🤖 ChatBot de reserves</h2>
      {step === 0 && (
        <div>
          <p>Com et dius?</p>
          <input value={clientName} onChange={(e) => setClientName(e.target.value)} />
          <button onClick={() => setStep(1)}>Següent</button>
        </div>
      )}
      {step === 1 && (
        <div>
          <p>Quin servei vols?</p>
          <input value={service} onChange={(e) => setService(e.target.value)} />
          <button onClick={() => setStep(2)}>Següent</button>
        </div>
      )}
      {step === 2 && (
        <div>
          <p>Quin dia i hora vols? (format: 2025-06-18T16:00:00)</p>
          <input value={dateTime} onChange={(e) => setDateTime(e.target.value)} />
          <button onClick={() => setStep(3)}>Següent</button>
        </div>
      )}
      {step === 3 && (
        <div>
          <p>Duració del servei (minuts):</p>
          <input type="number" value={duration} onChange={(e) => setDuration(parseInt(e.target.value))} />
          <button onClick={handleSubmit}>Reservar</button>
        </div>
      )}
      {response && <p>{response}</p>}
    </div>
  );
};

export default ChatBot;
