import requests
import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
from datetime import datetime
import webbrowser

# --- Replace with your NewsAPI key ---
API_KEY = "6a64fb3e5f7448a18a613dd57473d8dd"

# Color Schemes
DARK_THEME = {
    'bg': '#0f0f23',
    'secondary_bg': '#1a1a2e',
    'card_bg': '#16213e',
    'card_hover': '#1f2d50',
    'accent': '#00d4ff',
    'accent_hover': '#00b8e6',
    'text': '#e4e4e7',
    'text_secondary': '#a1a1aa',
    'border': '#2d3748',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

current_theme = DARK_THEME
is_loading = False

def create_gradient_header(canvas, width, height):
    """Create a beautiful gradient background"""
    steps = 100
    for i in range(steps):
        # Calculate color transition
        ratio = i / steps
        r1, g1, b1 = int('66', 16), int('7e', 16), int('ea', 16)
        r2, g2, b2 = int('76', 16), int('4b', 16), int('a2', 16)
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        y1 = int(height * i / steps)
        y2 = int(height * (i + 1) / steps)
        canvas.create_rectangle(0, y1, width, y2, fill=color, outline=color)

def fetch_news():
    global is_loading
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a topic to search!")
        return
    
    if is_loading:
        return
    
    # Show loading state
    is_loading = True
    search_btn.update_text("⏳ Searching...")
    search_btn.set_state("disabled")
    loading_label.config(text="🔍 Fetching latest news...")
    loading_label.pack(pady=20)
    
    # Clear previous results
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    # Run in thread to prevent UI freeze
    thread = threading.Thread(target=fetch_news_thread, args=(query,))
    thread.daemon = True
    thread.start()

def fetch_news_thread(query):
    global is_loading
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}&language=en&pageSize=20&sortBy=publishedAt"
        response = requests.get(url, timeout=10)
        data = response.json()

        # Update UI in main thread
        root.after(0, lambda: display_results(data))
    except Exception as e:
        root.after(0, lambda: show_error(str(e)))
    finally:
        is_loading = False
        root.after(0, lambda: search_btn.update_text("🔍 Search"))
        root.after(0, lambda: search_btn.set_state("normal"))
        root.after(0, lambda: loading_label.pack_forget())

def show_error(error_msg):
    messagebox.showerror("Error", f"Failed to fetch news:\n{error_msg}")

def display_results(data):
    if data.get("status") != "ok":
        messagebox.showerror("Error", "Failed to fetch news. Try again.")
        return

    articles = data.get("articles", [])
    if not articles:
        no_results = tk.Label(scrollable_frame, text="📭 No news found for this topic", 
                            font=("Segoe UI", 14), bg=current_theme['bg'], 
                            fg=current_theme['text_secondary'])
        no_results.pack(pady=50)
        return

    for idx, article in enumerate(articles):
        create_article_card(article, idx)

def create_article_card(article, idx):
    """Create a beautiful, modern article card with hover effects"""
    # Card container
    card = tk.Frame(scrollable_frame, bg=current_theme['card_bg'], 
                   highlightbackground=current_theme['border'], 
                   highlightthickness=1)
    card.pack(fill="x", pady=8, padx=20)
    
    # Add padding frame
    inner_frame = tk.Frame(card, bg=current_theme['card_bg'])
    inner_frame.pack(fill="both", expand=True, padx=20, pady=15)
    
    # Article number badge
    badge = tk.Label(inner_frame, text=f"#{idx+1}", 
                    font=("Segoe UI", 9, "bold"), 
                    bg=current_theme['accent'], 
                    fg=current_theme['bg'],
                    padx=8, pady=2)
    badge.pack(anchor="w", pady=(0, 8))
    
    # Title
    title_text = article.get('title', 'No title')
    if title_text:
        title = tk.Label(inner_frame, text=title_text, 
                        font=("Segoe UI", 13, "bold"), 
                        wraplength=700, 
                        bg=current_theme['card_bg'], 
                        fg=current_theme['text'],
                        justify="left",
                        cursor="hand2")
        title.pack(anchor="w", pady=(0, 10))
        
        # Make title clickable
        url = article.get('url', '')
        if url:
            title.bind("<Button-1>", lambda e, link=url: webbrowser.open(link))
            title.bind("<Enter>", lambda e: title.config(fg=current_theme['accent']))
            title.bind("<Leave>", lambda e: title.config(fg=current_theme['text']))
    
    # Description
    desc_text = article.get('description', 'No description available.')
    if desc_text:
        desc = tk.Label(inner_frame, text=desc_text, 
                       font=("Segoe UI", 10), 
                       wraplength=700, 
                       bg=current_theme['card_bg'], 
                       fg=current_theme['text_secondary'],
                       justify="left")
        desc.pack(anchor="w", pady=(0, 12))
    
    # Bottom info bar
    info_frame = tk.Frame(inner_frame, bg=current_theme['card_bg'])
    info_frame.pack(fill="x", pady=(5, 0))
    
    # Source
    source_name = article.get('source', {}).get('name', 'Unknown')
    source = tk.Label(info_frame, text=f"📰 {source_name}", 
                     font=("Segoe UI", 9), 
                     bg=current_theme['card_bg'], 
                     fg=current_theme['accent'])
    source.pack(side="left")
    
    # Published date
    pub_date = article.get('publishedAt', '')
    if pub_date:
        try:
            date_obj = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime("%b %d, %Y • %I:%M %p")
            date_label = tk.Label(info_frame, text=f"🕒 {formatted_date}", 
                                 font=("Segoe UI", 9), 
                                 bg=current_theme['card_bg'], 
                                 fg=current_theme['text_secondary'])
            date_label.pack(side="right")
        except:
            pass
    
    # Hover effect
    def on_enter(e):
        card.config(bg=current_theme['card_hover'])
        inner_frame.config(bg=current_theme['card_hover'])
        for child in inner_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=current_theme['card_hover'])
            elif isinstance(child, tk.Frame):
                child.config(bg=current_theme['card_hover'])
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Label):
                        subchild.config(bg=current_theme['card_hover'])
    
    def on_leave(e):
        card.config(bg=current_theme['card_bg'])
        inner_frame.config(bg=current_theme['card_bg'])
        for child in inner_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=current_theme['card_bg'])
            elif isinstance(child, tk.Frame):
                child.config(bg=current_theme['card_bg'])
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Label):
                        subchild.config(bg=current_theme['card_bg'])
    
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    inner_frame.bind("<Enter>", on_enter)
    inner_frame.bind("<Leave>", on_leave)

def search_on_enter(event):
    """Trigger search on Enter key"""
    fetch_news()

#

class RoundedButton(tk.Canvas):
    """Custom rounded button with gradient and shadow effects"""
    def __init__(self, parent, text, command, bg_color, hover_color, text_color="white", 
                 width=150, height=45, corner_radius=22, **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height, 
                          bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.text = text
        self.width = width
        self.height = height
        self.is_hovered = False
        
        # Draw the button
        self.draw_button()
        
        # Bind events
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.tag_bind("button", "<Button-1>", self.on_click)
        self.tag_bind("button", "<Enter>", self.on_enter)
        self.tag_bind("button", "<Leave>", self.on_leave)
        
    def draw_button(self):
        """Draw rounded rectangle button with shadow"""
        self.delete("all")
        
        # Shadow effect (offset slightly)
        shadow_color = "#000000"
        self.create_rounded_rect(3, 3, self.width, self.height, 
                                self.corner_radius, fill="#0a0a15", outline="", tags="shadow")
        
        # Main button
        color = self.hover_color if self.is_hovered else self.bg_color
        self.create_rounded_rect(0, 0, self.width-3, self.height-3, 
                                self.corner_radius, fill=color, outline="", tags="button")
        
        # Text
        self.create_text(self.width//2 - 1.5, self.height//2 - 1.5, 
                        text=self.text, fill=self.text_color, 
                        font=("Segoe UI", 12, "bold"), tags="button")
        
        # Shine effect (subtle gradient overlay)
        self.create_rounded_rect(2, 2, self.width-5, self.height//2, 
                                self.corner_radius-2, fill="white", 
                                outline="", tags="shine", stipple="gray25")
        self.itemconfig("shine", state="hidden")
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event=None):
        """Handle button click"""
        if self.command:
            self.command()
    
    def on_enter(self, event=None):
        """Handle mouse enter"""
        self.is_hovered = True
        self.draw_button()
        self.config(cursor="hand2")
    
    def on_leave(self, event=None):
        """Handle mouse leave"""
        self.is_hovered = False
        self.draw_button()
        self.config(cursor="")
    
    def update_text(self, new_text):
        """Update button text"""
        self.text = new_text
        self.draw_button()
    
    def set_state(self, state):
        """Enable or disable the button"""
        if state == "disabled":
            self.unbind("<Button-1>")
            self.tag_unbind("button", "<Button-1>")
            self.itemconfig("button", fill=current_theme['text_secondary'])
        else:
            self.bind("<Button-1>", self.on_click)
            self.tag_bind("button", "<Button-1>", self.on_click)
            self.draw_button()

class RoundedEntry(tk.Frame):
    """Custom rounded entry field"""
    def __init__(self, parent, placeholder="", **kwargs):
        tk.Frame.__init__(self, parent, bg=current_theme['secondary_bg'], 
                         highlightbackground=current_theme['accent'],
                         highlightcolor=current_theme['accent'],
                         highlightthickness=2, bd=0)
        
        self.placeholder = placeholder
        self.placeholder_color = current_theme['text_secondary']
        self.text_color = current_theme['text']
        
        # Create the actual entry widget
        self.entry = tk.Entry(self, 
                             font=("Segoe UI", 13), 
                             bg=current_theme['card_bg'], 
                             fg=self.placeholder_color,
                             insertbackground=current_theme['accent'],
                             relief="flat",
                             bd=0,
                             **kwargs)
        self.entry.pack(fill="both", expand=True, ipady=10, ipadx=15)
        
        # Set placeholder
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.bind('<FocusIn>', self.on_focus_in)
            self.entry.bind('<FocusOut>', self.on_focus_out)
    
    def on_focus_in(self, event):
        """Clear placeholder on focus"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg=self.text_color)
    
    def on_focus_out(self, event):
        """Restore placeholder if empty"""
        if self.entry.get() == '':
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.placeholder_color)
    
    def get(self):
        """Get entry value"""
        value = self.entry.get()
        return "" if value == self.placeholder else value
    
    def bind(self, event, handler):
        """Bind event to entry"""
        self.entry.bind(event, handler)


# --- GUI Setup ---
root = tk.Tk()
root.title("📰 Modern News Explorer")
root.geometry("900x700")
root.config(bg=current_theme['bg'])

# Header with gradient
header_canvas = tk.Canvas(root, height=140, bg=current_theme['bg'], highlightthickness=0)
header_canvas.pack(fill="x")
create_gradient_header(header_canvas, 900, 140)

# App title on gradient
title_label = tk.Label(header_canvas, text="📰 News Explorer", 
                      font=("Segoe UI", 28, "bold"), 
                      bg=current_theme['gradient_start'], 
                      fg="white")
header_canvas.create_window(450, 50, window=title_label)

subtitle_label = tk.Label(header_canvas, text="Discover the latest news from around the world", 
                         font=("Segoe UI", 11), 
                         bg=current_theme['gradient_end'], 
                         fg="white")
header_canvas.create_window(450, 85, window=subtitle_label)

# Search container
search_container = tk.Frame(root, bg=current_theme['secondary_bg'], 
                           highlightbackground=current_theme['border'], 
                           highlightthickness=1)
search_container.pack(pady=20, padx=40, fill="x")

search_inner = tk.Frame(search_container, bg=current_theme['secondary_bg'])
search_inner.pack(pady=15, padx=15, fill="x")

# Search entry with rounded styling
search_entry = RoundedEntry(search_inner, placeholder='Search for news...')
search_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 0))
search_entry.bind('<Return>', search_on_enter)

# Search button with fancy rounded styling
search_btn = RoundedButton(search_inner, 
                          text="🔍 Search",
                          command=fetch_news,
                          bg_color=current_theme['accent'],
                          hover_color=current_theme['accent_hover'],
                          text_color="white",
                          width=140,
                          height=48,
                          corner_radius=24)
search_btn.pack(side=tk.LEFT, padx=(15, 0))

# Loading label
loading_label = tk.Label(root, text="", font=("Segoe UI", 11), 
                        bg=current_theme['bg'], fg=current_theme['accent'])

# Scrollable area with custom styling
canvas = tk.Canvas(root, bg=current_theme['bg'], highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=current_theme['bg'])

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Custom scrollbar styling
style = ttk.Style()
style.theme_use('default')
style.configure("Vertical.TScrollbar", 
               background=current_theme['secondary_bg'],
               troughcolor=current_theme['bg'],
               bordercolor=current_theme['bg'],
               arrowcolor=current_theme['accent'])

canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 20))

# Mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Welcome message
welcome = tk.Label(scrollable_frame, 
                  text="👋 Welcome! Enter a topic above to discover the latest news", 
                  font=("Segoe UI", 12), 
                  bg=current_theme['bg'], 
                  fg=current_theme['text_secondary'])
welcome.pack(pady=50)

root.mainloop()
