import axios from 'axios'

const BASE = 'http://localhost:5000'

const getToken = () => localStorage.getItem('token')

const authHeaders = () => ({
  headers: { Authorization: `Bearer ${getToken()}` }
})

export const registerUser = (data) =>
  axios.post(`${BASE}/api/register`, data)

export const loginUser = (data) =>
  axios.post(`${BASE}/api/login`, data)

export const generateDataset = (prompt, rows) =>
  axios.post(`${BASE}/api/generate`, { prompt, rows }, authHeaders())

export const downloadCSV = (prompt, rows) =>
  axios.post(`${BASE}/api/download`, { prompt, rows },
    { ...authHeaders(), responseType: 'blob' })

export const getHistory = () =>
  axios.get(`${BASE}/api/history`, authHeaders())

export const deleteHistory = (id) =>
  axios.delete(`${BASE}/api/history/${id}`, authHeaders())

export const getSettings = () =>
  axios.get(`${BASE}/api/settings`, authHeaders())

export const updateSettings = (data) =>
  axios.put(`${BASE}/api/settings`, data, authHeaders())
