import React from 'react';
import './DatasetList.css';

function DatasetList({ datasets, selectedDataset, onSelectDataset, onDeleteDataset }) {
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    };

    return (
        <div className="dataset-list-container">
            <h2>Available Datasets</h2>

            {datasets.length === 0 ? (
                <div className="empty-state">
                    <svg className="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p>No datasets uploaded yet</p>
                    <p className="empty-hint">Upload a CSV file to get started</p>
                </div>
            ) : (
                <div className="dataset-grid">
                    {datasets.map((dataset) => (
                        <div
                            key={dataset.id}
                            className={`dataset-card ${selectedDataset?.id === dataset.id ? 'selected' : ''}`}
                            onClick={() => onSelectDataset(dataset)}
                        >
                            <div className="dataset-header">
                                <h3>{dataset.name}</h3>
                                <button
                                    className="delete-button"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        if (window.confirm('Are you sure you want to delete this dataset?')) {
                                            onDeleteDataset(dataset.id);
                                        }
                                    }}
                                    title="Delete dataset"
                                >
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                </button>
                            </div>

                            <div className="dataset-info">
                                <div className="info-row">
                                    <span className="label">Uploaded:</span>
                                    <span className="value">{formatDate(dataset.uploaded_at)}</span>
                                </div>
                                <div className="info-row">
                                    <span className="label">Equipment:</span>
                                    <span className="value">{dataset.total_equipment}</span>
                                </div>
                                <div className="info-row">
                                    <span className="label">By:</span>
                                    <span className="value">{dataset.uploaded_by}</span>
                                </div>
                            </div>

                            <div className="dataset-stats">
                                <div className="stat">
                                    <span className="stat-label">Avg Flowrate</span>
                                    <span className="stat-value">{dataset.avg_flowrate.toFixed(2)}</span>
                                </div>
                                <div className="stat">
                                    <span className="stat-label">Avg Pressure</span>
                                    <span className="stat-value">{dataset.avg_pressure.toFixed(2)}</span>
                                </div>
                                <div className="stat">
                                    <span className="stat-label">Avg Temp</span>
                                    <span className="stat-value">{dataset.avg_temperature.toFixed(2)}</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default DatasetList;
