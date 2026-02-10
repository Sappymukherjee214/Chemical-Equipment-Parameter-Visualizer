import React, { useState } from 'react';
import './Upload.css';

function Upload({ onUploadSuccess }) {
    const [name, setName] = useState('');
    const [file, setFile] = useState(null);
    const [dragActive, setDragActive] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const droppedFile = e.dataTransfer.files[0];
            if (droppedFile.name.endsWith('.csv')) {
                setFile(droppedFile);
                setError('');
            } else {
                setError('Please upload a CSV file');
            }
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (selectedFile.name.endsWith('.csv')) {
                setFile(selectedFile);
                setError('');
            } else {
                setError('Please upload a CSV file');
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!name.trim()) {
            setError('Please enter a dataset name');
            return;
        }

        if (!file) {
            setError('Please select a CSV file');
            return;
        }

        setUploading(true);
        setError('');

        try {
            await onUploadSuccess(name, file);
            setName('');
            setFile(null);
        } catch (err) {
            setError(err.message || 'Upload failed');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="upload-container">
            <h2>Upload New Dataset</h2>

            <form onSubmit={handleSubmit} className="upload-form">
                <div className="form-group">
                    <label htmlFor="dataset-name">Dataset Name</label>
                    <input
                        type="text"
                        id="dataset-name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="e.g., Plant A Equipment Data"
                        required
                    />
                </div>

                <div
                    className={`file-drop-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <input
                        type="file"
                        id="file-upload"
                        accept=".csv"
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                    />

                    {file ? (
                        <div className="file-info">
                            <svg className="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <p className="file-name">{file.name}</p>
                            <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
                            <button
                                type="button"
                                className="remove-file"
                                onClick={() => setFile(null)}
                            >
                                Remove
                            </button>
                        </div>
                    ) : (
                        <label htmlFor="file-upload" className="file-label">
                            <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                            </svg>
                            <p className="drop-text">
                                <span className="highlight">Click to upload</span> or drag and drop
                            </p>
                            <p className="drop-hint">CSV files only</p>
                        </label>
                    )}
                </div>

                {error && <div className="error-message">{error}</div>}

                <button type="submit" className="upload-button" disabled={uploading}>
                    {uploading ? 'Uploading...' : 'Upload Dataset'}
                </button>
            </form>
        </div>
    );
}

export default Upload;
