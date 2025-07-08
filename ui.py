# ui.py
import tkinter as tk
from tkinter import messagebox, ttk
from bot import BasicBot

class TradingUI:
    def __init__(self, root):
        self.bot = BasicBot()
        self.root = root
        self.root.title("Binance Futures Trading Bot")
        self.root.geometry("700x550")

        self.create_widgets()
        self.setup_order_history()
        self.create_clear_button()

    def create_widgets(self):
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Symbol (e.g., BTCUSDT)").grid(row=0, column=0, sticky="w")
        self.symbol_entry = tk.Entry(form_frame)
        self.symbol_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Side").grid(row=1, column=0, sticky="w")
        self.side_combo = ttk.Combobox(form_frame, values=["BUY", "SELL"], state="readonly")
        self.side_combo.grid(row=1, column=1)
        self.side_combo.current(0)

        tk.Label(form_frame, text="Order Type").grid(row=2, column=0, sticky="w")
        self.type_combo = ttk.Combobox(form_frame, values=["MARKET", "LIMIT"], state="readonly")
        self.type_combo.grid(row=2, column=1)
        self.type_combo.current(0)
        self.type_combo.bind("<<ComboboxSelected>>", self.toggle_price_field)

        tk.Label(form_frame, text="Quantity").grid(row=3, column=0, sticky="w")
        self.quantity_entry = tk.Entry(form_frame)
        self.quantity_entry.grid(row=3, column=1)

        tk.Label(form_frame, text="Price (LIMIT only)").grid(row=4, column=0, sticky="w")
        self.price_entry = tk.Entry(form_frame)
        self.price_entry.grid(row=4, column=1)

        tk.Button(form_frame, text="Place Order", command=self.place_order).grid(row=5, column=0, columnspan=2, pady=10)

    def toggle_price_field(self, event=None):
        if self.type_combo.get() == "MARKET":
            self.price_entry.config(state='disabled')
        else:
            self.price_entry.config(state='normal')

    def setup_order_history(self):
        tk.Label(self.root, text="Order History").pack()
        columns = ("Symbol", "Side", "Type", "Qty", "Price", "Status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        self.tree.pack(pady=10)

    def create_clear_button(self):
        btn_clear = tk.Button(self.root, text="Clear History", command=self.clear_history, bg="red", fg="white")
        btn_clear.pack(pady=5)

    def clear_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def place_order(self):
        try:
            symbol = self.symbol_entry.get().strip().upper()
            side = self.side_combo.get().strip().upper()
            order_type = self.type_combo.get().strip().upper()
            quantity = float(self.quantity_entry.get().strip())
            price = self.price_entry.get().strip()

            if order_type == "LIMIT":
                if price == "":
                    raise ValueError("Price is required for LIMIT order.")
                price = float(price)
            else:
                price = None

            self.bot.place_order(symbol, side, order_type, quantity, price)

            self.tree.insert("", "end", values=(
                symbol, side, order_type, quantity, price if price else "-", "FILLED"
            ))

            messagebox.showinfo("Success", "Order placed successfully (mock)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to place order:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingUI(root)
    root.mainloop()
