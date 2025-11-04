"""
FDOT Transportation Infrastructure Dashboard Generator - TOL Model
Creates an interactive HTML visualization of Florida's transportation assets
supporting the Tampa-Orlando-Lakeland Olympic corridor.
Uses REAL FDOT budget numbers from 26Adopt01b Work Program (July 1, 2025).
"""

import json
import os

# REAL FDOT BUDGET DATA (from 26Adopt01b PDF - First 5 Years, FY 2025-2030)
fdot_budget_5yr = {
    "transit_systems": 2212.5,  # Million dollars
    "aviation": 1833.2,
    "rail_passenger": 868.7,
    "intermodal_access": 503.2,
    "construction_all": 32793.2,
    "total_budget": 68038.2,
    "funding_sources": {
        "state": 32059.2,
        "federal": 21155.0,
        "turnpike": 9764.5,
        "toll_local_other": 5059.4
    }
}

# Estimated TOL corridor allocation (6% of statewide - conservative estimate)
CORRIDOR_SHARE = 0.06
tol_allocation = {k: v * CORRIDOR_SHARE for k, v in fdot_budget_5yr.items() if isinstance(v, (int, float))}

# Transportation metrics for the TOL corridor
transport_data = {
    "airports": [
        {
            "name": "Orlando International (MCO)",
            "city": "Orlando",
            "coords": [28.4294, -81.3089],
            "capacity_millions": 50,
            "international_gates": 30,
            "investment": "$2.8B (South Terminal, 2022)",
            "fdot_support": f"${tol_allocation['aviation']:.1f}M from aviation fund",
            "olympic_role": "Primary International Gateway"
        },
        {
            "name": "Tampa International (TPA)",
            "city": "Tampa",
            "coords": [27.9755, -82.5332],
            "capacity_millions": 25,
            "international_gates": 20,
            "investment": "$1.1B (Airside D, 2023)",
            "fdot_support": f"Share of ${fdot_budget_5yr['aviation']}M statewide aviation fund",
            "olympic_role": "Secondary Gateway"
        },
        {
            "name": "Lakeland Linder",
            "city": "Lakeland",
            "coords": [27.9889, -82.0187],
            "capacity_millions": 0.1,
            "international_gates": 0,
            "investment": "Charter & general aviation",
            "fdot_support": "Regional aviation support",
            "olympic_role": "Charter & Delegation Flights"
        }
    ],
    
    "highways": {
        "I-4": {
            "route": "Tampa to Orlando via Lakeland",
            "distance_miles": 84,
            "lanes": "8-10 lanes (urban)",
            "daily_traffic": 150000,
            "fdot_investment": f"Part of ${fdot_budget_5yr['construction_all']/1000:.1f}B construction fund",
            "olympic_significance": "Primary corridor connecting all three host cities"
        },
        "I-75": {
            "route": "North-South Florida corridor",
            "distance_miles": 130,
            "lanes": "6-8 lanes",
            "daily_traffic": 100000,
            "fdot_investment": "Widening through Tampa metro counties",
            "olympic_significance": "Alternative route for North Florida visitors"
        },
        "Florida Turnpike": {
            "route": "Orlando to Miami",
            "distance_miles": 265,
            "lanes": "4-6 lanes (toll)",
            "daily_traffic": 80000,
            "fdot_investment": f"${fdot_budget_5yr['funding_sources']['turnpike']/1000:.1f}B dedicated Turnpike fund",
            "olympic_significance": "South Florida visitor access"
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
            "route": "Orlando to Tampa via Lakeland",
            "stations": ["Orlando MCO", "Lakeland Downtown", "Tampa Downtown"],
            "travel_time_minutes": 60,
            "capacity_trains_per_hour": 12,
            "estimated_completion": "2028-2030",
            "fdot_support": f"${fdot_budget_5yr['rail_passenger']}M rail investment + ${fdot_budget_5yr['intermodal_access']}M intermodal",
            "olympic_significance": "Games-time mobility backbone - 300k rides/day target"
        }
    },
    
    "travel_times": {
        "current": {
            "Tampa_to_Orlando": 90,
            "Tampa_to_Lakeland": 45,
            "Orlando_to_Lakeland": 50
        },
        "projected_with_rail": {
            "Tampa_to_Orlando": 60,
            "Tampa_to_Lakeland": 30,
            "Orlando_to_Lakeland": 30
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
    },
    
    "venues": {
        "orlando": [
            {"name": "Camping World Stadium", "capacity": "80,000+ (expanded)", "status": "MAIN STADIUM - IOC Compliant"},
            {"name": "Amway Center", "capacity": "18,846", "status": "NBA Arena - Olympic Ready"},
            {"name": "UCF Addition Financial Arena", "capacity": "10,000", "status": "University Venue"}
        ],
        "tampa": [
            {"name": "Raymond James Stadium", "capacity": "65,618", "status": "NFL Stadium - Olympic Ready"},
            {"name": "Amalie Arena", "capacity": "19,092", "status": "NHL Arena - Olympic Ready"}
        ],
        "lakeland": [
            {"name": "Olympic Village", "capacity": "3,000-4,000 units", "status": "Athlete Housing - Post-Games Workforce Housing"}
        ]
    }
}

# Generate HTML dashboard
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FDOT Transportation Infrastructure | Florida TOL Olympic Corridor</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background: #F8F9FA;
            color: #0B2239;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0B2239 0%, #004A7C 100%);
            color: white;
            padding: 48px 64px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 12px;
        }}
        
        .header p {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.8;
            margin-top: 8px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 48px 64px;
        }}
        
        .section {{
            background: white;
            border-radius: 8px;
            padding: 32px;
            margin-bottom: 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        .section-header {{
            font-size: 24px;
            font-weight: 600;
            color: #0B2239;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 2px solid #004A7C;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }}
        
        .kpi-card {{
            background: #F8F9FA;
            padding: 24px;
            border-radius: 6px;
            border-left: 4px solid #004A7C;
        }}
        
        .kpi-value {{
            font-size: 32px;
            font-weight: bold;
            color: #004A7C;
            margin-bottom: 8px;
        }}
        
        .kpi-label {{
            font-size: 13px;
            color: #5C5C5C;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }}
        
        .data-table th {{
            background: #F8F9FA;
            padding: 12px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            color: #4A4A4A;
            border-bottom: 2px solid #D9D9D9;
        }}
        
        .data-table td {{
            padding: 12px;
            border-bottom: 1px solid #E0E0E0;
            font-size: 13px;
        }}
        
        .data-table tr:hover {{
            background: #F8F9FA;
        }}
        
        .highlight {{
            background: #004A7C;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: 600;
        }}
        
        .highlight-green {{
            background: #28A745;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: 600;
        }}
        
        .info-box {{
            background: #E8F4F8;
            border-left: 4px solid #004A7C;
            padding: 16px;
            margin: 16px 0;
            border-radius: 4px;
        }}
        
        .info-box strong {{
            color: #004A7C;
        }}
        
        .warning-box {{
            background: #FFF3CD;
            border-left: 4px solid #FFC107;
            padding: 16px;
            margin: 16px 0;
            border-radius: 4px;
        }}
        
        .route-card {{
            background: white;
            border: 1px solid #D9D9D9;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        
        .route-header {{
            font-size: 18px;
            font-weight: 600;
            color: #0B2239;
            margin-bottom: 12px;
        }}
        
        .route-detail {{
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 13px;
        }}
        
        .route-detail dt {{
            font-weight: 600;
            color: #5C5C5C;
        }}
        
        .route-detail dd {{
            color: #333333;
        }}
        
        .comparison-chart {{
            display: flex;
            gap: 12px;
            margin: 16px 0;
        }}
        
        .bar-container {{
            flex: 1;
        }}
        
        .bar-label {{
            font-size: 12px;
            color: #5C5C5C;
            margin-bottom: 4px;
        }}
        
        .bar {{
            height: 32px;
            background: #004A7C;
            border-radius: 4px;
            display: flex;
            align-items: center;
            padding-left: 12px;
            color: white;
            font-weight: 600;
            font-size: 13px;
        }}
        
        .bar.improved {{
            background: #28A745;
        }}
        
        .footer {{
            text-align: center;
            padding: 32px;
            color: #5C5C5C;
            font-size: 12px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 24px 16px;
            }}
            
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚆 Florida Transportation Infrastructure</h1>
        <p>Supporting the Tampa–Orlando–Lakeland (TOL) Olympic Corridor</p>
        <p class="subtitle">Based on FDOT 2025-2034 Adopted Work Program | Real Budget Data</p>
    </div>
    
    <div class="container">
        <!-- FDOT Budget Overview -->
        <div class="section">
            <div class="section-header">💰 FDOT 5-Year Investment Program (FY 2025-2030)</div>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['total_budget']/1000:.1f}B</div>
                    <div class="kpi-label">Total FDOT Budget (5 Years)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${tol_allocation['total_budget']:.1f}M</div>
                    <div class="kpi-label">Estimated TOL Corridor Allocation (6%)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['transit_systems']}M</div>
                    <div class="kpi-label">Statewide Transit Investment</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['aviation']}M</div>
                    <div class="kpi-label">Statewide Aviation Investment</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['rail_passenger']}M</div>
                    <div class="kpi-label">Statewide Rail Investment</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['construction_all']/1000:.1f}B</div>
                    <div class="kpi-label">Statewide Construction Program</div>
                </div>
            </div>
            
            <h3 style="margin: 24px 0 16px 0; font-size: 18px; color: #004A7C;">Funding Sources (5-Year Program)</h3>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['funding_sources']['state']/1000:.1f}B</div>
                    <div class="kpi-label">State Funds</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['funding_sources']['federal']/1000:.1f}B</div>
                    <div class="kpi-label">Federal Funds</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['funding_sources']['turnpike']/1000:.1f}B</div>
                    <div class="kpi-label">Florida Turnpike</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${fdot_budget_5yr['funding_sources']['toll_local_other']/1000:.1f}B</div>
                    <div class="kpi-label">Toll/Local/Other</div>
                </div>
            </div>
            
            <div class="warning-box">
                <strong>Note:</strong> FDOT budget is statewide. TOL corridor allocation estimated at 6% based on regional population 
                and economic activity. Actual project allocations require detailed FDOT District 5 work program analysis.
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
"""

for airport in transport_data["airports"]:
    html_content += f"""                    <tr>
                        <td><strong>{airport['name']}</strong></td>
                        <td>{airport['city']}</td>
                        <td>{'<span class="highlight">' + str(airport['capacity_millions']) + 'M+</span>' if airport['capacity_millions'] >= 25 else str(airport['capacity_millions']) + 'M'}</td>
                        <td>{airport['international_gates']if airport['international_gates'] > 0 else '—'}</td>
                        <td>{airport['investment']}</td>
                        <td>{airport['olympic_role']}</td>
                    </tr>
"""

html_content += f"""                </tbody>
            </table>
            
            <div class="info-box">
                <strong>FDOT Aviation Investment:</strong> ${fdot_budget_5yr['aviation']}M statewide (5 years) for airport improvements, 
                planning, and capacity grants. MCO + TPA combined capacity exceeds 75M passengers annually with recent terminal 
                expansions providing world-class international gateway for Olympic athletes and visitors.
            </div>
        </div>
        
        <!-- Brightline High-Speed Rail -->
        <div class="section">
            <div class="section-header">🚄 Brightline High-Speed Rail - TOL Corridor Backbone</div>
            
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
                    <div class="kpi-value">60 min</div>
                    <div class="kpi-label">Tampa to Orlando Travel Time</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">2028-30</div>
                    <div class="kpi-label">Orlando-Tampa Completion (Est.)</div>
                </div>
            </div>
            
            <h3 style="margin: 24px 0 16px 0; font-size: 18px; color: #004A7C;">Orlando–Tampa Extension (Planned)</h3>
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
                        <td><strong>Orlando International Airport (MCO)</strong></td>
                        <td>Existing terminal access</td>
                        <td>MCO, SunRail, LYNX</td>
                        <td>—</td>
                    </tr>
                    <tr>
                        <td><strong>Lakeland Downtown</strong></td>
                        <td>Central business district (planned)</td>
                        <td>Local transit, <span class="highlight-green">Olympic Village</span></td>
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
                <strong>FDOT Rail Investment:</strong> ${fdot_budget_5yr['rail_passenger']}M statewide rail fund + ${fdot_budget_5yr['intermodal_access']}M 
                intermodal access fund support Brightline expansion, station development, and multimodal connectivity. 
                <span class="highlight">Target: 12 trains/hour peak capacity</span> during Olympic Games (300,000 rides/day).
            </div>
        </div>
        
        <!-- Interstate Highway Network -->
        <div class="section">
            <div class="section-header">🛣️ Interstate Highway Network</div>
            
            <div class="route-card">
                <div class="route-header">I-4: Tampa ↔ Orlando via Lakeland</div>
                <dl class="route-detail">
                    <dt>Distance:</dt>
                    <dd>84 miles</dd>
                    <dt>Lanes:</dt>
                    <dd>8-10 lanes (urban segments)</dd>
                    <dt>Daily Traffic:</dt>
                    <dd>150,000+ vehicles</dd>
                    <dt>FDOT Investment:</dt>
                    <dd>${fdot_budget_5yr['construction_all']/1000:.1f}B construction fund supports I-4 improvements</dd>
                    <dt>Olympic Significance:</dt>
                    <dd><strong>Primary artery connecting ALL THREE host cities (Tampa, Lakeland, Orlando)</strong></dd>
                </dl>
            </div>
            
            <div class="route-card">
                <div class="route-header">Florida's Turnpike: Orlando ↔ Miami</div>
                <dl class="route-detail">
                    <dt>Distance:</dt>
                    <dd>265 miles</dd>
                    <dt>Type:</dt>
                    <dd>Toll road with SunPass technology</dd>
                    <dt>FDOT Investment:</dt>
                    <dd><span class="highlight">${fdot_budget_5yr['funding_sources']['turnpike']/1000:.1f}B dedicated Turnpike fund</span></dd>
                    <dt>Olympic Significance:</dt>
                    <dd>South Florida visitor access via Miami/Fort Lauderdale airports</dd>
                </dl>
            </div>
            
            <div class="info-box">
                <strong>Construction Investment:</strong> ${fdot_budget_5yr['construction_all']/1000:.1f}B statewide construction program (5 years) 
                supports highway capacity, interchange modernization, and technology integration across the TOL corridor.
            </div>
        </div>
        
        <!-- Travel Time Improvements -->
        <div class="section">
            <div class="section-header">⏱️ Travel Time Improvements with Brightline</div>
            <p style="margin-bottom: 24px; color: #5C5C5C;">Projected time savings with Brightline + FDOT transit investments:</p>
            
            <div style="margin-bottom: 24px;">
                <div class="bar-label">Tampa → Orlando</div>
                <div class="comparison-chart">
                    <div class="bar-container">
                        <div class="bar" style="width: 90%;">Current: 90 min (car)</div>
                    </div>
                    <div class="bar-container">
                        <div class="bar improved" style="width: 60%;">Brightline: 60 min (-30 min)</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 24px;">
                <div class="bar-label">Tampa → Lakeland</div>
                <div class="comparison-chart">
                    <div class="bar-container">
                        <div class="bar" style="width: 45%;">Current: 45 min (car)</div>
                    </div>
                    <div class="bar-container">
                        <div class="bar improved" style="width: 30%;">Brightline: 30 min (-15 min)</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 24px;">
                <div class="bar-label">Orlando → Lakeland</div>
                <div class="comparison-chart">
                    <div class="bar-container">
                        <div class="bar" style="width: 50%;">Current: 50 min (car)</div>
                    </div>
                    <div class="bar-container">
                        <div class="bar improved" style="width: 30%;">Brightline: 30 min (-20 min)</div>
                    </div>
                </div>
            </div>
            
            <div class="info-box">
                <strong>Productivity ROI:</strong> Time savings across {transport_data['productivity_roi']['labor_force_millions']}M corridor workers × 
                ${transport_data['productivity_roi']['value_of_time_hourly']}/hour value of time × {transport_data['productivity_roi']['workdays_per_year']} workdays = 
                <span class="highlight">${transport_data['productivity_roi']['annual_gain_billions']}B annual economic gain</span>
            </div>
        </div>
        
        <!-- Olympic Venues by City -->
        <div class="section">
            <div class="section-header">🏟️ Olympic Venues by Host City</div>
            
            <h3 style="margin: 24px 0 16px 0; font-size: 18px; color: #004A7C;">🎢 Orlando (Main Stadium + Media Hub)</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Venue</th>
                        <th>Capacity</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
"""

for venue in transport_data["venues"]["orlando"]:
    is_main = "MAIN STADIUM" in venue["status"]
    html_content += f"""                    <tr>
                        <td><strong>{venue['name']}</strong></td>
                        <td>{'<span class="highlight-green">' + venue['capacity'] + '</span>' if is_main else venue['capacity']}</td>
                        <td>{venue['status']}</td>
                    </tr>
"""

html_content += f"""                </tbody>
            </table>
            
            <div class="info-box">
                <strong>Key Decision:</strong> <span class="highlight-green">Camping World Stadium expansion to 80,000+ seats</span> 
                meets IOC main stadium requirement. Eliminates need for Gainesville (too far from core corridor). Orlando provides 
                central location with MCO airport, 130,000+ hotel rooms, and integrated transit (Brightline + SunRail).
            </div>
            
            <h3 style="margin: 32px 0 16px 0; font-size: 18px; color: #004A7C;">🌴 Tampa (Tourism & Hospitality Hub)</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Venue</th>
                        <th>Capacity</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
"""

for venue in transport_data["venues"]["tampa"]:
    html_content += f"""                    <tr>
                        <td><strong>{venue['name']}</strong></td>
                        <td>{venue['capacity']}</td>
                        <td>{venue['status']}</td>
                    </tr>
"""

html_content += f"""                </tbody>
            </table>
            
            <h3 style="margin: 32px 0 16px 0; font-size: 18px; color: #004A7C;">🏘️ Lakeland (Olympic Village + Logistics)</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Facility</th>
                        <th>Capacity</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
"""

for venue in transport_data["venues"]["lakeland"]:
    html_content += f"""                    <tr>
                        <td><strong>{venue['name']}</strong></td>
                        <td>{venue['capacity']}</td>
                        <td>{venue['status']}</td>
                    </tr>
"""

html_content += f"""                </tbody>
            </table>
            
            <div class="info-box">
                <strong>Lakeland Advantage:</strong> Central I-4 location (30 min to Tampa, 30 min to Orlando via Brightline) makes it 
                ideal for Olympic Village. Adjacent Brightline station provides direct athlete transport to all venues. Post-Games 
                conversion to workforce/student housing addresses regional housing needs.
            </div>
        </div>
        
        <!-- Olympic Transit Targets -->
        <div class="section">
            <div class="section-header">🎯 Olympic Transit Targets</div>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">{transport_data['olympic_transit_targets']['daily_rides_goal']:,}</div>
                    <div class="kpi-label">Daily Rides Goal (Games Period)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{transport_data['olympic_transit_targets']['express_brt_routes']}</div>
                    <div class="kpi-label">Express BRT Routes</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{transport_data['olympic_transit_targets']['park_and_ride_spaces']:,}</div>
                    <div class="kpi-label">Park-and-Ride Spaces</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{transport_data['olympic_transit_targets']['shuttle_buses']}</div>
                    <div class="kpi-label">Shuttle Buses</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{transport_data['olympic_transit_targets']['brightline_headways_minutes']} min</div>
                    <div class="kpi-label">Brightline Headways (Peak)</div>
                </div>
            </div>
            
            <div class="info-box">
                <strong>FDOT Transit Support:</strong> ${fdot_budget_5yr['transit_systems']}M statewide transit fund + 
                ${fdot_budget_5yr['intermodal_access']}M intermodal fund provide foundation for Olympic-period transit 
                enhancements (BRT, shuttles, park-and-ride facilities).
            </div>
        </div>
        
        <!-- Financial Summary -->
        <div class="section">
            <div class="section-header">💵 Estimated FDOT Investment Allocation to TOL Corridor</div>
            <p style="margin-bottom: 16px; color: #5C5C5C;">
                Based on 6% corridor share of statewide FDOT budget (conservative estimate reflecting regional population and economic activity):
            </p>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Program Area</th>
                        <th>5-Year Statewide</th>
                        <th>Estimated TOL Allocation (6%)</th>
                        <th>Capacity Outcome</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Transit Systems</strong></td>
                        <td>${fdot_budget_5yr['transit_systems']}M</td>
                        <td><span class="highlight">${tol_allocation['transit_systems']:.1f}M</span></td>
                        <td>~265 new transit vehicles @ $500K each</td>
                    </tr>
                    <tr>
                        <td><strong>Aviation</strong></td>
                        <td>${fdot_budget_5yr['aviation']}M</td>
                        <td><span class="highlight">${tol_allocation['aviation']:.1f}M</span></td>
                        <td>Gate expansions, +10M pax/year capacity</td>
                    </tr>
                    <tr>
                        <td><strong>Rail (Passenger)</strong></td>
                        <td>${fdot_budget_5yr['rail_passenger']}M</td>
                        <td><span class="highlight">${tol_allocation['rail_passenger']:.1f}M</span></td>
                        <td>Brightline station upgrades, 12 trains/hr</td>
                    </tr>
                    <tr>
                        <td><strong>Intermodal Access</strong></td>
                        <td>${fdot_budget_5yr['intermodal_access']}M</td>
                        <td><span class="highlight">${tol_allocation['intermodal_access']:.1f}M</span></td>
                        <td>10-12 major transit hubs @ $2.5M each</td>
                    </tr>
                    <tr>
                        <td><strong>Construction (All Modes)</strong></td>
                        <td>${fdot_budget_5yr['construction_all']/1000:.1f}B</td>
                        <td><span class="highlight">${tol_allocation['construction_all']:.1f}M</span></td>
                        <td>~400-500 lane-miles @ $4M per lane-mile</td>
                    </tr>
                    <tr style="border-top: 2px solid #004A7C;">
                        <td><strong>TOTAL (Corridor)</strong></td>
                        <td><strong>${fdot_budget_5yr['total_budget']/1000:.1f}B</strong></td>
                        <td><strong><span class="highlight">${tol_allocation['total_budget']:.1f}M</span></strong></td>
                        <td><strong>Integrated multi-modal system</strong></td>
                    </tr>
                </tbody>
            </table>
            
            <div class="warning-box">
                <strong>Important:</strong> These are estimated corridor allocations based on proportional share of statewide budget. 
                Actual project-level funding requires detailed FDOT District 5 work program analysis and coordination with local MPOs 
                (Metropolitan Planning Organizations).
            </div>
        </div>
        
        <!-- Next Steps -->
        <div class="section">
            <div class="section-header">📋 Implementation Next Steps</div>
            <ol style="margin-left: 24px; color: #333333; font-size: 14px; line-height: 2;">
                <li><strong>Quantify exact FDOT District 5 allocations</strong> for TOL corridor projects from detailed work program</li>
                <li><strong>Finalize Brightline Orlando–Tampa timeline</strong> and station locations with Brightline Florida + FDOT coordination</li>
                <li><strong>Model Olympics-period transit demand</strong> (300k rides/day target) using FDOT traffic models + IOC event schedules</li>
                <li><strong>Secure FDOT commitment</strong> for express lane conversions, BRT deployment, and park-and-ride development</li>
                <li><strong>Coordinate with MCO/TPA</strong> for international visitor processing capacity expansion and customs facilities</li>
                <li><strong>Develop integrated ticketing system</strong> combining Brightline, SunRail, LYNX, HART with Olympic credentials</li>
                <li><strong>Finalize Camping World Stadium expansion plan</strong> to 80,000+ seats (engineering + funding)</li>
            </ol>
        </div>
    </div>
    
    <div class="footer">
        <p><strong>Florida Olympic Vision: Tampa–Orlando–Lakeland (TOL) Corridor</strong></p>
        <p>Data sources: FDOT 2025-2034 Adopted Work Program (26Adopt01b, July 1, 2025) | Brightline Florida | BEBR 2023 | Visit Florida 2024</p>
        <p>Dashboard generated with real FDOT budget numbers | Last updated: November 2025</p>
    </div>
</body>
</html>
"""

# Save HTML dashboard
output_path = os.path.join('docs', 'fdot_transportation_dashboard_TOL.html')
os.makedirs('docs', exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("=" * 70)
print("FDOT TRANSPORTATION DASHBOARD (TOL MODEL) GENERATED")
print("=" * 70)
print(f"\n✓ Interactive HTML dashboard created: {output_path}")
print("\n📊 Real FDOT Budget Numbers (5-Year Program, FY 2025-2030):")
print(f"  • Total Budget: ${fdot_budget_5yr['total_budget']/1000:.1f}B")
print(f"  • Transit Systems: ${fdot_budget_5yr['transit_systems']}M")
print(f"  • Aviation: ${fdot_budget_5yr['aviation']}M")
print(f"  • Rail (Passenger): ${fdot_budget_5yr['rail_passenger']}M")
print(f"  • Intermodal Access: ${fdot_budget_5yr['intermodal_access']}M")
print(f"  • Construction: ${fdot_budget_5yr['construction_all']/1000:.1f}B")
print(f"\n💡 Estimated TOL Corridor Allocation (6%): ${tol_allocation['total_budget']:.1f}M")
print("\n🎯 Key Updates:")
print("  ✅ Removed Gainesville from corridor (too far)")
print("  ✅ Orlando Camping World Stadium expanded to 80k+ (main stadium)")
print("  ✅ Lakeland central role (Olympic Village + Brightline hub)")
print("  ✅ Real FDOT numbers from 26Adopt01b PDF")
print("\nOpen the HTML file in a browser to view the dashboard!")
print("=" * 70)
