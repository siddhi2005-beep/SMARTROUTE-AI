from json import load
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Smart Supply Chain AI",
    page_icon="🚚",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #0f172a;
            --muted: #64748b;
            --line: #e2e8f0;
            --blue: #2563eb;
            --blue-soft: #eff6ff;
            --purple: #7c3aed;
            --purple-soft: #f5f3ff;
            --green: #16a34a;
            --green-soft: #f0fdf4;
            --amber: #d97706;
            --amber-soft: #fff7ed;
            --red: #dc2626;
            --red-soft: #fef2f2;
            --shadow: 0 10px 35px rgba(15, 23, 42, 0.08);
            --shadow-hover: 0 18px 40px rgba(37, 99, 235, 0.12);
            --radius: 16px;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .block-container {
            max-width: 1320px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            border-right: 1px solid rgba(226, 232, 240, 0.95);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.35rem;
        }

        .hero {
            margin-bottom: 1.5rem;
        }

        .hero-title {
            font-size: 2.65rem;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0;
        }

        .hero-subtitle {
            color: var(--muted);
            font-size: 1.05rem;
            margin-top: 0.55rem;
        }

        .card {
            background: var(--card);
            border: 1px solid rgba(226, 232, 240, 0.9);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 1.35rem;
            margin-bottom: 1rem;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
            border-color: rgba(191, 219, 254, 0.95);
        }

        .highlight-card {
            background: linear-gradient(135deg, rgba(239, 246, 255, 1) 0%, rgba(245, 243, 255, 1) 100%);
            border: 1px solid #c7d2fe;
            border-left: 5px solid var(--blue);
        }

        .map-shell {
            overflow: hidden;
            border-radius: var(--radius);
            border: 1px solid rgba(226, 232, 240, 0.9);
            box-shadow: var(--shadow);
            margin-bottom: 1.15rem;
            background: #ffffff;
        }

        .map-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.2rem 0;
        }

        .section-title {
            font-size: 1.06rem;
            font-weight: 700;
            margin-bottom: 0.95rem;
            letter-spacing: -0.01em;
        }

        .section-kicker {
            color: var(--muted);
            font-size: 0.9rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.88rem;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .metric-subtext {
            color: var(--muted);
            font-size: 0.88rem;
            margin-top: 0.35rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 700;
            border: 1px solid transparent;
            white-space: nowrap;
        }

        .badge-blue {
            color: #1d4ed8;
            background: var(--blue-soft);
            border-color: #bfdbfe;
        }

        .badge-purple {
            color: #6d28d9;
            background: var(--purple-soft);
            border-color: #ddd6fe;
        }

        .badge-green {
            color: #166534;
            background: var(--green-soft);
            border-color: #bbf7d0;
        }

        .badge-amber {
            color: #9a3412;
            background: var(--amber-soft);
            border-color: #fed7aa;
        }

        .badge-red {
            color: #991b1b;
            background: var(--red-soft);
            border-color: #fecaca;
        }

        .info-list {
            margin: 0;
            padding-left: 1.15rem;
        }

        .info-list li {
            margin-bottom: 0.55rem;
            line-height: 1.55;
            color: var(--text);
        }

        .tile {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: 0.85rem;
            transition: transform 0.22s ease, box-shadow 0.22s ease;
        }

        .tile:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }

        .tile-label {
            color: var(--muted);
            font-size: 0.86rem;
            margin-bottom: 0.35rem;
        }

        .tile-value {
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .tile-subtext {
            color: var(--muted);
            font-size: 0.85rem;
            margin-top: 0.32rem;
        }

        .recommendation-title {
            font-size: 1.18rem;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }

        .recommendation-copy {
            color: var(--muted);
            line-height: 1.6;
            margin-bottom: 0.95rem;
        }

        .footer {
            text-align: center;
            color: var(--muted);
            font-size: 0.9rem;
            padding: 0.9rem 0 0.2rem;
        }

        .stButton > button {
            width: 100%;
            border: 0;
            border-radius: 12px;
            padding: 0.78rem 1rem;
            font-weight: 700;
            color: #ffffff;
            background: linear-gradient(135deg, var(--blue) 0%, var(--purple) 100%);
            box-shadow: 0 14px 28px rgba(99, 102, 241, 0.24);
            transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 30px rgba(99, 102, 241, 0.28);
            filter: brightness(1.02);
        }

        .stButton > button:disabled {
            background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
            box-shadow: none;
            cursor: not-allowed;
        }

        .stTextInput input,
        .stSelectbox div[data-baseweb="select"] input,
        .stTextArea textarea {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        .stTextInput > div > div > input,
        div[data-baseweb="select"] > div,
        .stSelectbox > div > div {
            background: #ffffff !important;
            border-radius: 12px !important;
            border-color: #dbe4f0 !important;
        }

        div[data-baseweb="select"] span {
            color: #0f172a !important;
        }

        .stAlert {
            border-radius: 12px;
        }

        hr {
            border: 0;
            border-top: 1px solid var(--line);
            margin: 1.1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

STATE_DEFAULTS = {
    "risk_score": None,
    "delay_hours": 0.0,
    "selected_reasons": [],
    "simulation_name": None,
    "decision": None,
    "manual_override": False,
    "distance_km": None,
    "duration_minutes": None,
    "better_route_savings_factor": None,
    "origin_coords": None,
    "destination_coords": None,
    "route_points": [],
    "route_condition": None,
    "optimized_route": None,
    "origin_name": "",
    "destination_name": "",
    "cargo_type": "Medicine",
    "traffic_level": "Low",
    "weather_condition": "Clear",
    "mode_label": "🚚 Standard Delivery",
    "insights": [],
    "recommendation_body": "",
}

MODE_OPTIONS = ["🚚 Standard Delivery", "⚡ High Priority", "🌱 Eco Mode"]
MODE_META = {
    "🚚 Standard Delivery": {
        "short": "Standard",
        "badge": "badge-blue",
        "reason": "Balances delivery speed and operating cost for dependable execution.",
    },
    "⚡ High Priority": {
        "short": "High Priority",
        "badge": "badge-purple",
        "reason": "Favors the fastest feasible route to protect service level commitments.",
    },
    "🌱 Eco Mode": {
        "short": "Eco",
        "badge": "badge-green",
        "reason": "Optimizes for lower emissions while allowing a modest increase in travel time.",
    },
}

for key, value in STATE_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def render_card_header(title, subtitle=None):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-kicker'>{subtitle}</div>", unsafe_allow_html=True)


def badge_markup(text, badge_class):
    return f"<span class='badge {badge_class}'>{text}</span>"


def metric_tile(label, value, subtext):
    st.markdown(
        f"""
        <div class="tile">
            <div class="tile-label">{label}</div>
            <div class="tile-value">{value}</div>
            <div class="tile-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def fetch_json(url, params=None):
    request_url = url
    if params:
        request_url = f"{url}?{urlencode(params)}"
    request = Request(request_url, headers={"User-Agent": "SmartRouteAI/1.0"})
    with urlopen(request, timeout=10) as response:
        return load(response)


def get_coordinates(city_name):
    data = fetch_json(
        "https://nominatim.openstreetmap.org/search",
        {"q": city_name, "format": "json", "limit": 1},
    )
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])


def get_route_details(origin_coords, destination_coords):
    origin_lat, origin_lon = origin_coords
    destination_lat, destination_lon = destination_coords
    route_url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{origin_lon},{origin_lat};{destination_lon},{destination_lat}"
    )
    data = fetch_json(route_url, {"overview": "full", "geometries": "geojson"})
    routes = data.get("routes", [])
    if not routes:
        return None
    route = routes[0]
    route_points = [[point[1], point[0]] for point in route["geometry"]["coordinates"]]
    return route["distance"] / 1000, route["duration"] / 60, route_points


def build_default_map():
    route_map = folium.Map(
        location=[22.5937, 78.9629],
        zoom_start=5,
        tiles="CartoDB positron",
    )
    folium.CircleMarker(
        [22.5937, 78.9629],
        radius=8,
        color="#7c3aed",
        fill=True,
        fill_color="#7c3aed",
        fill_opacity=0.9,
        tooltip="India logistics network",
    ).add_to(route_map)
    return route_map


def build_route_map(origin_coords, destination_coords, route_points):
    map_center = [
        (origin_coords[0] + destination_coords[0]) / 2,
        (origin_coords[1] + destination_coords[1]) / 2,
    ]
    route_map = folium.Map(location=map_center, zoom_start=6, tiles="CartoDB positron")
    folium.Marker(
        origin_coords,
        tooltip="Origin",
        popup="Origin",
        icon=folium.Icon(color="green", icon="play"),
    ).add_to(route_map)
    folium.Marker(
        destination_coords,
        tooltip="Destination",
        popup="Destination",
        icon=folium.Icon(color="red", icon="flag"),
    ).add_to(route_map)
    folium.PolyLine(route_points, color="#2563eb", weight=6, opacity=0.9).add_to(route_map)
    return route_map


def traffic_badge(level):
    return {
        "Low": "badge-green",
        "Medium": "badge-amber",
        "High": "badge-red",
    }[level]


def weather_badge(condition):
    return {
        "Clear": "badge-green",
        "Cloudy": "badge-amber",
        "Rain": "badge-red",
    }[condition]


def stable_seed(*values):
    return sum(sum(ord(ch) for ch in str(value)) for value in values)


def get_status(score):
    if score >= 75:
        return "High Risk", "badge-red"
    if score >= 45:
        return "Moderate Risk", "badge-amber"
    return "Low Risk", "badge-green"


def compute_operational_profile(distance_km, duration_minutes, cargo_type, mode_label, origin, destination):
    seed = stable_seed(origin.lower(), destination.lower(), cargo_type, mode_label)

    traffic_options = ["Low", "Medium", "High"]
    weather_options = ["Clear", "Cloudy", "Rain"]
    traffic_level = traffic_options[seed % len(traffic_options)]
    weather_condition = weather_options[(seed // 3) % len(weather_options)]

    traffic_delay = {"Low": 0.3, "Medium": 1.0, "High": 2.2}[traffic_level]
    weather_delay = {"Clear": 0.0, "Cloudy": 0.4, "Rain": 1.3}[weather_condition]
    cargo_delay = {"Medicine": 0.4, "Food": 0.3, "Electronics": 0.5}[cargo_type]
    mode_delay_adjustment = {
        "🚚 Standard Delivery": 0.0,
        "⚡ High Priority": -0.35,
        "🌱 Eco Mode": 0.45,
    }[mode_label]

    delay_hours = max(0.2, round(traffic_delay + weather_delay + cargo_delay + mode_delay_adjustment, 1))
    risk_score = int(
        min(
            92,
            max(
                28,
                22 + (distance_km / 24) + {"Low": 6, "Medium": 14, "High": 24}[traffic_level]
                + {"Clear": 4, "Cloudy": 9, "Rain": 16}[weather_condition]
                + {"Medicine": 12, "Food": 8, "Electronics": 10}[cargo_type],
            ),
        )
    )

    reasons = []
    reasons.append(f"{traffic_level} corridor traffic influencing route consistency")
    reasons.append(f"{weather_condition} weather profile impacting ETA reliability")
    if cargo_type == "Medicine":
        reasons.append("Temperature-sensitive handling requires tighter delivery windows")
    elif cargo_type == "Food":
        reasons.append("Perishable cargo prioritizes steady transit and minimal idling")
    else:
        reasons.append("High-value electronics shipment benefits from stable, lower-risk lanes")

    return {
        "traffic_level": traffic_level,
        "weather_condition": weather_condition,
        "delay_hours": delay_hours,
        "risk_score": risk_score,
        "selected_reasons": reasons,
        "distance_km": distance_km,
        "duration_minutes": duration_minutes,
    }


def get_recommendation(mode_label, profile):
    traffic_level = profile["traffic_level"]
    weather_condition = profile["weather_condition"]
    delay_hours = profile["delay_hours"]

    if mode_label == "⚡ High Priority":
        title = "Fastest express corridor recommended"
        body = (
            f"Prioritize the quickest lane and accept higher operating cost to keep the ETA protected. "
            f"Current {traffic_level.lower()} traffic and {weather_condition.lower()} conditions still support an accelerated dispatch window."
        )
        insights = [
            "This route reduces elapsed transit time ahead of cost efficiency.",
            f"Estimated delay exposure is contained to about {delay_hours:.1f} hours under present conditions.",
            "Priority handling avoids slower corridor congestion and protects urgent fulfillment commitments.",
        ]
    elif mode_label == "🌱 Eco Mode":
        title = "Low-emission route recommended"
        body = (
            "Shift toward the more efficient corridor with smoother traffic flow and lower idle time. "
            "A modest increase in travel time is acceptable to reduce carbon output."
        )
        insights = [
            "The selected route lowers emissions by avoiding stop-start segments.",
            f"The tradeoff is a manageable delay buffer of roughly {delay_hours:.1f} hours.",
            "This is the best fit when sustainability targets matter more than pure delivery speed.",
        ]
    else:
        title = "Balanced route recommended"
        body = (
            "Use the most stable route that balances transit speed, cost control, and service reliability. "
            "This profile fits standard delivery commitments without over-optimizing one dimension."
        )
        insights = [
            "The route balances ETA stability with transport cost efficiency.",
            f"Projected delay remains within a controllable range of about {delay_hours:.1f} hours.",
            "This option avoids unnecessary premium routing while maintaining dependable performance.",
        ]

    return title, body, insights


def optimize_route(mode_label, distance_km, duration_minutes, delay_hours):
    if mode_label == "⚡ High Priority":
        distance_factor = 0.94
        time_factor = 0.82
        cost_change = 380
        co2_factor = 0.04
    elif mode_label == "🌱 Eco Mode":
        distance_factor = 0.90
        time_factor = 0.95
        cost_change = -140
        co2_factor = 0.16
    else:
        distance_factor = 0.93
        time_factor = 0.88
        cost_change = -75
        co2_factor = 0.09

    optimized_distance = round(distance_km * distance_factor, 1)
    optimized_time_hours = round((duration_minutes / 60) * time_factor, 1)
    time_saved = round((duration_minutes / 60) - optimized_time_hours + max(0, delay_hours * 0.15), 1)
    co2_saved = round((distance_km - optimized_distance) * 0.22 + (distance_km * co2_factor), 1)

    return {
        "distance_km": optimized_distance,
        "time_saved": max(0.2, time_saved),
        "cost_difference": cost_change,
        "co2_saved": max(1.0, co2_saved),
    }


with st.sidebar:
    st.markdown("### Control Panel")
    mode = st.radio("Mode Selection", MODE_OPTIONS, index=MODE_OPTIONS.index(st.session_state.mode_label))
    st.session_state.mode_label = mode
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Platform Status")
    st.markdown(badge_markup("API Online", "badge-green"), unsafe_allow_html=True)
    st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)
    st.markdown(badge_markup("Routing Active", "badge-blue"), unsafe_allow_html=True)
    st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)
    st.markdown(
        badge_markup(MODE_META[mode]["short"], MODE_META[mode]["badge"]),
        unsafe_allow_html=True,
    )

if (
    st.session_state.distance_km is not None
    and st.session_state.origin_name
    and st.session_state.destination_name
):
    refreshed_profile = compute_operational_profile(
        st.session_state.distance_km,
        st.session_state.duration_minutes,
        st.session_state.cargo_type,
        mode,
        st.session_state.origin_name,
        st.session_state.destination_name,
    )
    refreshed_title, refreshed_body, refreshed_insights = get_recommendation(mode, refreshed_profile)
    st.session_state.delay_hours = refreshed_profile["delay_hours"]
    st.session_state.risk_score = refreshed_profile["risk_score"]
    st.session_state.selected_reasons = refreshed_profile["selected_reasons"]
    st.session_state.traffic_level = refreshed_profile["traffic_level"]
    st.session_state.weather_condition = refreshed_profile["weather_condition"]
    st.session_state.route_condition = (
        f"{refreshed_profile['traffic_level']} traffic / {refreshed_profile['weather_condition']}"
    )
    st.session_state.decision = refreshed_title
    st.session_state.recommendation_body = refreshed_body
    st.session_state.insights = refreshed_insights
    st.session_state.better_route_savings_factor = 0.12 if mode == "🌱 Eco Mode" else 0.08

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🚚 Smart Supply Chain AI</div>
        <div class="hero-subtitle">Adaptive Logistics Intelligence System</div>
    </div>
    """,
    unsafe_allow_html=True,
)

map_title_col, map_badge_col = st.columns([1.4, 0.6])
with map_title_col:
    st.markdown("<div class='section-title'>🗺 Map Overview</div>", unsafe_allow_html=True)
with map_badge_col:
    st.markdown(
        f"<div style='text-align:right'>{badge_markup(MODE_META[mode]['reason'], 'badge-purple')}</div>",
        unsafe_allow_html=True,
    )

current_map = build_default_map()
if st.session_state.origin_coords and st.session_state.destination_coords and st.session_state.route_points:
    current_map = build_route_map(
        st.session_state.origin_coords,
        st.session_state.destination_coords,
        st.session_state.route_points,
    )

st.markdown("<div class='map-shell'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="map-header">
        <div>
            <div class="section-title" style="margin-bottom:0.25rem;">Live Logistics Route</div>
            <div class="section-kicker">India-centered operational view with live route rendering once a shipment is analyzed.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st_folium(current_map, width=None, height=470)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
render_card_header("📦 Shipment Input", "Enter shipment details to generate route intelligence and operational recommendations.")
input_col1, input_col2, input_col3 = st.columns([1.1, 1.1, 0.85])
with input_col1:
    origin = st.text_input("Origin", value=st.session_state.origin_name, placeholder="Enter origin city")
with input_col2:
    destination = st.text_input("Destination", value=st.session_state.destination_name, placeholder="Enter destination city")
with input_col3:
    cargo_type = st.selectbox(
        "Cargo",
        ["Medicine", "Food", "Electronics"],
        index=["Medicine", "Food", "Electronics"].index(st.session_state.cargo_type),
    )

can_analyze = bool(origin.strip() and destination.strip())
if not can_analyze:
    st.error("Please enter both origin and destination to start analysis.")

if st.button("Analyze Shipment", disabled=not can_analyze, use_container_width=True):
    with st.spinner("Analyzing route, delivery conditions, and optimization opportunities..."):
        try:
            origin_coords = get_coordinates(origin.strip())
            destination_coords = get_coordinates(destination.strip())

            if not origin_coords or not destination_coords:
                st.error("One of the entered locations could not be found. Please try another city name.")
            else:
                route_details = get_route_details(origin_coords, destination_coords)
                if not route_details:
                    st.error("Unable to calculate a route right now. Please try again shortly.")
                else:
                    distance_km, duration_minutes, route_points = route_details
                    profile = compute_operational_profile(
                        distance_km,
                        duration_minutes,
                        cargo_type,
                        mode,
                        origin.strip(),
                        destination.strip(),
                    )
                    recommendation_title, recommendation_body, insights = get_recommendation(mode, profile)

                    st.session_state.origin_name = origin.strip()
                    st.session_state.destination_name = destination.strip()
                    st.session_state.cargo_type = cargo_type
                    st.session_state.origin_coords = origin_coords
                    st.session_state.destination_coords = destination_coords
                    st.session_state.route_points = route_points
                    st.session_state.distance_km = profile["distance_km"]
                    st.session_state.duration_minutes = profile["duration_minutes"]
                    st.session_state.delay_hours = profile["delay_hours"]
                    st.session_state.risk_score = profile["risk_score"]
                    st.session_state.selected_reasons = profile["selected_reasons"]
                    st.session_state.traffic_level = profile["traffic_level"]
                    st.session_state.weather_condition = profile["weather_condition"]
                    st.session_state.route_condition = f"{profile['traffic_level']} traffic / {profile['weather_condition']}"
                    st.session_state.simulation_name = None
                    st.session_state.decision = recommendation_title
                    st.session_state.optimized_route = None
                    st.session_state.better_route_savings_factor = 0.12 if mode == "🌱 Eco Mode" else 0.08
                    st.session_state.insights = insights
                    st.session_state.recommendation_body = recommendation_body
        except (HTTPError, URLError, TimeoutError, ValueError):
            st.error("Unable to connect to the routing service right now. Please try again.")
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.distance_km is not None:
    estimated_hours = st.session_state.duration_minutes / 60
    risk_text, risk_badge = get_status(st.session_state.risk_score)

    top_left, top_right = st.columns(2)

    with top_left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_card_header("📊 Route Overview")
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.markdown(
                f"""
                <div class="metric-label">Distance</div>
                <div class="metric-value">{st.session_state.distance_km:.1f} km</div>
                <div class="metric-subtext">Current planned corridor length</div>
                """,
                unsafe_allow_html=True,
            )
        with metric_col2:
            st.markdown(
                f"""
                <div class="metric-label">Time</div>
                <div class="metric-value">{estimated_hours:.1f} hrs</div>
                <div class="metric-subtext">Estimated drive duration before optimization</div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with top_right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_card_header("⚠ Route Condition")
        cond_col1, cond_col2, cond_col3 = st.columns(3)
        with cond_col1:
            st.markdown("Traffic")
            st.markdown(
                badge_markup(st.session_state.traffic_level, traffic_badge(st.session_state.traffic_level)),
                unsafe_allow_html=True,
            )
        with cond_col2:
            st.markdown("Weather")
            st.markdown(
                badge_markup(st.session_state.weather_condition, weather_badge(st.session_state.weather_condition)),
                unsafe_allow_html=True,
            )
        with cond_col3:
            st.markdown("Delay")
            delay_badge = "badge-red" if st.session_state.delay_hours >= 2 else "badge-amber" if st.session_state.delay_hours >= 1 else "badge-green"
            st.markdown(
                badge_markup(f"{st.session_state.delay_hours:.1f} hrs", delay_badge),
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card highlight-card'>", unsafe_allow_html=True)
    render_card_header("🤖 Smart Recommendation")
    st.markdown(
        f"""
        <div class="recommendation-title">{st.session_state.decision}</div>
        <div class="recommendation-copy">{st.session_state.recommendation_body}</div>
        {badge_markup(MODE_META[mode]['short'], MODE_META[mode]['badge'])}
        &nbsp;
        {badge_markup(risk_text, risk_badge)}
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    insight_col, risk_col = st.columns([1.1, 0.9])

    with insight_col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_card_header("🧠 AI Decision Insight")
        st.markdown(
            "<ul class='info-list'>" + "".join(f"<li>{item}</li>" for item in st.session_state.insights) + "</ul>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with risk_col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_card_header("Risk & Reliability")
        st.markdown(
            f"""
            <div class="metric-label">Risk Score</div>
            <div class="metric-value">{st.session_state.risk_score}%</div>
            <div style="margin:0.6rem 0 0.95rem 0;">{badge_markup(risk_text, risk_badge)}</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<ul class='info-list'>" + "".join(f"<li>{item}</li>" for item in st.session_state.selected_reasons) + "</ul>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_card_header("🔁 Optimization Section", "Generate an improved route profile based on the currently selected operating mode.")
    if st.button("Optimize Route", use_container_width=True):
        st.session_state.optimized_route = optimize_route(
            mode,
            st.session_state.distance_km,
            st.session_state.duration_minutes,
            st.session_state.delay_hours,
        )

    if st.session_state.optimized_route:
        optimization = st.session_state.optimized_route
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            metric_tile("New Distance", f"{optimization['distance_km']:.1f} km", "Projected optimized route length")
            metric_tile(
                "Cost Difference",
                f"{'+' if optimization['cost_difference'] > 0 else '-'}₹{abs(optimization['cost_difference'])}",
                "Positive indicates premium spend, negative indicates savings",
            )
        with opt_col2:
            metric_tile("Time Saved", f"{optimization['time_saved']:.1f} hrs", "Estimated improvement against current plan")
            metric_tile("CO2 Saved", f"{optimization['co2_saved']:.1f} kg", "Sustainability gain from route optimization")
    else:
        idle_col1, idle_col2 = st.columns(2)
        with idle_col1:
            metric_tile("Current Delay", f"{st.session_state.delay_hours:.1f} hrs", "Estimated operational delay exposure")
        with idle_col2:
            metric_tile("Mode Strategy", MODE_META[mode]["short"], MODE_META[mode]["reason"])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
        Built by Siddhi Choudhary | Smart Logistics AI Prototype
    </div>
    """,
    unsafe_allow_html=True,
)
