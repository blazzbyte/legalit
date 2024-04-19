'use client'
import React, { createContext, useContext, useState, ReactNode } from 'react';

interface UserContextType {
    userId: string;
    uploadedContext: boolean;
    setUserByDefault: () => void;
    setUploadedContext: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {

    const [userId, setUserId] = useState<string>(generateRandomUserId());
    const [uploadedContext, setUploadedContext] = useState<boolean>(false);

    const setUserByDefault = () => {
        setUserId('testing');
        setUploadedContext(true);
    };

    function generateRandomUserId() {
        return Math.random().toString(36).substring(7);
    }

    const contextValues: UserContextType = {
        userId,
        uploadedContext,
        setUserByDefault,
        setUploadedContext: () => setUploadedContext(true),
    };

    return (
        <UserContext.Provider value={contextValues}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = (): UserContextType => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used inside a UserProvider');
    }
    return context;
};