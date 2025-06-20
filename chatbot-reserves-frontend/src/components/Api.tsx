// src/api.ts
import axios from "axios";

export const postNameFromMessage = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/name_from_message", { message });
    return res.data.message;
  } catch {
    return "ERROR";
  }
};

export const postDateFromMessage = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/date_from_message", { message });
    return res.data.message;
  } catch {
    return "ERROR";
  }
};

export const getServices = async () => {
  try {
    const res = await axios.post("http://localhost:8000/get_services");
    return res.data.message.split(",").map((s: string) => s.trim());
  } catch {
    return "ERROR";
  }
};

export const postServiceFromMessage = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/service_from_message", { message });
    return res.data.message;
  } catch {
    return "ERROR";
  }
};

export const postEmpleatFromMessage = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/get_empleat_from_message", { message });
    return res.data.message;
  } catch {
    return "ERROR";
  }
};

export const postReserva = async (data: {
  client_name: string,
  service: string,
  iso_datetime: string,
  nom_empleat: string,
}) => {
  try {
    await axios.post("http://localhost:8000/reserva", data);
    return true;
  } catch {
    return false;
  }
};

export const getEmpleats = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/get_empleats_by_service", { message });
    return res.data.message
  } catch {
    return "ERROR";
  }
};

export const getServiceInfo = async (message: string) => {
  try {
    const res = await axios.post("http://localhost:8000/get_services_info", { message });
    return res.data.message
  } catch {
    return "ERROR";
  }
};

