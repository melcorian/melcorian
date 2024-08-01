import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from fpdf import FPDF
from datetime import datetime, timedelta

# Constants
API_KEY = "69e65af61aea45b7803fe1b1659d85dd"  # Your NewsAPI key
API_URL = "https://newsapi.org/v2/everything"

# Function to fetch articles from NewsAPI
def fetch_articles(keyword, from_date, to_date):
    params = {
        'apiKey': API_KEY,
        'q': keyword,
        'from': from_date,
        'to': to_date,
        'pageSize': 100,
        'language': 'en'
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data['status'] == 'ok':
            return data['articles']
        else:
            print(f"API error: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None

# Function to create PDF
def save_as_pdf(articles, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for article in articles:
        pdf.cell(200, 10, txt=article['title'], ln=True)
        pdf.cell(200, 10, txt=article['url'], ln=True)
        pdf.ln()
    pdf.output(filename)

# Function to create HTML
def save_as_html(articles, filename):
    with open(filename, 'w') as file:
        file.write('<html><body>\n')
        for article in articles:
            file.write(f'<h2>{article["title"]}</h2>\n')
            file.write(f'<a href="{article["url"]}">{article["url"]}</a><br>\n')
        file.write('</body></html>')

# Main application function
def main():
    def on_search():
        keyword = keyword_entry.get()
        if not keyword:
            messagebox.showerror("Error", "Keyword is required.")
            return

        today = datetime.now()
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

        articles = fetch_articles(keyword, start_date, end_date)
        if not articles:
            messagebox.showinfo("No Articles", "No articles found or there was an error.")
            return
        
        articles_listbox.delete(0, tk.END)
        for i, article in enumerate(articles):
            articles_listbox.insert(tk.END, f"{i+1}. {article['title']}")

        def on_save():
            selected_indices = articles_listbox.curselection()
            if not selected_indices:
                messagebox.showerror("Error", "No articles selected.")
                return
            
            selected_articles = [articles[i] for i in selected_indices]
            file_type = file_type_combobox.get()
            filename = filedialog.asksaveasfilename(defaultextension=f".{file_type}", filetypes=[(f"{file_type.upper()} file", f"*.{file_type}")])
            if filename:
                if file_type == 'pdf':
                    save_as_pdf(selected_articles, filename)
                elif file_type == 'html':
                    save_as_html(selected_articles, filename)
                messagebox.showinfo("Success", f"Articles saved to {filename}")

        save_button = tk.Button(root, text="Save Selected Articles", command=on_save)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    root = tk.Tk()
    root.title("NewsAPI Article Downloader")

    tk.Label(root, text="Keyword:").grid(row=0, column=0, padx=10, pady=10)
    keyword_entry = tk.Entry(root, width=50)
    keyword_entry.grid(row=0, column=1, padx=10, pady=10)

    search_button = tk.Button(root, text="Search Articles", command=on_search)
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

    articles_listbox = tk.Listbox(root, width=80, height=20)
    articles_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    tk.Label(root, text="Save As:").grid(row=3, column=0, padx=10, pady=10)
    file_type_combobox = ttk.Combobox(root, values=['pdf', 'html'])
    file_type_combobox.set('pdf')
    file_type_combobox.grid(row=3, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
