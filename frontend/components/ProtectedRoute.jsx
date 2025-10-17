'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useSelector } from 'react-redux'
import toast from 'react-hot-toast'

/**
 * ProtectedRoute Component
 * Protects routes that require authentication.
 * Redirects to home if user is not authenticated.
 */
export default function ProtectedRoute({ children }) {
    const router = useRouter()
    const { isAuthenticated, user } = useSelector((state) => state.auth)

    useEffect(() => {
        // Check if user is authenticated
        if (!isAuthenticated || !user) {
            toast.error('Please login to access this page')
            router.push('/')
        }
    }, [isAuthenticated, user, router])

    // Show loading or nothing while checking auth
    if (!isAuthenticated || !user) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-indigo-600 border-r-transparent"></div>
                    <p className="mt-4 text-gray-600">Loading...</p>
                </div>
            </div>
        )
    }

    // User is authenticated, render children
    return <>{children}</>
}
