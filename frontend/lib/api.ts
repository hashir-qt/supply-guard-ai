import { SimulationRequest } from './types'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'

export const api = {
    overview: {
        get: () => fetch(`${API_BASE}/overview/overview`).then(r => r.json()),
    },
    risks: {
        getAll: () => fetch(`${API_BASE}/risks/`).then(r => r.json()),
        getDetail: (id: string) => fetch(`${API_BASE}/risks/${id}`).then(r => r.json()),
    },
    suppliers: {
        getAll: (type?: string) => {
            const query = type ? `?supplier_type=${type}` : ''
            return fetch(`${API_BASE}/suppliers/${query}`).then(r => r.json())
        },
        getAtRisk: (threshold = 50) => fetch(`${API_BASE}/suppliers/at-risk?threshold=${threshold}`).then(r => r.json()),
        getDetail: (id: string) => fetch(`${API_BASE}/suppliers/${id}`).then(r => r.json()),
    },
    outlets: {
        getAll: (city?: string) => {
            const query = city ? `?city=${city}` : ''
            return fetch(`${API_BASE}/outlets/${query}`).then(r => r.json())
        },
        getLowInventory: (threshold = 2.0) => fetch(`${API_BASE}/outlets/low-inventory?threshold=${threshold}`).then(r => r.json()),
        getDetail: (id: string) => fetch(`${API_BASE}/outlets/${id}`).then(r => r.json()),
    },
    simulation: {
        run: (data: SimulationRequest) => fetch(`${API_BASE}/simulation/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => r.json())
    },
    agent: {
        chat: async (message: string, context: any = {}) => {
            const res = await fetch(`${API_BASE}/agent/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context })
            })
            return res.json()
        }
    }
}
