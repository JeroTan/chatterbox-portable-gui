"""
Reusable Dropdown Component
Like a React component - pass props, get callbacks!
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, List


class DropdownComponent:
    """
    Reusable searchable dropdown with grid layout
    
    Usage (like React):
        dropdown = DropdownComponent(
            parent=frame,
            items=["Item 1", "Item 2", "Item 3"],
            label="Select Item:",
            default_value="Item 1",
            on_select=handle_selection,
            columns=3  # Grid columns (1 = list mode, 3 = grid mode)
        )
    """
    
    def __init__(
        self,
        parent,
        items: List[str],
        label: str = "Select:",
        default_value: str = "",
        on_select: Optional[Callable[[str], None]] = None,
        button_width: int = 35,
        popup_width: int = 500,
        popup_height: int = 350,
        columns: int = 3
    ):
        """
        Props:
            parent: Parent widget
            items: List of choices
            label: Label text
            default_value: Initial value
            on_select: Callback when item selected (like onChange in React)
            button_width: Width of button
            popup_width: Popup width
            popup_height: Popup height
            columns: Grid columns (1=list, 3=grid)
        """
        self.items = items
        self.on_select = on_select
        self.popup_width = popup_width
        self.popup_height = popup_height
        self.columns = columns
        self.picker_window = None
        
        # Container frame
        self.frame = ttk.Frame(parent)
        
        # Label + Button
        ttk.Label(self.frame, text=label).pack(side=tk.LEFT, padx=(0, 10))
        
        self.selected_var = tk.StringVar(value=default_value or (items[0] if items else ""))
        
        self.button = ttk.Button(
            self.frame,
            textvariable=self.selected_var,
            command=self._show_picker,
            width=button_width
        )
        self.button.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _show_picker(self):
        """Show the dropdown overlay"""
        if self.picker_window:
            self._close_picker()
            return
        
        # Create toplevel window
        self.picker_window = tk.Toplevel(self.frame)
        self.picker_window.overrideredirect(True)
        
        # Position below button
        button_x = self.button.winfo_rootx()
        button_y = self.button.winfo_rooty() + self.button.winfo_height()
        self.picker_window.geometry(f"{self.popup_width}x{self.popup_height}+{button_x}+{button_y}")
        
        # Border
        main_frame = ttk.Frame(self.picker_window, relief=tk.SOLID, borderwidth=1)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search box
        search_frame = ttk.Frame(main_frame, padding="5")
        search_frame.pack(fill=tk.X)
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(fill=tk.X)
        search_entry.insert(0, "🔍 Type to search...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) if search_entry.get().startswith("🔍") else None)
        
        # Scrollable container
        list_container = ttk.Frame(main_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        canvas = tk.Canvas(list_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Store refs for filtering
        self.scrollable_frame = scrollable_frame
        self.search_var = search_var
        
        # Create buttons
        self._populate_items()
        
        # Search functionality
        search_var.trace_add("write", lambda *args: self._filter_items())
        
        # Bind events
        self.picker_window.bind("<FocusOut>", lambda e: self._close_picker())
        self.picker_window.focus_set()
    
    def _populate_items(self):
        """Populate items in grid or list layout"""
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get filtered items
        search_text = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        if search_text.startswith("🔍"):
            search_text = ""
        
        filtered = [item for item in self.items if search_text in item.lower()]
        
        if not filtered:
            ttk.Label(
                self.scrollable_frame,
                text="🔍 No items found",
                font=("Segoe UI", 10),
                foreground="gray"
            ).pack(pady=20)
            return
        
        # Grid layout
        row_frame = None
        buttons_in_row = 0
        
        for i, item in enumerate(filtered):
            # Create new row if needed
            if buttons_in_row == 0:
                row_frame = ttk.Frame(self.scrollable_frame)
                row_frame.pack(fill=tk.X, pady=2, padx=2)
                # Configure columns
                for col in range(self.columns):
                    row_frame.grid_columnconfigure(col, weight=1, uniform="button")
            
            btn = tk.Button(
                row_frame,
                text=item,
                command=lambda v=item: self._select_item(v),
                wraplength=130,
                justify=tk.CENTER,
                relief=tk.RAISED,
                borderwidth=1,
                padx=8,
                pady=5,
                width=15,
                anchor=tk.CENTER
            )
            btn.grid(row=0, column=buttons_in_row, padx=3, pady=2, sticky="nsew")
            
            buttons_in_row += 1
            if buttons_in_row >= self.columns:
                buttons_in_row = 0
    
    def _filter_items(self):
        """Re-populate with filtered items"""
        self._populate_items()
    
    def _select_item(self, value: str):
        """Handle selection (like onClick in React)"""
        self.selected_var.set(value)
        self._close_picker()
        
        if self.on_select:
            self.on_select(value)
    
    def _close_picker(self):
        """Close the dropdown"""
        if self.picker_window:
            self.picker_window.destroy()
            self.picker_window = None
    
    def get_value(self) -> str:
        """Get current value"""
        return self.selected_var.get()
    
    def set_value(self, value: str):
        """Set the value"""
        if value in self.items:
            self.selected_var.set(value)
