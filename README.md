

<!-- Using an object tag -->
<object data="[elis_executive_dashboard_en.html](https://github.com/user-attachments/files/33281119/elis_executive_dashboard_en.html)
" type="text/htm<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elis Danmark A/S - Executive Customer Satisfaction Dashboard & Report</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        :root {
            --primary-color: #1e3d59;
            --secondary-color: #17b978;
            --warning-color: #ff6e40;
            --bg-color: #f5f7fa;
            --card-bg: #ffffff;
            --text-color: #333333;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
            color: var(--text-color);
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #1e3d59 0%, #17b978 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .header h1 { margin: 0; font-size: 28px; }
        .header p { margin-top: 8px; font-size: 15px; opacity: 0.9; }

        /* KPI Cards */
        .kpi-container {
            display: flex;
            justify-content: space-between;
            gap: 15px;
            margin-bottom: 25px;
        }
        .kpi-card {
            flex: 1;
            background: var(--card-bg);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            text-align: center;
            border-top: 4px solid var(--primary-color);
        }
        .kpi-card h3 { margin: 0; font-size: 13px; color: #666; text-transform: uppercase; }
        .kpi-card .value { font-size: 28px; font-weight: bold; margin: 10px 0 5px 0; color: var(--primary-color); }
        .kpi-card .subtext { font-size: 12px; color: #888; }

        /* Chart Grid */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }
        .grid-full {
            margin-bottom: 25px;
        }
        .chart-card {
            background: var(--card-bg);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }

        /* Table & Segment Details */
        .section-card {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 25px;
        }
        .filter-banner {
            background-color: #e3f2fd;
            border-left: 5px solid #2196f3;
            padding: 12px 18px;
            margin-bottom: 15px;
            font-size: 14px;
            font-weight: 600;
            color: #0d47a1;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
            font-size: 13px;
            vertical-align: top;
        }
        th {
            background-color: #f8f9fa;
            color: var(--primary-color);
            font-weight: 600;
        }
        tr:hover { background-color: #f1f5f9; }
        .star-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            color: white;
            font-size: 11px;
            display: inline-block;
        }
        .star-1 { background-color: #e74c3c; }
        .star-2 { background-color: #e67e22; }
        .star-3 { background-color: #f1c40f; color: #333; }
        .star-4 { background-color: #2ecc71; }
        .star-5 { background-color: #27ae60; }

        /* Text Expand / Collapse */
        .review-text-container {
            max-width: 500px;
            line-height: 1.5;
        }
        .review-truncated {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .review-full {
            display: block;
            white-space: pre-wrap;
        }
        .toggle-btn {
            background: none;
            border: none;
            color: #2196f3;
            cursor: pointer;
            padding: 0;
            margin-top: 4px;
            font-size: 12px;
            font-weight: 600;
            text-decoration: underline;
        }

        /* Executive Report Section */
        .report-section {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-top: 6px solid var(--primary-color);
        }
        .report-section h2 {
            color: var(--primary-color);
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .report-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-top: 20px;
        }
        .report-box {
            background-color: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        .report-box h4 { margin-top: 0; color: var(--primary-color); font-size: 15px; }
        .report-box ul { padding-left: 20px; margin-bottom: 0; }
        .report-box li { margin-bottom: 8px; font-size: 13px; line-height: 1.5; }

        .btn-reset {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            float: right;
        }
        .btn-reset:hover { background-color: #132a3e; }
    </style>
</head>
<body>

    <!-- Header -->
    <div class="header">
        <h1>Elis Danmark A/S - Executive Customer Satisfaction Dashboard</h1>
        <p>Trustpilot Review Analytics, Categorized Operational Insights, & Strategic Management Report</p>
    </div>

    <!-- Executive KPI Cards -->
    <div class="kpi-container">
        <div class="kpi-card">
            <h3>Total Reviews Analyzed</h3>
            <div class="value">205</div>
            <div class="subtext">Net Unique Customer Reviews</div>
        </div>
        <div class="kpi-card">
            <h3>Average Rating Score</h3>
            <div class="value">2.87 / 5.0</div>
            <div class="subtext">Standard Deviation: 1.86</div>
        </div>
        <div class="kpi-card" style="border-top-color: #e74c3c;">
            <h3>Critical Dissatisfaction (1★)</h3>
            <div class="value" style="color: #e74c3c;">45.8%</div>
            <div class="subtext">94 Negative Reviews</div>
        </div>
        <div class="kpi-card" style="border-top-color: #27ae60;">
            <h3>High Satisfaction (5★)</h3>
            <div class="value" style="color: #27ae60;">38.0%</div>
            <div class="subtext">78 Positive Reviews</div>
        </div>
    </div>

    <!-- Interactive Charts Grid -->
    <div class="grid-2">
        <div class="chart-card">
            <div id="starDistChart"></div>
        </div>
        <div class="chart-card">
            <div id="categoryPieChart"></div>
        </div>
    </div>

    <div class="grid-full chart-card">
        <div id="trendChart"></div>
    </div>

    <!-- Interactive Segment Details Table -->
    <div class="section-card">
        <button class="btn-reset" onclick="resetFilter()">Reset Filters</button>
        <h3 style="margin-top:0; color: #1e3d59;">Segment-Specific Customer Reviews & Detailed Data Table</h3>
        <div id="filterBanner" class="filter-banner">
            Displaying all segments. Click on any bar, pie slice, or trend point in the charts above to filter table data.
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 15%;">Customer Name</th>
                    <th style="width: 15%;">Date & Time</th>
                    <th style="width: 10%;">Rating</th>
                    <th style="width: 20%;">Matched Category</th>
                    <th style="width: 40%;">Customer Review Text (Click to Expand)</th>
                </tr>
            </thead>
            <tbody id="tableBody"></tbody>
        </table>
    </div>

    <!-- Final Executive Comprehensive Report (In English) -->
    <div class="report-section">
        <h2>Executive Summary & Strategic Roadmap</h2>
        <p style="font-size: 14px; line-height: 1.6; color: #444;">
            A thorough data analysis of 205 net unique Trustpilot reviews for Elis Danmark A/S reveals a strongly bimodal customer sentiment distribution. While a solid portion of the customer base reports seamless operations, critical systemic bottlenecks in billing, contractual transparency, and response times drive severe dissatisfaction among negative reviewers.
        </p>

        <div class="report-grid">
            <div class="report-box">
                <h4>1. Descriptive Analysis & Polarization</h4>
                <ul>
                    <li><b>Bimodal Polarization:</b> Customer ratings are heavily clustered at the extremes: 45.8% for 1-Star and 38.0% for 5-Stars. Neutral feedback (3-Stars) accounts for only 5.4%, indicating that customer experience is either highly successful or severely disrupted.</li>
                    <li><b>High Star-Only Proportion:</b> Approximately 97.5% of reviews were submitted without written commentary. Establishing automated follow-up micro-surveys for star-only ratings will unlock deeper root-cause insights.</li>
                </ul>
            </div>

            <div class="report-box">
                <h4>2. Category-Level Operational Risks</h4>
                <ul>
                    <li><b>Finance & Billing:</b> Discrepancies in billing policies and lost item compensation terms generate significant friction. Forcing clients to purchase replacement items before issuing compensation represents a major pain point.</li>
                    <li><b>Pest Control:</b> Contractual limitations (e.g., 2-year subscriptions covering only 1 out of 40+ ant species) and slow response times for mole extermination requests create perceived gaps in service value.</li>
                    <li><b>Logistic & Transportation:</b> Delays in dispatch and delivery times directly trigger negative feedback and churn risk.</li>
                </ul>
            </div>

            <div class="report-box">
                <h4>3. Customer Retention & Recovery Success</h4>
                <ul>
                    <li><b>Proactive Outreach Impact:</b> Data confirms that prompt customer service interventions can successfully turn negative reviews into positive resolutions. Example: A customer edited their review to 4 stars after Elis reached out and waived an internal billing error.</li>
                    <li><b>Turnaround Opportunity:</b> Fast-track grievance handling actively prevents customer churn and restores brand trust.</li>
                </ul>
            </div>

            <div class="report-box">
                <h4>4. Strategic Recommendations</h4>
                <ul>
                    <li><b>Contractual Transparency:</b> Clearly communicate Pest Control subscription scopes, covered species, and billing terms during onboarding.</li>
                    <li><b>Revised Compensation Model:</b> Replace the mandatory upfront purchase requirement for lost textiles with direct credit adjustments or invoice offsets.</li>
                    <li><b>Real-Time Alert Webhooks:</b> Implement automated webhooks to route any new 1-star or 2-star Trustpilot review directly to the respective operational manager for immediate action within 24 hours.</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        const rawData = [{"Isim": "Richardt Nordberg", "Tarih_Saat": "02.02.2026 19:02", "Yildiz_Sayisi": 3.0, "Category_Str": "Pest Control, Logistic - Transportation, Finance - Billing, Customer Service", "Musteri_Yorumu": "Vi har betalt for 2 \u00e5rs abonnement p\u00e5 myre bek\u00e6mpelse af sort havemyre -men kun den een slags myre ud af 40-50 danske arter!\n\nVi har oplevet lange udrykningstider, efter opkald for bek\u00e6mpelse af...Se mereVirksomheden har svaret", "Yil_Ay": "2026-02"}, {"Isim": "Tim H\u00f8glund", "Tarih_Saat": "10.06.2026 09:47", "Yildiz_Sayisi": 3.0, "Category_Str": "Logistic - Transportation, Finance - Billing, Customer Service", "Musteri_Yorumu": "!!! STOP !!!\n\nV\u00e6r forsigtige med denne virksomhed. De opretter kundeforhold og aftaler i strid med g\u00e6ldende lovgivning.\n\n\n// 08-06-2026\nJeg blev telefonisk kontaktet af Elis, som dybt har beklage...Se mereVirksomheden har svaret", "Yil_Ay": "2026-06"}, {"Isim": "Ida Erikstad Pedersen", "Tarih_Saat": "17.03.2026 08:32", "Yildiz_Sayisi": 4.0, "Category_Str": "Pest Control, Finance - Billing, Customer Service", "Musteri_Yorumu": "*Redigeret* Elis tog kontakt og vi l\u00f8ste sagen p\u00e5 en god m\u00e5de, hvilket gjorde at jeg ikke skulle betale for deres interne fejl. *\n\nJeg bad om et tilbud p\u00e5 muldvarpebek\u00e6mpelse d. 30 januar, men h\u00f8rte...Se mereVirksomheden har svaret", "Yil_Ay": "2026-03"}, {"Isim": "Kent Holst", "Tarih_Saat": "27.03.2026 12:23", "Yildiz_Sayisi": 5.0, "Category_Str": "Customer Service", "Musteri_Yorumu": "Super s\u00f8de og hj\u00e6lpsomme.\nDe har sponsoreret h\u00e5ndkl\u00e6der til vores rideforening, s\u00e5 vi kan lave lidt kreative projekter med tekstiltryk og kan t\u00f8rre hestene omkring s\u00e5r(n\u00e5r det forekommer), \u00f8jne og n...Se mereVirksomheden har svaret", "Yil_Ay": "2026-03"}, {"Isim": "Jon Hreinsson", "Tarih_Saat": "24.09.2026 12:07", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-09"}, {"Isim": "Lene Jensen", "Tarih_Saat": "19.09.2026 11:38", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-09"}, {"Isim": "Rasmus Dahl", "Tarih_Saat": "17.09.2026 20:31", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-09"}, {"Isim": "Tobias Nielsen", "Tarih_Saat": "16.09.2026 08:08", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-09"}, {"Isim": "Anne Birch Christensen", "Tarih_Saat": "03.09.2026 07:44", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-09"}, {"Isim": "Sofie", "Tarih_Saat": "12.08.2026 17:19", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-08"}, {"Isim": "hui chen", "Tarih_Saat": "07.08.2026 12:31", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-08"}, {"Isim": "S\u00f8ren Bo Bojesen", "Tarih_Saat": "04.08.2026 19:55", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-08"}, {"Isim": "ML.", "Tarih_Saat": "04.08.2026 14:43", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-08"}, {"Isim": "Fabian Nielsen", "Tarih_Saat": "04.08.2026 12:31", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-08"}, {"Isim": "Caroline", "Tarih_Saat": "31.07.2026 14:54", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Betina K\u00f8ster", "Tarih_Saat": "29.07.2026 11:42", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Heino", "Tarih_Saat": "20.07.2026 08:56", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Jane", "Tarih_Saat": "17.07.2026 12:59", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "J\u00f8rgen", "Tarih_Saat": "15.07.2026 07:19", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Ann Wraae Bomholt", "Tarih_Saat": "11.07.2026 10:28", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Mette", "Tarih_Saat": "09.07.2026 15:35", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Kim Nih\u00f8j", "Tarih_Saat": "06.07.2026 10:11", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Gunvar Svak", "Tarih_Saat": "06.07.2026 09:27", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Annia Moesby", "Tarih_Saat": "03.07.2026 12:47", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Johnni s\u00f8rensen", "Tarih_Saat": "02.07.2026 10:24", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-07"}, {"Isim": "Charlotte B", "Tarih_Saat": "30.06.2026 22:50", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-06"}, {"Isim": "Marianne Berg-Sonne", "Tarih_Saat": "29.06.2026 17:57", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-06"}, {"Isim": "Maiken S\u00f8rensen", "Tarih_Saat": "12.06.2026 16:21", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-06"}, {"Isim": "Mikkel", "Tarih_Saat": "11.06.2026 08:58", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-06"}, {"Isim": "laura Rathschau Nielsen", "Tarih_Saat": "03.06.2026 22:20", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-06"}, {"Isim": "Tim H\u00f8glund", "Tarih_Saat": "10.06.2026 09:47", "Yildiz_Sayisi": 3.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-06"}, {"Isim": "Cecilia de Jong", "Tarih_Saat": "26.05.2026 11:06", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-05"}, {"Isim": "Lykke", "Tarih_Saat": "20.05.2026 09:07", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-05"}, {"Isim": "Isabel Donen", "Tarih_Saat": "18.05.2026 11:46", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-05"}, {"Isim": "Henry Hansen", "Tarih_Saat": "30.04.2026 10:21", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Jens Michelsen", "Tarih_Saat": "29.04.2026 08:45", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Bushra Hanif", "Tarih_Saat": "28.04.2026 18:28", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Heidi Bj\u00f8rn", "Tarih_Saat": "28.04.2026 17:39", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Ninna Brogaard", "Tarih_Saat": "24.04.2026 14:47", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Karl Damkj\u00e6r", "Tarih_Saat": "23.04.2026 14:46", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Jakob Therkildsen", "Tarih_Saat": "22.04.2026 12:34", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Carsten J\u00f8rgensen", "Tarih_Saat": "21.04.2026 11:45", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Rikke", "Tarih_Saat": "10.04.2026 10:45", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-04"}, {"Isim": "Kent Holst", "Tarih_Saat": "27.03.2026 12:23", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Kunde", "Tarih_Saat": "26.03.2026 13:45", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Murat", "Tarih_Saat": "19.03.2026 14:39", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Gitte", "Tarih_Saat": "18.03.2026 10:17", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Trine qvortrup Moltzen", "Tarih_Saat": "18.03.2026 01:04", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Ida Erikstad Pedersen", "Tarih_Saat": "17.03.2026 08:32", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Georg Kristensen", "Tarih_Saat": "10.03.2026 11:49", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Karsten Lauridsen", "Tarih_Saat": "06.03.2026 13:09", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-03"}, {"Isim": "Tove Kopp-S\u00f8rensen", "Tarih_Saat": "11.02.2026 21:37", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-02"}, {"Isim": "Carsten V. Petersen", "Tarih_Saat": "11.02.2026 16:33", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-02"}, {"Isim": "Dorthe Larsen", "Tarih_Saat": "09.02.2026 12:06", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-02"}, {"Isim": "Tove Beltran", "Tarih_Saat": "04.02.2026 22:28", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-02"}, {"Isim": "claus voss schrader", "Tarih_Saat": "04.02.2026 10:24", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-02"}, {"Isim": "Richardt Nordberg", "Tarih_Saat": "02.02.2026 19:02", "Yildiz_Sayisi": 3.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-02"}, {"Isim": "Lillian Sivertsen", "Tarih_Saat": "26.01.2026 11:47", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-01"}, {"Isim": "Lisbeth Spanggaard", "Tarih_Saat": "18.01.2026 23:36", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-01"}, {"Isim": "lars Normann", "Tarih_Saat": "08.01.2026 15:01", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-01"}, {"Isim": "Per Petersen", "Tarih_Saat": "08.01.2026 17:18", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2026-01"}, {"Isim": "jens jensen", "Tarih_Saat": "17.12.2025 19:13", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-12"}, {"Isim": "Jane Jensen", "Tarih_Saat": "16.12.2025 20:33", "Yildiz_Sayisi": 3.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-12"}, {"Isim": "lizzie pind", "Tarih_Saat": "09.12.2025 11:03", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-12"}, {"Isim": "Tom Elkj\u00e6r Bor\u00e9", "Tarih_Saat": "08.12.2025 13:30", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-12"}, {"Isim": "Bodil Pedersen", "Tarih_Saat": "19.12.2025 10:09", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-12"}, {"Isim": "Louise", "Tarih_Saat": "04.12.2025 18:33", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-12"}, {"Isim": "Lene Birke", "Tarih_Saat": "18.11.2025 15:54", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Dieter", "Tarih_Saat": "14.11.2025 12:31", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Peder Wiberg", "Tarih_Saat": "14.11.2025 10:15", "Yildiz_Sayisi": 3.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Monique", "Tarih_Saat": "10.11.2025 13:27", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Bdi", "Tarih_Saat": "09.11.2025 14:11", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Betina Samvirkende Menighedspl", "Tarih_Saat": "08.11.2025 12:55", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Maja", "Tarih_Saat": "07.11.2025 12:33", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Jeanette Uldall", "Tarih_Saat": "05.11.2025 15:21", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-11"}, {"Isim": "Wiebke Neymeyr", "Tarih_Saat": "31.10.2025 12:54", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Tina Kirkeb\u00e6kke", "Tarih_Saat": "28.10.2025 12:23", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Klaus Maitland", "Tarih_Saat": "21.10.2025 13:38", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Alexander", "Tarih_Saat": "15.10.2025 10:47", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Roman Stryga", "Tarih_Saat": "13.10.2025 10:20", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Ole", "Tarih_Saat": "11.10.2025 11:03", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Kenneth Andersen", "Tarih_Saat": "06.10.2025 19:35", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Leif Kejser Larsen", "Tarih_Saat": "05.10.2025 15:08", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "krumme lee", "Tarih_Saat": "04.10.2025 16:24", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Lasse Nielsen", "Tarih_Saat": "03.10.2025 19:20", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Bente Arildslund", "Tarih_Saat": "03.10.2025 13:18", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Kim Larsen", "Tarih_Saat": "01.10.2025 15:42", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-10"}, {"Isim": "Deirdre Ryan Christensen", "Tarih_Saat": "30.09.2025 12:56", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "DA film OLE L", "Tarih_Saat": "30.09.2025 10:37", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Tage Bering Christensen", "Tarih_Saat": "29.09.2025 00:06", "Yildiz_Sayisi": 3.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Malte.", "Tarih_Saat": "25.09.2025 09:22", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Amanda", "Tarih_Saat": "23.09.2025 14:13", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Anna Kj\u00e6r Voss", "Tarih_Saat": "22.09.2025 12:06", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Karin Kjeldsen", "Tarih_Saat": "19.09.2025 17:14", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Loize Hartmann Petersen", "Tarih_Saat": "16.09.2025 14:03", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Alexander Kruuse", "Tarih_Saat": "11.09.2025 17:59", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Helle Mogensen", "Tarih_Saat": "08.09.2025 13:08", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Inge U. Pedersen", "Tarih_Saat": "08.09.2025 11:43", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Ulla Henriksen", "Tarih_Saat": "07.09.2025 11:06", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Per Andersen", "Tarih_Saat": "02.09.2025 15:03", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Jens christian", "Tarih_Saat": "02.09.2025 11:16", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-09"}, {"Isim": "Nicolai", "Tarih_Saat": "28.08.2025 18:22", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Tina Vilykke", "Tarih_Saat": "28.08.2025 09:46", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Irmgardt seestedt seestedt", "Tarih_Saat": "26.08.2025 10:40", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Jens Erik \u201cDexermon\u201d Augustinu", "Tarih_Saat": "25.08.2025 12:47", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Grith Schucany", "Tarih_Saat": "23.08.2025 12:02", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Ulrik Th&#248;rner", "Tarih_Saat": "22.08.2025 13:40", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "JM", "Tarih_Saat": "20.08.2025 16:45", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Heidi Hansen", "Tarih_Saat": "14.08.2025 22:07", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Rikke", "Tarih_Saat": "13.08.2025 13:29", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "L\u00e9on Todran", "Tarih_Saat": "13.08.2025 10:49", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Ulla Lauritsen", "Tarih_Saat": "08.08.2025 16:53", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Lars Bo kragh - Hansen", "Tarih_Saat": "07.08.2025 17:52", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Vinni", "Tarih_Saat": "05.08.2025 15:37", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Evelynn Udengaard", "Tarih_Saat": "04.08.2025 13:15", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Klaus", "Tarih_Saat": "06.08.2025 15:53", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Jesper Thomsen", "Tarih_Saat": "01.08.2025 22:33", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-08"}, {"Isim": "Anne", "Tarih_Saat": "20.07.2025 11:26", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-07"}, {"Isim": "Tina Pauli", "Tarih_Saat": "18.07.2025 17:54", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-07"}, {"Isim": "Anette Jacobsen", "Tarih_Saat": "09.07.2025 12:04", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-07"}, {"Isim": "Gladsaxe Bibliotekerne", "Tarih_Saat": "04.07.2025 09:16", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-07"}, {"Isim": "Danny G", "Tarih_Saat": "01.07.2025 06:59", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-07"}, {"Isim": "Britta Stubkj\u00e6r", "Tarih_Saat": "18.06.2025 13:08", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-06"}, {"Isim": "Pia", "Tarih_Saat": "09.06.2025 10:34", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-06"}, {"Isim": "Kim Kok", "Tarih_Saat": "03.06.2025 09:55", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-06"}, {"Isim": "Leif Skrydstrup", "Tarih_Saat": "02.06.2025 11:50", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-06"}, {"Isim": "Jacob Vahl Olofson", "Tarih_Saat": "02.06.2025 12:53", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-06"}, {"Isim": "Kunde", "Tarih_Saat": "16.05.2025 20:38", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-05"}, {"Isim": "trine padmo", "Tarih_Saat": "14.05.2025 07:50", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-05"}, {"Isim": "Nomi S", "Tarih_Saat": "06.05.2025 18:54", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-05"}, {"Isim": "Emma", "Tarih_Saat": "05.05.2025 09:31", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-05"}, {"Isim": "Solbjorg Maria Gunnarsdottir", "Tarih_Saat": "29.04.2025 14:01", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-04"}, {"Isim": "Carsten", "Tarih_Saat": "23.04.2025 17:30", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-04"}, {"Isim": "Henrik Nielsen", "Tarih_Saat": "18.04.2025 12:39", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-04"}, {"Isim": "Kathrine De Place Bj\u00f8rn", "Tarih_Saat": "18.04.2025 10:58", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-04"}, {"Isim": "Ilse Irgend Trudslev", "Tarih_Saat": "16.04.2025 13:57", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-04"}, {"Isim": "Charlotte Buch", "Tarih_Saat": "02.04.2025 18:08", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-04"}, {"Isim": "Anne", "Tarih_Saat": "27.03.2025 14:24", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-03"}, {"Isim": "Nanna Gertz", "Tarih_Saat": "25.03.2025 15:10", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-03"}, {"Isim": "Rikke Lykstoft", "Tarih_Saat": "23.03.2025 17:37", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-03"}, {"Isim": "Anders", "Tarih_Saat": "12.03.2025 13:52", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-03"}, {"Isim": "Jesper Nyboe Nielsen", "Tarih_Saat": "27.03.2025 12:34", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-03"}, {"Isim": "Berit Rasmussen", "Tarih_Saat": "06.03.2025 14:59", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-03"}, {"Isim": "Tina", "Tarih_Saat": "24.02.2025 13:51", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-02"}, {"Isim": "Tobias", "Tarih_Saat": "12.02.2025 11:59", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-02"}, {"Isim": "S\u00f8ren", "Tarih_Saat": "12.02.2025 11:55", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-02"}, {"Isim": "pia larsen", "Tarih_Saat": "18.01.2025 11:50", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "NIKITA KLEE", "Tarih_Saat": "15.01.2025 15:37", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "Maren Asmussen", "Tarih_Saat": "14.01.2025 13:53", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "Claus Feldstedt", "Tarih_Saat": "13.01.2025 13:57", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "Dennisleonpetersengmail.com Pe", "Tarih_Saat": "06.01.2025 11:58", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "Carsten", "Tarih_Saat": "03.01.2025 12:48", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "Lui", "Tarih_Saat": "03.01.2025 11:02", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "Mathias Franderup eltoft", "Tarih_Saat": "27.12.2024 06:52", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-12"}, {"Isim": "Kira", "Tarih_Saat": "03.01.2025 14:10", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2025-01"}, {"Isim": "Stinne Bjorholm", "Tarih_Saat": "17.12.2024 16:56", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-12"}, {"Isim": "anni brander", "Tarih_Saat": "15.12.2024 14:24", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-12"}, {"Isim": "Anita", "Tarih_Saat": "10.12.2024 06:35", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-12"}, {"Isim": "Susanne Guldb\u00e6k", "Tarih_Saat": "04.12.2024 10:38", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-12"}, {"Isim": "Sarah", "Tarih_Saat": "29.11.2024 17:41", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Charlotte  Buch", "Tarih_Saat": "29.11.2024 08:30", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Karen", "Tarih_Saat": "28.11.2024 20:21", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Bente", "Tarih_Saat": "15.11.2024 12:22", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Lene", "Tarih_Saat": "11.11.2024 12:11", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Ulla", "Tarih_Saat": "07.11.2024 11:09", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Inge Henriksen", "Tarih_Saat": "06.11.2024 16:20", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Dan Kristiansen", "Tarih_Saat": "06.11.2024 14:45", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Mette Steen Larsen", "Tarih_Saat": "04.11.2024 10:26", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "MG", "Tarih_Saat": "01.11.2024 10:05", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-11"}, {"Isim": "Jane", "Tarih_Saat": "14.10.2024 13:05", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-10"}, {"Isim": "ASSENTOFT ANNETTE", "Tarih_Saat": "14.10.2024 12:45", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-10"}, {"Isim": "Tina Fomsgaard", "Tarih_Saat": "24.09.2024 08:01", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-09"}, {"Isim": "Charlotte  Fosvald", "Tarih_Saat": "16.09.2024 16:51", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-09"}, {"Isim": "Jennie", "Tarih_Saat": "06.09.2024 06:47", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-09"}, {"Isim": "Olcay", "Tarih_Saat": "05.09.2024 11:46", "Yildiz_Sayisi": 3.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-09"}, {"Isim": "Annika Vind", "Tarih_Saat": "05.09.2024 11:43", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-09"}, {"Isim": "Annette Melin", "Tarih_Saat": "27.08.2024 11:35", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-08"}, {"Isim": "Helene Lyngby Nielsen", "Tarih_Saat": "19.08.2024 09:19", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-08"}, {"Isim": "Lisa Pagan", "Tarih_Saat": "15.08.2024 17:13", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-08"}, {"Isim": "Fr. Anja Madsen", "Tarih_Saat": "15.08.2024 15:33", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-08"}, {"Isim": "Brian Nielsen", "Tarih_Saat": "29.07.2024 11:00", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-07"}, {"Isim": "Johan Glintborg", "Tarih_Saat": "29.07.2024 07:26", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-07"}, {"Isim": "Lasse Henningsen", "Tarih_Saat": "24.07.2024 12:14", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-07"}, {"Isim": "Carsten Allerslev", "Tarih_Saat": "15.07.2024 13:47", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-07"}, {"Isim": "Brian", "Tarih_Saat": "25.06.2024 14:54", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-06"}, {"Isim": "jan andersen", "Tarih_Saat": "20.06.2024 11:56", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-06"}, {"Isim": "TSIJ", "Tarih_Saat": "10.06.2024 08:53", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-06"}, {"Isim": "Michael Paulsen", "Tarih_Saat": "04.06.2024 11:06", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-06"}, {"Isim": "S. Al", "Tarih_Saat": "23.05.2024 13:51", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-05"}, {"Isim": "Birgitte", "Tarih_Saat": "29.05.2024 13:25", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-05"}, {"Isim": "Trine", "Tarih_Saat": "23.05.2024 09:40", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-05"}, {"Isim": "Nick", "Tarih_Saat": "14.05.2024 08:05", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-05"}, {"Isim": "Elin Christensen", "Tarih_Saat": "07.05.2024 11:37", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-05"}, {"Isim": "Rie", "Tarih_Saat": "30.04.2024 18:12", "Yildiz_Sayisi": 2.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-04"}, {"Isim": "Anders", "Tarih_Saat": "29.04.2024 15:16", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-04"}, {"Isim": "Anni", "Tarih_Saat": "04.04.2024 12:01", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-04"}, {"Isim": "Jens Tang", "Tarih_Saat": "18.03.2024 16:57", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "Harriet", "Tarih_Saat": "14.03.2024 15:20", "Yildiz_Sayisi": 4.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "henrik hjorth", "Tarih_Saat": "14.03.2024 14:59", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "Julie", "Tarih_Saat": "14.03.2024 14:02", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "Bettina", "Tarih_Saat": "13.03.2024 14:26", "Yildiz_Sayisi": 5.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "Helge Blak Pedersen", "Tarih_Saat": "15.03.2024 10:32", "Yildiz_Sayisi": 3.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "Tina", "Tarih_Saat": "11.03.2024 11:31", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "Annemette", "Tarih_Saat": "08.03.2024 15:39", "Yildiz_Sayisi": 1.0, "Category_Str": "General", "Musteri_Yorumu": "Star Rating Only (No text review provided)", "Yil_Ay": "2024-03"}, {"Isim": "ORTALAMA / DE\u011eERLEND\u0130RME", "Tarih_Saat": "-", "Yildiz_Sayisi": 3.01, "Category_Str": "General", "Musteri_Yorumu": "Toplam 240 adet yorum incelendi.", "Yil_Ay": "NaT"}];

        function renderTable(data, bannerText) {
            document.getElementById('filterBanner').innerText = bannerText;
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            if(data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No records found for the selected filter.</td></tr>';
                return;
            }

            data.forEach((row, idx) => {
                const tr = document.createElement('tr');
                const starInt = Math.floor(row.Yildiz_Sayisi);
                const isShort = row.Musteri_Yorumu.length <= 120;

                let textHtml = '';
                if(isShort) {
                    textHtml = `<div class="review-text-container">${row.Musteri_Yorumu}</div>`;
                } else {
                    textHtml = `
                        <div class="review-text-container">
                            <div id="text-truncated-${idx}" class="review-truncated">${row.Musteri_Yorumu}</div>
                            <div id="text-full-${idx}" class="review-full" style="display:none;">${row.Musteri_Yorumu}</div>
                            <button id="btn-toggle-${idx}" class="toggle-btn" onclick="toggleReviewText(${idx})">Show More</button>
                        </div>
                    `;
                }

                tr.innerHTML = `
                    <td><b>${row.Isim}</b></td>
                    <td>${row.Tarih_Saat}</td>
                    <td><span class="star-badge star-${starInt}">${row.Yildiz_Sayisi} ★</span></td>
                    <td><b>${row.Category_Str}</b></td>
                    <td>${textHtml}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function toggleReviewText(idx) {
            const truncated = document.getElementById(`text-truncated-${idx}`);
            const full = document.getElementById(`text-full-${idx}`);
            const btn = document.getElementById(`btn-toggle-${idx}`);

            if (full.style.display === "none") {
                full.style.display = "block";
                truncated.style.display = "none";
                btn.innerText = "Show Less";
            } else {
                full.style.display = "none";
                truncated.style.display = "-webkit-box";
                btn.innerText = "Show More";
            }
        }

        function resetFilter() {
            renderTable(rawData, "Displaying all segments. Click on any bar, pie slice, or trend point in the charts above to filter table data.");
        }

        renderTable(rawData, "Displaying all segments. Click on any bar, pie slice, or trend point in the charts above to filter table data.");

        // Star Bar Chart
        const starCounts = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 };
        rawData.forEach(d => {
            const s = Math.round(d.Yildiz_Sayisi).toString();
            if(starCounts[s] !== undefined) starCounts[s]++;
        });

        Plotly.newPlot('starDistChart', [{
            x: Object.keys(starCounts).map(k => k + ' Star'),
            y: Object.values(starCounts),
            type: 'bar',
            text: Object.values(starCounts),
            textposition: 'auto',
            marker: { color: ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#27ae60'] }
        }], {
            title: '<b>Star Rating Distribution (Click to Filter)</b>',
            xaxis: { title: 'Star Rating' },
            yaxis: { title: 'Number of Reviews' },
            margin: { t: 40, b: 40, l: 40, r: 20 }
        });

        document.getElementById('starDistChart').on('plotly_click', function(data){
            const selectedStar = parseInt(data.points[0].x);
            const filtered = rawData.filter(d => Math.round(d.Yildiz_Sayisi) === selectedStar);
            renderTable(filtered, `Filter Active: ${selectedStar} Star Ratings (${filtered.length} records)`);
        });

        // Category Pie Chart
        const catCounts = {};
        rawData.forEach(d => {
            const cats = d.Category_Str.split(', ');
            cats.forEach(c => {
                catCounts[c] = (catCounts[c] || 0) + 1;
            });
        });

        Plotly.newPlot('categoryPieChart', [{
            labels: Object.keys(catCounts),
            values: Object.values(catCounts),
            type: 'pie',
            hole: 0.4,
            marker: { colors: ['#3498db', '#e74c3c', '#9b59b6', '#1abc9c', '#f39c12', '#95a5a6'] }
        }], {
            title: '<b>Category Breakdown (Includes "General", Click to Filter)</b>',
            margin: { t: 40, b: 20, l: 20, r: 20 }
        });

        document.getElementById('categoryPieChart').on('plotly_click', function(data){
            const selectedCat = data.points[0].label;
            const filtered = rawData.filter(d => d.Category_Str.includes(selectedCat));
            renderTable(filtered, `Filter Active: '${selectedCat}' Category (${filtered.length} records)`);
        });

        // Monthly Trend Chart
        const monthlyStats = {};
        rawData.forEach(d => {
            const m = d.Yil_Ay;
            if(m && m !== 'NaT') {
                if(!monthlyStats[m]) monthlyStats[m] = { count: 0, sum: 0 };
                monthlyStats[m].count++;
                monthlyStats[m].sum += d.Yildiz_Sayisi;
            }
        });

        const months = Object.keys(monthlyStats).sort();
        const avgRatings = months.map(m => (monthlyStats[m].sum / monthlyStats[m].count).toFixed(2));
        const volumes = months.map(m => monthlyStats[m].count);

        Plotly.newPlot('trendChart', [
            { x: months, y: volumes, name: 'Review Volume', type: 'bar', marker: { color: '#cbd5e1' } },
            { x: months, y: avgRatings, name: 'Average Rating Score', type: 'scatter', mode: 'lines+markers', yaxis: 'y2', line: { color: '#1e3d59', width: 3 } }
        ], {
            title: '<b>Monthly Rating Score Trend & Review Volume</b>',
            xaxis: { title: 'Period (Year-Month)' },
            yaxis: { title: 'Review Count' },
            yaxis2: { title: 'Average Score', overlaying: 'y', side: 'right', range: [1, 5] },
            legend: { orientation: 'h', y: -0.2 },
            margin: { t: 40, b: 50, l: 40, r: 40 }
        });

        document.getElementById('trendChart').on('plotly_click', function(data){
            const selectedMonth = data.points[0].x;
            const filtered = rawData.filter(d => d.Yil_Ay === selectedMonth);
            renderTable(filtered, `Filter Active: Period ${selectedMonth} (${filtered.length} records)`);
        });
    </script>
</body>
</html>
l" style="width:100%; height:500px;"></object>

<!-- Alternatively, using an iframe -->
<iframe src="readme.html" style="width:100%; height:500px; border:none;"></iframe>

<img width="600" height="616" alt="Screenshot 2026-10-04 at 20 36 48" src="https://github.com/user-attachments/assets/abdf2030-4f48-4b71-8017-f3e3b5471f5d" />
" />

```js
python pipeline.py
```

```js
streamlit run dashboard.py
```



## $${\color{lightgreen}Resit\space Kadir}$$
## $${\color{green}22-09-2026\space }$$

