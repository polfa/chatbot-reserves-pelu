// src/components/ChatBot.tsx
import { useState, useRef } from "react";
import axios from "axios";

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const ChatBot = () => {
  const [clientName, setClientName] = useState("");
  const [service, setService] = useState("");
  const [dateTime, setDateTime] = useState("");
  const [duration, setDuration] = useState(30);
  const [conversation, setConversation] = useState<Message[]>([
    { text: "¡Hola! Soy tu asistente de reservas. ¿Cómo te llamas?", sender: 'bot' }
  ]);
  const [currentMessage, setCurrentMessage] = useState("");

  const stepRef = useRef(0);

  const handleSubmit = async () => {
    setConversation(prev => [...prev, { text: "Procesando tu reserva...", sender: 'bot' }]);
    try {
      await axios.post("http://localhost:8000/reserva", {
        client_name: clientName,
        service,
        iso_datetime: dateTime,
        duration_minutes: duration,
      });
      setConversation(prev => [...prev, { text: "✅ ¡Reserva creada con éxito!", sender: 'bot' }]);
    } catch (error) {
      setConversation(prev => [...prev, { text: "❌ Error al hacer la reserva.", sender: 'bot' }]);
    }
  };

const validateName = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/name_from_message", { message });
    return res.data.message; // <- nombre devuelto por el backend
  } catch {
    return "ERROR";
  }
};

const validateDate = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/date_from_message", { message });
    return res.data.message; // <- fecha devuelta por el backend
  } catch {
    return "ERROR";
  }
};

  const handleSendMessage = async () => {
    const trimmed = currentMessage.trim();
    if (!trimmed) return;

    setConversation(prev => [...prev, { text: trimmed, sender: 'user' }]);
    setCurrentMessage("");

    const step = stepRef.current;
    let nextBotMessage = "";

    if (step === 0) {
      // Validar nombre en backend
      const name = await validateName(trimmed);
      if (name === "ERROR") {
        setConversation(prev => [...prev, { text: "No entendí tu nombre, por favor intenta de nuevo.", sender: 'bot' }]);
        return;
      }
      setClientName(name);
      nextBotMessage = `Encantado, ${name}. ¿Qué servicio te gustaría reservar?`;
      stepRef.current += 1;
    }
    else if (step === 1) {
      // Guardamos el servicio directamente, sin validar con IA
      setService(trimmed);
      nextBotMessage = "Perfecto. ¿Qué día y hora te va bien? (puedes escribirlo como 'mañana a las 16:00')";
      stepRef.current += 1;
    }
    else if (step === 2) {
      // Validar fecha en backend
      const isoDate = await validateDate(trimmed);
      if (isoDate === "ERROR") {
        setConversation(prev => [...prev, { text: "No pude entender la fecha. Intenta algo como 'mañana a las 16:00'", sender: 'bot' }]);
        return;
      }
      setDateTime(isoDate);
      nextBotMessage = "¿Cuánto tiempo durará el servicio? (en minutos)";
      stepRef.current += 1;
    }
    else if (step === 3) {
      const mins = parseInt(trimmed);
      if (isNaN(mins) || mins <= 0) {
        setConversation(prev => [...prev, { text: "Por favor, indica un número válido en minutos.", sender: 'bot' }]);
        return;
      }
      setDuration(mins);
      nextBotMessage = "¡Gracias! Enviando tu reserva...";
      stepRef.current += 1;
      setConversation(prev => [...prev, { text: nextBotMessage, sender: 'bot' }]);
      await handleSubmit();
      return;
    } else {
      nextBotMessage = "La conversación ha terminado. Si quieres hacer otra reserva, recarga la página.";
    }

    setConversation(prev => [...prev, { text: nextBotMessage, sender: 'bot' }]);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", border: "1px solid #ccc", padding: "10px", borderRadius: "8px" }}>
      <h2>🤖 ChatBot de reservas</h2>

      <div style={{ height: "300px", overflowY: "scroll", border: "1px solid #eee", padding: "10px", marginBottom: "10px" }}>
        {conversation.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', margin: "5px 0" }}>
            <span style={{
              display: "inline-block",
              padding: "8px",
              borderRadius: "5px",
              backgroundColor: msg.sender === 'user' ? '#dcf8c6' : '#f1f0f0'
            }}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      <div style={{ display: "flex" }}>
        <input
          style={{ flexGrow: 1, marginRight: "10px", padding: "8px" }}
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Escribe tu mensaje..."
          disabled={stepRef.current > 3} // Bloquea cuando termina la reserva
        />
        <button onClick={handleSendMessage} disabled={stepRef.current > 3}>Enviar</button>
      </div>
    </div>
  );
};

export default ChatBot;
