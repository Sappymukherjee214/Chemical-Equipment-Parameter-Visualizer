import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Upload from './components/Upload';
import DatasetList from './components/DatasetList';
import Analytics from './components/Analytics';
import { login, logout, isAuthenticated, getUsername, getDatasets, getDataset, getDatasetAnalytics, uploadDataset, deleteDataset, downloadReport } from './services/api';
import './App.css';

function App() {
    const [authenticated, setAuthenticated] = useState(false);
    const [username, setUsername] = useState('');
    const [datasets, setDatasets] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState(null);
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (isAuthenticated()) {
            setAuthenticated(true);
            setUsername(getUsername());
            loadDatasets();
        }
    }, []);

    const loadDatasets = async () => {
        setLoading(true);
        setError('');
        try {
            const data = await getDatasets();
            setDatasets(data.results || data);
        } catch (err) {
            setError('Failed to load datasets');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = async (user, pass) => {
        const result = await login(user, pass);
        if (result.success) {
            setAuthenticated(true);
            setUsername(user);
            loadDatasets();
        } else {
            throw new Error(result.error);
        }
    };

    const handleLogout = () => {
        logout();
        setAuthenticated(false);
        setUsername('');
        setDatasets([]);
        setSelectedDataset(null);
        setAnalytics(null);
    };

    const handleUpload = async (name, file) => {
        try {
            await uploadDataset(name, file);
            await loadDatasets();
        } catch (err) {
            throw new Error(err.response?.data?.error || 'Upload failed');
        }
    };

    const handleSelectDataset = async (dataset) => {
        setSelectedDataset(dataset);
        setLoading(true);
        setError('');

        try {
            // Get full dataset details
            const fullDataset = await getDataset(dataset.id);
            setSelectedDataset(fullDataset);

            // Get analytics
            const analyticsData = await getDatasetAnalytics(dataset.id);
            setAnalytics(analyticsData);
        } catch (err) {
            setError('Failed to load analytics');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteDataset = async (id) => {
        try {
            await deleteDataset(id);
            if (selectedDataset?.id === id) {
                setSelectedDataset(null);
                setAnalytics(null);
            }
            await loadDatasets();
        } catch (err) {
            setError('Failed to delete dataset');
            console.error(err);
        }
    };

    const handleDownloadReport = async (id, name) => {
        try {
            await downloadReport(id, name);
        } catch (err) {
            setError('Failed to download report');
            console.error(err);
        }
    };

    if (!authenticated) {
        return <Login onLogin={handleLogin} />;
    }

    return (
        <div className="app">
            <header className="app-header">
                <div className="header-content">
                    <div className="header-title">
                        <h1>Chemical Equipment Parameter Visualizer</h1>
                        <p className="subtitle">Analyze and visualize equipment data</p>
                    </div>
                    <div className="header-actions">
                        <span className="user-info">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            {username}
                        </span>
                        <button onClick={handleLogout} className="logout-button">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                            </svg>
                            Logout
                        </button>
                    </div>
                </div>
            </header>

            <main className="app-main">
                <div className="container">
                    {error && (
                        <div className="error-banner">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {error}
                            <button onClick={() => setError('')}>×</button>
                        </div>
                    )}

                    <Upload onUploadSuccess={handleUpload} />

                    {loading && !selectedDataset ? (
                        <div className="loading">
                            <div className="spinner"></div>
                            <p>Loading datasets...</p>
                        </div>
                    ) : (
                        <DatasetList
                            datasets={datasets}
                            selectedDataset={selectedDataset}
                            onSelectDataset={handleSelectDataset}
                            onDeleteDataset={handleDeleteDataset}
                        />
                    )}

                    <Analytics
                        dataset={selectedDataset}
                        analytics={analytics}
                        onDownloadReport={handleDownloadReport}
                    />
                </div>
            </main>

            <footer className="app-footer">
                <p>Chemical Equipment Parameter Visualizer © 2026 | Internship Screening Project</p>
            </footer>
        </div>
    );
}

export default App;
