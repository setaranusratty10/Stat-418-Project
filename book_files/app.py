# app.py – Book-to-Book Content-Based Recommender (Python Shiny)

from shiny import App, ui, reactive, render
import pandas as pd, joblib, matplotlib.pyplot as plt

# ───────────────────────────────────────────
# 1. Load data + fitted k-NN pipeline
# ───────────────────────────────────────────
df     = pd.read_csv("data.csv")
model  = joblib.load("book_knn_model.pkl")

# ───────────────────────────────────────────
# 2. Helper functions
# ───────────────────────────────────────────
def recommend(title: str, k: int = 10,
              min_rating: float = 0.0, max_pages: int = 10_000) -> pd.DataFrame:
    idx = df.index[df["title"].str.lower() == title.lower()]
    if idx.empty:
        return pd.DataFrame()
    vec   = model["prep"].transform(df.iloc[[idx[0]]])
    _, ix = model["knn"].kneighbors(vec, n_neighbors=k + 1)
    recs  = (df.iloc[ix[0][1:]]
               .query("avg_rating >= @min_rating and num_pages <= @max_pages")
               .reset_index(drop=True))
    return recs

# ───────────────────────────────────────────
# 3. UI
# ───────────────────────────────────────────
app_ui = ui.page_fluid(
    ui.tags.style(".container-sm{max-width:800px}"),

    ui.div(                       # 1️⃣ children first …
        ui.h2("📚 Book-to-Book Recommender"),

        ui.input_selectize(
            "title", "Choose a book",
            choices=sorted(df["title"].unique()),
            multiple=False,
            options={"placeholder": "Start typing a title…"}
        ),

        ui.input_slider("k", "How many similar books?", 3, 20, 10),

        ui.div(
            ui.input_slider("min_rating", "Min. average rating ★",
                            0.0, 5.0, 0.0, step=0.1, width="200px"),
            ui.input_slider("max_pages", "Max. pages",
                            50, 1500, 1500, width="200px"),
            class_="d-flex gap-3 mb-3"
        ),

        ui.div(
            ui.output_plot("genre_plot", height="350px"),
            class_="mb-4"
        ),

        ui.output_ui("recs"),
        class_="container-sm"     # 2️⃣ keyword argument last
    )
)


# ───────────────────────────────────────────
# 4. Server
# ───────────────────────────────────────────
def server(input, output, session):

    @reactive.Calc
    def rec_df():
        if not input.title():
            return pd.DataFrame()
        return recommend(input.title(), input.k(),
                         input.min_rating(), input.max_pages())

    # genre plot
    @output
    @render.plot
    def genre_plot():
        df_out = rec_df()
        fig, ax = plt.subplots(figsize=(5, 3.5))

        if df_out.empty:
            ax.axis("off")
            ax.text(0.5, 0.5, "No data", ha="center", va="center")
            return fig

    # Top 10 genres by frequency
        counts = (df_out["genres"]
              .str.split(",").explode().str.strip()
              .value_counts().head(10))

    # Convert to % of recommendations
        pct = counts / counts.sum() * 100

    # Horizontal bar chart
        ax.barh(counts.index[::-1], counts.values[::-1], color="#3182bd")  # blue tone
        ax.set_xlabel("Number of recommended books")
        ax.set_title("Top genres among recommendations")
        ax.invert_yaxis()                      # largest on top

    # Show count + % at end of each bar
        for y, (n, p) in enumerate(zip(counts.values[::-1], pct.values[::-1])):
            ax.text(n + 0.2, y, f"{n}  ({p:.0f}%)", va="center")

        fig.tight_layout()
        return fig

    # Recommendation cards (title = link)
    # ────────────────────────────────
    @output
    @render.ui
    def recs():
        df_out = rec_df()
        if df_out.empty:
            return ui.p("No recommendations meet those filters.",
                        class_="text-muted")

        cards = []
        for _, row in df_out.iterrows():
            # safely fetch the URL (may be NaN)
            url_val = row.get("url", None)

            # hyperlink the title; opens in a new tab
            title_link = ui.a(
                row.title,
                href=url_val if pd.notna(url_val) else "#",
                target="_blank",
                rel="noopener"        # security best-practice
                # omit text-decoration-none so you can SEE the link
            )

            body = ui.div(
                ui.strong(title_link, class_="mb-1"),
                ui.p(row.author, class_="text-muted small mb-1"),
                ui.p(f"⭐ {row.avg_rating:.2f} • {row.num_pages} pp",
                     class_="small mb-0"),
            )

            cards.append(
                ui.card(
                    body,
                    class_="p-3 shadow-sm",
                    style="min-width:260px; max-width:340px;"
                )
            )

        return ui.div(*cards, class_="d-flex flex-wrap gap-3")    
# ───────────────────────────────────────────
app = App(app_ui, server)

