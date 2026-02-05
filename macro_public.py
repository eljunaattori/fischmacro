import cv2
import numpy as np
import mss
import pydirectinput
import pygetwindow as gw
import time
import tkinter as tk
from tkinter import ttk
import threading
import os
import configparser
import random
import webbrowser
from pathlib import Path
from pynput import keyboard
from PIL import Image, ImageDraw, ImageTk

SKIN_PROFILES = {
    "Default": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Onirifalx": {
        "bar_min": np.array([160, 110, 80]),
        "bar_max": np.array([255, 235, 195]),
        "tolerance_bar": 50,
        "fish_min": np.array([0, 0, 0]),
        "fish_max": np.array([50, 50, 50]),
        "tolerance_fish": 5
    },
    "Duskwire": {
        "bar_min": np.array([0, 0, 0]),
        "bar_max": np.array([90, 90, 90]),
        "tolerance_bar": 45,
        "fish_min": np.array([240, 240, 240]),
        "fish_max": np.array([255, 255, 255]),
        "tolerance_fish": 10
    },
    "Astraeus Serenade": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Axe of Rhoads": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Blade of Glorp": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Chrysalis": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Eardrum": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Experimental Rod": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Fabulous Rod": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Mealstrom": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Nates Blade": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Nico's Yarncaster": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Noctone": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Polaris Serenade": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Rainbow Cluster Rod": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Requiem": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Sanguine Spire": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Silly Fun Happy Rod": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Sword of Darkness": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Thalassar's Ruin": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
    "Wingripper": {
        "bar_min": np.array([230, 230, 230]),
        "bar_max": np.array([255, 255, 255]),
        "tolerance_bar": 12,
        "fish_min": np.array([60, 60, 80]),
        "fish_max": np.array([80, 90, 105]),
        "tolerance_fish": 10
    },
}

BAR_COLOR = np.array([241, 241, 241])
BAR_COLOR_2 = np.array([67, 252, 0])
MISS_BAR_MIN = np.array([82, 36, 36])
MISS_BAR_MAX = np.array([74, 93, 68])
FISH_COLOR = np.array([67, 75, 91])
TOLERANCE = 8
WHITE_BAR_TOLERANCE = 12
MISS_BAR_TOLERANCE = 25
FISH_TOLERANCE = 10
TRANSPARENT_COLOR = '#ff00ff'
CONTROL_STAT = 0.1
CONTROL_TO_PIXELS = 3100
MAX_BAR_WIDTH_PCT = 0.7
SIDE_HOLD_LEFT_PCT = 70
SIDE_HOLD_RIGHT_PCT = 70

class FischMacro:
    def __init__(self):
        self.find_roblox()
        self.running = False
        self.overlay = None
        self.minigame_thread = None
        self.debug_canvas = None
        self.bar_overlay_window = None
        self.debug_overlay_window = None
        self.state_overlay_window = None
        self.resilience_overlay_window = None
        self.current_profile = SKIN_PROFILES["Default"]
        self.current_state = "Idle"
        self.pid_kp = 0.8
        self.pid_kd = 0.3
        self.last_error = 0.0
        self.prediction_time = 0.05
        self.tolerance = TOLERANCE
        self.white_bar_tolerance = WHITE_BAR_TOLERANCE
        self.miss_bar_tolerance = MISS_BAR_TOLERANCE
        self.fish_tolerance = FISH_TOLERANCE
        self.control_to_pixels = CONTROL_TO_PIXELS
        self.max_bar_width_pct = MAX_BAR_WIDTH_PCT
        self.frames_since_lost = 0
        self.max_frames_lost = 8
        self.frames_since_fish_lost = 0
        self.shake_white_threshold = 210
        self.shake_area_min = 2000
        self.shake_area_max = 20000
        self.shake_aspect_min = 0.8
        self.shake_aspect_max = 1.2
        self.shake_solidity_min = 0.85
        self.shake_roi_top_pct = 0.1
        self.shake_roi_left_pct = 0.1
        self.shake_roi_width_pct = 0.8
        self.shake_roi_height_pct = 0.8
        self.last_hover_time = time.time()
        self.transparency_delay = 5.0
        self.transparency_enabled = True
        self.is_transparent = False
        self.auto_recast_enabled = True
        self.auto_shake_enabled = True
        self.shake_type = "Mouse"
        self.shake_nav_key = "'"
        self.waiting_for_key = False
        self.waiting_for_hotkey = False
        self.auto_lower_graphics_enabled = True
        self.graphics_lowered_this_session = False
        self.auto_camera_mode_enabled = True
        self.camera_mode_enabled_this_session = False
        self.toggle_hotkey = 'f8'
        self.auto_cast_enabled = False
        self.auto_cast_delay = 1.0
        self.cast_duration = 0.6
        self.focus_loss_stop = True
        self.macro_start_time = None
        self.auto_blur_enabled = True
        self.blur_enabled_this_session = False
        self.rod_equipped_this_session = False
        self.debug_display_enabled = False
        self.state_display_enabled = True
        self.resilience_display_enabled = False
        self.active_time_display_enabled = False
        self.visual_debug_enabled = False
        self.visual_debug_show_raw = True
        self.visual_debug_show_bar_mask = False
        self.visual_debug_show_fish_mask = False
        self.visual_debug_show_white_mask = False
        self.visual_debug_show_dark_mask = False
        self.visual_debug_show_contours = False
        self.visual_debug_show_bar_box = True
        self.visual_debug_show_fish_pos = True
        self.minigame_visuals_enabled = True
        self.rod_custom_ui_enabled = False
        self.rod_skin_selection = ""
        self.shake_detected = False
        self.shake_start_time = None
        self.last_shake_check_time = 0.0
        self.script_dir = Path(__file__).parent
        self.config_dir = self.script_dir / "configs"
        self.config_dir.mkdir(exist_ok=True)
        print(f"Config directory: {self.config_dir}")
        bar_width_pct = 30 + (CONTROL_STAT * 100)
        roi_width = 883
        self.expected_bar_width = int((bar_width_pct / 100) * roi_width)
        self.max_bar_width = self.expected_bar_width * 2
        self.calculate_regions()
        self.current_control_stat = CONTROL_STAT
        self.last_bar_center = None
        self.last_bar_width = self.expected_bar_width
        self.last_time = None
        self.bar_velocity = 0.0
        self.holding = False
        self.hold_start_time = None
        self.target_hold_duration = 0.0
        self.hold_release_time = None
        self.last_detection_time = None
        self.detection_timeout = 2.0
        self.max_bar_speed = 500.0
        self.debug_screenshot_taken = False
        
        self.control_params = {
            'critical_distance': 8,
            'close_distance': 20,
            'moderate_distance': 50,
            'far_distance': 100,
            'critical_decel': 200.0,
            'close_decel': 350.0,
            'moderate_decel': 500.0,
            'far_decel': 700.0,
            'left_critical_decel': 200.0,
            'left_close_decel': 350.0,
            'left_moderate_decel': 500.0,
            'left_far_decel': 700.0,
            'right_critical_decel': 200.0,
            'right_close_decel': 350.0,
            'right_moderate_decel': 500.0,
            'right_far_decel': 700.0,
        }
        self.stabilization_zone_pct = 2
        self.side_hold_left_pct = 30
        self.side_hold_right_pct = 30
        self.side_hold_visuals_enabled = False
        self.consecutive_releases = 0
        self.fish_jump_detected = False
        self.last_jump_time = None
        self.jump_cooldown = 0.200
        self.rod_resilience = 0.20
        self.bait_resilience = -0.15
        self.effective_resilience = max(0.20, self.rod_resilience + self.bait_resilience)
        self.onirifalx_resilience_enabled = False
        self.onirifalx_prev_rod_resilience = self.rod_resilience
        self.last_detected_fish_x = None
        self.last_movement_detection_time = None
        self.time_since_last_movement = 0.0
        self.last_jump_fish_x = None
        self.expected_landing_zone_min = None
        self.expected_landing_zone_max = None
        self.prediction_active = False
        self.accel_threshold = 500.0
        self.fish_velocity_threshold = 20.0
        self.last_fish_x = None
        self.last_fish_time = None
        self.fish_velocity = 0.0
        self.fish_accel = 0.0
        self.critical_distance_slider = None
        self.close_distance_slider = None
        self.moderate_distance_slider = None
        self.far_distance_slider = None
        self.critical_decel_slider = None
        self.close_decel_slider = None
        self.moderate_decel_slider = None
        self.far_decel_slider = None
        self.left_critical_decel_slider = None
        self.left_close_decel_slider = None
        self.left_moderate_decel_slider = None
        self.left_far_decel_slider = None
        self.right_critical_decel_slider = None
        self.right_close_decel_slider = None
        self.right_moderate_decel_slider = None
        self.right_far_decel_slider = None
        self.side_hold_left_slider = None
        self.side_hold_right_slider = None
        self.setup_overlay()
        self.setup_bar_overlay()
        self.setup_debug_overlay()
        self.setup_state_overlay()
        self.setup_active_time_overlay()
        self.setup_visual_debug_overlay()
        self.setup_hotkey()
        self.overlay.after(100, self.auto_load_latest_delayed)

    def find_roblox(self):
        try:
            self.window = gw.getWindowsWithTitle('Roblox')[0]
            self.window.activate()
        except IndexError:
            print("Roblox not found!")
            exit()

    def focus_roblox(self):
        try:
            if self.window.isMinimized:
                self.window.restore()
            self.window.activate()
            time.sleep(0.2)
            center_x = self.window.left + (self.window.width // 2)
            center_y = self.window.top + (self.window.height // 2)
            pydirectinput.moveTo(center_x, center_y)
            print(f"Roblox window focused and mouse centered at ({center_x}, {center_y})")
            return True
        except Exception as e:
            print(f"Failed to focus Roblox window: {e}")
            return False

    def calculate_regions(self):
        left = self.window.left
        top = self.window.top
        window_width = self.window.width
        window_height = self.window.height
        minigame_width = int(window_width * 0.46)
        minigame_left = left + int(window_width * 0.27)
        minigame_height = int(window_height * 0.04)
        minigame_top = top + int(window_height * 0.835)
        
        self.fish_bar_roi = {
            'top': minigame_top,
            'left': minigame_left,
            'width': minigame_width,
            'height': minigame_height
        }
        
        self.max_bar_width = int(minigame_width * self.max_bar_width_pct)
        print(f"Minigame ROI: {self.fish_bar_roi}")
        print(f"Max bar width: {self.max_bar_width}px ({self.max_bar_width_pct*100}% of ROI)")
        print(f"Window size: {window_width}x{window_height}")
        print(f"Scanning centered region at bottom of screen")

    def setup_bar_overlay(self):
        self.bar_overlay_window = tk.Toplevel()
        self.bar_overlay_window.attributes('-topmost', True)
        self.bar_overlay_window.attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.bar_overlay_window.configure(bg=TRANSPARENT_COLOR)
        roi = self.fish_bar_roi
        indicator_height = 40
        overlay_top = roi['top'] + roi['height'] + 6
        self.bar_overlay_window.geometry(f"{roi['width']}x{indicator_height}+{roi['left']}+{overlay_top}")
        self.bar_overlay_window.overrideredirect(True)
        self.bar_canvas = tk.Canvas(
            self.bar_overlay_window,
            width=roi['width'],
            height=indicator_height,
            bg=TRANSPARENT_COLOR,
            highlightthickness=0
        )
        self.bar_canvas.pack(fill=tk.BOTH, expand=True)

    def setup_debug_overlay(self):
        self.debug_overlay_window = tk.Toplevel()
        self.debug_overlay_window.attributes('-topmost', True)
        self.debug_overlay_window.attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.debug_overlay_window.configure(bg=TRANSPARENT_COLOR)
        self.debug_overlay_window.overrideredirect(True)
        self.screen_width = self.debug_overlay_window.winfo_screenwidth()
        self.overlay_right_x = self.screen_width - 20
        self.overlay_start_y = 60
        self.overlay_spacing = 120
        self.debug_width = 220
        self.debug_height = 110
        self.state_width = 220
        self.state_height = 110
        self.resilience_width = 220
        self.resilience_height = 110
        self.performance_width = 220
        self.performance_height = 110
        debug_x = self.overlay_right_x - self.debug_width
        self.debug_overlay_window.geometry(f"{self.debug_width}x{self.debug_height}+{debug_x}+{self.overlay_start_y}")
        debug_bg = tk.Frame(
            self.debug_overlay_window,
            bg='#1e1e1e',
            highlightthickness=1,
            highlightbackground='#3e3e42'
        )
        debug_bg.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.debug_display_label = tk.Label(
            debug_bg,
            text="Bar: --\nFish: --",
            font=("Consolas", 8),
            fg="#4ec9b0",
            bg='#1e1e1e',
            anchor='w',
            justify='left',
            padx=8,
            pady=8
        )
        self.debug_display_label.pack(fill=tk.BOTH, expand=True)
        self.debug_overlay_window.withdraw()

    def setup_state_overlay(self):
        self.state_overlay_window = tk.Toplevel()
        self.state_overlay_window.attributes('-topmost', True)
        self.state_overlay_window.attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.state_overlay_window.configure(bg=TRANSPARENT_COLOR)
        self.state_overlay_window.overrideredirect(True)
        state_x = self.overlay_right_x - self.state_width
        self.state_overlay_window.geometry(f"{self.state_width}x{self.state_height}+{state_x}+{self.overlay_start_y}")
        state_bg = tk.Frame(
            self.state_overlay_window,
            bg='#1e1e1e',
            highlightthickness=1,
            highlightbackground='#3e3e42'
        )
        state_bg.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.state_display_label = tk.Label(
            state_bg,
            text="Idle",
            font=("Segoe UI", 8),
            fg="#FFD700",
            bg='#1e1e1e',
            anchor='w',
            justify='left',
            padx=8,
            pady=8
        )
        self.state_display_label.pack(fill=tk.BOTH, expand=True)

        self.resilience_overlay_window = tk.Toplevel()
        self.resilience_overlay_window.attributes('-topmost', True)
        self.resilience_overlay_window.attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.resilience_overlay_window.configure(bg=TRANSPARENT_COLOR)
        self.resilience_overlay_window.overrideredirect(True)
        resilience_x = self.overlay_right_x - self.resilience_width
        self.resilience_overlay_window.geometry(f"{self.resilience_width}x{self.resilience_height}+{resilience_x}+{self.overlay_start_y}")
        resilience_bg = tk.Frame(
            self.resilience_overlay_window,
            bg='#1e1e1e',
            highlightthickness=1,
            highlightbackground='#3e3e42'
        )
        resilience_bg.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.resilience_display_label = tk.Label(
            resilience_bg,
            text="Resilience: Waiting...",
            font=("Segoe UI", 8),
            fg="#00D7FF",
            bg='#1e1e1e',
            anchor='w',
            justify='left',
            padx=8,
            pady=8
        )
        self.resilience_display_label.pack(fill=tk.BOTH, expand=True)
        self.resilience_overlay_window.withdraw()
        
        self.performance_overlay_window = tk.Toplevel()
        self.performance_overlay_window.attributes('-topmost', True)
        self.performance_overlay_window.attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.performance_overlay_window.configure(bg=TRANSPARENT_COLOR)
        self.performance_overlay_window.overrideredirect(True)
        performance_x = self.overlay_right_x - self.performance_width
        self.performance_overlay_window.geometry(f"{self.performance_width}x{self.performance_height}+{performance_x}+{self.overlay_start_y}")
        performance_bg = tk.Frame(
            self.performance_overlay_window,
            bg='#1e1e1e',
            highlightthickness=1,
            highlightbackground='#3e3e42'
        )
        performance_bg.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.performance_display_label = tk.Label(
            performance_bg,
            text="FPS: --\nFrame Time: --ms\nState Time: --ms",
            font=("Consolas", 8),
            fg="#ce9178",
            bg='#1e1e1e',
            anchor='w',
            justify='left',
            padx=8,
            pady=8
        )
        self.performance_display_label.pack(fill=tk.BOTH, expand=True)
        self.performance_overlay_window.withdraw()
        self.perf_frame_times = []
        self.perf_last_frame = time.time()
        self.performance_display_enabled = False
        self.update_overlay_positions()

    def setup_active_time_overlay(self):
        self.active_time_overlay_window = tk.Toplevel()
        self.active_time_overlay_window.attributes('-topmost', True)
        self.active_time_transparent_color = "#000000"
        self.active_time_overlay_window.attributes('-transparentcolor', self.active_time_transparent_color)
        self.active_time_overlay_window.configure(bg=self.active_time_transparent_color)
        self.active_time_overlay_window.overrideredirect(True)
        self.active_time_width = 260
        self.active_time_height = 24
        self.active_time_label = tk.Label(
            self.active_time_overlay_window,
            text="Macro active: 00:00:00",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg=self.active_time_transparent_color,
            anchor='center'
        )
        self.active_time_label.pack(fill=tk.BOTH, expand=True)
        self.update_active_time_position()
        self.active_time_overlay_window.withdraw()
        self.overlay.after(1000, self.update_active_time_display)

    def update_active_time_position(self):
        try:
            screen_width = self.active_time_overlay_window.winfo_screenwidth()
            x = max(0, (screen_width - self.active_time_width) // 2)
            y = 40
            self.active_time_overlay_window.geometry(
                f"{self.active_time_width}x{self.active_time_height}+{x}+{y}"
            )
        except Exception:
            pass

    def update_active_time_display(self):
        try:
            if self.running and self.macro_start_time is not None:
                elapsed = int(time.time() - self.macro_start_time)
            else:
                elapsed = 0

            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            self.active_time_label.config(text=f"Macro active: {hours:02d}:{minutes:02d}:{seconds:02d}")
        except Exception:
            pass
        if hasattr(self, 'overlay'):
            self.overlay.after(1000, self.update_active_time_display)

    def setup_visual_debug_overlay(self):
        self.visual_debug_overlay_window = tk.Toplevel()
        self.visual_debug_overlay_window.attributes('-topmost', True)
        self.visual_debug_overlay_window.configure(bg='#1e1e1e')
        self.visual_debug_overlay_window.overrideredirect(True)
        self.visual_debug_width = 320
        self.visual_debug_height = 200
        self.visual_debug_label = tk.Label(
            self.visual_debug_overlay_window,
            bg='#1e1e1e'
        )
        self.visual_debug_label.pack(fill=tk.BOTH, expand=True)
        self.visual_debug_overlay_window.withdraw()

    def update_visual_debug_overlay(self, sct, bar_left, bar_right, bar_center, fish_x):
        if not self.visual_debug_enabled:
            return
        try:
            roi = self.fish_bar_roi
            img = np.array(sct.grab(roi))
            bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            if self.visual_debug_show_raw:
                base = bgr.copy()
            else:
                base = np.zeros_like(bgr)
            bar_min = self.current_profile.get("bar_min", np.array([230, 230, 230]))
            bar_max = self.current_profile.get("bar_max", np.array([255, 255, 255]))
            bar_mask = cv2.inRange(bgr, bar_min, bar_max)
            fish_min = self.current_profile.get("fish_min", np.array([60, 60, 80]))
            fish_max = self.current_profile.get("fish_max", np.array([80, 90, 105]))
            fish_mask = cv2.inRange(bgr, fish_min, fish_max)
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            _, white_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            _, dark_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
            if self.visual_debug_show_bar_mask:
                bar_color = np.zeros_like(bgr)
                bar_color[:, :, 1] = bar_mask
                base = cv2.addWeighted(base, 1.0, bar_color, 0.5, 0)
            if self.visual_debug_show_fish_mask:
                fish_color = np.zeros_like(bgr)
                fish_color[:, :, 2] = fish_mask
                base = cv2.addWeighted(base, 1.0, fish_color, 0.5, 0)
            if self.visual_debug_show_white_mask:
                white_color = np.zeros_like(bgr)
                white_color[:, :, 0] = white_mask
                base = cv2.addWeighted(base, 1.0, white_color, 0.4, 0)
            if self.visual_debug_show_dark_mask:
                dark_color = np.zeros_like(bgr)
                dark_color[:, :, 2] = dark_mask
                base = cv2.addWeighted(base, 1.0, dark_color, 0.3, 0)
            if self.visual_debug_show_contours:
                contour_source = bar_mask
                contours, _ = cv2.findContours(contour_source, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(base, contours, -1, (255, 255, 0), 1)
            if self.visual_debug_show_bar_box and bar_left is not None and bar_right is not None:
                cv2.rectangle(base, (bar_left, 1), (bar_right, base.shape[0] - 2), (0, 255, 255), 1)
                if bar_center is not None:
                    cv2.line(base, (bar_center, 0), (bar_center, base.shape[0]), (0, 255, 255), 1)
            if self.visual_debug_show_fish_pos and fish_x is not None:
                cv2.line(base, (fish_x, 0), (fish_x, base.shape[0]), (0, 255, 0), 1)
            h, w = base.shape[:2]
            scale = min(self.visual_debug_width / w, self.visual_debug_height / h)
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            resized = cv2.resize(base, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb)
            tk_img = ImageTk.PhotoImage(pil_img)
            self.visual_debug_label.configure(image=tk_img)
            self.visual_debug_label.image = tk_img
        except Exception:
            pass

    def detect_shake_circle(self, sct):
        width = self.window.width
        height = self.window.height
        roi = {
            'top': self.window.top + int(height * self.shake_roi_top_pct),
            'left': self.window.left + int(width * self.shake_roi_left_pct),
            'width': int(width * self.shake_roi_width_pct),
            'height': int(height * self.shake_roi_height_pct)
        }
        img = np.array(sct.grab(roi))
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        _, thresh = cv2.threshold(gray, self.shake_white_threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.shake_area_min < area < self.shake_area_max:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 0 and h > 0:
                    aspect_ratio = float(w) / h
                    if self.shake_aspect_min < aspect_ratio < self.shake_aspect_max:
                        hull = cv2.convexHull(contour)
                        hull_area = cv2.contourArea(hull)
                        if hull_area > 0:
                            solidity = float(area) / hull_area
                            if solidity > self.shake_solidity_min:
                                click_x = roi['left'] + x + w // 2
                                click_y = roi['top'] + y + h // 2
                                print(f"[SHAKE] Shake button detected at ({click_x}, {click_y}), area={area:.0f}, ratio={aspect_ratio:.2f}, solidity={solidity:.2f}")
                                return (click_x, click_y)
        return None

    def perform_shake(self, circle_pos):
        if circle_pos is None:
            return
        if self.shake_type == "Mouse":
            x, y = circle_pos
            offset_x = x + random.randint(-3, 3)
            offset_y = y + random.randint(-3, 3)
            pydirectinput.moveTo(offset_x, offset_y)
            time.sleep(0.005)
            pydirectinput.moveTo(x, y)
            pydirectinput.mouseDown()
            pydirectinput.mouseUp()
            
            print(f"Clicked shake circle at ({x}, {y})")
        else:
            self.focus_roblox()
            time.sleep(0.02)
            pydirectinput.press('enter')
            time.sleep(0.03)
            print("Pressed ENTER for shake")

    def find_bar_color_strict(self, screenshot, target_color, tolerance):
        lower = np.clip(target_color - tolerance, 0, 255)
        upper = np.clip(target_color + tolerance, 0, 255)
        mask = cv2.inRange(screenshot, lower, upper)
        coords = np.where(mask > 0)
        if len(coords[1]) == 0:
            return None, None
        left_x = int(np.min(coords[1]))
        right_x = int(np.max(coords[1]))
        detected_width = right_x - left_x
        if detected_width < 5:
            return None, None
        if detected_width > 100:
            if detected_width > self.max_bar_width:
                return None, None
            if detected_width < 50:
                return None, None
        return left_x, right_x

    def find_bar_by_darkness(self, screenshot):
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        mean_darkness = np.mean(gray, axis=0)
        min_idx = int(np.argmin(mean_darkness))
        threshold = mean_darkness[min_idx] + 20
        left_x = min_idx
        while left_x > 0 and mean_darkness[left_x] < threshold:
            left_x -= 1
        right_x = min_idx
        while right_x < len(mean_darkness) - 1 and mean_darkness[right_x] < threshold:
            right_x += 1
        detected_width = right_x - left_x
        if detected_width > self.max_bar_width or detected_width < 50:
            return None, None
        return int(left_x), int(right_x)
    
    def find_miss_bar_by_color_range(self, screenshot):
        lower_bound = np.clip(MISS_BAR_MIN - self.miss_bar_tolerance, 0, 255)
        upper_bound = np.clip(MISS_BAR_MAX + self.miss_bar_tolerance, 0, 255)
        mask = cv2.inRange(screenshot, lower_bound, upper_bound)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        h, w = mask.shape
        col_hits = np.sum(mask > 0, axis=0)
        col_threshold = int(h * 0.15)
        cols = np.where(col_hits >= col_threshold)[0]
        if cols.size == 0:
            return None, None
        breaks = np.where(np.diff(cols) > 2)[0]
        spans = []
        start = 0
        for b in breaks:
            spans.append((cols[start], cols[b]))
            start = b + 1
        spans.append((cols[start], cols[-1]))
        left_x, right_x = max(spans, key=lambda s: s[1] - s[0])
        detected_width = right_x - left_x
        if detected_width < 30:
            return None, None
        return int(left_x), int(right_x)

    def minigame_loop(self):
        sct = mss.mss()
        consecutive_no_real_fish_detections = 0
        fish_miss_count = 0
        fish_miss_threshold = 8
        bar_miss_count = 0
        bar_miss_threshold = 15
        minigame_start_time = time.time()
        seen_real_fish = False
        loop_start_time = time.time()
        try:
            while self.running:
                now = time.time()
                if self.focus_loss_stop:
                    try:
                        active_window = gw.getActiveWindow()
                        if active_window is None or 'roblox' not in active_window.title.lower():
                            print("Roblox window lost focus - emergency stop!")
                            self.set_state("Focus lost - stopping")
                            self.stop_macro()
                            break
                    except Exception as e:
                        pass
                if self.performance_display_enabled:
                    current_time = time.time()
                    frame_time = (current_time - self.perf_last_frame) * 1000
                    self.perf_frame_times.append(frame_time)
                    if len(self.perf_frame_times) > 30:
                        self.perf_frame_times.pop(0)
                    self.perf_last_frame = current_time
                bar_left, bar_right, bar_center = self.get_bar_edges(sct, self.fish_bar_roi, None)
                frames_lost_before = getattr(self, 'frames_since_fish_lost', 0)
                fish_x = self.get_pixel_pos(sct, self.fish_bar_roi, None)
                frames_lost_after = getattr(self, 'frames_since_fish_lost', 0)
                had_actual_detection = (frames_lost_after == 0)
                if bar_center is not None and fish_x is not None and not self.debug_screenshot_taken:
                    self.debug_screenshot_taken = True
                    self.debug_save_screenshot_from_sct(sct)
                    print("Debug screenshot captured (bar and fish detected)")
                if bar_center is not None:
                    bar_miss_count = 0
                else:
                    bar_miss_count += 1
                if had_actual_detection:
                    consecutive_no_real_fish_detections = 0
                    fish_miss_count = 0
                    self.last_detection_time = now
                    seen_real_fish = True
                else:
                    if not seen_real_fish and (now - minigame_start_time) < 2.0:
                        time.sleep(0.01)
                        continue
                    consecutive_no_real_fish_detections += 1
                    fish_miss_count += 1
                    if seen_real_fish and consecutive_no_real_fish_detections >= fish_miss_threshold:
                        print(f"Fish missing (no actual detection) for {consecutive_no_real_fish_detections} scans - minigame ended (FISH LOSS)")
                        if self.holding:
                            pydirectinput.mouseUp()
                            self.holding = False
                        self.set_state("Minigame ended")
                        time.sleep(0.2)
                        if self.auto_recast_enabled:
                            print("Auto-recast enabled, recasting...")
                            if self.auto_cast_enabled:
                                print(f"Waiting {self.auto_cast_delay}s before casting...")
                                time.sleep(self.auto_cast_delay)
                            else:
                                time.sleep(1.0)
                            self.start()
                        else:
                            self.set_state("Idle")
                            self.stop_macro()
                        break
                if bar_miss_count >= bar_miss_threshold and fish_x is None:
                    print(f"Bar and fish both completely missing - minigame ended (DOUBLE LOSS)")
                    if self.holding:
                        pydirectinput.mouseUp()
                        self.holding = False
                    self.set_state("Minigame ended")
                    time.sleep(0.2)
                    if self.auto_recast_enabled:
                        print("Auto-recast enabled, recasting...")
                        if self.auto_cast_enabled:
                            print(f"Waiting {self.auto_cast_delay}s before casting...")
                            time.sleep(self.auto_cast_delay)
                        else:
                            time.sleep(1.0)
                        self.start()
                    else:
                        self.set_state("Idle")
                        self.stop_macro()
                    break
                if fish_x is not None:
                    if self.last_fish_x is not None and self.last_fish_time is not None:
                        dt = max(1e-6, now - self.last_fish_time)
                        new_fish_velocity = (fish_x - self.last_fish_x) / dt
                        self.fish_accel = (new_fish_velocity - self.fish_velocity) / dt
                        self.fish_velocity = 0.7 * self.fish_velocity + 0.3 * new_fish_velocity
                    self.last_fish_x = fish_x
                    self.last_fish_time = now
                if bar_center is not None and self.last_bar_center is not None and self.last_time is not None:
                    dt = max(1e-6, now - self.last_time)
                    delta = abs(bar_center - self.last_bar_center)
                    max_delta = self.max_bar_speed * dt
                    if delta > max_delta:
                        bar_center = None
                        bar_left = None
                        bar_right = None
                if bar_center is not None:
                    if self.last_bar_center is not None and self.last_time is not None:
                        dt = max(1e-6, now - self.last_time)
                        measured_v = (bar_center - self.last_bar_center) / dt
                        self.bar_velocity = 0.75 * self.bar_velocity + 0.25 * measured_v
                    self.last_bar_center = bar_center
                    self.last_bar_width = (bar_right - bar_left) if (bar_left is not None and bar_right is not None) else self.last_bar_width
                    self.last_time = now
                    predicted_center = bar_center
                else:
                    predicted_center = self.predict_bar_center(now)
                    if self.last_bar_width is not None and predicted_center is not None:
                        half = self.last_bar_width // 2
                        bar_left = int(max(0, predicted_center - half))
                        bar_right = int(min(self.fish_bar_roi['width'] - 1, predicted_center + half))
                    bar_center = predicted_center
                self.update_debug_display(bar_left, bar_right, fish_x)
                self.update_resilience_display()
                self.draw_bar_line(bar_left, bar_right, bar_center, fish_x)
                if self.visual_debug_enabled:
                    self.update_visual_debug_overlay(sct, bar_left, bar_right, bar_center, fish_x)
                if bar_center is not None and fish_x is not None:
                    self.apply_dynamic_control(bar_center, fish_x, now)
                if self.performance_display_enabled and len(self.perf_frame_times) > 0:
                    avg_frame_time = sum(self.perf_frame_times) / len(self.perf_frame_times)
                    fps = 1000 / avg_frame_time if avg_frame_time > 0 else 0
                    state_time = (time.time() - now) * 1000
                    self.performance_display_label.config(
                        text=f"FPS: {fps:.1f}\nAvg Frame: {avg_frame_time:.1f}ms\nState Time: {state_time:.1f}ms"
                    )
                time.sleep(0.01)
        finally:
            sct.__exit__(None, None, None)
            if self.holding:
                pydirectinput.mouseUp()
                self.holding = False

    def apply_dynamic_control(self, bar_center, fish_x, now_time):
        if bar_center is None or fish_x is None:
            if self.holding:
                pydirectinput.mouseUp()
                self.holding = False
            return
        roi_width = self.fish_bar_roi['width']
        left_hold_threshold = roi_width * (self.side_hold_left_pct / 100.0)
        right_hold_threshold = roi_width * (1 - self.side_hold_right_pct / 100.0)
        in_left_side_hold = fish_x < left_hold_threshold
        in_right_side_hold = fish_x > right_hold_threshold
        if in_left_side_hold:
            self.set_state("Playing minigame (side hold left: release)")
            if self.holding:
                pydirectinput.mouseUp()
                self.holding = False
            self.last_error = 0.0
            return
        if in_right_side_hold:
            self.set_state("Playing minigame (side hold right: hold)")
            if not self.holding:
                pydirectinput.mouseDown()
                self.holding = True
                self.hold_start_time = now_time
            self.last_error = 0.0
            return
        bar_width = self.last_bar_width if self.last_bar_width is not None else 100
        predicted_fish_x = fish_x
        if self.last_fish_x is not None and self.last_fish_time is not None:
            dt = max(1e-6, now_time - self.last_fish_time)
            predicted_fish_x = fish_x + (self.fish_velocity * self.prediction_time)
        error = predicted_fish_x - bar_center
        if self.last_fish_time is not None:
            dt = max(1e-6, now_time - self.last_fish_time)
            derivative = (error - self.last_error) / dt
        else:
            derivative = 0.0
        pid_output = (error * self.pid_kp) + (derivative * self.pid_kd)
        self.last_error = error
        stabilization_zone = bar_width * (self.stabilization_zone_pct / 100.0)
        if abs(error) < stabilization_zone:
            self.set_state("Playing minigame (stabilize)")
            print(f"[STABIL] Fish:{fish_x:3.0f} Bar:{bar_center:3.0f} Err:{error:+6.1f}px VelF:{self.fish_velocity:+6.0f} Hold:{self.holding}")
            self.consecutive_releases = 0
            if not hasattr(self, 'last_stabilize_toggle'):
                self.last_stabilize_toggle = now_time
            if abs(error) > 5.0:
                if not hasattr(self, 'stabil_hold_start'):
                    self.stabil_hold_start = now_time
                elapsed = now_time - self.stabil_hold_start
                if elapsed < 0.020:
                    if not self.holding:
                        pydirectinput.mouseDown()
                        self.holding = True
                    return
                else:
                    self.stabil_hold_start = now_time
            else:
                self.stabil_hold_start = now_time
            if now_time - self.last_stabilize_toggle > 0.020:
                if self.holding:
                    pydirectinput.mouseUp()
                    self.holding = False
                else:
                    pydirectinput.mouseDown()
                    self.holding = True
                self.last_stabilize_toggle = now_time
            return
        self.last_stabilize_toggle = now_time
        jump_threshold = 2000.0
        if abs(self.fish_accel) > jump_threshold:
            if not self.fish_jump_detected:
                print(f"[JUMP!] Fish:{fish_x:3.0f} Accel:{self.fish_accel:+8.0f}px/s² - Resilience movement detected, escape hatch disabled")
                self.last_jump_fish_x = fish_x
                self.last_movement_detection_time = now_time
            self.fish_jump_detected = True
            self.last_jump_time = now_time
            self.consecutive_releases = 0
        if self.fish_jump_detected and self.last_jump_time is not None:
            if now_time - self.last_jump_time > self.jump_cooldown:
                self.fish_jump_detected = False
        self.update_movement_timing(fish_x, now_time)
        if self.prediction_active and self.expected_landing_zone_min is not None and self.expected_landing_zone_max is not None:
            target_fish_x = (self.expected_landing_zone_min + self.expected_landing_zone_max) / 2.0
            predicted_error = target_fish_x - bar_center
            if 15 <= abs(predicted_error) <= 150:
                self.set_state("Playing minigame (predictive positioning)")
                if predicted_error > 0:
                    if not self.holding:
                        pydirectinput.mouseDown()
                        self.holding = True
                        self.hold_start_time = now_time
                        self.target_hold_duration = 0.030
                else:
                    if self.holding:
                        pydirectinput.mouseUp()
                        self.holding = False
                return
        is_accelerating_right = self.fish_accel > self.accel_threshold and not self.fish_jump_detected
        is_accelerating_left = self.fish_accel < -self.accel_threshold and not self.fish_jump_detected
        if is_accelerating_right and error > 0:
            self.set_state("Playing minigame (accel hold right)")
            print(f"[ACCEL-R] Fish:{fish_x:3.0f} Bar:{bar_center:3.0f} Err:{error:+6.1f}px Accel:{self.fish_accel:+6.0f}px/s² HOLDING 250ms")
            if not self.holding:
                pydirectinput.mouseDown()
                self.holding = True
                self.hold_start_time = now_time
                self.target_hold_duration = 0.25
            return
        if is_accelerating_left and error < 0:
            self.set_state("Playing minigame (accel damping left)")
            print(f"[ACCEL-L] Fish:{fish_x:3.0f} Bar:{bar_center:3.0f} Err:{error:+6.1f}px Accel:{self.fish_accel:+6.0f}px/s² HOLDING 20ms")
            if not self.holding:
                pydirectinput.mouseDown()
                self.holding = True
                self.hold_start_time = now_time
                self.target_hold_duration = 0.02
            return
        if self.holding and self.bar_velocity > 100 and error < 0:
            self.set_state("Playing minigame (damping overshoot)")
            if self.hold_start_time is None:
                self.hold_start_time = now_time
            elapsed = now_time - self.hold_start_time
            if elapsed >= 0.015:
                pydirectinput.mouseUp()
                self.holding = False
            return
        if self.holding and bar_center > predicted_fish_x:
            self.set_state("Playing minigame (overshoot release)")
            print(f"[OVER] Fish:{fish_x:3.0f} Bar:{bar_center:3.0f} Err:{error:+6.1f}px RELEASING (bar passed fish)")
            pydirectinput.mouseUp()
            self.holding = False
            self.consecutive_releases = 0
            return
        if error <= 0:
            if not self.fish_jump_detected:
                self.consecutive_releases += 1
            if self.consecutive_releases >= 3 and not self.fish_jump_detected:
                self.set_state("Playing minigame (release escape - hold recovery)")
                print(f"[RELEASE] Fish:{fish_x:3.0f} Bar:{bar_center:3.0f} Err:{error:+6.1f}px RELEASING (fish left) [ESCAPE: forcing 20ms hold]")
                if not self.holding:
                    pydirectinput.mouseDown()
                    self.holding = True
                    self.hold_start_time = now_time
                    self.target_hold_duration = 0.020
                    self.consecutive_releases = 0
                return
            self.set_state("Playing minigame (release left)")
            print(f"[RELEASE] Fish:{fish_x:3.0f} Bar:{bar_center:3.0f} Err:{error:+6.1f}px RELEASING (fish left)")
            if self.holding:
                pydirectinput.mouseUp()
                self.holding = False
            return
        abs_error = abs(error)
        self.consecutive_releases = 0
        if error < 0:
            if abs_error < self.control_params['critical_distance']:
                decel_target = self.control_params['left_critical_decel']
                state_msg = "Playing minigame (left critical)"
            elif abs_error < self.control_params['close_distance']:
                decel_target = self.control_params['left_close_decel']
                state_msg = "Playing minigame (left close)"
            elif abs_error < self.control_params['moderate_distance']:
                decel_target = self.control_params['left_moderate_decel']
                state_msg = "Playing minigame (left moderate)"
            elif abs_error < self.control_params['far_distance']:
                decel_target = self.control_params['left_far_decel']
                state_msg = "Playing minigame (left far)"
            else:
                decel_target = self.control_params['left_far_decel'] * 0.8
                state_msg = "Playing minigame (left max)"
        else:
            if abs_error < self.control_params['critical_distance']:
                decel_target = self.control_params['right_critical_decel']
                state_msg = "Playing minigame (right critical)"
            elif abs_error < self.control_params['close_distance']:
                decel_target = self.control_params['right_close_decel']
                state_msg = "Playing minigame (right close)"
            elif abs_error < self.control_params['moderate_distance']:
                decel_target = self.control_params['right_moderate_decel']
                state_msg = "Playing minigame (right moderate)"
            elif abs_error < self.control_params['far_distance']:
                decel_target = self.control_params['right_far_decel']
                state_msg = "Playing minigame (right far)"
            else:
                decel_target = self.control_params['right_far_decel'] * 0.8
                state_msg = "Playing minigame (right max)"
        calculated_hold = (abs_error / max(decel_target, 1.0))
        velocity_factor = 1.0 + (abs(self.fish_velocity) / 400.0) * 0.35
        velocity_factor = max(0.7, min(1.5, velocity_factor))
        calculated_hold *= velocity_factor
        min_hold = 0.010
        max_hold = 0.500
        target_hold_s = max(min_hold, min(max_hold, calculated_hold))
        self.set_state(state_msg)
        print(f"[TRACK] Fish:{fish_x:3.0f} Bar:{bar_center:3.0f} Err:{error:+6.1f}px Vel:{self.fish_velocity:+6.0f}px/s Zone:{'LEFT' if error < 0 else 'RIGHT':4} Decel:{decel_target:5.0f} HoldDur:{target_hold_s*1000:5.1f}ms")
        if not self.holding:
            pydirectinput.mouseDown()
            self.holding = True
            self.hold_start_time = now_time
            self.target_hold_duration = target_hold_s
        else:
            if self.hold_start_time is None:
                self.hold_start_time = now_time
            elapsed = now_time - self.hold_start_time
            if elapsed >= self.target_hold_duration:
                pydirectinput.mouseUp()
                self.holding = False
                self.hold_release_time = now_time

    def predict_bar_center(self, now_time):
        if self.last_bar_center is None or self.last_time is None:
            return None
        dt = max(0.0, now_time - self.last_time)
        pred = self.last_bar_center + self.bar_velocity * dt
        bias = 0.0
        if self.holding:
            bias = 20.0 * dt
        else:
            bias = -20.0 * dt
        pred += bias
        roi_width = self.fish_bar_roi['width']
        min_bound = max(0, 50)
        max_bound = min(roi_width - 1, roi_width - 50)
        pred = int(max(min_bound, min(max_bound, pred)))
        return pred

    def is_valid_bar_width(self, detected_width):
        tolerance = self.expected_bar_width * 1.5
        min_width = max(50, self.expected_bar_width - tolerance)
        max_width = self.expected_bar_width + tolerance
        is_valid = min_width <= detected_width <= max_width
        return is_valid

    def get_bar_edges(self, sct, region, color):
        screenshot = np.array(sct.grab(region))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        if "bar_min" in self.current_profile and "bar_max" in self.current_profile:
            tol = int(self.current_profile.get("tolerance_bar", 0))
            bar_min = np.clip(self.current_profile["bar_min"].astype(np.int16) - tol, 0, 255).astype(np.uint8)
            bar_max = np.clip(self.current_profile["bar_max"].astype(np.int16) + tol, 0, 255).astype(np.uint8)
            result = self._detect_bar_by_color_range(screenshot, bar_min, bar_max)
            if result[2] is not None:
                return result
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        result = self._detect_bar_white(gray, screenshot)
        if result[2] is not None:
            return result
        result = self._detect_bar_dark(gray, screenshot)
        if result[2] is not None:
            return result
        self.frames_since_lost += 1
        if self.frames_since_lost < self.max_frames_lost and self.last_bar_center is not None:
            half_width = self.last_bar_width // 2 if self.last_bar_width else 50
            bar_left = int(self.last_bar_center - half_width)
            bar_right = int(self.last_bar_center + half_width)
            return bar_left, bar_right, self.last_bar_center
        return None, None, None
    
    def _detect_bar_by_color_range(self, screenshot, bar_min, bar_max):
        mask = cv2.inRange(screenshot, bar_min, bar_max)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 1))
        closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, horizontal_kernel)
        contour_result = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contour_result) == 2:
            contours, _ = contour_result
        else:
            _, contours, _ = contour_result
        roi_h, roi_w = screenshot.shape[:2]
        best_bar = None
        max_area = 0
        control_stat = getattr(self, 'current_control_stat', 0.1)
        max_multiplier = 1.5 + (control_stat * 0.5)
        max_width_allowed = min(self.expected_bar_width * max_multiplier, 500)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w < (roi_w * 0.15):
                continue
            if w > max_width_allowed:
                continue
            aspect_ratio = w / float(max(1, h))
            if aspect_ratio < 2.5:
                continue
            center_y = y + (h / 2.0)
            if abs(center_y - (roi_h / 2.0)) > (roi_h * 0.4):
                continue
            area = w * h
            if area > max_area:
                max_area = area
                best_bar = (int(x), int(x + w), int(x + w / 2.0))
        if best_bar is not None:
            self.frames_since_lost = 0
            self.last_bar_center = best_bar[2]
            self.last_bar_width = best_bar[1] - best_bar[0]
            return best_bar
        self.frames_since_lost += 1
        if self.frames_since_lost < self.max_frames_lost and self.last_bar_center is not None:
            half_width = self.last_bar_width // 2 if self.last_bar_width else 50
            bar_left = int(self.last_bar_center - half_width)
            bar_right = int(self.last_bar_center + half_width)
            return bar_left, bar_right, self.last_bar_center
        return None, None, None
    
    def _detect_bar_white(self, gray, screenshot):
        _, binary_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 1))
        closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, horizontal_kernel)
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        dilated_mask = cv2.dilate(closed_mask, dilate_kernel, iterations=1)
        kernel = np.ones((3, 3), np.uint8)
        cleaned_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_OPEN, kernel)
        return self._find_bar_from_mask(gray, cleaned_mask)
    
    def _detect_bar_dark(self, gray, screenshot):
        _, binary_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 1))
        closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, horizontal_kernel)
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))
        dilated_mask = cv2.dilate(closed_mask, dilate_kernel, iterations=2)
        kernel = np.ones((3, 3), np.uint8)
        cleaned_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_OPEN, kernel)
        return self._find_bar_from_mask(gray, cleaned_mask, brightness_threshold=80)
    
    def _find_bar_from_mask(self, gray, mask, brightness_threshold=100):
        contour_result = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contour_result) == 2:
            contours, _ = contour_result
        else:
            _, contours, _ = contour_result
        roi_h, roi_w = gray.shape[:2]
        best_bar = None
        max_area = 0
        control_stat = getattr(self, 'current_control_stat', 0.1)
        max_multiplier = 1.5 + (control_stat * 0.5)
        max_width_allowed = min(self.expected_bar_width * max_multiplier, 500)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w < (roi_w * 0.15):
                continue
            if w > max_width_allowed:
                continue
            aspect_ratio = w / float(max(1, h))
            if aspect_ratio < 2.5:
                continue
            center_y = y + (h / 2.0)
            if abs(center_y - (roi_h / 2.0)) > (roi_h * 0.4):
                continue
            bar_region = gray[y:y+h, x:x+w]
            mean_brightness = np.mean(bar_region)
            if mean_brightness < brightness_threshold:
                continue
            area = w * h
            if area > max_area:
                max_area = area
                best_bar = (x, x + w, int(x + w / 2.0), w, mean_brightness)
        if best_bar:
            bar_left, bar_right, center, detected_width, brightness = best_bar
            self.frames_since_lost = 0
            self.last_bar_center = center
            self.last_bar_width = detected_width
            return int(bar_left), int(bar_right), int(center)
        return None, None, None

    def draw_bar_line(self, bar_left, bar_right, bar_center, fish_x):
        try:
            if fish_x is None:
                self.bar_overlay_window.withdraw()
                return
            if not self.bar_overlay_window.winfo_viewable():
                self.bar_overlay_window.deiconify()
            roi_width = self.fish_bar_roi['width']
            roi_height = 40
            self.bar_canvas.delete("all")
            if self.side_hold_visuals_enabled:
                roi_width = self.fish_bar_roi['width']
                left_threshold = roi_width * (self.side_hold_left_pct / 100.0)
                right_threshold = roi_width * (1 - self.side_hold_right_pct / 100.0)
                self.bar_canvas.create_rectangle(
                    0, 0, left_threshold, roi_height,
                    fill="#c72e2e", stipple="gray50", outline=""
                )
                self.bar_canvas.create_line(
                    left_threshold, 0, left_threshold, roi_height,
                    fill="#f48771", width=2, dash=(4, 4)
                )
                self.bar_canvas.create_rectangle(
                    right_threshold, 0, roi_width, roi_height,
                    fill="#89d185", stipple="gray50", outline=""
                )
                self.bar_canvas.create_line(
                    right_threshold, 0, right_threshold, roi_height,
                    fill="#4ec9b0", width=2, dash=(4, 4)
                )
            if self.minigame_visuals_enabled and bar_left is not None and bar_right is not None:
                self.bar_canvas.create_rectangle(
                    bar_left, 5, bar_right, roi_height - 5,
                    outline="cyan", width=2
                )
                if bar_center is not None:
                    self.bar_canvas.create_line(
                        bar_center, 5, bar_center, roi_height - 5,
                        fill="cyan", width=2
                    )
            if self.minigame_visuals_enabled and self.prediction_active and self.expected_landing_zone_min is not None and self.expected_landing_zone_max is not None:
                zone_min = max(0, min(roi_width, self.expected_landing_zone_min))
                zone_max = max(0, min(roi_width, self.expected_landing_zone_max))
                self.bar_canvas.create_rectangle(
                    zone_min, 8, zone_max, roi_height - 8,
                    fill="#ffff00", stipple="gray50", outline="#ffff00", width=1
                )
                self.bar_canvas.create_line(
                    zone_min, 5, zone_min, roi_height - 5,
                    fill="#ffff00", width=1, dash=(3, 3)
                )
                self.bar_canvas.create_line(
                    zone_max, 5, zone_max, roi_height - 5,
                    fill="#ffff00", width=1, dash=(3, 3)
                )
            if self.minigame_visuals_enabled and fish_x is not None:
                self.bar_canvas.create_oval(
                    fish_x - 5, 15, fish_x + 5, 25,
                    fill="lime", outline="lime"
                )
            self.bar_canvas.create_line(
                roi_width // 2, 0, roi_width // 2, roi_height,
                fill="gray", width=1, dash=(2, 2)
            )
        except:
            pass

    def get_pixel_pos(self, sct, region, color):
        screenshot = np.array(sct.grab(region))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        if "fish_min" in self.current_profile and "fish_max" in self.current_profile:
            tol = int(self.current_profile.get("tolerance_fish", 0))
            profile_fish_min = self.current_profile["fish_min"]
            profile_fish_max = self.current_profile["fish_max"]
            if np.array_equal(profile_fish_min, np.array([60, 60, 80])) and np.array_equal(profile_fish_max, np.array([80, 90, 105])):
                fish_rgb = FISH_COLOR.astype(np.int16)
                lower_fish_rgb = np.clip(fish_rgb - FISH_TOLERANCE, 0, 255)
                upper_fish_rgb = np.clip(fish_rgb + FISH_TOLERANCE, 0, 255)
                fish_min = lower_fish_rgb[::-1]
                fish_max = upper_fish_rgb[::-1]
            else:
                fish_min = np.clip(profile_fish_min.astype(np.int16) - tol, 0, 255).astype(np.uint8)
                fish_max = np.clip(profile_fish_max.astype(np.int16) + tol, 0, 255).astype(np.uint8)
        else:
            fish_rgb = color.astype(np.int16)
            tolerance = self.current_profile.get("tolerance_fish", 10)
            lower_fish_rgb = np.clip(fish_rgb - tolerance, 0, 255)
            upper_fish_rgb = np.clip(fish_rgb + tolerance, 0, 255)
            fish_min = lower_fish_rgb[::-1]
            fish_max = upper_fish_rgb[::-1]
        mask = cv2.inRange(screenshot, fish_min, fish_max)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
        valid_components = []
        for label in range(1, num_labels):
            area = stats[label, cv2.CC_STAT_AREA]
            x = stats[label, cv2.CC_STAT_LEFT]
            y = stats[label, cv2.CC_STAT_TOP]
            width = stats[label, cv2.CC_STAT_WIDTH]
            height = stats[label, cv2.CC_STAT_HEIGHT]
            if 50 < area < 800:
                aspect_ratio = float(height) / width if width > 0 else 0
                if aspect_ratio > 2.0 and y < region['height'] * 0.7:
                    cx = centroids[label][0]
                    valid_components.append((int(cx), area, aspect_ratio, height))
        if valid_components:
            valid_components.sort(key=lambda c: c[3], reverse=True)
            fish_x = valid_components[0][0]
            if self.last_fish_x is not None:
                if abs(fish_x - self.last_fish_x) > 100:
                    fish_x = self.last_fish_x + np.sign(fish_x - self.last_fish_x) * 40
            if 0 <= fish_x < region['width']:
                self.frames_since_fish_lost = 0
                return fish_x
        if not hasattr(self, 'frames_since_fish_lost'):
            self.frames_since_fish_lost = 0
        self.frames_since_fish_lost += 1
        if self.frames_since_fish_lost < 3 and self.last_fish_x is not None:
            return self.last_fish_x
        return None

    def cast_rod(self):
        self.set_state("Casting")
        print(f"Casting... (holding for {self.cast_duration:.2f}s)")
        pydirectinput.mouseDown()
        time.sleep(self.cast_duration)
        pydirectinput.mouseUp()

    def start(self):
        if self.shake_type == "Key" and self.auto_shake_enabled:
            print(f"Pressing '{self.shake_nav_key}' to enable keyboard navigation...")
            try:
                from pynput.keyboard import Key, Controller
                kb_controller = Controller()
                kb_controller.press(self.shake_nav_key)
                kb_controller.release(self.shake_nav_key)
                print(f"Successfully pressed navigation key: {self.shake_nav_key}")
            except Exception as e:
                print(f"Error pressing navigation key: {e}")
                try:
                    pydirectinput.press(self.shake_nav_key)
                except:
                    print(f"Fallback also failed for key: {self.shake_nav_key}")
            time.sleep(0.2)
        if not self.running:
            return
        if not self.rod_equipped_this_session:
            self.rapid_key_press()
            self.rod_equipped_this_session = True
        if not self.running:
            return
        if self.auto_lower_graphics_enabled and not self.graphics_lowered_this_session:
            self.lower_graphics()
            self.graphics_lowered_this_session = True
        if not self.running:
            return
        if self.auto_blur_enabled and not self.blur_enabled_this_session:
            self.enable_blur()
            self.blur_enabled_this_session = True
        if not self.running:
            return
        if self.auto_camera_mode_enabled and not self.camera_mode_enabled_this_session:
            self.enable_camera_mode()
            self.camera_mode_enabled_this_session = True
        if not self.running:
            return
        self.cast_rod()
        if not self.running:
            return
        self.set_state("Waiting for bite")
        print("Waiting for bite...")
        if self.auto_shake_enabled:
            sct = mss.mss()
            shake_check_duration = 7.0
            shake_check_start = time.time()
            shake_checks = 0
            last_circle_time = time.time()
            minigame_detections = 0
            while time.time() - shake_check_start < shake_check_duration and self.running:
                if not self.running:
                    sct.__exit__(None, None, None)
                    return
                if self.check_minigame_active(sct):
                    minigame_detections += 1
                    if minigame_detections >= 3:
                        print("Bar minigame confirmed! Ending shake detection...")
                        break
                else:
                    minigame_detections = 0
                circle_pos = self.detect_shake_circle(sct)
                shake_checks += 1
                if circle_pos is not None:
                    last_circle_time = time.time()
                    self.set_state("Shaking")
                    if not self.running:
                        sct.__exit__(None, None, None)
                        return
                    self.perform_shake(circle_pos)
                    print(f"Shake minigame detected at position {circle_pos}!")
                    time.sleep(0.05)
                if shake_checks % 40 == 0:
                    elapsed = time.time() - shake_check_start
                    print(f"Waiting for shake... {elapsed:.1f}s elapsed, {shake_checks} checks")
                time.sleep(0.05)
            print(f"Shake check completed. Total checks: {shake_checks}")
            sct.__exit__(None, None, None)
            if not self.running:
                return
            print("Waiting 1s before bar minigame...")
            for _ in range(10):
                if not self.running:
                    return
                time.sleep(0.1)
        else:
            print("Auto-shake disabled, checking for minigame...")
            sct = mss.mss()
            wait_duration = 3.0
            wait_start = time.time()
            while time.time() - wait_start < wait_duration and self.running:
                if not self.running:
                    sct.__exit__(None, None, None)
                    return
                if self.check_minigame_active(sct):
                    print("Minigame detected! Skipping wait...")
                    break
                time.sleep(0.1)
            sct.__exit__(None, None, None)
            if not self.running:
                return
            for _ in range(5):
                if not self.running:
                    return
                time.sleep(0.1)
        if not self.running:
            return
        self.last_detection_time = time.time()
        self.set_state("Playing minigame")
        print("Starting Bar Minigame...")
        self.minigame_loop()

    def setup_overlay(self):
        self.overlay = tk.Tk()
        self.overlay.title("Fisch Macro by Elju")
        self.overlay.attributes('-topmost', True)
        self.overlay.geometry("350x500+10+60")
        self.overlay.configure(bg='#1e1e1e')
        style = ttk.Style(self.overlay)
        style.theme_use('clam')
        style.configure(
            "Dark.TCombobox",
            fieldbackground="#252526",
            background="#252526",
            foreground="#cccccc",
            arrowcolor="#cccccc",
            bordercolor="#3e3e42",
            lightcolor="#3e3e42",
            darkcolor="#3e3e42",
            selectbackground="#007acc",
            selectforeground="#ffffff"
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[('readonly', '#252526'), ('disabled', '#1e1e1e')],
            background=[('readonly', '#252526'), ('disabled', '#1e1e1e')],
            foreground=[('disabled', '#6b6b6b')],
            arrowcolor=[('disabled', '#6b6b6b')]
        )
        self.overlay.option_add('*TCombobox*Listbox.background', '#252526')
        self.overlay.option_add('*TCombobox*Listbox.foreground', '#cccccc')
        self.overlay.option_add('*TCombobox*Listbox.selectBackground', '#007acc')
        self.overlay.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')
        self.overlay.overrideredirect(True)
        self.is_minimized = False
        self.overlay.bind("<Map>", lambda e: self.restore_overlay())
        self.overlay.attributes('-alpha', 1.0)
        def on_enter(event):
            self.last_hover_time = time.time()
            if self.is_transparent:
                self.overlay.attributes('-alpha', 1.0)
                self.is_transparent = False
        def on_leave(event):
            self.last_hover_time = time.time()
        self.overlay.bind('<Enter>', on_enter)
        self.overlay.bind('<Leave>', on_leave)
        self.start_transparency_timer()
        titlebar = tk.Frame(self.overlay, bg='#1e1e1e', height=30)
        titlebar.pack(fill=tk.X, side=tk.TOP)
        title_text = tk.Label(
            titlebar,
            text="Fisch Macro by",
            font=("Segoe UI", 10, "bold"),
            fg="#cccccc",
            bg='#1e1e1e'
        )
        title_text.pack(side=tk.LEFT, padx=(10, 0))
        title_link = tk.Label(
            titlebar,
            text="Elju",
            font=("Segoe UI", 10, "bold", "underline"),
            fg="#cccccc",
            bg='#1e1e1e',
            cursor="hand2"
        )
        title_link.pack(side=tk.LEFT)
        def open_elju_profile(event=None):
            webbrowser.open("https://www.roblox.com/users/58117238/profile")
        def on_link_enter(event):
            title_link.config(fg="#cccccc")
        def on_link_leave(event):
            title_link.config(fg="#cccccc")
        title_link.bind("<Button-1>", open_elju_profile, add="+")
        title_link.bind("<Enter>", on_link_enter)
        title_link.bind("<Leave>", on_link_leave)
        close_btn = tk.Button(
            titlebar,
            text="✕",
            font=("Segoe UI", 12),
            fg="#cccccc",
            bg='#1e1e1e',
            relief=tk.FLAT,
            activebackground='#c72e2e',
            activeforeground='#ffffff',
            command=self.on_closing,
            width=3
        )
        close_btn.pack(side=tk.RIGHT, padx=2)
        def on_close_enter(event):
            close_btn.config(bg='#c72e2e', fg='#ffffff')
        def on_close_leave(event):
            close_btn.config(bg='#1e1e1e', fg='#cccccc')
        close_btn.bind("<Enter>", on_close_enter)
        close_btn.bind("<Leave>", on_close_leave)
        minimize_btn = tk.Button(
            titlebar,
            text="─",
            font=("Segoe UI", 12),
            fg="#cccccc",
            bg='#1e1e1e',
            relief=tk.FLAT,
            activebackground='#3e3e42',
            activeforeground='#ffffff',
            command=self.minimize_overlay,
            width=3
        )
        minimize_btn.pack(side=tk.RIGHT, padx=2)
        def on_minimize_enter(event):
            minimize_btn.config(bg='#3e3e42', fg='#ffffff')
        def on_minimize_leave(event):
            minimize_btn.config(bg='#1e1e1e', fg='#cccccc')
        minimize_btn.bind("<Enter>", on_minimize_enter)
        minimize_btn.bind("<Leave>", on_minimize_leave)
        def start_move(event):
            self.overlay._drag_start_x = event.x
            self.overlay._drag_start_y = event.y
        def stop_move(event):
            self.overlay._drag_start_x = None
            self.overlay._drag_start_y = None
        def do_move(event):
            if hasattr(self.overlay, '_drag_start_x'):
                dx = event.x - self.overlay._drag_start_x
                dy = event.y - self.overlay._drag_start_y
                x = self.overlay.winfo_x() + dx
                y = self.overlay.winfo_y() + dy
                self.overlay.geometry(f"+{x}+{y}")
        titlebar.bind("<Button-1>", start_move)
        titlebar.bind("<ButtonRelease-1>", stop_move)
        titlebar.bind("<B1-Motion>", do_move)
        title_text.bind("<Button-1>", start_move)
        title_text.bind("<ButtonRelease-1>", stop_move)
        title_text.bind("<B1-Motion>", do_move)
        main_container = tk.Frame(self.overlay, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True)
        sidebar = tk.Frame(main_container, bg='#252526', width=120)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        header = tk.Label(
            sidebar,
            text="FISCH MACRO",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg='#252526',
            pady=5
        )
        header.pack()
        version_label = tk.Label(
            sidebar,
            text="v0.8 rev.3",
            font=("Segoe UI", 8, "bold", "italic"),
            fg="#858585",
            bg='#252526'
        )
        version_label.pack(pady=(0, 5))
        self.status_label = tk.Label(
            sidebar,
            text="● STOPPED",
            font=("Segoe UI", 10, "bold"),
            fg="#f48771",
            bg='#252526'
        )
        self.status_label.pack(pady=5)
        sep = tk.Frame(sidebar, bg='#3e3e42', height=1)
        sep.pack(fill=tk.X, pady=15, padx=10)
        self.tab_buttons = {}
        self.current_tab = None
        tabs = [
            ("General", "⚙"),
            ("Control", "🎮"),
            ("Detection", "👁"),
            ("Advanced", "⚡"),
            ("Config", "💾")
        ]
        for tab_name, icon in tabs:
            btn = tk.Button(
                sidebar,
                text=f"  {icon}  {tab_name}",
                font=("Segoe UI", 10),
                fg="#cccccc",
                bg='#252526',
                activebackground='#2d2d30',
                activeforeground="#ffffff",
                relief=tk.FLAT,
                anchor='w',
                padx=10,
                pady=12,
                command=lambda t=tab_name: self.switch_tab(t)
            )
            btn.pack(fill=tk.X)
            self.tab_buttons[tab_name] = btn
        bottom_frame = tk.Frame(sidebar, bg='#252526')
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        info_label = tk.Label(
            bottom_frame,
            text="Press F8 to toggle",
            font=("Segoe UI", 8),
            fg="#858585",
            bg='#252526'
        )
        info_label.pack(pady=5)
        self.toggle_button = tk.Button(
            bottom_frame,
            text="START MACRO",
            command=self.toggle_macro,
            bg="#2e7d32",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            activebackground="#1b5e20",
            pady=8
        )
        self.toggle_button.pack(fill=tk.X, padx=10)
        content_container = tk.Frame(main_container, bg='#1e1e1e')
        content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.content_canvas = tk.Canvas(content_container, bg='#1e1e1e', highlightthickness=0)
        scrollbar_frame = tk.Frame(content_container, bg='#2d2d30', width=12)
        scrollbar_canvas = tk.Canvas(scrollbar_frame, bg='#2d2d30', width=12, highlightthickness=0)
        scrollbar_canvas.pack(fill=tk.BOTH, expand=True)
        self.content_area = tk.Frame(self.content_canvas, bg='#1e1e1e')
        self.scroll_thumb = scrollbar_canvas.create_rectangle(
            2, 0, 10, 50,
            fill='#424242',
            outline='#424242'
        )
        def update_scrollbar(*args):
            first, last = self.content_canvas.yview()
            canvas_height = scrollbar_canvas.winfo_height()
            thumb_height = max(20, int(canvas_height * (last - first)))
            thumb_y = int(canvas_height * first)
            scrollbar_canvas.coords(
                self.scroll_thumb,
                2, thumb_y, 10, thumb_y + thumb_height
            )
        def on_scrollbar_click(event):
            canvas_height = scrollbar_canvas.winfo_height()
            thumb_coords = scrollbar_canvas.coords(self.scroll_thumb)
            thumb_y1, thumb_y2 = thumb_coords[1], thumb_coords[3]
            thumb_height = max(1, thumb_y2 - thumb_y1)
            if thumb_y1 <= event.y <= thumb_y2:
                self.scroll_drag_offset = event.y - thumb_y1
            else:
                self.scroll_drag_offset = thumb_height / 2
            new_top = max(0, min(canvas_height - thumb_height, event.y - self.scroll_drag_offset))
            self.content_canvas.yview_moveto(new_top / canvas_height)
        
        def on_scrollbar_drag(event):
            canvas_height = scrollbar_canvas.winfo_height()
            thumb_coords = scrollbar_canvas.coords(self.scroll_thumb)
            thumb_height = max(1, thumb_coords[3] - thumb_coords[1])
            offset = getattr(self, 'scroll_drag_offset', thumb_height / 2)
            new_top = max(0, min(canvas_height - thumb_height, event.y - offset))
            self.content_canvas.yview_moveto(new_top / canvas_height)
        scrollbar_canvas.bind("<Button-1>", on_scrollbar_click)
        scrollbar_canvas.bind("<B1-Motion>", on_scrollbar_drag)
        def on_scrollbar_enter(event):
            scrollbar_canvas.itemconfig(self.scroll_thumb, fill='#555555', outline='#555555')
        def on_scrollbar_leave(event):
            scrollbar_canvas.itemconfig(self.scroll_thumb, fill='#424242', outline='#424242')
        scrollbar_canvas.bind("<Enter>", on_scrollbar_enter)
        scrollbar_canvas.bind("<Leave>", on_scrollbar_leave)
        self.content_area.bind(
            "<Configure>",
            lambda e: (
                self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")),
                update_scrollbar()
            )
        )
        self.content_canvas.configure(yscrollcommand=lambda *args: (update_scrollbar(), None))
        scrollbar_frame.pack(side="right", fill="y")
        self.content_canvas.pack(side="left", fill="both", expand=True)
        self.content_canvas.create_window((0, 0), window=self.content_area, anchor="nw")
        def _on_mousewheel(event):
            self.content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            update_scrollbar()
        def _bound_to_mousewheel(event):
            self.content_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbound_to_mousewheel(event):
            self.content_canvas.unbind_all("<MouseWheel>")
        self.content_canvas.bind('<Enter>', _bound_to_mousewheel)
        self.content_canvas.bind('<Leave>', _unbound_to_mousewheel)
        def _configure_scroll_region(event):
            self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
            bbox = self.content_canvas.bbox("all")
            if bbox:
                content_height = bbox[3] - bbox[1]
                canvas_height = self.content_canvas.winfo_height()
                if content_height <= canvas_height:
                    self.content_canvas.yview_moveto(0)
            update_scrollbar()
        self.content_area.bind("<Configure>", _configure_scroll_region)
        self.tab_panels = {}
        self.create_general_tab()
        self.create_control_tab()
        self.create_detection_tab()
        self.create_advanced_tab()
        self.create_config_tab()
        self.switch_tab("General")
        self.overlay_thread = threading.Thread(target=self.overlay_loop, daemon=True)
        self.overlay_thread.start()

    def on_closing(self):
        print("Closing application...")
        self.auto_save_latest()
        self.stop_macro()
        self.overlay.destroy()

    def switch_tab(self, tab_name):
        for panel in self.tab_panels.values():
            panel.pack_forget()
        for name, btn in self.tab_buttons.items():
            if name == tab_name:
                btn.configure(bg='#37373d', fg='#ffffff')
            else:
                btn.configure(bg='#252526', fg='#cccccc')
        self.tab_panels[tab_name].pack(fill=tk.BOTH, expand=True)
        self.current_tab = tab_name
        if hasattr(self, 'content_canvas'):
            self.content_canvas.yview_moveto(0)

    def create_general_tab(self):
        panel = tk.Frame(self.content_area, bg='#1e1e1e')
        self.tab_panels["General"] = panel
        title = tk.Label(
            panel,
            text="General",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg='#1e1e1e'
        )
        title.pack(anchor='w', padx=15, pady=(15, 8))
        recast_frame = self.create_section(panel, "Auto Features")
        checkbox_container = tk.Frame(recast_frame, bg='#252526')
        checkbox_container.pack(fill=tk.X, padx=15, pady=6)
        self.auto_recast_var = tk.BooleanVar(value=True)
        auto_recast_check = tk.Checkbutton(
            checkbox_container,
            text="Auto Recast",
            variable=self.auto_recast_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_auto_recast
        )
        auto_recast_check.pack(anchor='w')
        self.auto_shake_var = tk.BooleanVar(value=True)
        auto_shake_check = tk.Checkbutton(
            checkbox_container,
            text="Auto Shake",
            variable=self.auto_shake_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_auto_shake
        )
        auto_shake_check.pack(anchor='w', pady=(4, 0))
        self.auto_lower_graphics_var = tk.BooleanVar(value=True)
        auto_lower_graphics_check = tk.Checkbutton(
            checkbox_container,
            text="Auto Lower Graphics",
            variable=self.auto_lower_graphics_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_auto_lower_graphics
        )
        auto_lower_graphics_check.pack(anchor='w', pady=(4, 0))
        self.auto_camera_mode_var = tk.BooleanVar(value=True)
        auto_camera_mode_check = tk.Checkbutton(
            checkbox_container,
            text="Auto Camera Mode",
            variable=self.auto_camera_mode_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_auto_camera_mode
        )
        auto_camera_mode_check.pack(anchor='w', pady=(4, 0))
        self.auto_blur_var = tk.BooleanVar(value=True)
        auto_blur_check = tk.Checkbutton(
            checkbox_container,
            text="Auto Blur",
            variable=self.auto_blur_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_auto_blur
        )
        auto_blur_check.pack(anchor='w', pady=(4, 0))
        self.auto_cast_var = tk.BooleanVar(value=self.auto_cast_enabled)
        auto_cast_check = tk.Checkbutton(
            checkbox_container,
            text="Auto Cast Delay",
            variable=self.auto_cast_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_auto_cast
        )
        auto_cast_check.pack(anchor='w', pady=(4, 0))
        delay_container = tk.Frame(recast_frame, bg='#252526')
        delay_container.pack(fill=tk.X, padx=15, pady=6)
        delay_top_frame = tk.Frame(delay_container, bg='#252526')
        delay_top_frame.pack(fill=tk.X)
        delay_label = tk.Label(
            delay_top_frame,
            text="Auto Cast Delay",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            anchor='w'
        )
        delay_label.pack(side=tk.LEFT)
        self.auto_cast_delay_value_label = tk.Label(
            delay_top_frame,
            text=f"{self.auto_cast_delay:.1f}s",
            font=("Segoe UI", 8, "bold"),
            fg="#4ec9b0",
            bg='#252526'
        )
        self.auto_cast_delay_value_label.pack(side=tk.RIGHT)
        self.auto_cast_delay_slider = tk.Scale(
            delay_container,
            from_=0.1,
            to=5.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.update_auto_cast_delay,
            bg='#3e3e42',
            fg='#cccccc',
            troughcolor='#2d2d30',
            activebackground='#007acc',
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            showvalue=False
        )
        self.auto_cast_delay_slider.set(self.auto_cast_delay)
        self.auto_cast_delay_slider.pack(fill=tk.X, pady=(4, 0))
        cast_duration_container = tk.Frame(recast_frame, bg='#252526')
        cast_duration_container.pack(fill=tk.X, padx=15, pady=6)
        cast_duration_top_frame = tk.Frame(cast_duration_container, bg='#252526')
        cast_duration_top_frame.pack(fill=tk.X)
        cast_duration_label = tk.Label(
            cast_duration_top_frame,
            text="Cast Duration",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            anchor='w'
        )
        cast_duration_label.pack(side=tk.LEFT)
        self.cast_duration_value_label = tk.Label(
            cast_duration_top_frame,
            text=f"{self.cast_duration:.2f}s",
            font=("Segoe UI", 8, "bold"),
            fg="#4ec9b0",
            bg='#252526'
        )
        self.cast_duration_value_label.pack(side=tk.RIGHT)
        self.cast_duration_slider = tk.Scale(
            cast_duration_container,
            from_=0.1,
            to=2.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            command=self.update_cast_duration,
            bg='#3e3e42',
            fg='#cccccc',
            troughcolor='#2d2d30',
            activebackground='#007acc',
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            showvalue=False
        )
        self.cast_duration_slider.set(self.cast_duration)
        self.cast_duration_slider.pack(fill=tk.X, pady=(4, 0))
        hotkey_frame = self.create_section(panel, "Hotkey Settings")
        hotkey_container = tk.Frame(hotkey_frame, bg='#252526')
        hotkey_container.pack(fill=tk.X, padx=15, pady=6)
        hotkey_label = tk.Label(
            hotkey_container,
            text="Macro Toggle Key",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        hotkey_label.pack(anchor='w', pady=(0, 4))
        self.hotkey_button = tk.Button(
            hotkey_container,
            text=f"Current: {self.toggle_hotkey.upper()}",
            command=self.start_hotkey_binding,
            bg='#3e3e42',
            fg='#cccccc',
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            activebackground='#007acc',
            activeforeground='#ffffff',
            pady=6,
            cursor="hand2"
        )
        self.hotkey_button.pack(fill=tk.X, pady=(0, 4))
        def on_hotkey_btn_enter(event):
            if not self.waiting_for_hotkey:
                self.hotkey_button.config(bg='#4e4e52')
        def on_hotkey_btn_leave(event):
            if not self.waiting_for_hotkey:
                self.hotkey_button.config(bg='#3e3e42')
        self.hotkey_button.bind("<Enter>", on_hotkey_btn_enter)
        self.hotkey_button.bind("<Leave>", on_hotkey_btn_leave)
        self.focus_loss_stop_var = tk.BooleanVar(value=self.focus_loss_stop)
        focus_loss_check = tk.Checkbutton(
            hotkey_container,
            text="Emergency Stop (Focus Loss)",
            variable=self.focus_loss_stop_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_focus_loss_stop
        )
        focus_loss_check.pack(anchor='w', pady=(4, 0))
        custom_ui_frame = self.create_section(panel, "Custom UI Settings")
        custom_ui_container = tk.Frame(custom_ui_frame, bg='#252526')
        custom_ui_container.pack(fill=tk.X, padx=15, pady=6)
        self.rod_custom_ui_var = tk.BooleanVar(value=False)
        rod_custom_ui_check = tk.Checkbutton(
            custom_ui_container,
            text="Rod Custom UI",
            variable=self.rod_custom_ui_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_rod_custom_ui
        )
        rod_custom_ui_check.pack(anchor='w')
        rod_skin_label = tk.Label(
            custom_ui_container,
            text="Rod Skin",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        rod_skin_label.pack(anchor='w', pady=(6, 2))
        rod_skins = [
            "Astraeus Serenade",
            "Axe of Rhoads",
            "Blade of Glorp",
            "Chrysalis",
            "Duskwire",
            "Eardrum",
            "Experimental Rod",
            "Fabulous Rod",
            "Mealstrom",
            "Nates Blade",
            "Nico's Yarncaster",
            "Noctone",
            "Onirifalx",
            "Polaris Serenade",
            "Rainbow Cluster Rod",
            "Requiem",
            "Sanguine Spire",
            "Silly Fun Happy Rod",
            "Sword of Darkness",
            "Thalassar's Ruin",
            "Wingripper"
        ]
        self.rod_skin_var = tk.StringVar(value="")
        self.rod_skin_combo = ttk.Combobox(
            custom_ui_container,
            textvariable=self.rod_skin_var,
            values=rod_skins,
            state='disabled',
            font=("Segoe UI", 8),
            width=25,
            style="Dark.TCombobox"
        )
        self.rod_skin_combo.pack(anchor='w', fill=tk.X, pady=(0, 2))
        self.rod_skin_combo.bind('<<ComboboxSelected>>', self.on_rod_skin_selected)
        self.rod_skin_combo.bind('<MouseWheel>', lambda e: 'break')
        self.rod_skin_combo.bind('<Button-4>', lambda e: 'break')
        self.rod_skin_combo.bind('<Button-5>', lambda e: 'break')
        shake_settings_frame = self.create_section(panel, "Shake Settings")
        shake_container = tk.Frame(shake_settings_frame, bg='#252526')
        shake_container.pack(fill=tk.X, padx=15, pady=6)
        shake_label = tk.Label(
            shake_container,
            text="Shake Type",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        shake_label.pack(anchor='w', pady=(0, 4))
        shake_type_frame = tk.Frame(shake_container, bg='#252526')
        shake_type_frame.pack(fill=tk.X)
        self.shake_type_var = tk.StringVar(value="Mouse")
        mouse_radio = tk.Radiobutton(
            shake_type_frame,
            text="Mouse",
            variable=self.shake_type_var,
            value="Mouse",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.update_shake_type
        )
        mouse_radio.pack(side=tk.LEFT, padx=(0, 10))
        key_radio = tk.Radiobutton(
            shake_type_frame,
            text="Key",
            variable=self.shake_type_var,
            value="Key",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.update_shake_type
        )
        key_radio.pack(side=tk.LEFT)
        nav_key_label = tk.Label(
            shake_container,
            text="Navigation Key",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        nav_key_label.pack(anchor='w', pady=(8, 4))
        self.nav_key_button = tk.Button(
            shake_container,
            text=f"Current: {self.shake_nav_key.upper()}",
            command=self.start_key_binding,
            bg='#3e3e42',
            fg='#cccccc',
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            activebackground='#007acc',
            activeforeground='#ffffff',
            pady=6,
            cursor="hand2"
        )
        self.nav_key_button.pack(fill=tk.X, pady=(0, 4))
        def on_key_btn_enter(event):
            if not self.waiting_for_key:
                self.nav_key_button.config(bg='#4e4e52')
        def on_key_btn_leave(event):
            if not self.waiting_for_key:
                self.nav_key_button.config(bg='#3e3e42')
        self.nav_key_button.bind("<Enter>", on_key_btn_enter)
        self.nav_key_button.bind("<Leave>", on_key_btn_leave)
        control_frame = self.create_section(panel, "Game Settings")
        self.add_control_stat_config(control_frame, "Control Stat", -0.37, 0.7, CONTROL_STAT)
        resilience_frame = self.create_section(panel, "Resilience Settings")
        self.add_resilience_config(resilience_frame, "Rod Resilience (%)", -100, 200, 5, self.rod_resilience * 100, "rod_resilience")
        self.add_resilience_config(resilience_frame, "Bait Resilience (%)", -100, 100, 5, self.bait_resilience * 100, "bait_resilience")
        onirifalx_container = tk.Frame(resilience_frame, bg='#252526')
        onirifalx_container.pack(fill=tk.X, padx=15, pady=(0, 6))
        self.onirifalx_resilience_var = tk.BooleanVar(value=self.onirifalx_resilience_enabled)
        onirifalx_check = tk.Checkbutton(
            onirifalx_container,
            text="Onirifalx Toggle",
            variable=self.onirifalx_resilience_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_onirifalx_resilience
        )
        onirifalx_check.pack(anchor='w')

    def create_control_tab(self):
        panel = tk.Frame(self.content_area, bg='#1e1e1e')
        self.tab_panels["Control"] = panel
        title = tk.Label(
            panel,
            text="Control",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg='#1e1e1e'
        )
        title.pack(anchor='w', padx=15, pady=(15, 8))
        distance_frame = self.create_section(panel, "Distance Thresholds (pixels)")
        self.add_slider_config(distance_frame, "Critical", 5, 40, 1, self.control_params['critical_distance'], self.update_critical_distance, "critical_distance")
        self.add_slider_config(distance_frame, "Close", 20, 80, 5, self.control_params['close_distance'], self.update_close_distance, "close_distance")
        self.add_slider_config(distance_frame, "Moderate", 40, 160, 10, self.control_params['moderate_distance'], self.update_moderate_distance, "moderate_distance")
        self.add_slider_config(distance_frame, "Far", 80, 240, 10, self.control_params['far_distance'], self.update_far_distance, "far_distance")
        left_frame = self.create_section(panel, "Left Movement (Release)")
        self.add_slider_config(left_frame, "Critical Decel", 50, 1000, 10, self.control_params['left_critical_decel'], self.update_left_critical_decel, "left_critical_decel")
        self.add_slider_config(left_frame, "Close Decel", 50, 1000, 10, self.control_params['left_close_decel'], self.update_left_close_decel, "left_close_decel")
        self.add_slider_config(left_frame, "Moderate Decel", 50, 1500, 10, self.control_params['left_moderate_decel'], self.update_left_moderate_decel, "left_moderate_decel")
        self.add_slider_config(left_frame, "Far Decel", 50, 2000, 10, self.control_params['left_far_decel'], self.update_left_far_decel, "left_far_decel")
        right_frame = self.create_section(panel, "Right Movement (Hold)")
        self.add_slider_config(right_frame, "Critical Decel", 50, 1000, 10, self.control_params['right_critical_decel'], self.update_right_critical_decel, "right_critical_decel")
        self.add_slider_config(right_frame, "Close Decel", 50, 1000, 10, self.control_params['right_close_decel'], self.update_right_close_decel, "right_close_decel")
        self.add_slider_config(right_frame, "Moderate Decel", 50, 1500, 10, self.control_params['right_moderate_decel'], self.update_right_moderate_decel, "right_moderate_decel")
        self.add_slider_config(right_frame, "Far Decel", 50, 2000, 10, self.control_params['right_far_decel'], self.update_right_far_decel, "right_far_decel")
        side_frame = self.create_section(panel, "Side Hold Zones")
        side_help = tk.Label(
            side_frame,
            text="Set distance from edges to trigger hold/release",
            font=("Segoe UI", 7, "italic"),
            fg="#858585",
            bg='#252526'
        )
        side_help.pack(anchor='w', padx=15, pady=(0, 6))
        self.add_slider_config(side_frame, "% From Left Edge", 5, 50, 1, self.side_hold_left_pct, self.update_side_hold_left, "side_hold_left")
        self.add_slider_config(side_frame, "% From Right Edge", 5, 50, 1, self.side_hold_right_pct, self.update_side_hold_right, "side_hold_right")
        pid_frame = self.create_section(panel, "PID Tuning")
        pid_help = tk.Label(
            pid_frame,
            text="Kp = aggressiveness.\nKd = damping.\nPrediction = look-ahead time",
            font=("Segoe UI", 7, "italic"),
            fg="#858585",
            bg='#252526',
            justify='left',
            anchor='w'
        )
        pid_help.pack(anchor='w', padx=15, pady=(0, 6))
        self.add_slider_config(pid_frame, "PID Kp", 0.1, 2.0, 0.05, self.pid_kp, self.update_pid_kp, "pid_kp")
        self.add_slider_config(pid_frame, "PID Kd", 0.05, 1.0, 0.05, self.pid_kd, self.update_pid_kd, "pid_kd")
        self.add_slider_config(pid_frame, "Prediction Time (s)", 0.01, 0.2, 0.01, self.prediction_time, self.update_prediction_time, "prediction_time")
        scaling_frame = self.create_section(panel, "Control Scaling")
        scaling_help = tk.Label(
            scaling_frame,
            text="Control To Pixels = bar width scaling.\nMax Bar Width = detection cap.",
            font=("Segoe UI", 7, "italic"),
            fg="#858585",
            bg='#252526',
            justify='left',
            anchor='w'
        )
        scaling_help.pack(anchor='w', padx=15, pady=(0, 6))
        self.add_slider_config(scaling_frame, "Control To Pixels", 1000, 6000, 100, self.control_to_pixels, self.update_control_to_pixels, "control_to_pixels")
        self.add_slider_config(scaling_frame, "Max Bar Width (%)", 30, 90, 1, self.max_bar_width_pct * 100, self.update_max_bar_width_pct, "max_bar_width_pct")
        if not hasattr(self, 'left_critical_decel_slider'):
            self.left_critical_decel_slider = None
            self.left_close_decel_slider = None
            self.left_moderate_decel_slider = None
            self.left_far_decel_slider = None
            self.right_critical_decel_slider = None
            self.right_close_decel_slider = None
            self.right_moderate_decel_slider = None
            self.right_far_decel_slider = None
        stab_frame = self.create_section(panel, "Stabilization")
        self.add_slider_config(stab_frame, "Zone Size (%)", 1, 20, 1, 6, self.update_stabilization_zone, "stabilization_zone")

    def create_detection_tab(self):
        panel = tk.Frame(self.content_area, bg='#1e1e1e')
        self.tab_panels["Detection"] = panel
        title = tk.Label(
            panel,
            text="Detection",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg='#1e1e1e'
        )
        title.pack(anchor='w', padx=15, pady=(15, 8))
        vel_frame = self.create_section(panel, "Velocity & Acceleration")
        vel_help = tk.Label(
            vel_frame,
            text="Max Bar Vel = cap on bar speed.\nFish Accel = jump detection sensitivity.\nStabil Vel = velocity cutoff for stabilization.",
            font=("Segoe UI", 7, "italic"),
            fg="#858585",
            bg='#252526',
            justify='left',
            anchor='w'
        )
        vel_help.pack(anchor='w', padx=15, pady=(0, 6))
        self.add_slider_config(vel_frame, "Max Bar Vel (px/s)", 100, 1000, 50, 500, self.update_max_velocity, "max_velocity")
        self.add_slider_config(vel_frame, "Fish Accel (px/s²)", 100, 2000, 100, 500, self.update_accel_threshold, "accel_threshold")
        self.add_slider_config(vel_frame, "Stabil Vel (px/s)", 5, 50, 5, 20, self.update_fish_velocity_threshold, "fish_velocity_threshold")
        bar_loss_frame = self.create_section(panel, "Bar Loss Tolerance")
        self.add_slider_config(bar_loss_frame, "Max Frames Lost", 1, 20, 1, self.max_frames_lost, self.update_max_frames_lost, "max_frames_lost")
        tol_frame = self.create_section(panel, "Detection Tolerances")
        self.add_slider_config(tol_frame, "Generic Tolerance", 0, 30, 1, self.tolerance, self.update_tolerance, "tolerance")
        self.add_slider_config(tol_frame, "White Bar Tolerance", 0, 30, 1, self.white_bar_tolerance, self.update_white_bar_tolerance, "white_bar_tolerance")
        self.add_slider_config(tol_frame, "Miss Bar Tolerance", 0, 60, 1, self.miss_bar_tolerance, self.update_miss_bar_tolerance, "miss_bar_tolerance")
        self.add_slider_config(tol_frame, "Fish Tolerance", 0, 30, 1, self.fish_tolerance, self.update_fish_tolerance, "fish_tolerance")
        shake_frame = self.create_section(panel, "Shake Detection")
        self.add_slider_config(shake_frame, "White Threshold", 150, 255, 1, self.shake_white_threshold, self.update_shake_white_threshold, "shake_white_threshold")
        self.add_slider_config(shake_frame, "Area Min", 500, 10000, 100, self.shake_area_min, self.update_shake_area_min, "shake_area_min")
        self.add_slider_config(shake_frame, "Area Max", 5000, 50000, 500, self.shake_area_max, self.update_shake_area_max, "shake_area_max")
        self.add_slider_config(shake_frame, "Aspect Min", 0.5, 1.5, 0.05, self.shake_aspect_min, self.update_shake_aspect_min, "shake_aspect_min")
        self.add_slider_config(shake_frame, "Aspect Max", 0.5, 1.5, 0.05, self.shake_aspect_max, self.update_shake_aspect_max, "shake_aspect_max")
        self.add_slider_config(shake_frame, "Solidity Min", 0.5, 1.0, 0.01, self.shake_solidity_min, self.update_shake_solidity_min, "shake_solidity_min")
        shake_roi_frame = self.create_section(panel, "Shake ROI")
        self.add_slider_config(shake_roi_frame, "Top %", 0.05, 0.3, 0.01, self.shake_roi_top_pct, self.update_shake_roi_top, "shake_roi_top_pct")
        self.add_slider_config(shake_roi_frame, "Left %", 0.05, 0.3, 0.01, self.shake_roi_left_pct, self.update_shake_roi_left, "shake_roi_left_pct")
        self.add_slider_config(shake_roi_frame, "Width %", 0.5, 0.9, 0.01, self.shake_roi_width_pct, self.update_shake_roi_width, "shake_roi_width_pct")
        self.add_slider_config(shake_roi_frame, "Height %", 0.5, 0.9, 0.01, self.shake_roi_height_pct, self.update_shake_roi_height, "shake_roi_height_pct")

    def create_advanced_tab(self):
        panel = tk.Frame(self.content_area, bg='#1e1e1e')
        self.tab_panels["Advanced"] = panel
        title = tk.Label(
            panel,
            text="Advanced",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg='#1e1e1e'
        )
        title.pack(anchor='w', padx=15, pady=(15, 8))
        debug_frame = self.create_section(panel, "Info Settings")
        debug_checkbox_container = tk.Frame(debug_frame, bg='#252526')
        debug_checkbox_container.pack(fill=tk.X, padx=15, pady=6)
        self.debug_display_var = tk.BooleanVar(value=False)
        debug_display_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Minigame Overlay",
            variable=self.debug_display_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_debug_display
        )
        debug_display_check.pack(anchor='w')
        self.state_display_var = tk.BooleanVar(value=True)
        state_display_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show State Overlay",
            variable=self.state_display_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_state_display
        )
        state_display_check.pack(anchor='w', pady=(4, 0))
        self.resilience_display_var = tk.BooleanVar(value=False)
        resilience_display_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Resilience Overlay",
            variable=self.resilience_display_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_resilience_display
        )
        resilience_display_check.pack(anchor='w', pady=(4, 0))
        self.performance_display_var = tk.BooleanVar(value=False)
        performance_display_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Performance Metrics",
            variable=self.performance_display_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_performance_display
        )
        performance_display_check.pack(anchor='w', pady=(4, 0))
        self.active_time_display_var = tk.BooleanVar(value=self.active_time_display_enabled)
        active_time_display_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Active Time",
            variable=self.active_time_display_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_active_time_display
        )
        active_time_display_check.pack(anchor='w', pady=(4, 0))
        self.side_hold_visuals_var = tk.BooleanVar(value=False)
        side_hold_visuals_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Side Hold Visuals",
            variable=self.side_hold_visuals_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_side_hold_visuals
        )
        side_hold_visuals_check.pack(anchor='w', pady=(4, 0))
        self.minigame_visuals_var = tk.BooleanVar(value=True)
        minigame_visuals_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Minigame Visualisation",
            variable=self.minigame_visuals_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_minigame_visuals
        )
        minigame_visuals_check.pack(anchor='w', pady=(4, 0))
        visual_debug_label = tk.Label(
            debug_checkbox_container,
            text="Visual Debug Overlay",
            font=("Segoe UI", 8, "bold"),
            fg="#cccccc",
            bg='#252526'
        )
        visual_debug_label.pack(anchor='w', pady=(10, 2))
        self.visual_debug_var = tk.BooleanVar(value=self.visual_debug_enabled)
        visual_debug_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Enable Visual Debug",
            variable=self.visual_debug_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_overlay
        )
        visual_debug_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_raw_var = tk.BooleanVar(value=self.visual_debug_show_raw)
        visual_debug_raw_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Raw ROI",
            variable=self.visual_debug_raw_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_raw
        )
        visual_debug_raw_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_bar_mask_var = tk.BooleanVar(value=self.visual_debug_show_bar_mask)
        visual_debug_bar_mask_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Bar Mask",
            variable=self.visual_debug_bar_mask_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_bar_mask
        )
        visual_debug_bar_mask_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_fish_mask_var = tk.BooleanVar(value=self.visual_debug_show_fish_mask)
        visual_debug_fish_mask_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Fish Mask",
            variable=self.visual_debug_fish_mask_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_fish_mask
        )
        visual_debug_fish_mask_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_white_mask_var = tk.BooleanVar(value=self.visual_debug_show_white_mask)
        visual_debug_white_mask_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show White Mask",
            variable=self.visual_debug_white_mask_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_white_mask
        )
        visual_debug_white_mask_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_dark_mask_var = tk.BooleanVar(value=self.visual_debug_show_dark_mask)
        visual_debug_dark_mask_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Dark Mask",
            variable=self.visual_debug_dark_mask_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_dark_mask
        )
        visual_debug_dark_mask_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_contours_var = tk.BooleanVar(value=self.visual_debug_show_contours)
        visual_debug_contours_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Contours",
            variable=self.visual_debug_contours_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_contours
        )
        visual_debug_contours_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_bar_box_var = tk.BooleanVar(value=self.visual_debug_show_bar_box)
        visual_debug_bar_box_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Bar Box",
            variable=self.visual_debug_bar_box_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_bar_box
        )
        visual_debug_bar_box_check.pack(anchor='w', pady=(2, 0))
        self.visual_debug_fish_pos_var = tk.BooleanVar(value=self.visual_debug_show_fish_pos)
        visual_debug_fish_pos_check = tk.Checkbutton(
            debug_checkbox_container,
            text="Show Fish Position",
            variable=self.visual_debug_fish_pos_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_visual_debug_fish_pos
        )
        visual_debug_fish_pos_check.pack(anchor='w', pady=(2, 0))
        transparency_frame = self.create_section(panel, "UI Transparency")
        transparency_container = tk.Frame(transparency_frame, bg='#252526')
        transparency_container.pack(fill=tk.X, padx=15, pady=6)
        self.transparency_enabled_var = tk.BooleanVar(value=self.transparency_enabled)
        transparency_toggle = tk.Checkbutton(
            transparency_container,
            text="Enable Window Transparency",
            variable=self.transparency_enabled_var,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            activebackground='#252526',
            activeforeground='#cccccc',
            selectcolor='#3e3e42',
            command=self.toggle_transparency_enabled
        )
        transparency_toggle.pack(anchor='w', pady=(0, 6))
        self.add_slider_config(transparency_frame, "Transparency Timeout (s)", 1, 20, 1, self.transparency_delay, self.update_transparency_delay, "transparency_delay")
        profiles_frame = self.create_section(panel, "Skin Profiles")
        profiles_container = tk.Frame(profiles_frame, bg='#252526')
        profiles_container.pack(fill=tk.X, padx=15, pady=6)
        profile_label = tk.Label(
            profiles_container,
            text="Profile",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        profile_label.pack(anchor='w', pady=(0, 4))
        self.skin_profile_var = tk.StringVar(value="Default")
        self.skin_profile_combo = ttk.Combobox(
            profiles_container,
            textvariable=self.skin_profile_var,
            values=list(SKIN_PROFILES.keys()),
            state='readonly',
            font=("Segoe UI", 8),
            style="Dark.TCombobox"
        )
        self.skin_profile_combo.pack(anchor='w', fill=tk.X, pady=(0, 6))
        self.skin_profile_combo.bind('<<ComboboxSelected>>', self.on_skin_profile_selected)
        self.profile_bar_min_entry = self._create_color_entry(profiles_container, "Bar Min (B,G,R)")
        self.profile_bar_max_entry = self._create_color_entry(profiles_container, "Bar Max (B,G,R)")
        self.profile_fish_min_entry = self._create_color_entry(profiles_container, "Fish Min (B,G,R)")
        self.profile_fish_max_entry = self._create_color_entry(profiles_container, "Fish Max (B,G,R)")
        apply_btn = tk.Button(
            profiles_container,
            text="Apply Profile",
            command=self.apply_skin_profile,
            bg="#4ec9b0",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            activebackground="#3da88a",
            pady=6
        )
        apply_btn.pack(fill=tk.X, pady=(6, 0))
        self.load_skin_profile_fields("Default")

    def create_config_tab(self):
        panel = tk.Frame(self.content_area, bg='#1e1e1e')
        self.tab_panels["Config"] = panel
        title = tk.Label(
            panel,
            text="Configuration",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg='#1e1e1e'
        )
        title.pack(anchor='w', padx=15, pady=(15, 8))
        save_frame = self.create_section(panel, "Save Configuration")
        save_container = tk.Frame(save_frame, bg='#252526')
        save_container.pack(fill=tk.X, padx=15, pady=6)
        save_label = tk.Label(
            save_container,
            text="Config Name:",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        save_label.pack(anchor='w', pady=(0, 4))
        self.save_config_var = tk.StringVar()
        self.save_combo = ttk.Combobox(
            save_container,
            textvariable=self.save_config_var,
            font=("Segoe UI", 9),
            state='normal',
            style="Dark.TCombobox"
        )
        self.save_combo.pack(fill=tk.X, pady=(0, 8))
        save_btn = tk.Button(
            save_container,
            text="Save Config",
            command=self.save_config,
            bg="#007acc",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            activebackground="#005a9e",
            pady=6
        )
        save_btn.pack(fill=tk.X)
        load_frame = self.create_section(panel, "Load Configuration")
        load_container = tk.Frame(load_frame, bg='#252526')
        load_container.pack(fill=tk.X, padx=15, pady=6)
        load_label = tk.Label(
            load_container,
            text="Select Config:",
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        load_label.pack(anchor='w', pady=(0, 4))
        self.load_config_var = tk.StringVar()
        self.load_combo = ttk.Combobox(
            load_container,
            textvariable=self.load_config_var,
            font=("Segoe UI", 9),
            state='readonly',
            style="Dark.TCombobox"
        )
        self.load_combo.pack(fill=tk.X, pady=(0, 8))
        self.load_combo.bind('<<ComboboxSelected>>', lambda e: self.update_config_list())
        load_btn = tk.Button(
            load_container,
            text="Load Config",
            command=self.load_config,
            bg="#4ec9b0",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            activebackground="#3da88a",
            pady=6
        )
        load_btn.pack(fill=tk.X, pady=(0, 4))
        delete_btn = tk.Button(
            load_container,
            text="Delete Config",
            command=self.delete_config,
            bg="#c72e2e",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            activebackground="#a82424",
            pady=6
        )
        delete_btn.pack(fill=tk.X)
        self.config_status_label = tk.Label(
            panel,
            text="",
            font=("Segoe UI", 7),
            fg="#858585",
            bg='#1e1e1e'
        )
        self.config_status_label.pack(anchor='w', padx=15, pady=(8, 0))
        self.update_config_list()

    def auto_load_latest_delayed(self):
        latest_path = self.config_dir / "latest.ini"
        if latest_path.exists():
            print("Auto-loading latest.ini...")
            self.load_config_var.set("latest")
            self.load_config()
        else:
            print("No latest.ini found, using default settings")

    def auto_load_latest(self):
        latest_path = self.config_dir / "latest.ini"
        if latest_path.exists():
            print("Auto-loading latest.ini...")
            self.load_config_from_path(latest_path)
        else:
            print("No latest.ini found, using default settings")

    def auto_save_latest(self):
        print("Auto-saving to latest.ini...")
        self.save_config_to_path(self.config_dir / "latest.ini")

    def save_config_to_path(self, config_path):
        config = configparser.ConfigParser()
        config['AutoFeatures'] = {
            'auto_recast': str(self.auto_recast_enabled),
            'auto_shake': str(self.auto_shake_enabled),
            'auto_lower_graphics': str(self.auto_lower_graphics_enabled),
            'auto_camera_mode': str(self.auto_camera_mode_enabled),
            'auto_blur': str(self.auto_blur_enabled),
            'auto_cast_enabled': str(self.auto_cast_enabled),
            'auto_cast_delay': str(self.auto_cast_delay),
            'cast_duration': str(self.cast_duration)
        }
        config['ShakeSettings'] = {
            'shake_type': self.shake_type,
            'nav_key': self.shake_nav_key
        }
        config['HotkeySettings'] = {
            'toggle_hotkey': self.toggle_hotkey,
            'focus_loss_stop': str(self.focus_loss_stop)
        }
        try:
            control_value = self.current_control_stat
        except:
            control_value = CONTROL_STAT
        if hasattr(self, 'onirifalx_resilience_var'):
            self.onirifalx_resilience_enabled = self.onirifalx_resilience_var.get()
        config['GameSettings'] = {
            'control_stat': str(control_value),
            'rod_resilience': str(self.rod_resilience),
            'bait_resilience': str(self.bait_resilience),
            'onirifalx_resilience': str(self.onirifalx_resilience_enabled)
        }
        config['PIDTuning'] = {
            'pid_kp': str(self.pid_kp),
            'pid_kd': str(self.pid_kd),
            'prediction_time': str(self.prediction_time)
        }
        config['DetectionTolerances'] = {
            'tolerance': str(self.tolerance),
            'white_bar_tolerance': str(self.white_bar_tolerance),
            'miss_bar_tolerance': str(self.miss_bar_tolerance),
            'fish_tolerance': str(self.fish_tolerance),
            'max_frames_lost': str(self.max_frames_lost)
        }
        config['ShakeDetection'] = {
            'white_threshold': str(self.shake_white_threshold),
            'area_min': str(self.shake_area_min),
            'area_max': str(self.shake_area_max),
            'aspect_min': str(self.shake_aspect_min),
            'aspect_max': str(self.shake_aspect_max),
            'solidity_min': str(self.shake_solidity_min)
        }
        config['ShakeROI'] = {
            'top_pct': str(self.shake_roi_top_pct),
            'left_pct': str(self.shake_roi_left_pct),
            'width_pct': str(self.shake_roi_width_pct),
            'height_pct': str(self.shake_roi_height_pct)
        }
        config['ControlScaling'] = {
            'control_to_pixels': str(self.control_to_pixels),
            'max_bar_width_pct': str(self.max_bar_width_pct)
        }
        config['DistanceVelocityControl'] = {
            'critical_distance': str(self.control_params['critical_distance']),
            'close_distance': str(self.control_params['close_distance']),
            'moderate_distance': str(self.control_params['moderate_distance']),
            'far_distance': str(self.control_params['far_distance']),
            'critical_decel': str(self.control_params['critical_decel']),
            'close_decel': str(self.control_params['close_decel']),
            'moderate_decel': str(self.control_params['moderate_decel']),
            'far_decel': str(self.control_params['far_decel']),
            'left_critical_decel': str(self.control_params['left_critical_decel']),
            'left_close_decel': str(self.control_params['left_close_decel']),
            'left_moderate_decel': str(self.control_params['left_moderate_decel']),
            'left_far_decel': str(self.control_params['left_far_decel']),
            'right_critical_decel': str(self.control_params['right_critical_decel']),
            'right_close_decel': str(self.control_params['right_close_decel']),
            'right_moderate_decel': str(self.control_params['right_moderate_decel']),
            'right_far_decel': str(self.control_params['right_far_decel']),
        }
        try:
            left_pct = float(self.side_hold_left_slider.get())
        except Exception:
            left_pct = self.side_hold_left_pct
        try:
            right_pct = float(self.side_hold_right_slider.get())
        except Exception:
            right_pct = self.side_hold_right_pct
        config['SideHoldZones'] = {
            'left_pct': str(left_pct),
            'right_pct': str(right_pct)
        }
        config['Detection'] = {
            'max_bar_speed': str(self.max_bar_speed),
            'accel_threshold': str(self.accel_threshold),
            'fish_velocity_threshold': str(self.fish_velocity_threshold)
        }
        config['Advanced'] = {
            'stabilization_zone_pct': str(self.stabilization_zone_pct),
            'debug_display': str(self.debug_display_enabled),
            'state_display': str(self.state_display_enabled),
            'resilience_display': str(self.resilience_display_enabled),
            'performance_display': str(self.performance_display_enabled),
            'active_time_display': str(self.active_time_display_enabled),
            'visual_debug_enabled': str(self.visual_debug_enabled),
            'visual_debug_show_raw': str(self.visual_debug_show_raw),
            'visual_debug_show_bar_mask': str(self.visual_debug_show_bar_mask),
            'visual_debug_show_fish_mask': str(self.visual_debug_show_fish_mask),
            'visual_debug_show_white_mask': str(self.visual_debug_show_white_mask),
            'visual_debug_show_dark_mask': str(self.visual_debug_show_dark_mask),
            'visual_debug_show_contours': str(self.visual_debug_show_contours),
            'visual_debug_show_bar_box': str(self.visual_debug_show_bar_box),
            'visual_debug_show_fish_pos': str(self.visual_debug_show_fish_pos),
            'side_hold_visuals': str(self.side_hold_visuals_enabled),
            'minigame_visuals': str(self.minigame_visuals_enabled)
        }
        config['AdvancedUI'] = {
            'transparency_delay': str(self.transparency_delay),
            'transparency_enabled': str(self.transparency_enabled)
        }
        config['SkinProfiles'] = {}
        for profile_name, profile in SKIN_PROFILES.items():
            for key in ('bar_min', 'bar_max', 'fish_min', 'fish_max'):
                if key in profile:
                    val = profile[key]
                    config['SkinProfiles'][f"{profile_name}_{key}"] = f"{val[0]},{val[1]},{val[2]}"
        config['CustomUI'] = {
            'rod_custom_ui_enabled': str(self.rod_custom_ui_enabled),
            'rod_skin_selection': str(self.rod_skin_selection)
        }
        try:
            with open(config_path, 'w') as f:
                config.write(f)
            print(f"Config saved to {config_path}")
        except Exception as e:
            print(f"Error saving config: {e}")

    def load_config_from_path(self, config_path):
        if not config_path.exists():
            return False
        config = configparser.ConfigParser()
        try:
            config.read(config_path)
            if 'AutoFeatures' in config:
                self.auto_recast_enabled = config.getboolean('AutoFeatures', 'auto_recast', fallback=True)
                self.auto_shake_enabled = config.getboolean('AutoFeatures', 'auto_shake', fallback=True)
                self.auto_lower_graphics_enabled = config.getboolean('AutoFeatures', 'auto_lower_graphics', fallback=True)
                self.auto_camera_mode_enabled = config.getboolean('AutoFeatures', 'auto_camera_mode', fallback=True)
                self.auto_blur_enabled = config.getboolean('AutoFeatures', 'auto_blur', fallback=True)
                self.auto_cast_enabled = config.getboolean('AutoFeatures', 'auto_cast_enabled', fallback=False)
                self.auto_cast_delay = config.getfloat('AutoFeatures', 'auto_cast_delay', fallback=1.0)
                self.cast_duration = config.getfloat('AutoFeatures', 'cast_duration', fallback=0.6)
            if 'ShakeSettings' in config:
                self.shake_type = config.get('ShakeSettings', 'shake_type', fallback='Mouse')
                self.shake_nav_key = config.get('ShakeSettings', 'nav_key', fallback="'")
            if 'HotkeySettings' in config:
                self.toggle_hotkey = config.get('HotkeySettings', 'toggle_hotkey', fallback='f8')
                self.focus_loss_stop = config.getboolean('HotkeySettings', 'focus_loss_stop', fallback=True)
            if 'GameSettings' in config:
                control_stat = config.getfloat('GameSettings', 'control_stat', fallback=0.1)
                control_stat = max(-0.37, min(0.7, control_stat))
                self.current_control_stat = control_stat
                bar_width_pct = 30 + (control_stat * 100)
                roi_width = 883
                self.expected_bar_width = int((bar_width_pct / 100) * roi_width)
                self.rod_resilience = config.getfloat('GameSettings', 'rod_resilience', fallback=0.20)
                self.bait_resilience = config.getfloat('GameSettings', 'bait_resilience', fallback=-0.15)
                self.effective_resilience = max(0.20, self.rod_resilience + self.bait_resilience)
                self.onirifalx_resilience_enabled = config.getboolean('GameSettings', 'onirifalx_resilience', fallback=False)
            if 'PIDTuning' in config:
                self.pid_kp = config.getfloat('PIDTuning', 'pid_kp', fallback=self.pid_kp)
                self.pid_kd = config.getfloat('PIDTuning', 'pid_kd', fallback=self.pid_kd)
                self.prediction_time = config.getfloat('PIDTuning', 'prediction_time', fallback=self.prediction_time)
            if 'DetectionTolerances' in config:
                self.tolerance = config.getint('DetectionTolerances', 'tolerance', fallback=self.tolerance)
                self.white_bar_tolerance = config.getint('DetectionTolerances', 'white_bar_tolerance', fallback=self.white_bar_tolerance)
                self.miss_bar_tolerance = config.getint('DetectionTolerances', 'miss_bar_tolerance', fallback=self.miss_bar_tolerance)
                self.fish_tolerance = config.getint('DetectionTolerances', 'fish_tolerance', fallback=self.fish_tolerance)
                self.max_frames_lost = config.getint('DetectionTolerances', 'max_frames_lost', fallback=self.max_frames_lost)
            if 'ShakeDetection' in config:
                self.shake_white_threshold = config.getint('ShakeDetection', 'white_threshold', fallback=self.shake_white_threshold)
                self.shake_area_min = config.getint('ShakeDetection', 'area_min', fallback=self.shake_area_min)
                self.shake_area_max = config.getint('ShakeDetection', 'area_max', fallback=self.shake_area_max)
                self.shake_aspect_min = config.getfloat('ShakeDetection', 'aspect_min', fallback=self.shake_aspect_min)
                self.shake_aspect_max = config.getfloat('ShakeDetection', 'aspect_max', fallback=self.shake_aspect_max)
                self.shake_solidity_min = config.getfloat('ShakeDetection', 'solidity_min', fallback=self.shake_solidity_min)
            if 'ShakeROI' in config:
                self.shake_roi_top_pct = config.getfloat('ShakeROI', 'top_pct', fallback=self.shake_roi_top_pct)
                self.shake_roi_left_pct = config.getfloat('ShakeROI', 'left_pct', fallback=self.shake_roi_left_pct)
                self.shake_roi_width_pct = config.getfloat('ShakeROI', 'width_pct', fallback=self.shake_roi_width_pct)
                self.shake_roi_height_pct = config.getfloat('ShakeROI', 'height_pct', fallback=self.shake_roi_height_pct)
            if 'ControlScaling' in config:
                self.control_to_pixels = config.getfloat('ControlScaling', 'control_to_pixels', fallback=self.control_to_pixels)
                self.max_bar_width_pct = config.getfloat('ControlScaling', 'max_bar_width_pct', fallback=self.max_bar_width_pct)
            if 'AdvancedUI' in config:
                self.transparency_delay = config.getfloat('AdvancedUI', 'transparency_delay', fallback=self.transparency_delay)
                self.transparency_enabled = config.getboolean('AdvancedUI', 'transparency_enabled', fallback=self.transparency_enabled)
            if 'SkinProfiles' in config:
                for profile_name in SKIN_PROFILES.keys():
                    for key in ('bar_min', 'bar_max', 'fish_min', 'fish_max'):
                        cfg_key = f"{profile_name}_{key}"
                        if cfg_key in config['SkinProfiles']:
                            parts = [p.strip() for p in config['SkinProfiles'][cfg_key].split(',')]
                            if len(parts) == 3:
                                try:
                                    SKIN_PROFILES[profile_name][key] = np.array([int(parts[0]), int(parts[1]), int(parts[2])])
                                except ValueError:
                                    pass
            if 'DistanceVelocityControl' in config:
                self.control_params['critical_distance'] = int(round(config.getfloat('DistanceVelocityControl', 'critical_distance', fallback=12)))
                self.control_params['close_distance'] = int(round(config.getfloat('DistanceVelocityControl', 'close_distance', fallback=35)))
                self.control_params['moderate_distance'] = int(round(config.getfloat('DistanceVelocityControl', 'moderate_distance', fallback=80)))
                self.control_params['far_distance'] = int(round(config.getfloat('DistanceVelocityControl', 'far_distance', fallback=150)))
                self.control_params['critical_decel'] = config.getfloat('DistanceVelocityControl', 'critical_decel', fallback=140)
                self.control_params['close_decel'] = config.getfloat('DistanceVelocityControl', 'close_decel', fallback=240)
                self.control_params['moderate_decel'] = config.getfloat('DistanceVelocityControl', 'moderate_decel', fallback=360)
                self.control_params['far_decel'] = config.getfloat('DistanceVelocityControl', 'far_decel', fallback=520)
                self.control_params['left_critical_decel'] = config.getfloat('DistanceVelocityControl', 'left_critical_decel', fallback=140)
                self.control_params['left_close_decel'] = config.getfloat('DistanceVelocityControl', 'left_close_decel', fallback=240)
                self.control_params['left_moderate_decel'] = config.getfloat('DistanceVelocityControl', 'left_moderate_decel', fallback=360)
                self.control_params['left_far_decel'] = config.getfloat('DistanceVelocityControl', 'left_far_decel', fallback=520)
                self.control_params['right_critical_decel'] = config.getfloat('DistanceVelocityControl', 'right_critical_decel', fallback=140)
                self.control_params['right_close_decel'] = config.getfloat('DistanceVelocityControl', 'right_close_decel', fallback=240)
                self.control_params['right_moderate_decel'] = config.getfloat('DistanceVelocityControl', 'right_moderate_decel', fallback=360)
                self.control_params['right_far_decel'] = config.getfloat('DistanceVelocityControl', 'right_far_decel', fallback=520)
            if 'SideHoldZones' in config:
                self.side_hold_left_pct = config.getfloat('SideHoldZones', 'left_pct', fallback=30)
                self.side_hold_right_pct = config.getfloat('SideHoldZones', 'right_pct', fallback=30)
            if 'Detection' in config:
                self.max_bar_speed = config.getfloat('Detection', 'max_bar_speed', fallback=500)
                self.accel_threshold = config.getfloat('Detection', 'accel_threshold', fallback=500)
                self.fish_velocity_threshold = config.getfloat('Detection', 'fish_velocity_threshold', fallback=20)
            if 'Advanced' in config:
                self.stabilization_zone_pct = config.getfloat('Advanced', 'stabilization_zone_pct', fallback=6)
                self.debug_display_enabled = config.getboolean('Advanced', 'debug_display', fallback=False)
                self.state_display_enabled = config.getboolean('Advanced', 'state_display', fallback=True)
                self.resilience_display_enabled = config.getboolean('Advanced', 'resilience_display', fallback=False)
                self.performance_display_enabled = config.getboolean('Advanced', 'performance_display', fallback=False)
                self.active_time_display_enabled = config.getboolean('Advanced', 'active_time_display', fallback=False)
                self.visual_debug_enabled = config.getboolean('Advanced', 'visual_debug_enabled', fallback=False)
                self.visual_debug_show_raw = config.getboolean('Advanced', 'visual_debug_show_raw', fallback=True)
                self.visual_debug_show_bar_mask = config.getboolean('Advanced', 'visual_debug_show_bar_mask', fallback=False)
                self.visual_debug_show_fish_mask = config.getboolean('Advanced', 'visual_debug_show_fish_mask', fallback=False)
                self.visual_debug_show_white_mask = config.getboolean('Advanced', 'visual_debug_show_white_mask', fallback=False)
                self.visual_debug_show_dark_mask = config.getboolean('Advanced', 'visual_debug_show_dark_mask', fallback=False)
                self.visual_debug_show_contours = config.getboolean('Advanced', 'visual_debug_show_contours', fallback=False)
                self.visual_debug_show_bar_box = config.getboolean('Advanced', 'visual_debug_show_bar_box', fallback=True)
                self.visual_debug_show_fish_pos = config.getboolean('Advanced', 'visual_debug_show_fish_pos', fallback=True)
                self.side_hold_visuals_enabled = config.getboolean('Advanced', 'side_hold_visuals', fallback=False)
                self.minigame_visuals_enabled = config.getboolean('Advanced', 'minigame_visuals', fallback=True)
            if 'CustomUI' in config:
                self.rod_custom_ui_enabled = config.getboolean('CustomUI', 'rod_custom_ui_enabled', fallback=False)
                self.rod_skin_selection = config.get('CustomUI', 'rod_skin_selection', fallback="")
                if self.rod_custom_ui_enabled and self.rod_skin_selection in SKIN_PROFILES:
                    self.current_profile = SKIN_PROFILES[self.rod_skin_selection]
                else:
                    self.current_profile = SKIN_PROFILES["Default"]
            print(f"Config loaded from {config_path}")
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    def update_config_list(self):
        config_files = [f.stem for f in self.config_dir.glob("*.ini")]
        self.save_combo['values'] = config_files
        self.load_combo['values'] = config_files

    def save_config(self):
        config_name = self.save_config_var.get().strip()
        if not config_name:
            self.config_status_label.config(text="❌ Please enter a config name", fg="#f48771")
            return
        if config_name.endswith('.ini'):
            config_name = config_name[:-4]
        config_path = self.config_dir / f"{config_name}.ini"
        self.save_config_to_path(config_path)
        self.config_status_label.config(text=f"✓ Saved: {config_name}.ini", fg="#89d185")
        self.update_config_list()

    def load_config(self):
        config_name = self.load_config_var.get().strip()
        if not config_name:
            self.config_status_label.config(text="❌ Please select a config", fg="#f48771")
            return
        config_path = self.config_dir / f"{config_name}.ini"
        if not config_path.exists():
            self.config_status_label.config(text=f"❌ Config not found: {config_name}", fg="#f48771")
            return
        if self.load_config_from_path(config_path):
            try:
                self.auto_recast_var.set(self.auto_recast_enabled)
                self.auto_shake_var.set(self.auto_shake_enabled)
                self.auto_lower_graphics_var.set(self.auto_lower_graphics_enabled)
                self.auto_camera_mode_var.set(self.auto_camera_mode_enabled)
                self.auto_blur_var.set(self.auto_blur_enabled)
                if hasattr(self, 'auto_cast_var'):
                    self.auto_cast_var.set(self.auto_cast_enabled)
                if hasattr(self, 'auto_cast_delay_slider'):
                    self.auto_cast_delay_slider.set(self.auto_cast_delay)
                    self.auto_cast_delay_value_label.config(text=f"{self.auto_cast_delay:.1f}s")
                if hasattr(self, 'cast_duration_slider'):
                    self.cast_duration_slider.set(self.cast_duration)
                    self.cast_duration_value_label.config(text=f"{self.cast_duration:.2f}s")
                if hasattr(self, 'hotkey_button'):
                    self.hotkey_button.config(text=f"Current: {self.toggle_hotkey.upper()}")
                if hasattr(self, 'focus_loss_stop_var'):
                    self.focus_loss_stop_var.set(self.focus_loss_stop)
                if hasattr(self, 'shake_type_var'):
                    self.shake_type_var.set(self.shake_type)
                if hasattr(self, 'nav_key_button'):
                    self.nav_key_button.config(text=f"Current: {self.shake_nav_key.upper()}")
                if hasattr(self, 'control_stat_slider') and self.control_stat_slider is not None:
                    self.control_stat_slider.set(self.current_control_stat)
                    self.control_stat_value_label.config(text=f"{self.current_control_stat:.2f}")
                    if hasattr(self, 'control_stat_input') and self.control_stat_input is not None:
                        self.control_stat_input.delete(0, tk.END)
                        self.control_stat_input.insert(0, f"{self.current_control_stat:.2f}")
                if hasattr(self, 'rod_resilience_slider') and self.rod_resilience_slider is not None:
                    self.rod_resilience_slider.set(self.rod_resilience * 100)
                    self.rod_resilience_value_label.config(text=f"{self.rod_resilience * 100:.0f}%")
                    if hasattr(self, 'rod_resilience_input') and self.rod_resilience_input is not None:
                        self.rod_resilience_input.delete(0, tk.END)
                        self.rod_resilience_input.insert(0, f"{self.rod_resilience * 100:.0f}")
                if hasattr(self, 'bait_resilience_slider') and self.bait_resilience_slider is not None:
                    self.bait_resilience_slider.set(self.bait_resilience * 100)
                    self.bait_resilience_value_label.config(text=f"{self.bait_resilience * 100:.0f}%")
                    if hasattr(self, 'bait_resilience_input') and self.bait_resilience_input is not None:
                        self.bait_resilience_input.delete(0, tk.END)
                        self.bait_resilience_input.insert(0, f"{self.bait_resilience * 100:.0f}")
                if hasattr(self, 'onirifalx_resilience_var'):
                    self.onirifalx_resilience_var.set(self.onirifalx_resilience_enabled)
                    if self.onirifalx_resilience_enabled:
                        self.toggle_onirifalx_resilience()
                    else:
                        if hasattr(self, 'rod_resilience_slider') and self.rod_resilience_slider is not None:
                            self.rod_resilience_slider.config(state='normal')
                        if hasattr(self, 'rod_resilience_input') and self.rod_resilience_input is not None:
                            self.rod_resilience_input.config(state='normal')
                if hasattr(self, 'critical_distance_slider') and self.critical_distance_slider is not None:
                    self.critical_distance_slider.set(self.control_params['critical_distance'])
                    self.critical_distance_value_label.config(text=str(self.control_params['critical_distance']))
                if hasattr(self, 'close_distance_slider') and self.close_distance_slider is not None:
                    self.close_distance_slider.set(self.control_params['close_distance'])
                    self.close_distance_value_label.config(text=str(self.control_params['close_distance']))
                if hasattr(self, 'moderate_distance_slider') and self.moderate_distance_slider is not None:
                    self.moderate_distance_slider.set(self.control_params['moderate_distance'])
                    self.moderate_distance_value_label.config(text=str(self.control_params['moderate_distance']))
                if hasattr(self, 'far_distance_slider') and self.far_distance_slider is not None:
                    self.far_distance_slider.set(self.control_params['far_distance'])
                    self.far_distance_value_label.config(text=str(self.control_params['far_distance']))
                if hasattr(self, 'critical_decel_slider') and self.critical_decel_slider is not None:
                    self.critical_decel_slider.set(self.control_params['critical_decel'])
                    self.critical_decel_value_label.config(text=str(self.control_params['critical_decel']))
                if hasattr(self, 'close_decel_slider') and self.close_decel_slider is not None:
                    self.close_decel_slider.set(self.control_params['close_decel'])
                    self.close_decel_value_label.config(text=str(self.control_params['close_decel']))
                if hasattr(self, 'moderate_decel_slider') and self.moderate_decel_slider is not None:
                    self.moderate_decel_slider.set(self.control_params['moderate_decel'])
                    self.moderate_decel_value_label.config(text=str(self.control_params['moderate_decel']))
                if hasattr(self, 'far_decel_slider') and self.far_decel_slider is not None:
                    self.far_decel_slider.set(self.control_params['far_decel'])
                    self.far_decel_value_label.config(text=str(self.control_params['far_decel']))
                if hasattr(self, 'left_critical_decel_slider') and self.left_critical_decel_slider is not None:
                    self.left_critical_decel_slider.set(self.control_params['left_critical_decel'])
                    self.left_critical_decel_value_label.config(text=str(self.control_params['left_critical_decel']))
                if hasattr(self, 'left_close_decel_slider') and self.left_close_decel_slider is not None:
                    self.left_close_decel_slider.set(self.control_params['left_close_decel'])
                    self.left_close_decel_value_label.config(text=str(self.control_params['left_close_decel']))
                if hasattr(self, 'left_moderate_decel_slider') and self.left_moderate_decel_slider is not None:
                    self.left_moderate_decel_slider.set(self.control_params['left_moderate_decel'])
                    self.left_moderate_decel_value_label.config(text=str(self.control_params['left_moderate_decel']))
                if hasattr(self, 'left_far_decel_slider') and self.left_far_decel_slider is not None:
                    self.left_far_decel_slider.set(self.control_params['left_far_decel'])
                    self.left_far_decel_value_label.config(text=str(self.control_params['left_far_decel']))
                if hasattr(self, 'right_critical_decel_slider') and self.right_critical_decel_slider is not None:
                    self.right_critical_decel_slider.set(self.control_params['right_critical_decel'])
                    self.right_critical_decel_value_label.config(text=str(self.control_params['right_critical_decel']))
                if hasattr(self, 'right_close_decel_slider') and self.right_close_decel_slider is not None:
                    self.right_close_decel_slider.set(self.control_params['right_close_decel'])
                    self.right_close_decel_value_label.config(text=str(self.control_params['right_close_decel']))
                if hasattr(self, 'right_moderate_decel_slider') and self.right_moderate_decel_slider is not None:
                    self.right_moderate_decel_slider.set(self.control_params['right_moderate_decel'])
                    self.right_moderate_decel_value_label.config(text=str(self.control_params['right_moderate_decel']))
                if hasattr(self, 'right_far_decel_slider') and self.right_far_decel_slider is not None:
                    self.right_far_decel_slider.set(self.control_params['right_far_decel'])
                    self.right_far_decel_value_label.config(text=str(self.control_params['right_far_decel']))
                if hasattr(self, 'side_hold_left_slider') and self.side_hold_left_slider is not None:
                    self.side_hold_left_slider.set(self.side_hold_left_pct)
                    self.side_hold_left_value_label.config(text=str(self.side_hold_left_pct))
                if hasattr(self, 'side_hold_right_slider') and self.side_hold_right_slider is not None:
                    self.side_hold_right_slider.set(self.side_hold_right_pct)
                    self.side_hold_right_value_label.config(text=str(self.side_hold_right_pct))
                if hasattr(self, 'max_velocity_slider') and self.max_velocity_slider is not None:
                    self.max_velocity_slider.set(self.max_bar_speed)
                    self.max_velocity_value_label.config(text=str(self.max_bar_speed))
                if hasattr(self, 'accel_threshold_slider') and self.accel_threshold_slider is not None:
                    self.accel_threshold_slider.set(self.accel_threshold)
                    self.accel_threshold_value_label.config(text=str(self.accel_threshold))
                if hasattr(self, 'fish_velocity_threshold_slider') and self.fish_velocity_threshold_slider is not None:
                    self.fish_velocity_threshold_slider.set(self.fish_velocity_threshold)
                    self.fish_velocity_threshold_value_label.config(text=str(self.fish_velocity_threshold))
                if hasattr(self, 'stabilization_zone_slider') and self.stabilization_zone_slider is not None:
                    self.stabilization_zone_slider.set(self.stabilization_zone_pct)
                    self.stabilization_zone_value_label.config(text=str(self.stabilization_zone_pct))
                if hasattr(self, 'pid_kp_slider') and self.pid_kp_slider is not None:
                    self.pid_kp_slider.set(self.pid_kp)
                    self.pid_kp_value_label.config(text=str(self.pid_kp))
                if hasattr(self, 'pid_kd_slider') and self.pid_kd_slider is not None:
                    self.pid_kd_slider.set(self.pid_kd)
                    self.pid_kd_value_label.config(text=str(self.pid_kd))
                if hasattr(self, 'prediction_time_slider') and self.prediction_time_slider is not None:
                    self.prediction_time_slider.set(self.prediction_time)
                    self.prediction_time_value_label.config(text=str(self.prediction_time))
                if hasattr(self, 'control_to_pixels_slider') and self.control_to_pixels_slider is not None:
                    self.control_to_pixels_slider.set(self.control_to_pixels)
                    self.control_to_pixels_value_label.config(text=str(self.control_to_pixels))
                if hasattr(self, 'max_bar_width_pct_slider') and self.max_bar_width_pct_slider is not None:
                    self.max_bar_width_pct_slider.set(self.max_bar_width_pct * 100)
                    self.max_bar_width_pct_value_label.config(text=str(int(self.max_bar_width_pct * 100)))
                if hasattr(self, 'max_frames_lost_slider') and self.max_frames_lost_slider is not None:
                    self.max_frames_lost_slider.set(self.max_frames_lost)
                    self.max_frames_lost_value_label.config(text=str(self.max_frames_lost))
                if hasattr(self, 'tolerance_slider') and self.tolerance_slider is not None:
                    self.tolerance_slider.set(self.tolerance)
                    self.tolerance_value_label.config(text=str(self.tolerance))
                if hasattr(self, 'white_bar_tolerance_slider') and self.white_bar_tolerance_slider is not None:
                    self.white_bar_tolerance_slider.set(self.white_bar_tolerance)
                    self.white_bar_tolerance_value_label.config(text=str(self.white_bar_tolerance))
                if hasattr(self, 'miss_bar_tolerance_slider') and self.miss_bar_tolerance_slider is not None:
                    self.miss_bar_tolerance_slider.set(self.miss_bar_tolerance)
                    self.miss_bar_tolerance_value_label.config(text=str(self.miss_bar_tolerance))
                if hasattr(self, 'fish_tolerance_slider') and self.fish_tolerance_slider is not None:
                    self.fish_tolerance_slider.set(self.fish_tolerance)
                    self.fish_tolerance_value_label.config(text=str(self.fish_tolerance))
                if hasattr(self, 'shake_white_threshold_slider') and self.shake_white_threshold_slider is not None:
                    self.shake_white_threshold_slider.set(self.shake_white_threshold)
                    self.shake_white_threshold_value_label.config(text=str(self.shake_white_threshold))
                if hasattr(self, 'shake_area_min_slider') and self.shake_area_min_slider is not None:
                    self.shake_area_min_slider.set(self.shake_area_min)
                    self.shake_area_min_value_label.config(text=str(self.shake_area_min))
                if hasattr(self, 'shake_area_max_slider') and self.shake_area_max_slider is not None:
                    self.shake_area_max_slider.set(self.shake_area_max)
                    self.shake_area_max_value_label.config(text=str(self.shake_area_max))
                if hasattr(self, 'shake_aspect_min_slider') and self.shake_aspect_min_slider is not None:
                    self.shake_aspect_min_slider.set(self.shake_aspect_min)
                    self.shake_aspect_min_value_label.config(text=str(self.shake_aspect_min))
                if hasattr(self, 'shake_aspect_max_slider') and self.shake_aspect_max_slider is not None:
                    self.shake_aspect_max_slider.set(self.shake_aspect_max)
                    self.shake_aspect_max_value_label.config(text=str(self.shake_aspect_max))
                if hasattr(self, 'shake_solidity_min_slider') and self.shake_solidity_min_slider is not None:
                    self.shake_solidity_min_slider.set(self.shake_solidity_min)
                    self.shake_solidity_min_value_label.config(text=str(self.shake_solidity_min))
                if hasattr(self, 'shake_roi_top_pct_slider') and self.shake_roi_top_pct_slider is not None:
                    self.shake_roi_top_pct_slider.set(self.shake_roi_top_pct)
                    self.shake_roi_top_pct_value_label.config(text=str(self.shake_roi_top_pct))
                if hasattr(self, 'shake_roi_left_pct_slider') and self.shake_roi_left_pct_slider is not None:
                    self.shake_roi_left_pct_slider.set(self.shake_roi_left_pct)
                    self.shake_roi_left_pct_value_label.config(text=str(self.shake_roi_left_pct))
                if hasattr(self, 'shake_roi_width_pct_slider') and self.shake_roi_width_pct_slider is not None:
                    self.shake_roi_width_pct_slider.set(self.shake_roi_width_pct)
                    self.shake_roi_width_pct_value_label.config(text=str(self.shake_roi_width_pct))
                if hasattr(self, 'shake_roi_height_pct_slider') and self.shake_roi_height_pct_slider is not None:
                    self.shake_roi_height_pct_slider.set(self.shake_roi_height_pct)
                    self.shake_roi_height_pct_value_label.config(text=str(self.shake_roi_height_pct))
                if hasattr(self, 'transparency_delay_slider') and self.transparency_delay_slider is not None:
                    self.transparency_delay_slider.set(self.transparency_delay)
                    self.transparency_delay_value_label.config(text=str(self.transparency_delay))
                if hasattr(self, 'transparency_enabled_var'):
                    self.transparency_enabled_var.set(self.transparency_enabled)
                    self.toggle_transparency_enabled()
                if hasattr(self, 'skin_profile_var'):
                    current = self.skin_profile_var.get()
                    if current not in SKIN_PROFILES:
                        current = 'Default'
                        self.skin_profile_var.set(current)
                    self.load_skin_profile_fields(current)
                self.debug_display_var.set(self.debug_display_enabled)
                self.state_display_var.set(self.state_display_enabled)
                self.resilience_display_var.set(self.resilience_display_enabled)
                self.performance_display_var.set(self.performance_display_enabled)
                if hasattr(self, 'active_time_display_var'):
                    self.active_time_display_var.set(self.active_time_display_enabled)
                    self.toggle_active_time_display()
                if hasattr(self, 'visual_debug_var'):
                    self.visual_debug_var.set(self.visual_debug_enabled)
                    self.toggle_visual_debug_overlay()
                if hasattr(self, 'visual_debug_raw_var'):
                    self.visual_debug_raw_var.set(self.visual_debug_show_raw)
                if hasattr(self, 'visual_debug_bar_mask_var'):
                    self.visual_debug_bar_mask_var.set(self.visual_debug_show_bar_mask)
                if hasattr(self, 'visual_debug_fish_mask_var'):
                    self.visual_debug_fish_mask_var.set(self.visual_debug_show_fish_mask)
                if hasattr(self, 'visual_debug_white_mask_var'):
                    self.visual_debug_white_mask_var.set(self.visual_debug_show_white_mask)
                if hasattr(self, 'visual_debug_dark_mask_var'):
                    self.visual_debug_dark_mask_var.set(self.visual_debug_show_dark_mask)
                if hasattr(self, 'visual_debug_contours_var'):
                    self.visual_debug_contours_var.set(self.visual_debug_show_contours)
                if hasattr(self, 'visual_debug_bar_box_var'):
                    self.visual_debug_bar_box_var.set(self.visual_debug_show_bar_box)
                if hasattr(self, 'visual_debug_fish_pos_var'):
                    self.visual_debug_fish_pos_var.set(self.visual_debug_show_fish_pos)
                self.side_hold_visuals_var.set(self.side_hold_visuals_enabled)
                self.minigame_visuals_var.set(self.minigame_visuals_enabled)
                self.rod_custom_ui_var.set(self.rod_custom_ui_enabled)
                if self.rod_custom_ui_enabled:
                    self.rod_skin_combo.config(state='readonly')
                    self.rod_skin_var.set(self.rod_skin_selection)
                else:
                    self.rod_skin_combo.config(state='disabled')
                    self.rod_skin_var.set("")
                self.toggle_debug_display()
                self.toggle_state_display()
                self.toggle_resilience_display()
                self.toggle_performance_display()
            except Exception as e:
                print(f"Error updating UI: {e}")
            self.config_status_label.config(text=f"✓ Loaded: {config_name}.ini", fg="#89d185")
        else:
            self.config_status_label.config(text=f"❌ Error loading config", fg="#f48771")

    def delete_config(self):
        config_name = self.load_config_var.get().strip()
        if not config_name:
            self.config_status_label.config(text="❌ Please select a config to delete", fg="#f48771")
            return
        config_path = self.config_dir / f"{config_name}.ini"
        if not config_path.exists():
            self.config_status_label.config(text=f"❌ Config not found: {config_name}", fg="#f48771")
            return
        try:
            config_path.unlink()
            self.config_status_label.config(text=f"✓ Deleted: {config_name}.ini", fg="#89d185")
            print(f"Config deleted: {config_path}")
            self.load_config_var.set('')
            self.update_config_list()
        except Exception as e:
            self.config_status_label.config(text=f"❌ Error deleting: {str(e)}", fg="#f48771")
            print(f"Error deleting config: {e}")

    def create_section(self, parent, title):
        section = tk.Frame(parent, bg='#1e1e1e')
        section.pack(fill=tk.X, padx=15, pady=8)
        title_label = tk.Label(
            section,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg="#cccccc",
            bg='#1e1e1e'
        )
        title_label.pack(anchor='w', pady=(0, 4))
        content_wrapper = tk.Frame(section, bg='#1e1e1e')
        content_wrapper.pack(fill=tk.X)
        content = tk.Frame(content_wrapper, bg='#252526')
        content.pack(fill=tk.BOTH, expand=True, pady=4)
        return content

    def add_slider_config(self, parent, label_text, from_val, to_val, increment, default_val, callback, var_name=None):
        container = tk.Frame(parent, bg='#252526')
        container.pack(fill=tk.X, padx=15, pady=6)
        top_frame = tk.Frame(container, bg='#252526')
        top_frame.pack(fill=tk.X)
        label = tk.Label(
            top_frame,
            text=label_text,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            anchor='w'
        )
        label.pack(side=tk.LEFT)
        value_label = tk.Label(
            top_frame,
            text=str(default_val),
            font=("Segoe UI", 8, "bold"),
            fg="#4ec9b0",
            bg='#252526'
        )
        value_label.pack(side=tk.RIGHT)
        slider = tk.Scale(
            container,
            from_=from_val,
            to=to_val,
            resolution=increment,
            orient=tk.HORIZONTAL,
            bg='#3e3e42',
            fg='#cccccc',
            troughcolor='#2d2d30',
            activebackground='#007acc',
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            showvalue=False,
            command=lambda val: self.on_slider_change(val, value_label, callback)
        )
        slider.set(default_val)
        slider.pack(fill=tk.X, pady=(4, 0))
        if var_name:
            setattr(self, f"{var_name}_slider", slider)
            setattr(self, f"{var_name}_value_label", value_label)

    def on_slider_change(self, value, value_label, callback):
        value_label.config(text=str(float(value)))
        callback()

    def add_control_stat_config(self, parent, label_text, min_val, max_val, default_val):
        container = tk.Frame(parent, bg='#252526')
        container.pack(fill=tk.X, padx=15, pady=6)
        top_frame = tk.Frame(container, bg='#252526')
        top_frame.pack(fill=tk.X)
        label = tk.Label(
            top_frame,
            text=label_text,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            anchor='w'
        )
        label.pack(side=tk.LEFT)
        value_label = tk.Label(
            top_frame,
            text=f"{default_val:.2f}",
            font=("Segoe UI", 8, "bold"),
            fg="#4ec9b0",
            bg='#252526'
        )
        value_label.pack(side=tk.RIGHT)
        middle_frame = tk.Frame(container, bg='#252526')
        middle_frame.pack(fill=tk.X, pady=(4, 4))
        slider = tk.Scale(
            middle_frame,
            from_=min_val,
            to=max_val,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            bg='#3e3e42',
            fg='#cccccc',
            troughcolor='#2d2d30',
            activebackground='#007acc',
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            showvalue=False
        )
        slider.set(default_val)
        slider.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        input_frame = tk.Frame(middle_frame, bg='#252526')
        input_frame.pack(side=tk.RIGHT)
        input_field = tk.Entry(
            input_frame,
            width=8,
            font=("Segoe UI", 8),
            bg='#3e3e42',
            fg='#cccccc',
            insertbackground='#cccccc',
            disabledbackground='#3e3e42',
            disabledforeground='#cccccc',
            relief=tk.FLAT,
            borderwidth=1
        )
        input_field.pack(side=tk.LEFT)
        input_field.insert(0, f"{default_val:.2f}")
        
        def on_slider_move(val):
            slider_val = float(val)
            input_field.delete(0, tk.END)
            input_field.insert(0, f"{slider_val:.2f}")
            value_label.config(text=f"{slider_val:.2f}")
            self.update_control_stat_value(slider_val)
        
        def on_input_change(event):
            try:
                input_val = float(input_field.get())
                input_val = max(min_val, min(max_val, input_val))
                slider.set(input_val)
                value_label.config(text=f"{input_val:.2f}")
                self.update_control_stat_value(input_val)
            except ValueError:
                current = float(slider.get())
                input_field.delete(0, tk.END)
                input_field.insert(0, f"{current:.2f}")
        
        slider.config(command=on_slider_move)
        input_field.bind('<Return>', on_input_change)
        input_field.bind('<FocusOut>', on_input_change)
        self.control_stat_slider = slider
        self.control_stat_input = input_field
        self.control_stat_value_label = value_label

    def add_resilience_config(self, parent, label_text, min_val, max_val, step, default_val, config_name):
        container = tk.Frame(parent, bg='#252526')
        container.pack(fill=tk.X, padx=15, pady=6)
        top_frame = tk.Frame(container, bg='#252526')
        top_frame.pack(fill=tk.X)
        label = tk.Label(
            top_frame,
            text=label_text,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526',
            anchor='w'
        )
        label.pack(side=tk.LEFT)
        value_label = tk.Label(
            top_frame,
            text=f"{default_val:.0f}%",
            font=("Segoe UI", 8, "bold"),
            fg="#4ec9b0",
            bg='#252526'
        )
        value_label.pack(side=tk.RIGHT)
        middle_frame = tk.Frame(container, bg='#252526')
        middle_frame.pack(fill=tk.X, pady=(4, 4))
        slider = tk.Scale(
            middle_frame,
            from_=min_val,
            to=max_val,
            resolution=step,
            orient=tk.HORIZONTAL,
            bg='#3e3e42',
            fg='#cccccc',
            troughcolor='#2d2d30',
            activebackground='#007acc',
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            showvalue=False
        )
        slider.set(default_val)
        slider.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        input_frame = tk.Frame(middle_frame, bg='#252526')
        input_frame.pack(side=tk.RIGHT)
        input_field = tk.Entry(
            input_frame,
            width=8,
            font=("Segoe UI", 8),
            bg='#3e3e42',
            fg='#cccccc',
            insertbackground='#cccccc',
            relief=tk.FLAT,
            borderwidth=1
        )
        input_field.pack(side=tk.LEFT)
        input_field.insert(0, f"{default_val:.0f}")
        
        def on_slider_move(val):
            slider_val = float(val)
            input_field.delete(0, tk.END)
            input_field.insert(0, f"{slider_val:.0f}")
            value_label.config(text=f"{slider_val:.0f}%")
            self.update_resilience_value(config_name, slider_val / 100.0)
        
        def on_input_change(event):
            try:
                input_val = float(input_field.get())
                input_val = max(min_val, min(max_val, input_val))
                slider.set(input_val)
                value_label.config(text=f"{input_val:.0f}%")
                self.update_resilience_value(config_name, input_val / 100.0)
            except ValueError:
                current = float(slider.get())
                input_field.delete(0, tk.END)
                input_field.insert(0, f"{current:.0f}")
        slider.config(command=on_slider_move)
        input_field.bind('<Return>', on_input_change)
        input_field.bind('<FocusOut>', on_input_change)
        setattr(self, f"{config_name}_slider", slider)
        setattr(self, f"{config_name}_input", input_field)
        setattr(self, f"{config_name}_value_label", value_label)

    def _create_color_entry(self, parent, label_text):
        container = tk.Frame(parent, bg='#252526')
        container.pack(fill=tk.X, pady=(0, 4))
        label = tk.Label(
            container,
            text=label_text,
            font=("Segoe UI", 8),
            fg="#cccccc",
            bg='#252526'
        )
        label.pack(anchor='w')
        entry = tk.Entry(
            container,
            font=("Segoe UI", 8),
            bg='#3e3e42',
            fg='#cccccc',
            insertbackground='#cccccc',
            disabledbackground='#3e3e42',
            disabledforeground='#cccccc',
            relief=tk.FLAT,
            borderwidth=1
        )
        entry.pack(fill=tk.X, pady=(2, 0))
        return entry

    def _parse_color_triplet(self, text):
        parts = [p.strip() for p in text.split(',')]
        if len(parts) != 3:
            raise ValueError("Color must be in B,G,R format")
        values = [int(p) for p in parts]
        for v in values:
            if v < 0 or v > 255:
                raise ValueError("Color values must be 0-255")
        return np.array(values)

    def load_skin_profile_fields(self, profile_name):
        if profile_name not in SKIN_PROFILES:
            return
        profile = SKIN_PROFILES[profile_name]
        bar_min = profile.get('bar_min')
        bar_max = profile.get('bar_max')
        fish_min = profile.get('fish_min')
        fish_max = profile.get('fish_max')
        if bar_min is not None:
            self.profile_bar_min_entry.delete(0, tk.END)
            self.profile_bar_min_entry.insert(0, f"{bar_min[0]},{bar_min[1]},{bar_min[2]}")
        if bar_max is not None:
            self.profile_bar_max_entry.delete(0, tk.END)
            self.profile_bar_max_entry.insert(0, f"{bar_max[0]},{bar_max[1]},{bar_max[2]}")
        if fish_min is not None:
            self.profile_fish_min_entry.delete(0, tk.END)
            self.profile_fish_min_entry.insert(0, f"{fish_min[0]},{fish_min[1]},{fish_min[2]}")
        if fish_max is not None:
            self.profile_fish_max_entry.delete(0, tk.END)
            self.profile_fish_max_entry.insert(0, f"{fish_max[0]},{fish_max[1]},{fish_max[2]}")

    def on_skin_profile_selected(self, event=None):
        profile_name = self.skin_profile_var.get()
        self.load_skin_profile_fields(profile_name)

    def apply_skin_profile(self):
        profile_name = self.skin_profile_var.get()
        if profile_name not in SKIN_PROFILES:
            return
        try:
            bar_min = self._parse_color_triplet(self.profile_bar_min_entry.get())
            bar_max = self._parse_color_triplet(self.profile_bar_max_entry.get())
            fish_min = self._parse_color_triplet(self.profile_fish_min_entry.get())
            fish_max = self._parse_color_triplet(self.profile_fish_max_entry.get())
            SKIN_PROFILES[profile_name]['bar_min'] = bar_min
            SKIN_PROFILES[profile_name]['bar_max'] = bar_max
            SKIN_PROFILES[profile_name]['fish_min'] = fish_min
            SKIN_PROFILES[profile_name]['fish_max'] = fish_max
            if self.rod_custom_ui_enabled and self.rod_skin_selection == profile_name:
                self.current_profile = SKIN_PROFILES[profile_name]
            elif not self.rod_custom_ui_enabled and profile_name == "Default":
                self.current_profile = SKIN_PROFILES["Default"]
            print(f"Profile updated: {profile_name}")
        except ValueError as e:
            print(f"Invalid profile values: {e}")
    
    def update_resilience_value(self, config_name, new_value):
        try:
            if config_name == "rod_resilience":
                self.rod_resilience = new_value
                print(f"Rod resilience updated to {new_value*100:.0f}%")
            elif config_name == "bait_resilience":
                self.bait_resilience = new_value
                print(f"Bait resilience updated to {new_value*100:.0f}%")
            self.effective_resilience = max(0.20, self.rod_resilience + self.bait_resilience)
            movement_interval = 2.15 * self.effective_resilience
            movement_distance = 0.40 * self.effective_resilience * 0.80
            movement_distance_max = 0.40 * self.effective_resilience * 1.20
            print(f"Effective resilience: {self.effective_resilience*100:.0f}% | Movement interval: ~{movement_interval*1000:.0f}ms | Distance: ±{movement_distance*100:.1f}-{movement_distance_max*100:.1f}% of bar width")
        except (ValueError, AttributeError):
            pass

    def update_movement_timing(self, fish_x, now_time):
        """Track fish movement timing and calculate predicted landing zone."""
        if fish_x is None:
            return
        if self.last_movement_detection_time is not None:
            self.time_since_last_movement = now_time - self.last_movement_detection_time
        expected_interval = 2.15 * self.effective_resilience
        time_until_next_jump = expected_interval - self.time_since_last_movement
        if time_until_next_jump < 0.100 and time_until_next_jump > -0.050:
            self.prediction_active = True
            movement_distance_px = int(0.40 * self.effective_resilience * 441)
            min_px = movement_distance_px * 0.80
            max_px = movement_distance_px * 1.20
            self.expected_landing_zone_min = fish_x - max_px
            self.expected_landing_zone_max = fish_x + max_px
        else:
            self.prediction_active = False
        self.last_detected_fish_x = fish_x

    def minimize_overlay(self):
        self.overlay.unbind("<Map>")
        self.overlay.overrideredirect(False)
        self.overlay.update()
        self.overlay.iconify()
        self.is_minimized = True
        self.overlay.bind("<Map>", lambda e: self.restore_overlay())
        
    def restore_overlay(self):
        if hasattr(self, 'is_minimized') and self.is_minimized:
            self.overlay.overrideredirect(True)
            self.is_minimized = False

    def update_overlay_positions(self):
        current_y = self.overlay_start_y
        if self.debug_display_enabled:
            debug_x = self.overlay_right_x - self.debug_width
            self.debug_overlay_window.geometry(f"+{debug_x}+{current_y}")
            current_y += self.overlay_spacing
        if self.state_display_enabled:
            state_x = self.overlay_right_x - self.state_width
            self.state_overlay_window.geometry(f"+{state_x}+{current_y}")
            current_y += self.overlay_spacing
        if self.resilience_display_enabled:
            resilience_x = self.overlay_right_x - self.resilience_width
            self.resilience_overlay_window.geometry(f"+{resilience_x}+{current_y}")
            current_y += self.overlay_spacing
        if self.performance_display_enabled:
            performance_x = self.overlay_right_x - self.performance_width
            self.performance_overlay_window.geometry(f"+{performance_x}+{current_y}")
            current_y += self.overlay_spacing
        if self.visual_debug_enabled:
            visual_x = self.overlay_right_x - self.visual_debug_width
            self.visual_debug_overlay_window.geometry(
                f"{self.visual_debug_width}x{self.visual_debug_height}+{visual_x}+{current_y}"
            )
            current_y += self.overlay_spacing
        if hasattr(self, 'active_time_overlay_window'):
            self.update_active_time_position()
    def toggle_state_display(self):
        self.state_display_enabled = self.state_display_var.get()
        if self.state_display_enabled:
            self.state_overlay_window.deiconify()
            print("State overlay enabled")
        else:
            self.state_overlay_window.withdraw()
            print("State overlay disabled")
        self.update_overlay_positions()

    def toggle_debug_display(self):
        self.debug_display_enabled = self.debug_display_var.get()
        if self.debug_display_enabled:
            self.debug_overlay_window.deiconify()
            print("Debug overlay enabled")
        else:
            self.debug_overlay_window.withdraw()
            print("Debug overlay disabled")
        self.update_overlay_positions()

    def toggle_resilience_display(self):
        self.resilience_display_enabled = self.resilience_display_var.get()
        if self.resilience_display_enabled:
            self.resilience_overlay_window.deiconify()
            print("Resilience overlay enabled")
        else:
            self.resilience_overlay_window.withdraw()
            print("Resilience overlay disabled")
        self.update_overlay_positions()
    
    def toggle_performance_display(self):
        self.performance_display_enabled = self.performance_display_var.get()
        if self.performance_display_enabled:
            self.performance_overlay_window.deiconify()
            print("Performance metrics overlay enabled")
        else:
            self.performance_overlay_window.withdraw()
            print("Performance metrics overlay disabled")
        self.update_overlay_positions()

    def toggle_active_time_display(self):
        self.active_time_display_enabled = self.active_time_display_var.get()
        if self.active_time_display_enabled:
            self.active_time_overlay_window.deiconify()
            print("Active time overlay enabled")
        else:
            self.active_time_overlay_window.withdraw()
            print("Active time overlay disabled")

    def toggle_visual_debug_overlay(self):
        self.visual_debug_enabled = self.visual_debug_var.get()
        if self.visual_debug_enabled:
            self.visual_debug_overlay_window.deiconify()
            print("Visual debug overlay enabled")
        else:
            self.visual_debug_overlay_window.withdraw()
            print("Visual debug overlay disabled")
        self.update_overlay_positions()

    def toggle_visual_debug_raw(self):
        self.visual_debug_show_raw = self.visual_debug_raw_var.get()

    def toggle_visual_debug_bar_mask(self):
        self.visual_debug_show_bar_mask = self.visual_debug_bar_mask_var.get()

    def toggle_visual_debug_fish_mask(self):
        self.visual_debug_show_fish_mask = self.visual_debug_fish_mask_var.get()

    def toggle_visual_debug_white_mask(self):
        self.visual_debug_show_white_mask = self.visual_debug_white_mask_var.get()

    def toggle_visual_debug_dark_mask(self):
        self.visual_debug_show_dark_mask = self.visual_debug_dark_mask_var.get()

    def toggle_visual_debug_contours(self):
        self.visual_debug_show_contours = self.visual_debug_contours_var.get()

    def toggle_visual_debug_bar_box(self):
        self.visual_debug_show_bar_box = self.visual_debug_bar_box_var.get()

    def toggle_visual_debug_fish_pos(self):
        self.visual_debug_show_fish_pos = self.visual_debug_fish_pos_var.get()

    def toggle_side_hold_visuals(self):
        self.side_hold_visuals_enabled = self.side_hold_visuals_var.get()
        status = "enabled" if self.side_hold_visuals_enabled else "disabled"
        print(f"Side hold visuals {status}")

    def toggle_minigame_visuals(self):
        self.minigame_visuals_enabled = self.minigame_visuals_var.get()
        status = "enabled" if self.minigame_visuals_enabled else "disabled"
        print(f"Minigame visualisation {status}")

    def toggle_auto_shake(self):
        self.auto_shake_enabled = self.auto_shake_var.get()
        status = "enabled" if self.auto_shake_enabled else "disabled"
        print(f"Auto-shake {status}")

    def toggle_auto_recast(self):
        self.auto_recast_enabled = self.auto_recast_var.get()
        status = "enabled" if self.auto_recast_enabled else "disabled"
        print(f"Auto-recast {status}")

    def toggle_auto_lower_graphics(self):
        self.auto_lower_graphics_enabled = self.auto_lower_graphics_var.get()
        status = "enabled" if self.auto_lower_graphics_enabled else "disabled"
        print(f"Auto-lower graphics {status}")

    def toggle_auto_camera_mode(self):
        self.auto_camera_mode_enabled = self.auto_camera_mode_var.get()
        status = "enabled" if self.auto_camera_mode_enabled else "disabled"
        print(f"Auto-camera mode {status}")

    def toggle_auto_blur(self):
        self.auto_blur_enabled = self.auto_blur_var.get()
        status = "enabled" if self.auto_blur_enabled else "disabled"
        print(f"Auto-blur {status}")

    def toggle_rod_custom_ui(self):
        self.rod_custom_ui_enabled = self.rod_custom_ui_var.get()
        status = "enabled" if self.rod_custom_ui_enabled else "disabled"
        new_state = 'readonly' if self.rod_custom_ui_enabled else 'disabled'
        self.rod_skin_combo.config(state=new_state)
        if self.rod_custom_ui_enabled:
            selected_skin = self.rod_skin_var.get()
            if selected_skin in SKIN_PROFILES:
                self.current_profile = SKIN_PROFILES[selected_skin]
                self.rod_skin_selection = selected_skin
        else:
            self.current_profile = SKIN_PROFILES["Default"]
            self.rod_skin_selection = ""
        print(f"Rod custom UI {status}")

    def toggle_onirifalx_resilience(self):
        self.onirifalx_resilience_enabled = self.onirifalx_resilience_var.get()
        if self.onirifalx_resilience_enabled:
            self.onirifalx_prev_rod_resilience = self.rod_resilience
            min_val = -100.0
            self.update_resilience_value("rod_resilience", min_val / 100.0)
            if hasattr(self, 'rod_resilience_slider') and self.rod_resilience_slider is not None:
                self.rod_resilience_slider.set(min_val)
                self.rod_resilience_slider.config(state='disabled')
            if hasattr(self, 'rod_resilience_input') and self.rod_resilience_input is not None:
                self.rod_resilience_input.delete(0, tk.END)
                self.rod_resilience_input.insert(0, f"{min_val:.0f}")
                self.rod_resilience_input.config(state='disabled')
            if hasattr(self, 'rod_resilience_value_label') and self.rod_resilience_value_label is not None:
                self.rod_resilience_value_label.config(text=f"{min_val:.0f}%")
            print("Onirifalx resilience enabled: Rod resilience set to -100%")
        else:
            restore_val = (self.onirifalx_prev_rod_resilience * 100.0)
            self.update_resilience_value("rod_resilience", restore_val / 100.0)
            if hasattr(self, 'rod_resilience_slider') and self.rod_resilience_slider is not None:
                self.rod_resilience_slider.config(state='normal')
                self.rod_resilience_slider.set(restore_val)
            if hasattr(self, 'rod_resilience_input') and self.rod_resilience_input is not None:
                self.rod_resilience_input.config(state='normal')
                self.rod_resilience_input.delete(0, tk.END)
                self.rod_resilience_input.insert(0, f"{restore_val:.0f}")
            if hasattr(self, 'rod_resilience_value_label') and self.rod_resilience_value_label is not None:
                self.rod_resilience_value_label.config(text=f"{restore_val:.0f}%")
            print("Onirifalx resilience disabled: Rod resilience restored")
    
    def on_rod_skin_selected(self, event=None):
        if self.rod_custom_ui_enabled:
            selected_skin = self.rod_skin_var.get()
            if selected_skin in SKIN_PROFILES:
                self.current_profile = SKIN_PROFILES[selected_skin]
                self.rod_skin_selection = selected_skin
                print(f"Switched to {selected_skin} profile")

    def update_control_stat(self):
        self.update_control_stat_value(float(self.control_stat_slider.get()))

    def update_control_stat_value(self, new_stat):
        try:
            new_stat = max(-0.37, min(0.7, new_stat))
            self.current_control_stat = new_stat
            bar_width_pct = 30 + (new_stat * 100)
            roi_width = 883
            self.expected_bar_width = int((bar_width_pct / 100) * roi_width)
            print(f"Control stat updated to {new_stat:.2f}, bar width: {bar_width_pct:.1f}% ({self.expected_bar_width}px)")
        except (ValueError, AttributeError):
            pass

    def update_stabilization_zone(self):
        try:
            val = float(self.stabilization_zone_slider.get())
            self.stabilization_zone_pct = max(1, min(20, val))
            print(f"Stabilization zone updated to {self.stabilization_zone_pct}%")
        except (ValueError, AttributeError):
            pass

    def update_critical_distance(self):
        try:
            val = float(self.critical_distance_slider.get())
            self.control_params['critical_distance'] = max(5, min(50, val))
        except (ValueError, AttributeError):
            pass

    def update_close_distance(self):
        try:
            val = float(self.close_distance_slider.get())
            self.control_params['close_distance'] = max(30, min(100, val))
        except (ValueError, AttributeError):
            pass

    def update_moderate_distance(self):
        try:
            val = float(self.moderate_distance_slider.get())
            self.control_params['moderate_distance'] = max(50, min(200, val))
        except (ValueError, AttributeError):
            pass

    def update_far_distance(self):
        try:
            val = float(self.far_distance_slider.get())
            self.control_params['far_distance'] = max(100, min(300, val))
        except (ValueError, AttributeError):
            pass

    def update_critical_decel(self):
        try:
            val = float(self.critical_decel_slider.get())
            self.control_params['critical_decel'] = max(50, min(1000, val))
        except (ValueError, AttributeError):
            pass

    def update_close_decel(self):
        try:
            val = float(self.close_decel_slider.get())
            self.control_params['close_decel'] = max(50, min(1000, val))
        except (ValueError, AttributeError):
            pass

    def update_moderate_decel(self):
        try:
            val = float(self.moderate_decel_slider.get())
            self.control_params['moderate_decel'] = max(50, min(1500, val))
        except (ValueError, AttributeError):
            pass

    def update_far_decel(self):
        try:
            val = float(self.far_decel_slider.get())
            self.control_params['far_decel'] = max(50, min(2000, val))
        except (ValueError, AttributeError):
            pass

    def update_left_critical_decel(self):
        try:
            val = float(self.left_critical_decel_slider.get())
            self.control_params['left_critical_decel'] = max(50, min(1000, val))
        except (ValueError, AttributeError):
            pass

    def update_left_close_decel(self):
        try:
            val = float(self.left_close_decel_slider.get())
            self.control_params['left_close_decel'] = max(50, min(1000, val))
        except (ValueError, AttributeError):
            pass

    def update_left_moderate_decel(self):
        try:
            val = float(self.left_moderate_decel_slider.get())
            self.control_params['left_moderate_decel'] = max(50, min(1500, val))
        except (ValueError, AttributeError):
            pass

    def update_left_far_decel(self):
        try:
            val = float(self.left_far_decel_slider.get())
            self.control_params['left_far_decel'] = max(50, min(2000, val))
        except (ValueError, AttributeError):
            pass

    def update_right_critical_decel(self):
        try:
            val = float(self.right_critical_decel_slider.get())
            self.control_params['right_critical_decel'] = max(50, min(1000, val))
        except (ValueError, AttributeError):
            pass

    def update_right_close_decel(self):
        try:
            val = float(self.right_close_decel_slider.get())
            self.control_params['right_close_decel'] = max(50, min(1000, val))
        except (ValueError, AttributeError):
            pass

    def update_right_moderate_decel(self):
        try:
            val = float(self.right_moderate_decel_slider.get())
            self.control_params['right_moderate_decel'] = max(50, min(1500, val))
        except (ValueError, AttributeError):
            pass

    def update_right_far_decel(self):
        try:
            val = float(self.right_far_decel_slider.get())
            self.control_params['right_far_decel'] = max(50, min(2000, val))
        except (ValueError, AttributeError):
            pass

    def update_max_velocity(self):
        try:
            val = float(self.max_velocity_slider.get())
            self.max_bar_speed = max(100, min(1000, val))
        except (ValueError, AttributeError):
            pass

    def update_accel_threshold(self):
        try:
            val = float(self.accel_threshold_slider.get())
            self.accel_threshold = max(100, min(2000, val))
        except (ValueError, AttributeError):
            pass

    def update_fish_velocity_threshold(self):
        try:
            val = float(self.fish_velocity_threshold_slider.get())
            self.fish_velocity_threshold = max(5, min(50, val))
        except (ValueError, AttributeError):
            pass

    def update_pid_kp(self):
        try:
            self.pid_kp = float(self.pid_kp_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_pid_kd(self):
        try:
            self.pid_kd = float(self.pid_kd_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_prediction_time(self):
        try:
            self.prediction_time = float(self.prediction_time_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_max_frames_lost(self):
        try:
            self.max_frames_lost = int(float(self.max_frames_lost_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_tolerance(self):
        try:
            self.tolerance = int(float(self.tolerance_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_white_bar_tolerance(self):
        try:
            self.white_bar_tolerance = int(float(self.white_bar_tolerance_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_miss_bar_tolerance(self):
        try:
            self.miss_bar_tolerance = int(float(self.miss_bar_tolerance_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_fish_tolerance(self):
        try:
            self.fish_tolerance = int(float(self.fish_tolerance_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_shake_white_threshold(self):
        try:
            self.shake_white_threshold = int(float(self.shake_white_threshold_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_shake_area_min(self):
        try:
            self.shake_area_min = int(float(self.shake_area_min_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_shake_area_max(self):
        try:
            self.shake_area_max = int(float(self.shake_area_max_slider.get()))
        except (ValueError, AttributeError):
            pass

    def update_shake_aspect_min(self):
        try:
            self.shake_aspect_min = float(self.shake_aspect_min_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_shake_aspect_max(self):
        try:
            self.shake_aspect_max = float(self.shake_aspect_max_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_shake_solidity_min(self):
        try:
            self.shake_solidity_min = float(self.shake_solidity_min_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_shake_roi_top(self):
        try:
            self.shake_roi_top_pct = float(self.shake_roi_top_pct_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_shake_roi_left(self):
        try:
            self.shake_roi_left_pct = float(self.shake_roi_left_pct_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_shake_roi_width(self):
        try:
            self.shake_roi_width_pct = float(self.shake_roi_width_pct_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_shake_roi_height(self):
        try:
            self.shake_roi_height_pct = float(self.shake_roi_height_pct_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_control_to_pixels(self):
        try:
            self.control_to_pixels = float(self.control_to_pixels_slider.get())
        except (ValueError, AttributeError):
            pass

    def update_max_bar_width_pct(self):
        try:
            pct = float(self.max_bar_width_pct_slider.get())
            self.max_bar_width_pct = max(0.3, min(0.9, pct / 100.0))
            if hasattr(self, 'fish_bar_roi') and self.fish_bar_roi is not None:
                self.max_bar_width = int(self.fish_bar_roi['width'] * self.max_bar_width_pct)
        except (ValueError, AttributeError):
            pass

    def update_transparency_delay(self):
        try:
            self.transparency_delay = float(self.transparency_delay_slider.get())
        except (ValueError, AttributeError):
            pass

    def toggle_transparency_enabled(self):
        self.transparency_enabled = self.transparency_enabled_var.get()
        if hasattr(self, 'transparency_delay_slider') and self.transparency_delay_slider is not None:
            state = 'normal' if self.transparency_enabled else 'disabled'
            self.transparency_delay_slider.config(state=state)
        if not self.transparency_enabled:
            if self.overlay is not None:
                self.overlay.attributes('-alpha', 1.0)
            self.is_transparent = False

    def update_side_hold_left(self):
        try:
            val = float(self.side_hold_left_slider.get())
            self.side_hold_left_pct = max(5, min(50, val))
            print(f"Left side hold updated to {self.side_hold_left_pct}% from left edge")
        except (ValueError, AttributeError):
            pass

    def update_side_hold_right(self):
        try:
            val = float(self.side_hold_right_slider.get())
            self.side_hold_right_pct = max(5, min(50, val))
            print(f"Right side hold updated to {self.side_hold_right_pct}% from right edge")
        except (ValueError, AttributeError):
            pass

    def check_minigame_active(self, sct):
        screenshot = np.array(sct.grab(self.fish_bar_roi))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        if "bar_min" in self.current_profile and "bar_max" in self.current_profile:
            bar_min = self.current_profile["bar_min"]
            bar_max = self.current_profile["bar_max"]
            mask = cv2.inRange(screenshot, bar_min, bar_max)
        else:
            lower = BAR_COLOR - self.tolerance
            upper = BAR_COLOR + self.tolerance
            mask = cv2.inRange(screenshot, lower, upper)
        bar_pixels = np.sum(mask > 0)
        if "fish_min" in self.current_profile and "fish_max" in self.current_profile:
            profile_fish_min = self.current_profile["fish_min"]
            profile_fish_max = self.current_profile["fish_max"]
            if np.array_equal(profile_fish_min, np.array([60, 60, 80])) and np.array_equal(profile_fish_max, np.array([80, 90, 105])):
                fish_rgb = FISH_COLOR.astype(np.int16)
                lower_fish_rgb = np.clip(fish_rgb - FISH_TOLERANCE, 0, 255)
                upper_fish_rgb = np.clip(fish_rgb + FISH_TOLERANCE, 0, 255)
                fish_min = lower_fish_rgb[::-1]
                fish_max = upper_fish_rgb[::-1]
                mask = cv2.inRange(screenshot, fish_min, fish_max)
            else:
                mask = cv2.inRange(screenshot, profile_fish_min, profile_fish_max)
        else:
            lower = FISH_COLOR - self.fish_tolerance
            upper = FISH_COLOR + self.fish_tolerance
            mask = cv2.inRange(screenshot, lower, upper)
        fish_pixels = np.sum(mask > 0)
        if bar_pixels > 500 and fish_pixels > 20:
            return True
        return False

    def start_transparency_timer(self):
        def check_transparency():
            while True:
                try:
                    current_time = time.time()
                    time_since_hover = current_time - self.last_hover_time
                    if not self.transparency_enabled:
                        if self.is_transparent:
                            self.overlay.attributes('-alpha', 1.0)
                            self.is_transparent = False
                        time.sleep(0.5)
                        continue
                    if time_since_hover >= self.transparency_delay and not self.is_transparent:
                        self.overlay.attributes('-alpha', 0.3)
                        self.is_transparent = True
                    time.sleep(0.5)
                except:
                    break
        transparency_thread = threading.Thread(target=check_transparency, daemon=True)
        transparency_thread.start()

    def overlay_loop(self):
        try:
            self.overlay.mainloop()
        except:
            pass

    def update_debug_display(self, bar_left, bar_right, fish_x):
        if not self.debug_display_enabled:
            return
        try:
            if bar_left is not None and bar_right is not None:
                center = (bar_left + bar_right) // 2
                bar_text = f"Bar: L:{bar_left} C:{center} R:{bar_right}"
            else:
                bar_text = "Bar: MISS"
            if fish_x is not None:
                fish_text = f"Fish: {fish_x}"
                if bar_left is not None and bar_right is not None:
                    center = (bar_left + bar_right) // 2
                    if center < fish_x:
                        fish_text += " →"
                    else:
                        fish_text += " ←"
            else:
                fish_text = "Fish: MISS"
            jump_text = ""
            if self.fish_jump_detected:
                jump_text = " [JUMP!]"
            elif self.prediction_active:
                jump_text = " [PRED]"
            
            debug_text = f"{bar_text}\n{fish_text}{jump_text}"
            self.debug_display_label.config(text=debug_text)
        except:
            pass

    def update_resilience_display(self):
        """Update resilience overlay with prediction info."""
        if not self.resilience_display_enabled:
            return
        
        try:
            effective_resilience = max(0.20, self.rod_resilience + self.bait_resilience)
            movement_interval = 2.15 * effective_resilience
            movement_distance = 0.40 * effective_resilience
            bar_width = self.last_bar_width if self.last_bar_width is not None else 441
            distance_px_min = int(movement_distance * 0.80 * bar_width)
            distance_px_max = int(movement_distance * 1.20 * bar_width)
            resilience_text = (
                f"Rod:{self.rod_resilience*100:+.0f}% Bait:{self.bait_resilience*100:+.0f}%\n"
                f"Eff:{effective_resilience*100:.0f}% Int:~{movement_interval*1000:.0f}ms\n"
                f"Mov:±{distance_px_min}-{distance_px_max}px"
            )
            self.resilience_display_label.config(text=resilience_text)
        except Exception as e:
            pass

    def setup_hotkey(self):
        def on_hotkey_press(key):
            try:
                key_name = None
                if hasattr(key, 'char') and key.char:
                    key_name = key.char.lower()
                elif hasattr(key, 'name'):
                    key_name = key.name.lower()
                if key_name == self.toggle_hotkey.lower():
                    self.toggle_macro()
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_hotkey_press)
        listener.daemon = True
        listener.start()

    def toggle_macro(self):
        if self.running:
            self.stop_macro()
            self.toggle_button.config(
                text="START MACRO",
                bg="#2e7d32",
                activebackground="#1b5e20"
            )
        else:
            self.start_macro()
            self.toggle_button.config(
                text="STOP MACRO",
                bg="#c72e2e",
                activebackground="#a82424"
            )
    
    def start_macro(self):
        if not self.running:
            if not self.focus_roblox():
                print("Warning: Could not focus Roblox window")
            self.running = True
            self.macro_start_time = time.time()
            self.update_status_label("RUNNING")
            self.set_state("Starting")
            print("Macro started!")
            self.bar_overlay_window.deiconify()
            self.minigame_thread = threading.Thread(target=self.start, daemon=True)
            self.minigame_thread.start()

    def stop_macro(self):
        self.running = False
        pydirectinput.mouseUp()
        self.update_status_label("STOPPED")
        self.set_state("Stopped")
        self.bar_overlay_window.withdraw()
        self.debug_screenshot_taken = False
        self.rod_equipped_this_session = False
        self.macro_start_time = None
        print("Macro stopped!")

    def update_status_label(self, status):
        try:
            if status == "RUNNING":
                self.status_label.config(text="● RUNNING", fg="#89d185")
            else:
                self.status_label.config(text="● STOPPED", fg="#f48771")
        except:
            pass

    def start_key_binding(self):
        if self.waiting_for_key:
            return
        
        self.waiting_for_key = True
        self.nav_key_button.config(
            text="Press any key...",
            bg='#007acc',
            fg='#ffffff'
        )
        print("Waiting for key press...")
        
        def on_key_press_bind(key):
            try:
                if hasattr(key, 'char') and key.char:
                    new_key = key.char.lower()
                elif hasattr(key, 'name'):
                    new_key = key.name.lower()
                else:
                    new_key = str(key).replace("'", "").lower()
                self.shake_nav_key = new_key
                self.nav_key_button.config(
                    text=f"Current: {self.shake_nav_key.upper()}",
                    bg='#3e3e42',
                    fg='#cccccc'
                )
                self.waiting_for_key = False
                print(f"Navigation key set to: {self.shake_nav_key}")
                return False
            except Exception as e:
                print(f"Error binding key: {e}")
                self.waiting_for_key = False
                self.nav_key_button.config(
                    text=f"Current: {self.shake_nav_key.upper()}",
                    bg='#3e3e42',
                    fg='#cccccc'
                )
                return False
        listener = keyboard.Listener(on_press=on_key_press_bind)
        listener.start()

    def start_hotkey_binding(self):
        if self.waiting_for_hotkey:
            return
        self.waiting_for_hotkey = True
        self.hotkey_button.config(
            text="Press any key...",
            bg='#007acc',
            fg='#ffffff'
        )
        print("Waiting for hotkey press...")
        def on_key_press_bind_hotkey(key):
            try:
                if hasattr(key, 'char') and key.char:
                    new_key = key.char.lower()
                elif hasattr(key, 'name'):
                    new_key = key.name.lower()
                else:
                    new_key = str(key).replace("'", "").lower()
                self.toggle_hotkey = new_key
                self.hotkey_button.config(
                    text=f"Current: {self.toggle_hotkey.upper()}",
                    bg='#3e3e42',
                    fg='#cccccc'
                )
                self.waiting_for_hotkey = False
                print(f"Toggle hotkey set to: {self.toggle_hotkey}")
                self.setup_hotkey()
                return False
            except Exception as e:
                print(f"Error binding hotkey: {e}")
                self.waiting_for_hotkey = False
                self.hotkey_button.config(
                    text=f"Current: {self.toggle_hotkey.upper()}",
                    bg='#3e3e42',
                    fg='#cccccc'
                )
                return False
        listener = keyboard.Listener(on_press=on_key_press_bind_hotkey)
        listener.start()

    def toggle_auto_cast(self):
        self.auto_cast_enabled = self.auto_cast_var.get()
        print(f"Auto-cast {'enabled' if self.auto_cast_enabled else 'disabled'}")

    def toggle_focus_loss_stop(self):
        self.focus_loss_stop = self.focus_loss_stop_var.get()
        print(f"Emergency stop on focus loss {'enabled' if self.focus_loss_stop else 'disabled'}")

    def update_auto_cast_delay(self, value):
        self.auto_cast_delay = float(value)
        self.auto_cast_delay_value_label.config(text=f"{self.auto_cast_delay:.1f}s")

    def update_cast_duration(self, value):
        self.cast_duration = float(value)
        self.cast_duration_value_label.config(text=f"{self.cast_duration:.2f}s")

    def update_shake_type(self):
        self.shake_type = self.shake_type_var.get()
        print(f"Shake type set to: {self.shake_type}")

    def set_state(self, state_text):
        if state_text != self.current_state:
            self.current_state = state_text
            try:
                if self.state_display_enabled:
                    if "Playing minigame" in state_text:
                        if "(" in state_text and ")" in state_text:
                            action = state_text[state_text.find("(")+1:state_text.find(")")]
                            display_text = f"Playing minigame\n{action}"
                        else:
                            display_text = state_text
                    else:
                        display_text = state_text
                    
                    self.state_display_label.config(text=display_text)
            except:
                pass

    def lower_graphics(self):
        print("Lowering graphics settings...")
        self.set_state("Lowering graphics")
        for i in range(12):
            if not self.running:
                print("Graphics lowering interrupted")
                return
            pydirectinput.keyDown('shift')
            time.sleep(0.02)
            pydirectinput.press('f10')
            time.sleep(0.02)
            pydirectinput.keyUp('shift')
            time.sleep(0.06)
            print(f"Pressed SHIFT+F10 ({i+1}/12)")
        print("Graphics lowering complete")
        time.sleep(0.5)

    def smooth_mouse_move(self, target_x, target_y, duration=0.02, steps=8):
        import pyautogui
        current_x, current_y = pyautogui.position()
        dx = target_x - current_x
        dy = target_y - current_y
        start_time = time.time()
        for i in range(steps + 1):
            progress = i / steps
            new_x = int(current_x + dx * progress)
            new_y = int(current_y + dy * progress)
            pydirectinput.moveTo(new_x, new_y)
            elapsed = time.time() - start_time
            expected_elapsed = (duration / (steps + 1)) * (i + 1)
            sleep_time = max(0, expected_elapsed - elapsed)
            time.sleep(sleep_time)
        pydirectinput.moveTo(target_x, target_y)

    def enable_camera_mode(self):
        print("Enabling camera mode...")
        self.set_state("Enabling camera mode")
        if not self.running:
            return
        camera_x = self.window.right - 35
        camera_y = self.window.top + 35
        pydirectinput.moveTo(camera_x, camera_y)
        time.sleep(0.01)
        import random
        for _ in range(1):
            jitter_x = camera_x + random.randint(-1, 1)
            jitter_y = camera_y + random.randint(-1, 1)
            pydirectinput.moveTo(jitter_x, jitter_y)
            time.sleep(0.01)
        if not self.running:
            return
        pydirectinput.click()
        print(f"Clicked camera icon at ({camera_x}, {camera_y})")
        time.sleep(0.3)
        if not self.running:
            return
        center_x = self.window.left + (self.window.width // 2)
        center_y = self.window.top + (self.window.height // 2)
        pydirectinput.moveTo(center_x, center_y)
        time.sleep(0.1)
        if not self.running:
            return
        import random
        for _ in range(1):
            jitter_x = center_x + random.randint(-1, 1)
            jitter_y = center_y + random.randint(-1, 1)
            pydirectinput.moveTo(jitter_x, jitter_y)
            time.sleep(0.01)
        print("Camera mode enabled")

    def detect_menu_button(self, sct):
        scan_width = 200
        scan_height = 60
        scan_x = self.window.left + (self.window.width // 2) - (scan_width // 2)
        scan_y = self.window.top + 10
        menu_region = {
            'top': scan_y,
            'left': scan_x,
            'width': scan_width,
            'height': scan_height
        }
        screenshot = np.array(sct.grab(menu_region))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if 50 < area < 2000:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                if 1.5 < aspect_ratio < 5.0:
                    center_x = scan_x + x + w // 2
                    center_y = scan_y + y + h // 2
                    return (center_x, center_y)
        return (self.window.left + self.window.width // 2, self.window.top + 30)

    def detect_search_field(self, sct):
        scan_width = 800
        scan_height = 500
        scan_x = self.window.left + (self.window.width // 2) - (scan_width // 2)
        scan_y = self.window.top + 150
        search_region = {
            'top': scan_y,
            'left': scan_x,
            'width': scan_width,
            'height': scan_height
        }
        screenshot = np.array(sct.grab(search_region))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        lower_dark = np.array([0, 0, 0])
        upper_dark = np.array([180, 255, 50])
        mask = cv2.inRange(hsv, lower_dark, upper_dark)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        best_match = None
        best_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 8000:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                if aspect_ratio > 15.0 and h > 20 and h < 80:
                    if area > best_area:
                        best_area = area
                        center_x = scan_x + x + w // 2
                        center_y = scan_y + y + h // 2
                        best_match = (center_x, center_y)
                        print(f"Found search field candidate: area={area}, w={w}, h={h}, ratio={aspect_ratio:.1f}")
        if best_match:
            print(f"Search field detected with area {best_area}")
            return best_match
        fallback_x = self.window.left + (self.window.width // 2)
        fallback_y = self.window.top + 315
        print(f"Search field not detected, using fallback: ({fallback_x}, {fallback_y})")
        return (fallback_x, fallback_y)

    def enable_blur(self):
        print("Enabling blur...")
        self.set_state("Enabling blur")
        if not self.running:
            return
        sct = mss.mss()
        menu_pos = self.detect_menu_button(sct)
        if menu_pos:
            menu_x, menu_y = menu_pos
            print(f"Menu button detected at ({menu_x}, {menu_y})")
        else:
            menu_x = self.window.left + (self.window.width // 2)
            menu_y = self.window.top + 30
            print(f"Using fallback menu position: ({menu_x}, {menu_y})")
        if not self.running:
            sct.__exit__(None, None, None)
            return
        pydirectinput.moveTo(menu_x, menu_y)
        time.sleep(0.01)
        import random
        for _ in range(1):
            jitter_x = menu_x + random.randint(-1, 1)
            jitter_y = menu_y + random.randint(-1, 1)
            pydirectinput.moveTo(jitter_x, jitter_y)
            time.sleep(0.01)
        if not self.running:
            sct.__exit__(None, None, None)
            return
        pydirectinput.click()
        print(f"Clicked menu button at ({menu_x}, {menu_y})")
        time.sleep(0.8)
        if not self.running:
            sct.__exit__(None, None, None)
            return
        search_pos = self.detect_search_field(sct)
        sct.__exit__(None, None, None)
        if search_pos:
            search_x, search_y = search_pos
            print(f"Search field detected at ({search_x}, {search_y})")
        else:
            search_x = self.window.left + (self.window.width // 2)
            search_y = self.window.top + 150
            print(f"Using fallback search position: ({search_x}, {search_y})")
        if not self.running:
            return
        pydirectinput.moveTo(search_x, search_y)
        time.sleep(0.01)
        import random
        for _ in range(1):
            jitter_x = search_x + random.randint(-1, 1)
            jitter_y = search_y + random.randint(-1, 1)
            pydirectinput.moveTo(jitter_x, jitter_y)
            time.sleep(0.01)
        if not self.running:
            return
        pydirectinput.click()
        print(f"Clicked search field at ({search_x}, {search_y})")
        time.sleep(0.3)
        if not self.running:
            return
        pydirectinput.write("madebyelju", interval=0.01)
        print("Typed 'madebyelju' in search field")
        time.sleep(0.3)
        if not self.running:
            return
        center_x = self.window.left + (self.window.width // 2)
        center_y = self.window.top + (self.window.height // 2)
        pydirectinput.moveTo(center_x, center_y)
        print(f"Cursor returned to center at ({center_x}, {center_y})")
        time.sleep(0.2)
        print("Blur enabled")
    def rapid_key_press(self):
        print("Equipping rod")
        self.set_state("Equipping rod")
        self.focus_roblox()
        time.sleep(0.01)
        pydirectinput.press('2')
        time.sleep(0.01)
        pydirectinput.press('1')
        time.sleep(0.01)
        print("Rod equipped")

    def debug_save_screenshot_from_sct(self, sct):
        try:
            screenshot = np.array(sct.grab(self.fish_bar_roi))
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            temp_dir = os.getenv("TEMP", "c:\\temp")
            out_path = os.path.join(temp_dir, "debug_fish_bar.png")
            cv2.imwrite(out_path, screenshot)
            print(f"Debug screenshot saved to {out_path}")
        except Exception as e:
            print(f"Error saving debug screenshot: {e}")

    def debug_save_screenshot_manual(self):
        """Manual debug screenshot (for testing only)."""
        sct = mss.mss()
        screenshot = np.array(sct.grab(self.fish_bar_roi))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        out_path = os.path.join(os.getenv("TEMP", "c:\\temp"), "debug_fish_bar_manual.png")
        cv2.imwrite(out_path, screenshot)
        print(f"Manual screenshot saved to {out_path}")
        sct.__exit__(None, None, None)

if __name__ == "__main__":
    macro = FischMacro()
    try:
        macro.overlay.mainloop()
    except KeyboardInterrupt:
        print("Exiting...")
        macro.auto_save_latest()
        macro.stop_macro()