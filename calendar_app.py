import calendar
import datetime
import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser

DATA_FILE = "calendar_events.json"
TEAM_FILE = "team_interface.html"


def load_events():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return {}
    return {}


def save_events(events):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=2)


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Lab Calendar")
        self.root.geometry("640x520")
        self.root.configure(bg="#15202b")

        self.palette = {
            "bg": "#15202b",
            "panel": "#20303f",
            "text": "#e8f1ff",
            "accent": "#4f9eed",
            "button": "#5e9cec",
            "button_text": "#ffffff",
            "weekday": "#a0d8ff",
            "weekend": "#f6c26b",
            "other_month": "#576876",
            "selected": "#60afff",
            "selected_text": "#0f172a",
            "event_day": "#3dc077",
            "event_text": "#0f172a",
        }

        self.events = load_events()
        self.current_date = datetime.date.today().replace(day=1)
        self.selected_date = datetime.date.today()

        self.header_frame = tk.Frame(root, bg=self.palette["panel"])
        self.header_frame.pack(pady=10, fill="x", padx=10)

        self.prev_button = tk.Button(
            self.header_frame,
            text="←",
            width=4,
            command=self.prev_month,
            bg=self.palette["button"],
            fg=self.palette["button_text"],
            activebackground="#76b5ff",
            relief="flat",
        )
        self.prev_button.grid(row=0, column=0, padx=(5, 0), pady=10)

        self.month_label = tk.Label(
            self.header_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["text"],
        )
        self.month_label.grid(row=0, column=1, padx=12)

        self.next_button = tk.Button(
            self.header_frame,
            text="→",
            width=4,
            command=self.next_month,
            bg=self.palette["button"],
            fg=self.palette["button_text"],
            activebackground="#76b5ff",
            relief="flat",
        )
        self.next_button.grid(row=0, column=2, padx=(0, 5), pady=10)

        self.team_button = tk.Button(
            self.header_frame,
            text="👥 Team",
            command=self.open_team_view,
            bg="#9f7aea",
            fg=self.palette["button_text"],
            activebackground="#b794f6",
            relief="flat",
            padx=8,
        )
        self.team_button.grid(row=0, column=3, padx=(0, 5), pady=10)

        self.calendar_frame = tk.Frame(root, bg=self.palette["bg"])
        self.calendar_frame.pack(padx=10)

        self.details_frame = tk.Frame(root, bg=self.palette["panel"])
        self.details_frame.pack(fill="x", padx=10, pady=12)

        tk.Label(
            self.details_frame,
            text="Selected Date:",
            bg=self.palette["panel"],
            fg=self.palette["text"],
        ).grid(row=0, column=0, sticky="w")
        self.selected_label = tk.Label(
            self.details_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["accent"],
        )
        self.selected_label.grid(row=0, column=1, sticky="w")

        tk.Label(
            self.details_frame,
            text="Event:",
            bg=self.palette["panel"],
            fg=self.palette["text"],
        ).grid(row=1, column=0, sticky="nw", pady=(8, 0))
        self.event_text = scrolledtext.ScrolledText(
            self.details_frame,
            width=60,
            height=4,
            bg="#1b2734",
            fg=self.palette["text"],
            insertbackground=self.palette["text"],
            relief="flat",
        )
        self.event_text.grid(row=1, column=1, pady=(8, 0), padx=(8, 0))

        self.button_frame = tk.Frame(self.details_frame, bg=self.palette["panel"])
        self.button_frame.grid(row=2, column=1, sticky="e", pady=8)

        tk.Button(
            self.button_frame,
            text="Add/Update Event",
            command=self.add_event,
            bg=self.palette["button"],
            fg=self.palette["button_text"],
            activebackground="#76b5ff",
            relief="flat",
        ).pack(side="left", padx=4)
        tk.Button(
            self.button_frame,
            text="Delete Event",
            command=self.delete_event,
            bg="#d9534f",
            fg=self.palette["button_text"],
            activebackground="#ef6c70",
            relief="flat",
        ).pack(side="left", padx=4)

        tk.Label(
            root,
            text="Events for Selected Date:",
            font=("Arial", 12, "bold"),
            bg=self.palette["bg"],
            fg=self.palette["text"],
        ).pack(anchor="w", padx=10)
        self.events_list = scrolledtext.ScrolledText(
            root,
            width=74,
            height=10,
            state="disabled",
            bg="#1b2734",
            fg=self.palette["text"],
            relief="flat",
        )
        self.events_list.pack(padx=10, pady=(0, 10))

        self.refresh_calendar()
        self.update_selected_date(self.selected_date)

    def refresh_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        month_name = self.current_date.strftime("%B %Y")
        self.month_label.config(text=month_name)

        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for idx, day in enumerate(week_days):
            fg_color = self.palette["weekend"] if idx >= 5 else self.palette["weekday"]
            tk.Label(
                self.calendar_frame,
                text=day,
                width=8,
                fg=fg_color,
                bg=self.palette["bg"],
                font=("Arial", 10, "bold"),
            ).grid(row=0, column=idx, pady=(0, 6))

        month_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(self.current_date.year, self.current_date.month)

        for week_index, week in enumerate(month_calendar, start=1):
            for day_index, day in enumerate(week):
                if day.month != self.current_date.month:
                    label = tk.Label(
                        self.calendar_frame,
                        text=day.day,
                        width=8,
                        fg=self.palette["other_month"],
                        bg=self.palette["bg"],
                    )
                    label.grid(row=week_index, column=day_index)
                else:
                    is_weekend = day.weekday() >= 5
                    has_event = bool(self.get_event(day))
                    button_bg = self.palette["panel"]
                    button_fg = self.palette["text"]

                    if day == self.selected_date:
                        button_bg = self.palette["selected"]
                        button_fg = self.palette["selected_text"]
                    elif has_event:
                        button_bg = self.palette["event_day"]
                        button_fg = self.palette["event_text"]
                    elif is_weekend:
                        button_bg = "#2f4f6d"
                        button_fg = self.palette["weekend"]

                    button = tk.Button(
                        self.calendar_frame,
                        text=str(day.day),
                        width=8,
                        relief="flat",
                        bg=button_bg,
                        fg=button_fg,
                        activebackground=self.palette["accent"],
                        command=lambda d=day: self.update_selected_date(d),
                    )
                    button.grid(row=week_index, column=day_index, padx=2, pady=2)

    def update_selected_date(self, date_value):
        self.selected_date = date_value
        self.selected_label.config(text=self.selected_date.isoformat())
        event_text = self.get_event(self.selected_date) or ""
        self.event_text.delete("1.0", tk.END)
        self.event_text.insert(tk.END, event_text)
        self.refresh_calendar()
        self.render_events_list()

    def get_event(self, date_value):
        return self.events.get(date_value.isoformat(), "")

    def add_event(self):
        text = self.event_text.get("1.0", tk.END).strip()
        date_key = self.selected_date.isoformat()
        if not text:
            messagebox.showwarning("Empty Event", "Enter an event description before saving.")
            return
        self.events[date_key] = text
        save_events(self.events)
        self.refresh_calendar()
        self.render_events_list()
        messagebox.showinfo("Saved", f"Event saved for {date_key}.")

    def delete_event(self):
        date_key = self.selected_date.isoformat()
        if date_key in self.events:
            del self.events[date_key]
            save_events(self.events)
            self.event_text.delete("1.0", tk.END)
            self.refresh_calendar()
            self.render_events_list()
            messagebox.showinfo("Deleted", f"Event deleted for {date_key}.")
        else:
            messagebox.showinfo("No Event", "There is no event to delete for this date.")

    def render_events_list(self):
        self.events_list.config(state="normal")
        self.events_list.delete("1.0", tk.END)
        if not self.events:
            self.events_list.insert(tk.END, "No saved events yet.\n")
        else:
            for date_key in sorted(self.events.keys()):
                self.events_list.insert(tk.END, f"{date_key}: {self.events[date_key]}\n\n")
        self.events_list.config(state="disabled")

    def prev_month(self):
        first = self.current_date.replace(day=1)
        prev_month = first - datetime.timedelta(days=1)
        self.current_date = prev_month.replace(day=1)
        self.refresh_calendar()

    def next_month(self):
        year = self.current_date.year + (self.current_date.month // 12)
        month = self.current_date.month % 12 + 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self.refresh_calendar()

    def open_team_view(self):
        """Open team interface in web browser."""
        team_path = os.path.abspath(TEAM_FILE)
        try:
            webbrowser.open(f"file://{team_path}")
            messagebox.showinfo("Team View", "Opening team scheduler in your browser...")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open team view: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    CalendarApp(root)
    root.mainloop()
