import { SimulationRequest } from './types'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'

async function handleResponse<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `HTTP ${res.status}: ${res.statusText}`)
    }
    return res.json()
}

export const api = {
    overview: {
        get: () => fetch(`${API_BASE}/overview/overview`).then(r => handleResponse(r)),
    },
    risks: {
        getAll: () => fetch(`${API_BASE}/risks/`).then(r => handleResponse(r)),
        getDetail: (id: string) => fetch(`${API_BASE}/risks/${id}`).then(r => handleResponse(r)),
    },
    suppliers: {
        getAll: (type?: string) => {
            const query = type ? `?supplier_type=${type}` : ''
            return fetch(`${API_BASE}/suppliers/${query}`).then(r => handleResponse(r))
        },
        getAtRisk: (threshold = 50) => fetch(`${API_BASE}/suppliers/at-risk?threshold=${threshold}`).then(r => handleResponse(r)),
        getDetail: (id: string) => fetch(`${API_BASE}/suppliers/${id}`).then(r => handleResponse(r)),
    },
    outlets: {
        getAll: (city?: string) => {
            const query = city ? `?city=${city}` : ''
            return fetch(`${API_BASE}/outlets/${query}`).then(r => handleResponse(r))
        },
        getLowInventory: (threshold = 2.0) => fetch(`${API_BASE}/outlets/low-inventory?threshold=${threshold}`).then(r => handleResponse(r)),
        getDetail: (id: string) => fetch(`${API_BASE}/outlets/${id}`).then(r => handleResponse(r)),
    },
    simulation: {
        run: (data: SimulationRequest) => fetch(`${API_BASE}/simulation/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => handleResponse(r))
    },
    agent: {
        chat: async (message: string, context: object = {}) => {
            const res = await fetch(`${API_BASE}/agent/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context })
            })
            return handleResponse<{ response: string; tools_used: string[]; conversation_id: string }>(res)
        }
    }
}
