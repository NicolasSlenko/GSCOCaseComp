"""
FDOT Transportation Infrastructure Dashboard Generator
Creates an interactive HTML visualization of Florida's transportation assets
supporting the Tampa-Orlando-Lakeland Olympic corridor.
"""

import json
import os

# Transportation metrics for the GTO corridor
transport_data = {
    "airports": [
        {
            "name": "Orlando International (MCO)",
            "city": "Orlando",
            "coords": [28.4294, -81.3089],
            "capacity_millions": 50,
            "international_gates": 30,
            "investment": "$2.8B (South Terminal)",
            "olympic_role": "Primary International Gateway"
        },
        {
            "name": "Tampa International (TPA)",
            "city": "Tampa",
            "coords": [27.9755, -82.5332],
            "capacity_millions": 25,
            "international_gates": 20,
            "investment": "$1.1B (Airside D)",
            "olympic_role": "Secondary Gateway"
        },
        {
            "name": "Gainesville Regional (GNV)",
            "city": "Gainesville",
            "coords": [29.6900, -82.2718],
            "capacity_millions": 0.3,
            "international_gates": 0,
            "investment": "Regional expansion",
            "olympic_role": "Stadium Access"
        }
    ],
    
    "highways": {
        "I-4": {
            "route": "Tampa to Orlando",
            "distance_miles": 84,
            "lanes": "8-10 lanes (urban)",
            "daily_traffic": 150000,
            "fdot_projects": "I-4 Ultimate (completed 2021), ongoing capacity",
            "olympic_significance": "Primary corridor connecting host cities"
        },
        "I-75": {
            "route": "Gainesville to Tampa",
            "distance_miles": 130,
            "lanes": "6-8 lanes",
            "daily_traffic": 100000,
            "fdot_projects": "Widening through Hernando, Pasco, Hillsborough",
            "olympic_significance": "Links main stadium to Tampa venues"
        },
        "Florida Turnpike": {
            "route": "Orlando to Miami",
            "distance_miles": 265,
            "lanes": "4-6 lanes (toll)",
            "daily_traffic": 80000,
            "fdot_projects": "SunPass technology upgrades",
            "olympic_significance": "Alternative route for South Florida visitors"
        }
    },
    
    "brightline": {
        "existing": {
            "route": "Miami to Orlando",
            "status": "Operational (2023)",
            "annual_ridership": 1500000,
            "top_speed_mph": 125,
            "on_time_rate": 0.95
        },
        "planned": {
            "route": "Orlando to Tampa",
            "stations": ["Orlando Airport", "Lakeland Downtown", "Tampa Downtown"],
            "travel_time_minutes": 60,
            "capacity_trains_per_hour": 8,
            "estimated_completion": "2028-2030",
            "olympic_significance": "Games-time mobility backbone"
        }
    },
    
    "travel_times": {
        "current": {
            "Tampa_to_Orlando": 90,
            "Tampa_to_Lakeland": 45,
            "Orlando_to_Lakeland": 50,
            "Gainesville_to_Tampa": 130,
            "Gainesville_to_Orlando": 120
        },
        "projected_with_rail": {
            "Tampa_to_Orlando": 60,
            "Tampa_to_Lakeland": 25,
            "Orlando_to_Lakeland": 30,
            "Gainesville_to_Tampa": 90,
            "Gainesville_to_Orlando": 75
        }
    },
    
    "fdot_investment": {
        "total_billions": 66,
        "central_florida_billions": 18,
        "timeframe": "2025-2030",
        "key_projects": [
            "I-4 technology integration",
            "SR-528 Beachline expansion",
            "US-27 Polk County improvements",
            "Interchange modernization",
            "Smart traffic signal deployment"
        ]
    },
    
    "transit_systems": {
        "LYNX_Orlando": {
            "type": "Bus",
            "routes": 60,
            "service_area": "Orange, Seminole, Osceola counties"
        },
        "HART_Tampa": {
            "type": "Bus + BRT",
            "routes": 40,
            "service_area": "Hillsborough County"
        },
        "SunRail_Orlando": {
            "type": "Commuter Rail",
            "miles": 32,
            "stations": 16,
            "service_area": "Orlando metro"
        }
    },
    
    "olympic_transit_targets": {
        "daily_rides_goal": 300000,
        "express_brt_routes": 12,
        "park_and_ride_spaces": 25000,
        "shuttle_buses": 500,
        "brightline_headways_minutes": 15
    },
    
    "productivity_roi": {
        "labor_force_millions": 2.5,
        "avg_time_saved_minutes": 25,
        "value_of_time_hourly": 25,
        "workdays_per_year": 250,
        "annual_gain_billions": 2.6
    }
}

# Generate HTML dashboard
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FDOT Transportation Infrastructure | Florida GTO Olympic Corridor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background: #F8F9FA;
            color: #0B2239;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #0B2239 0%, #004A7C 100%);
            color: white;
            padding: 48px 64px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 12px;
        }
        
        .header p {
            font-size: 18px;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 48px 64px;
        }
        
        .section {
            background: white;
            border-radius: 8px;
            padding: 32px;
            margin-bottom: 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .section-header {
            font-size: 24px;
            font-weight: 600;
            color: #0B2239;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 2px solid #004A7C;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }
        
        .kpi-card {
            background: #F8F9FA;
            padding: 24px;
            border-radius: 6px;
            border-left: 4px solid #004A7C;
        }
        
        .kpi-value {
            font-size: 32px;
            font-weight: bold;
            color: #004A7C;
            margin-bottom: 8px;
        }
        
        .kpi-label {
            font-size: 13px;
            color: #5C5C5C;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        
        .data-table th {
            background: #F8F9FA;
            padding: 12px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            color: #4A4A4A;
            border-bottom: 2px solid #D9D9D9;
        }
        
        .data-table td {
            padding: 12px;
            border-bottom: 1px solid #E0E0E0;
            font-size: 13px;
        }
        
        .data-table tr:hover {
            background: #F8F9FA;
        }
        
        .highlight {
            background: #004A7C;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: 600;
        }
        
        .info-box {
            background: #E8F4F8;
            border-left: 4px solid #004A7C;
            padding: 16px;
            margin: 16px 0;
            border-radius: 4px;
        }
        
        .info-box strong {
            color: #004A7C;
        }
        
        .route-card {
            background: white;
            border: 1px solid #D9D9D9;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 16px;
        }
        
        .route-header {
            font-size: 18px;
            font-weight: 600;
            color: #0B2239;
            margin-bottom: 12px;
        }
        
        .route-detail {
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 13px;
        }
        
        .route-detail dt {
            font-weight: 600;
            color: #5C5C5C;
        }
        
        .route-detail dd {
            color: #333333;
        }
        
        .comparison-chart {
            display: flex;
            gap: 12px;
            margin: 16px 0;
        }
        
        .bar-container {
            flex: 1;
        }
        
        .bar-label {
            font-size: 12px;
            color: #5C5C5C;
            margin-bottom: 4px;
        }
        
        .bar {
            height: 32px;
            background: #004A7C;
            border-radius: 4px;
            display: flex;
            align-items: center;
            padding-left: 12px;
            color: white;
            font-weight: 600;
            font-size: 13px;
        }
        
        .bar.improved {
            background: #28A745;
        }
        
        .footer {
            text-align: center;
            padding: 32px;
            color: #5C5C5C;
            font-size: 12px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 24px 16px;
            }
            
            .kpi-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚆 Florida Transportation Infrastructure</h1>
        <p>Supporting the Tampa–Orlando–Lakeland Olympic Corridor</p>
    </div>
    
    <div class="container">
        <!-- Key Metrics Overview -->
        <div class="section">
            <div class="section-header">📊 Key Infrastructure Metrics</div>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">$66B</div>
                    <div class="kpi-label">FDOT Investment (2025-2030)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">$18B</div>
                    <div class="kpi-label">Central Florida Allocation</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">84 mi</div>
                    <div class="kpi-label">I-4 Corridor (Tampa-Orlando)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">50M+</div>
                    <div class="kpi-label">MCO Airport Capacity/Year</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">60 min</div>
                    <div class="kpi-label">Brightline: Tampa to Orlando</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">$2.6B</div>
                    <div class="kpi-label">Annual Productivity Gain (Est.)</div>
                </div>
            </div>
        </div>
        
        <!-- Airport Infrastructure -->
        <div class="section">
            <div class="section-header">✈️ Airport Infrastructure</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Airport</th>
                        <th>City</th>
                        <th>Capacity (Annual)</th>
                        <th>International Gates</th>
                        <th>Recent Investment</th>
                        <th>Olympic Role</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Orlando International (MCO)</strong></td>
                        <td>Orlando</td>
                        <td><span class="highlight">50M+</span></td>
                        <td>30+</td>
                        <td>$2.8B (South Terminal)</td>
                        <td>Primary International Gateway</td>
                    </tr>
                    <tr>
                        <td><strong>Tampa International (TPA)</strong></td>
                        <td>Tampa</td>
                        <td>25M+</td>
                        <td>20+</td>
                        <td>$1.1B (Airside D)</td>
                        <td>Secondary Gateway</td>
                    </tr>
                    <tr>
                        <td><strong>Gainesville Regional (GNV)</strong></td>
                        <td>Gainesville</td>
                        <td>300K</td>
                        <td>0</td>
                        <td>Regional expansion</td>
                        <td>Stadium Access</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="info-box">
                <strong>Olympic Advantage:</strong> Combined MCO + TPA capacity exceeds 75 million passengers annually, 
                with direct international service from 100+ destinations. Recent terminal expansions provide 
                world-class arrival experience for athletes and global visitors.
            </div>
        </div>
        
        <!-- Interstate Highway System -->
        <div class="section">
            <div class="section-header">🛣️ Interstate Highway Network</div>
            
            <div class="route-card">
                <div class="route-header">I-4: Tampa ↔ Orlando</div>
                <dl class="route-detail">
                    <dt>Distance:</dt>
                    <dd>84 miles</dd>
                    <dt>Lanes:</dt>
                    <dd>8-10 lanes (urban segments)</dd>
                    <dt>Daily Traffic:</dt>
                    <dd>150,000+ vehicles</dd>
                    <dt>FDOT Projects:</dt>
                    <dd>I-4 Ultimate (completed 2021), ongoing capacity & technology upgrades</dd>
                    <dt>Olympic Significance:</dt>
                    <dd><strong>Primary artery connecting Tampa (hospitality) and Orlando (media/tech hubs)</strong></dd>
                </dl>
            </div>
            
            <div class="route-card">
                <div class="route-header">I-75: Gainesville ↔ Tampa</div>
                <dl class="route-detail">
                    <dt>Distance:</dt>
                    <dd>~130 miles</dd>
                    <dt>Lanes:</dt>
                    <dd>6-8 lanes</dd>
                    <dt>Daily Traffic:</dt>
                    <dd>100,000+ vehicles</dd>
                    <dt>FDOT Projects:</dt>
                    <dd>Widening through Hernando, Pasco, Hillsborough counties</dd>
                    <dt>Olympic Significance:</dt>
                    <dd><strong>Links main stadium (Ben Hill Griffin, 88k capacity) to Tampa infrastructure</strong></dd>
                </dl>
            </div>
            
            <div class="route-card">
                <div class="route-header">Florida's Turnpike: Orlando ↔ Miami</div>
                <dl class="route-detail">
                    <dt>Distance:</dt>
                    <dd>265 miles</dd>
                    <dt>Type:</dt>
                    <dd>Toll road with SunPass technology</dd>
                    <dt>Daily Traffic:</dt>
                    <dd>80,000+ vehicles</dd>
                    <dt>Olympic Significance:</dt>
                    <dd>Alternative route for international visitors arriving via Miami/Fort Lauderdale</dd>
                </dl>
            </div>
        </div>
        
        <!-- Brightline High-Speed Rail -->
        <div class="section">
            <div class="section-header">🚄 Brightline High-Speed Rail</div>
            
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">125 mph</div>
                    <div class="kpi-label">Top Speed</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">95%</div>
                    <div class="kpi-label">On-Time Performance</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">1.5M</div>
                    <div class="kpi-label">Annual Riders (Miami-Orlando)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">2028-30</div>
                    <div class="kpi-label">Orlando-Tampa Completion (Est.)</div>
                </div>
            </div>
            
            <h3 style="margin: 24px 0 16px 0; font-size: 18px; color: #004A7C;">Planned Orlando–Tampa Extension</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Station</th>
                        <th>Location</th>
                        <th>Connection</th>
                        <th>Travel Time from Orlando</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Orlando International Airport</strong></td>
                        <td>Existing terminal access</td>
                        <td>MCO, SunRail, LYNX</td>
                        <td>—</td>
                    </tr>
                    <tr>
                        <td><strong>Lakeland Downtown</strong></td>
                        <td>Central business district (planned)</td>
                        <td>Local transit, Olympic Village</td>
                        <td>~30 minutes</td>
                    </tr>
                    <tr>
                        <td><strong>Tampa Downtown</strong></td>
                        <td>Near Amalie Arena (planned)</td>
                        <td>HART, venue cluster</td>
                        <td>~60 minutes</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="info-box">
                <strong>Olympic Impact:</strong> Brightline provides Games-time mobility backbone with capacity for 
                <span class="highlight">8 trains/hour</span> during peak periods. Reduces highway congestion and 
                creates legacy transit infrastructure connecting all three host cities.
            </div>
        </div>
        
        <!-- Travel Time Improvements -->
        <div class="section">
            <div class="section-header">⏱️ Travel Time Improvements</div>
            <p style="margin-bottom: 24px; color: #5C5C5C;">Projected time savings with Brightline + BRT investments:</p>
            
            <div style="margin-bottom: 24px;">
                <div class="bar-label">Tampa → Orlando</div>
                <div class="comparison-chart">
                    <div class="bar-container">
                        <div class="bar" style="width: 90%;">Current: 90 min</div>
                    </div>
                    <div class="bar-container">
                        <div class="bar improved" style="width: 60%;">Projected: 60 min (-30 min)</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 24px;">
                <div class="bar-label">Tampa → Lakeland</div>
                <div class="comparison-chart">
                    <div class="bar-container">
                        <div class="bar" style="width: 45%;">Current: 45 min</div>
                    </div>
                    <div class="bar-container">
                        <div class="bar improved" style="width: 25%;">Projected: 25 min (-20 min)</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 24px;">
                <div class="bar-label">Orlando → Lakeland</div>
                <div class="comparison-chart">
                    <div class="bar-container">
                        <div class="bar" style="width: 50%;">Current: 50 min</div>
                    </div>
                    <div class="bar-container">
                        <div class="bar improved" style="width: 30%;">Projected: 30 min (-20 min)</div>
                    </div>
                </div>
            </div>
            
            <div class="info-box">
                <strong>Productivity ROI:</strong> Time savings across 2.5M corridor workers × $25/hour value of time 
                × 250 workdays = <span class="highlight">$2.6 billion annual productivity gain</span>
            </div>
        </div>
        
        <!-- Olympic Transit Plan -->
        <div class="section">
            <div class="section-header">🎯 Olympic Transit Targets</div>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">300K</div>
                    <div class="kpi-label">Daily Rides Goal (Games Period)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">12</div>
                    <div class="kpi-label">Express BRT Routes</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">25K</div>
                    <div class="kpi-label">Park-and-Ride Spaces</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">500</div>
                    <div class="kpi-label">Shuttle Buses</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">15 min</div>
                    <div class="kpi-label">Brightline Headways (Peak)</div>
                </div>
            </div>
            
            <h3 style="margin: 32px 0 16px 0; font-size: 18px; color: #004A7C;">Existing Transit Systems</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>System</th>
                        <th>Type</th>
                        <th>Coverage</th>
                        <th>Olympic Enhancement</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>LYNX (Orlando)</strong></td>
                        <td>Bus</td>
                        <td>60+ routes, Orange/Seminole/Osceola counties</td>
                        <td>Express venue shuttles + integrated ticketing</td>
                    </tr>
                    <tr>
                        <td><strong>HART (Tampa)</strong></td>
                        <td>Bus + BRT</td>
                        <td>40+ routes, Hillsborough County</td>
                        <td>Expanded BRT to Brightline stations</td>
                    </tr>
                    <tr>
                        <td><strong>SunRail (Orlando)</strong></td>
                        <td>Commuter Rail</td>
                        <td>32 miles, 16 stations</td>
                        <td>Extended hours + Brightline integration</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- City Infrastructure Summary -->
        <div class="section">
            <div class="section-header">🏙️ Host City Transportation Summary</div>
            
            <div class="route-card">
                <div class="route-header">🌴 Tampa (Tourism & Hospitality Hub)</div>
                <ul style="margin-left: 24px; color: #333333; font-size: 14px; line-height: 1.8;">
                    <li>✈️ Tampa International Airport (TPA): 25M passengers/year</li>
                    <li>🏟️ Raymond James Stadium (65,618) + Amalie Arena (19,092)</li>
                    <li>🚆 Brightline station (downtown, planned)</li>
                    <li>🛣️ Interstate access: I-4, I-75, I-275</li>
                    <li>🏨 25,000+ hotel rooms (expandable to 35,000)</li>
                </ul>
            </div>
            
            <div class="route-card">
                <div class="route-header">🎢 Orlando (Media & Tech Hub)</div>
                <ul style="margin-left: 24px; color: #333333; font-size: 14px; line-height: 1.8;">
                    <li>✈️ Orlando International Airport (MCO): 50M+ passengers/year</li>
                    <li>🏟️ Camping World Stadium (65,438) + Amway Center (18,846)</li>
                    <li>🚆 Brightline + SunRail integrated rail network</li>
                    <li>🛣️ Interstate access: I-4, Florida's Turnpike, SR-528</li>
                    <li>🏨 130,000+ hotel rooms (theme park infrastructure)</li>
                </ul>
            </div>
            
            <div class="route-card">
                <div class="route-header">🏘️ Lakeland (Olympic Village & Logistics)</div>
                <ul style="margin-left: 24px; color: #333333; font-size: 14px; line-height: 1.8;">
                    <li>🚆 Brightline station: Midpoint on Orlando–Tampa corridor</li>
                    <li>🏘️ Olympic Village site: Central location, land availability</li>
                    <li>🛣️ Interstate access: I-4, US-98</li>
                    <li>📦 Central distribution for venues across corridor</li>
                    <li>🏡 Post-Games: Convert to 3,000–4,000 workforce/student housing</li>
                </ul>
            </div>
            
            <div class="route-card">
                <div class="route-header">🐊 Gainesville (Main Stadium)</div>
                <ul style="margin-left: 24px; color: #333333; font-size: 14px; line-height: 1.8;">
                    <li>🏟️ Ben Hill Griffin Stadium: 88,548 capacity ✅ (meets 80k requirement)</li>
                    <li>🎓 University of Florida: 55,000 students, existing event infrastructure</li>
                    <li>✈️ Gainesville Regional Airport (GNV): Regional/charter capacity</li>
                    <li>🛣️ Interstate access: I-75, US-441</li>
                </ul>
            </div>
        </div>
        
        <!-- Next Steps -->
        <div class="section">
            <div class="section-header">📋 Implementation Next Steps</div>
            <ol style="margin-left: 24px; color: #333333; font-size: 14px; line-height: 2;">
                <li><strong>Finalize Brightline Orlando–Tampa timeline</strong> and station locations with coordination between Brightline Florida and FDOT</li>
                <li><strong>Model Olympics-period transit demand</strong> (300k rides/day target) using FDOT traffic models + IOC event schedules</li>
                <li><strong>Secure FDOT commitment</strong> for express lane conversions, BRT deployment, and park-and-ride development</li>
                <li><strong>Coordinate with MCO/TPA</strong> for international visitor processing capacity and customs expansion</li>
                <li><strong>Develop integrated ticketing system</strong> combining Brightline, SunRail, LYNX, HART with Olympic credentials</li>
            </ol>
        </div>
    </div>
    
    <div class="footer">
        <p><strong>Document prepared for Florida Olympic Vision: GTO Case Competition</strong></p>
        <p>Data sources: FDOT 2025 Infrastructure Program | Brightline Florida | BEBR 2023 | Visit Florida 2024</p>
        <p>Last updated: November 2025</p>
    </div>
</body>
</html>
"""

# Save HTML dashboard
output_path = os.path.join('docs', 'fdot_transportation_dashboard.html')
os.makedirs('docs', exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("=" * 70)
print("FDOT TRANSPORTATION INFRASTRUCTURE DASHBOARD GENERATED")
print("=" * 70)
print(f"\n✓ Interactive HTML dashboard created: {output_path}")
print("\nKey highlights included:")
print("  • $66B FDOT investment program (2025-2030)")
print("  • Airport capacity: MCO (50M+), TPA (25M+)")
print("  • Interstate highways: I-4 (84 mi), I-75 (130 mi)")
print("  • Brightline Orlando-Tampa extension (60 min travel time)")
print("  • $2.6B annual productivity ROI from transit improvements")
print("  • Olympic transit targets: 300k daily rides, 12 BRT routes")
print("\nOpen the HTML file in a browser to view the interactive dashboard!")
print("=" * 70)
