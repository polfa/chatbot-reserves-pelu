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

  const stepRef = useRef(0); // Reemplaza el contador global

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

  const handleSendMessage = () => {
    const trimmed = currentMessage.trim();
    if (!trimmed) return;

    // Añadir mensaje del usuario
    setConversation(prev => [...prev, { text: trimmed, sender: 'user' }]);

    // Procesar paso actual
    const step = stepRef.current;
    let nextBotMessage = "";

    switch (step) {
      case 0:
        setClientName(trimmed);
        nextBotMessage = "Encantado, " + trimmed + ". ¿Qué servicio te gustaría reservar?";
        break;
      case 1:
        setService(trimmed);
        nextBotMessage = "Perfecto. ¿Qué día y hora te va bien? (formato ISO: YYYY-MM-DDTHH:MM)";
        break;
      case 2:
        setDateTime(trimmed);
        nextBotMessage = "¿Cuánto tiempo durará el servicio? (en minutos)";
        break;
      case 3:
        const mins = parseInt(trimmed);
        if (isNaN(mins) || mins <= 0) {
          setConversation(prev => [...prev, { text: "Por favor, indica un número válido en minutos.", sender: 'bot' }]);
          setCurrentMessage("");
          return;
        }
        setDuration(mins);
        nextBotMessage = "¡Gracias! Enviando tu reserva...";
        handleSubmit();
        break;
      default:
        nextBotMessage = "La conversación ha terminado. Puedes empezar otra si lo deseas.";
        break;
    }

    stepRef.current += 1;
    setConversation(prev => [...prev, { text: nextBotMessage, sender: 'bot' }]);
    setCurrentMessage("");
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
        />
        <button onClick={handleSendMessage}>Enviar</button>
      </div>
    </div>
  );
};

export default ChatBot;
