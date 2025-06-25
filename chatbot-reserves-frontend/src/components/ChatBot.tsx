// src/components/ChatBot.tsx
import { useState } from "react";
import * as api from "./Api"

interface Message {
  text: string;
  sender: "user" | "bot";
}

export const Steps = {
  AskName: 0,
  AskService: 1,
  AskEmpleat: 2,
  AskDate: 3,
  Completed: 4,
} as const;

export type Steps = typeof Steps[keyof typeof Steps];


const ChatBot = () => {
  const [conversation, setConversation] = useState<Message[]>([
    { text: "¡Hola! Soy tu asistente de reservas. ¿Cómo te llamas?", sender: "bot" },
  ]);
  const [currentMessage, setCurrentMessage] = useState("");
  const [step, setStep] = useState<Steps>(Steps.AskName);

  const [clientName, setClientName] = useState("");
  const [service, setService] = useState("");
  const [workerName, setWorkerName] = useState("");
  const [dateTime, setDateTime] = useState("");

  // Añade mensaje a la conversación
  const addBotMessage = (text: string) => {
    setConversation((prev) => [...prev, { text, sender: "bot" }]);
  };

  const addUserMessage = (text: string) => {
    setConversation((prev) => [...prev, { text, sender: "user" }]);
  };

  const handleSendMessage = async () => {
    const trimmed = currentMessage.trim();
    if (!trimmed) return;

    addUserMessage(trimmed);
    setCurrentMessage("");

    switch (step) {
      case Steps.AskName: {
        const name = await api.postNameFromMessage(trimmed);
        if (name === "ERROR") {
          addBotMessage("No entendí tu nombre, por favor intenta de nuevo.");
          return;
        }
        setClientName(name);
        const services = await api.getServices();
        if (services === "ERROR") {
          addBotMessage(`Encantado, ${name}. Pero no pude obtener los servicios disponibles. Intenta más tarde.`);
        } else {
          addBotMessage(`Encantado, ${name}. ¿Qué servicio te gustaría reservar?\nOpciones: ${services.join(", ")}`);
          setStep(Steps.AskService);
        }
        break;
      }
      case Steps.AskService: {
        const s = await api.postServiceFromMessage(trimmed);
        if (s === "ERROR") {
          addBotMessage("No entendí el tipo de servicio, por favor intenta de nuevo.");
          return;
        }else if(s == "CONSULTA"){
          const info = await api.getServiceInfo(trimmed)
          addBotMessage(info);
          return;
        }
        setService(s);
        const empleats_str = await api.getEmpleats(s);
        addBotMessage(`Has elegido el servicio: ${s}. Estos son los empleados que tenemos para este servicio: ${empleats_str}. ¿Cuál quieres? Si no es el servicio que quieres escribe NO.`);
        setStep(Steps.AskEmpleat);
        break;
      }
      case Steps.AskEmpleat: {
        if (trimmed === "NO") {
          addBotMessage("Escribe el tipo de servicio que quieres reservar.");
          setStep(Steps.AskService);
          return;
        }
        const e = await api.postEmpleatFromMessage(trimmed);
        if (e.includes("[$C]")) {
          const novaCadena = e.replace("[$C]", "");
          addBotMessage(novaCadena);
          return;
        }
        if (e === "ERROR") {
          addBotMessage("No pude encontrar el empleado que te pidieron. Intenta algo como 'NO'");
          return;
        }
        setWorkerName(e);
        addBotMessage(`Perfecto con ${e}. ¿Qué día y hora te va bien? (puedes escribirlo como 'mañana a las 16:00')`);
        setStep(Steps.AskDate);
        break;
      }
      case Steps.AskDate: {
        const isoDate = await api.postDateFromMessage(trimmed);
        if (isoDate === "ERROR") {
          addBotMessage("No pude entender la fecha. Intenta algo como 'mañana a las 16:00'");
          return;
        }
        setDateTime(isoDate);
        addBotMessage("¡Gracias! Enviando tu reserva...");

        const success = await api.postReserva({
          client_name: clientName,
          service,
          iso_datetime: isoDate,
          nom_empleat: workerName,
        });

        if (success) {
          addBotMessage(`✅ ¡Reserva creada con éxito! \nDetalles: ${isoDate} - ${service} - ${workerName}`);
        } else {
          addBotMessage("❌ Error al hacer la reserva.");
        }
        setStep(Steps.Completed);
        break;
      }
      case Steps.Completed:
        addBotMessage("La conversación ha terminado. Si quieres hacer otra reserva, recarga la página.");
        break;
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSendMessage();
  };

return (
  <div
    style={{
      maxWidth: 600,
      width: "90vw",
      height: "80vh",
      margin: "20px auto",
      border: "1px solid #ccc",
      borderRadius: 12,
      display: "flex",
      flexDirection: "column",
      backgroundColor: "#fafafa",
      boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    }}
  >
    <h2
      style={{
        margin: "16px",
        textAlign: "center",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        color: "#333",
      }}
    >
      🤖 ChatBot de reservas
    </h2>

    <div
      style={{
        flexGrow: 1,
        overflowY: "auto",
        padding: "16px",
        borderTop: "1px solid #eee",
        borderBottom: "1px solid #eee",
        backgroundColor: "white",
      }}
      id="chat-container"
    >
      {conversation.map((msg, i) => (
        <div
          key={i}
          style={{
            display: "flex",
            justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
            marginBottom: 12,
          }}
        >
          <span
            style={{
              maxWidth: "70%",
              padding: "12px 16px",
              borderRadius: 20,
              backgroundColor: msg.sender === "user" ? "#4caf50" : "#e0e0e0",
              color: msg.sender === "user" ? "white" : "#333",
              fontSize: 16,
              lineHeight: 1.4,
              fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
              whiteSpace: "pre-wrap",
            }}
          >
            {msg.text}
          </span>
        </div>
      ))}
    </div>

    <form
      onSubmit={(e) => {
        e.preventDefault();
        handleSendMessage();
      }}
      style={{ display: "flex", padding: "12px", backgroundColor: "#f9f9f9" }}
    >
      <input
        style={{
          flexGrow: 1,
          padding: "12px 16px",
          borderRadius: 24,
          border: "1px solid #ccc",
          fontSize: 16,
          fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          outline: "none",
          marginRight: 12,
        }}
        value={currentMessage}
        onChange={(e) => setCurrentMessage(e.target.value)}
        placeholder="Escribe tu mensaje..."
        disabled={step === Steps.Completed}
      />
      <button
        type="submit"
        disabled={step === Steps.Completed || !currentMessage.trim()}
        style={{
          backgroundColor: "#4caf50",
          color: "white",
          border: "none",
          borderRadius: 24,
          padding: "0 24px",
          cursor: step === Steps.Completed || !currentMessage.trim() ? "not-allowed" : "pointer",
          fontSize: 16,
          fontWeight: "bold",
          fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          transition: "background-color 0.3s ease",
        }}
        onMouseEnter={(e) => {
          if (step !== Steps.Completed && currentMessage.trim())
            e.currentTarget.style.backgroundColor = "#45a049";
        }}
        onMouseLeave={(e) => {
          if (step !== Steps.Completed && currentMessage.trim())
            e.currentTarget.style.backgroundColor = "#4caf50";
        }}  
      >
        Enviar
      </button>
    </form>
  </div>
);

}

export default ChatBot;


