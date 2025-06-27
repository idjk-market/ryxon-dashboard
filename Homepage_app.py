<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Dashboard</title>
    <style>
        :root {
            --primary-color: #2962FF;
            --success-color: #00C853;
            --warning-color: #FFAB00;
            --danger-color: #D50000;
            --bg-color: #121212;
            --card-color: #1E1E1E;
            --text-color: #E0E0E0;
            --border-color: #333333;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
            min-height: 100vh;
        }
        
        .sidebar {
            background-color: var(--card-color);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .main-content {
            display: grid;
            grid-template-rows: auto 1fr;
            gap: 20px;
        }
        
        .metrics-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        
        .card {
            background-color: var(--card-color);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .card h2 {
            margin-top: 0;
            font-size: 1.2rem;
            color: #9E9E9E;
        }
        
        .card .value {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .card .change {
            display: flex;
            align-items: center;
            font-size: 1rem;
            color: var(--success-color);
        }
        
        .card .change.danger {
            color: var(--danger-color);
        }
        
        .card .change.warning {
            color: var(--warning-color);
        }
        
        .table-container {
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        th {
            background-color: var(--card-color);
            color: #9E9E9E;
            font-weight: 600;
        }
        
        tr:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        .status-active {
            color: var(--success-color);
        }
        
        .status-expired {
            color: #9E9E9E;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            padding: 12px 0;
            cursor: pointer;
            border-bottom: 1px solid var(--border-color);
        }
        
        .nav-item:last-child {
            border-bottom: none;
        }
        
        .nav-item.active {
            color: var(--primary-color);
            font-weight: bold;
        }
        
        .theme-switch {
            display: flex;
            align-items: center;
            margin-top: 30px;
            padding: 10px;
            border-radius: 5px;
            background-color: rgba(41, 98, 255, 0.1);
            cursor: pointer;
        }
        
        @media (max-width: 1200px) {
            .metrics-container {
                grid-template-columns: 1fr 1fr;
            }
        }
        
        @media (max-width: 768px) {
            body {
                grid-template-columns: 1fr;
            }
            
            .metrics-container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h1>Trading Dashboard</h1>
        
        <div class="nav-item active">Dashboard</div>
        <div class="nav-item">Upload Trades</div>
        <div class="nav-item">Manual Entry</div>
        <div class="nav-item">Analytics</div>
        <div class="nav-item">Settings</div>
        <div class="nav-item">Logout</div>
        
        <div class="theme-switch">
            <span>Dark Mode</span>
        </div>
    </div>
    
    <div class="main-content">
        <div class="metrics-container">
            <div class="card">
                <h2>Open Positions</h2>
                <div class="value">142</div>
                <div class="change">
                    ↑ +12% from last week
                </div>
            </div>
            
            <div class="card">
                <h2>Risk Exposure</h2>
                <div class="value">$4.2M</div>
                <div class="change">
                    ↑ Within limits
                </div>
            </div>
            
            <div class="card">
                <h2>Today's P&L</h2>
                <div class="value">$124K</div>
                <div class="change">
                    ↑ +2.4% MTD
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>Recent Trades</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Trade ID</th>
                            <th>Instrument</th>
                            <th>Notional</th>
                            <th>Price</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>FX-2023-0456</td>
                            <td>EUR/USD</td>
                            <td>$5,000,000</td>
                            <td>1.0856</td>
                            <td>2023-05-15</td>
                            <td class="status-active">Active</td>
                        </tr>
                        <tr>
                            <td>IRS-2023-0789</td>
                            <td>10Y IRS</td>
                            <td>$10,000,000</td>
                            <td>2.34</td>
                            <td>2023-05-14</td>
                            <td class="status-active">Active</td>
                        </tr>
                        <tr>
                            <td>OPT-2023-0321</td>
                            <td>SPX Call</td>
                            <td>$2,500,000</td>
                            <td>35.5</td>
                            <td>2023-05-13</td>
                            <td class="status-expired">Expired</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
