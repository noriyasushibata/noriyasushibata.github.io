import json
from datetime import datetime, timedelta

TEAM_FILE = "team_data.json"

TIMEZONE_OFFSETS = {
    "PST": -8,
    "CST": -6,
    "EST": -5,
}

DAY_MAP = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


def load_team():
    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_availability(availability_str):
    """Parse availability string like 'Mon-Fri, 9am-5pm' into structured data."""
    parts = availability_str.split(", ")
    days_part = parts[0]
    time_part = parts[1]

    day_range = days_part.split("-")
    start_day = DAY_MAP[day_range[0]]
    end_day = DAY_MAP[day_range[1]]

    time_range = time_part.split("-")
    start_time = parse_time(time_range[0])
    end_time = parse_time(time_range[1])

    return {
        "days": (start_day, end_day),
        "hours": (start_time, end_time),
    }


def parse_time(time_str):
    """Convert '9am' or '5pm' to 24-hour format."""
    time_str = time_str.lower().strip()
    is_pm = "pm" in time_str
    hour = int(time_str.replace("am", "").replace("pm", ""))
    if is_pm and hour != 12:
        hour += 12
    elif not is_pm and hour == 12:
        hour = 0
    return hour


def get_utc_hour(local_hour, timezone):
    """Convert local hour to UTC."""
    offset = TIMEZONE_OFFSETS.get(timezone, 0)
    utc_hour = (local_hour - offset) % 24
    return utc_hour


def find_overlap():
    """Find overlapping availability across all team members."""
    team = load_team()

    overlaps = {}

    for day_num, day_name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]):
        available_utc_hours = None

        for member in team:
            avail = parse_availability(member["availability"])
            day_start, day_end = avail["days"]

            if day_start <= day_num <= day_end:
                local_start, local_end = avail["hours"]
                utc_start = get_utc_hour(local_start, member["timezone"])
                utc_end = get_utc_hour(local_end, member["timezone"])

                if utc_start <= utc_end:
                    member_hours = set(range(utc_start, utc_end))
                else:
                    member_hours = set(range(utc_start, 24)) | set(range(0, utc_end))

                if available_utc_hours is None:
                    available_utc_hours = member_hours
                else:
                    available_utc_hours &= member_hours
            else:
                if available_utc_hours is None:
                    available_utc_hours = set()
                else:
                    available_utc_hours &= set()

        if available_utc_hours:
            sorted_hours = sorted(available_utc_hours)
            overlaps[day_name] = {
                "utc_hours": sorted_hours,
                "local_times": get_local_times(sorted_hours, team),
            }
        else:
            overlaps[day_name] = {"utc_hours": [], "local_times": {}}

    return overlaps


def get_local_times(utc_hours, team):
    """Convert UTC hours back to local times for each team member."""
    local_times = {}
    for member in team:
        offset = TIMEZONE_OFFSETS.get(member["timezone"], 0)
        local_hours = [(hour + offset) % 24 for hour in utc_hours]
        local_times[member["name"]] = sorted(set(local_hours))
    return local_times


def display_overlap():
    """Print team overlap results."""
    overlap = find_overlap()
    team = load_team()

    print("\n" + "=" * 80)
    print("TEAM SCHEDULING OVERLAP ANALYSIS")
    print("=" * 80 + "\n")

    for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        data = overlap.get(day, {})
        print(f"📅 {day}")
        if data.get("utc_hours"):
            print(f"   ✓ Overlap window (UTC): {data['utc_hours']}")
            for name, hours in data.get("local_times", {}).items():
                print(f"   • {name}: {hours}")
        else:
            print(f"   ✗ No overlap found")
        print()

    print("=" * 80 + "\n")


if __name__ == "__main__":
    display_overlap()
