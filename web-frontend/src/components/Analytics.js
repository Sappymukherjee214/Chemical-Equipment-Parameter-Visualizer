import React, { useState } from 'react';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar, Scatter } from 'react-chartjs-2';
import './Analytics.css';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend);

function Analytics({ dataset, analytics, onDownloadReport }) {
    const [downloading, setDownloading] = useState(false);

    if (!dataset || !analytics) {
        return (
            <div className="analytics-container">
                <div className="no-selection">
                    <svg className="no-selection-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    <p>Select a dataset to view analytics</p>
                </div>
            </div>
        );
    }

    // Equipment type distribution chart
    const typeLabels = Object.keys(analytics.equipment_types);
    const typeCounts = Object.values(analytics.equipment_types);

    const pieData = {
        labels: typeLabels,
        datasets: [
            {
                label: 'Equipment Count',
                data: typeCounts,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(199, 199, 199, 0.8)',
                    'rgba(83, 102, 255, 0.8)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)',
                    'rgba(83, 102, 255, 1)',
                ],
                borderWidth: 2,
            },
        ],
    };

    // Parameter comparison bar chart
    const barData = {
        labels: typeLabels,
        datasets: [
            {
                label: 'Avg Flowrate',
                data: typeCounts.map(() => analytics.avg_flowrate),
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
            },
            {
                label: 'Avg Pressure',
                data: typeCounts.map(() => analytics.avg_pressure),
                backgroundColor: 'rgba(255, 206, 86, 0.8)',
            },
            {
                label: 'Avg Temperature',
                data: typeCounts.map(() => analytics.avg_temperature),
                backgroundColor: 'rgba(255, 99, 132, 0.8)',
            },
        ],
    };

    // Scatter plot data (if we have equipment records)
    const scatterData = {
        datasets: [
            {
                label: 'Pressure vs Flowrate',
                data: dataset.equipment_records?.map(record => ({
                    x: record.flowrate,
                    y: record.pressure,
                })) || [],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
            },
        ],
    };

    const handleDownload = async () => {
        setDownloading(true);
        try {
            await onDownloadReport(dataset.id, dataset.name);
        } finally {
            setDownloading(false);
        }
    };

    return (
        <div className="analytics-container">
            <div className="analytics-header">
                <h2>Analytics: {dataset.name}</h2>
                <button
                    className="download-button"
                    onClick={handleDownload}
                    disabled={downloading}
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    {downloading ? 'Generating...' : 'Download PDF Report'}
                </button>
            </div>

            <div className="summary-stats">
                <div className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                        </svg>
                    </div>
                    <div className="stat-content">
                        <div className="stat-label">Total Equipment</div>
                        <div className="stat-value">{analytics.total_equipment}</div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                        </svg>
                    </div>
                    <div className="stat-content">
                        <div className="stat-label">Avg Flowrate</div>
                        <div className="stat-value">{analytics.avg_flowrate.toFixed(2)}</div>
                        <div className="stat-range">{analytics.min_flowrate.toFixed(1)} - {analytics.max_flowrate.toFixed(1)}</div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    </div>
                    <div className="stat-content">
                        <div className="stat-label">Avg Pressure</div>
                        <div className="stat-value">{analytics.avg_pressure.toFixed(2)}</div>
                        <div className="stat-range">{analytics.min_pressure.toFixed(1)} - {analytics.max_pressure.toFixed(1)}</div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' }}>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="stat-content">
                        <div className="stat-label">Avg Temperature</div>
                        <div className="stat-value">{analytics.avg_temperature.toFixed(2)}</div>
                        <div className="stat-range">{analytics.min_temperature.toFixed(1)} - {analytics.max_temperature.toFixed(1)}</div>
                    </div>
                </div>
            </div>

            <div className="charts-grid">
                <div className="chart-card">
                    <h3>Equipment Type Distribution</h3>
                    <div className="chart-wrapper">
                        <Pie data={pieData} options={{ maintainAspectRatio: true, responsive: true }} />
                    </div>
                </div>

                <div className="chart-card">
                    <h3>Average Parameters by Type</h3>
                    <div className="chart-wrapper">
                        <Bar data={barData} options={{ maintainAspectRatio: true, responsive: true }} />
                    </div>
                </div>

                {dataset.equipment_records && dataset.equipment_records.length > 0 && (
                    <div className="chart-card full-width">
                        <h3>Pressure vs Flowrate Correlation</h3>
                        <div className="chart-wrapper">
                            <Scatter
                                data={scatterData}
                                options={{
                                    maintainAspectRatio: true,
                                    responsive: true,
                                    scales: {
                                        x: { title: { display: true, text: 'Flowrate' } },
                                        y: { title: { display: true, text: 'Pressure' } }
                                    }
                                }}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Analytics;
