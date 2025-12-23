'use client'
import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import type { SupplyChainOverview } from '@/lib/types'

export function useOverview() {
    const [data, setData] = useState<SupplyChainOverview | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<Error | null>(null)

    useEffect(() => {
        api.overview.get()
            .then(setData)
            .catch(setError)
            .finally(() => setLoading(false))
    }, [])

    return { data, loading, error }
}
