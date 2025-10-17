'use client'
import StoreLayout from "@/components/store/StoreLayout";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function RootAdminLayout({ children }) {

    return (
        <ProtectedRoute>
            <StoreLayout>
                {children}
            </StoreLayout>
        </ProtectedRoute>
    );
}
