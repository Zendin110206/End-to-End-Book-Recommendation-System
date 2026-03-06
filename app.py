import os
import sys
import html
import pickle
import numpy as np
import streamlit as st

from books_recommender.logger.log import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.pipeline.training_pipeline import TrainingPipeline
from books_recommender.exception.exception_handler import AppException


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="BookFlix | Books Recommender",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# CUSTOM CSS
# =========================
def inject_custom_css():
    st.markdown("""
    <style>
    /* ===== Global ===== */
    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(120, 119, 198, 0.18), transparent 25%),
            radial-gradient(circle at top right, rgba(255, 99, 132, 0.12), transparent 20%),
            linear-gradient(180deg, #0B1020 0%, #090D18 45%, #05070D 100%);
        color: #F8FAFC;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* ===== Hero ===== */
    .hero-wrapper {
        padding: 2rem 2rem 1.6rem 2rem;
        border-radius: 24px;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03)),
            linear-gradient(135deg, rgba(99,102,241,0.20), rgba(236,72,153,0.10));
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
        backdrop-filter: blur(18px);
        margin-bottom: 1.25rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.38rem 0.85rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        color: #D1D5DB;
        font-size: 0.86rem;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.05;
        margin: 0;
        color: #FFFFFF;
        letter-spacing: -0.03em;
    }

    .hero-gradient {
        background: linear-gradient(90deg, #A78BFA 0%, #F472B6 50%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        margin-top: 0.9rem;
        font-size: 1.02rem;
        color: #CBD5E1;
        line-height: 1.75;
        max-width: 900px;
    }

    /* ===== Premium Container ===== */
    .glass-card {
        padding: 1.2rem 1.2rem 1rem 1.2rem;
        border-radius: 22px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 35px rgba(0,0,0,0.28);
        backdrop-filter: blur(14px);
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #FFFFFF;
    }

    .section-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 1rem;
    }

    /* ===== Stat Cards ===== */
    .stat-card {
        padding: 1rem 1.1rem;
        border-radius: 20px;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        min-height: 110px;
    }

    .stat-label {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }

    .stat-value {
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.8rem;
        line-height: 1.1;
    }

    .stat-foot {
        color: #CBD5E1;
        font-size: 0.86rem;
        margin-top: 0.4rem;
    }

    /* ===== Book Cards ===== */
    .book-card {
        position: relative;
        border-radius: 22px;
        overflow: hidden;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
        transition: all 0.25s ease;
        min-height: 370px;
    }

    .book-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 24px 55px rgba(0,0,0,0.42);
        border: 1px solid rgba(255,255,255,0.16);
    }

    .book-rank {
        position: absolute;
        top: 14px;
        left: 14px;
        z-index: 2;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        color: #FFFFFF;
        background: linear-gradient(90deg, #7C3AED, #EC4899);
        box-shadow: 0 10px 25px rgba(124,58,237,0.35);
    }

    .book-cover {
        width: 100%;
        height: 270px;
        object-fit: cover;
        display: block;
        background: #111827;
    }

    .book-cover-placeholder {
        width: 100%;
        height: 270px;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            linear-gradient(135deg, rgba(99,102,241,0.22), rgba(236,72,153,0.18));
        color: #E2E8F0;
        font-weight: 700;
        font-size: 1rem;
        text-align: center;
        padding: 1rem;
    }

    .book-body {
        padding: 1rem 1rem 1.1rem 1rem;
    }

    .book-title {
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.45;
        min-height: 3rem;
        margin-bottom: 0.4rem;
    }

    .book-meta {
        color: #94A3B8;
        font-size: 0.86rem;
    }

    /* ===== Spotlight ===== */
    .spotlight-card {
        display: flex;
        gap: 1rem;
        align-items: center;
        padding: 1rem;
        border-radius: 22px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 0.4rem;
    }

    .spotlight-cover {
        width: 110px;
        height: 155px;
        object-fit: cover;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.10);
        background: #111827;
    }

    .spotlight-placeholder {
        width: 110px;
        height: 155px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0.6rem;
        background:
            linear-gradient(135deg, rgba(99,102,241,0.22), rgba(236,72,153,0.18));
        border: 1px solid rgba(255,255,255,0.10);
        color: #E2E8F0;
        font-weight: 700;
        font-size: 0.9rem;
    }

    .spotlight-kicker {
        color: #A5B4FC;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    .spotlight-title {
        color: #FFFFFF;
        font-size: 1.4rem;
        font-weight: 800;
        line-height: 1.3;
        margin-bottom: 0.35rem;
    }

    .spotlight-text {
        color: #CBD5E1;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* ===== Streamlit Native Components ===== */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 14px !important;
        min-height: 54px !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] input {
        color: #FFFFFF !important;
    }

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.10);
        background: linear-gradient(90deg, #7C3AED, #EC4899);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.96rem;
        box-shadow: 0 14px 30px rgba(124,58,237,0.28);
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 18px 34px rgba(124,58,237,0.36);
    }

    .stAlert {
        border-radius: 16px;
    }

    hr {
        border-color: rgba(255,255,255,0.08);
    }

    .footer-note {
        text-align: center;
        color: #64748B;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


# =========================
# CACHED LOADING
# =========================
@st.cache_resource(show_spinner=False)
def load_pickle_object(path: str):
    with open(path, "rb") as file_obj:
        return pickle.load(file_obj)


@st.cache_resource(show_spinner=False)
def load_recommendation_assets(model_path, pivot_path, rating_path, book_names_path):
    model = load_pickle_object(model_path)
    book_pivot = load_pickle_object(pivot_path)
    final_rating = load_pickle_object(rating_path)

    if book_names_path and os.path.exists(book_names_path):
        book_names = load_pickle_object(book_names_path)
    else:
        book_names = list(book_pivot.index)

    title_to_image = (
        final_rating[["title", "image_url"]]
        .dropna(subset=["title"])
        .drop_duplicates(subset=["title"])
        .set_index("title")["image_url"]
        .to_dict()
    )

    return model, book_pivot, final_rating, book_names, title_to_image


# =========================
# CORE CLASS
# =========================
class Recommendation:
    def __init__(self, app_config=None):
        try:
            if app_config is None:
                app_config = AppConfiguration()

            self.recommendation_config = app_config.get_recommendation_config()

        except Exception as e:
            raise AppException(e, sys) from e

    def _resolve_book_names_path(self):
        try:
            candidates = [
                os.path.join("artifacts", "serialized_object", "book_names.pkl"),
                getattr(self.recommendation_config, "book_names_serialized_objects", None),
            ]

            for path in candidates:
                if path and os.path.exists(path):
                    return path

            return None

        except Exception as e:
            raise AppException(e, sys) from e

    def load_assets(self):
        try:
            model_path = self.recommendation_config.trained_model_path
            pivot_path = self.recommendation_config.book_pivot_serialized_objects
            rating_path = self.recommendation_config.final_rating_serialized_objects
            book_names_path = self._resolve_book_names_path()

            return load_recommendation_assets(
                model_path,
                pivot_path,
                rating_path,
                book_names_path
            )

        except Exception as e:
            raise AppException(e, sys) from e

    def recommend_book(self, selected_book, n_recommendations=5):
        try:
            model, book_pivot, _, _, title_to_image = self.load_assets()

            if selected_book not in book_pivot.index:
                raise ValueError(f"Buku '{selected_book}' tidak ditemukan di data model.")

            book_id = np.where(book_pivot.index == selected_book)[0][0]

            # Ambil lebih banyak kandidat supaya setelah buang buku asli + duplikat
            # tetap tersisa minimal 5 rekomendasi
            total_books = len(book_pivot.index)
            safe_neighbors = min(max(n_recommendations + 10, 10), total_books)

            distances, suggestions = model.kneighbors(
                book_pivot.iloc[book_id, :].values.reshape(1, -1),
                n_neighbors=safe_neighbors
            )

            suggestions = suggestions.flatten().tolist()

            recommended_items = []
            seen_titles = set()

            for idx in suggestions:
                title = book_pivot.index[idx]

                if title == selected_book:
                    continue

                if title in seen_titles:
                    continue

                seen_titles.add(title)

                recommended_items.append({
                    "title": title,
                    "poster_url": title_to_image.get(title, None)
                })

                if len(recommended_items) == n_recommendations:
                    break

            return recommended_items

        except Exception as e:
            raise AppException(e, sys) from e

    def train_engine(self):
        try:
            trainer = TrainingPipeline()
            trainer.start_training_pipeline()

            # clear cache setelah training agar artifact terbaru dipakai
            load_pickle_object.clear()
            load_recommendation_assets.clear()

            logging.info("Model trained successfully via UI!")
            return True

        except Exception as e:
            raise AppException(e, sys) from e


# =========================
# UI HELPERS
# =========================
def render_hero():
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-badge">Collaborative Filtering • KNN Model • Premium UI</div>
        <h1 class="hero-title">
            Discover your next<br>
            <span class="hero-gradient">favorite book</span>
        </h1>
        <div class="hero-subtitle">
            Sistem rekomendasi buku dengan tampilan modern, minimalis, dan profesional.
            Cari buku yang kamu suka, lalu biarkan model menemukan judul lain yang paling relevan untukmu.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stats(total_books, total_ratings):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Catalog Size</div>
            <div class="stat-value">{total_books:,}</div>
            <div class="stat-foot">Jumlah judul yang bisa dipilih</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Processed Records</div>
            <div class="stat-value">{total_ratings:,}</div>
            <div class="stat-foot">Data rating/final dataset siap rekomendasi</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">UI Style</div>
            <div class="stat-value">Premium</div>
            <div class="stat-foot">Dark, clean, minimal, presentation-ready</div>
        </div>
        """, unsafe_allow_html=True)


def render_spotlight(selected_title, poster_url):
    safe_title = html.escape(selected_title)

    if poster_url:
        cover_html = f'<img src="{poster_url}" class="spotlight-cover" alt="{safe_title}">'
    else:
        cover_html = '<div class="spotlight-placeholder">No Cover</div>'

    st.markdown(f"""
    <div class="spotlight-card">
        {cover_html}
        <div>
            <div class="spotlight-kicker">Selected Book</div>
            <div class="spotlight-title">{safe_title}</div>
            <div class="spotlight-text">
                Ini adalah buku acuan yang kamu pilih. Model akan mencari buku lain
                yang paling mirip berdasarkan pola rating pengguna.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_book_card(rank, title, poster_url):
    safe_title = html.escape(str(title))

    if poster_url:
        cover_part = f'<img src="{poster_url}" class="book-cover" alt="{safe_title}">'
    else:
        cover_part = '<div class="book-cover-placeholder">Cover<br>Not Available</div>'

    st.markdown(f"""
    <div class="book-card">
        <div class="book-rank">#{rank}</div>
        {cover_part}
        <div class="book-body">
            <div class="book-title">{safe_title}</div>
            <div class="book-meta">Recommended for you</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_recommendations(items):
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Top Recommendations</div>
        <div class="section-subtitle">
            Berikut 5 buku yang paling relevan berdasarkan pilihanmu.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    cols = st.columns(5)
    for idx, item in enumerate(items):
        with cols[idx]:
            render_book_card(
                rank=idx + 1,
                title=item["title"],
                poster_url=item["poster_url"]
            )


def init_session_state():
    if "recommended_items" not in st.session_state:
        st.session_state.recommended_items = None

    if "selected_book_last" not in st.session_state:
        st.session_state.selected_book_last = None


# =========================
# MAIN APP
# =========================
def main():
    inject_custom_css()
    init_session_state()

    st.title("")  # placeholder supaya spacing enak
    render_hero()

    try:
        recommender = Recommendation()
        model, book_pivot, final_rating, book_names, title_to_image = recommender.load_assets()

        total_books = len(book_names)
        total_ratings = len(final_rating)

        render_stats(total_books=total_books, total_ratings=total_ratings)
        st.write("")

        # ===== Sidebar =====
        with st.sidebar:
            st.markdown("## ⚙️ Control Panel")
            st.caption("Kelola model dan informasi aplikasi")

            if st.button("Train Recommender System"):
                with st.spinner("Training model sedang berjalan..."):
                    success = recommender.train_engine()

                if success:
                    st.success("Training selesai. Artifact terbaru sudah dimuat.")
                    st.rerun()

            st.markdown("---")
            st.markdown("### 📌 About")
            st.write(
                "Aplikasi ini menggunakan pendekatan collaborative filtering "
                "untuk mencari buku dengan pola preferensi yang mirip."
            )

            st.markdown("### 🧠 Model Flow")
            st.write(
                "Book Selection → Vector Lookup → KNN Similarity Search → Top Recommendations"
            )

            st.markdown("### 💡 UI Goals")
            st.write(
                "Minimalis, premium, gelap, modern, dan cocok untuk demo portfolio atau presentasi."
            )

        # ===== Main Search Area =====
        left_col, right_col = st.columns([1.35, 1], gap="large")

        with left_col:
            st.markdown("""
            <div class="glass-card">
                <div class="section-title">Find a Book</div>
                <div class="section-subtitle">
                    Ketik atau pilih buku, lalu tampilkan rekomendasinya.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            with st.form("recommendation_form"):
                selected_book = st.selectbox(
                    "Type or select a book from the dropdown",
                    options=book_names
                )

                submitted = st.form_submit_button("Show Recommendation")

            if submitted:
                with st.spinner("Mencari rekomendasi terbaik untukmu..."):
                    recommended_items = recommender.recommend_book(
                        selected_book=selected_book,
                        n_recommendations=5
                    )

                st.session_state.recommended_items = recommended_items
                st.session_state.selected_book_last = selected_book

        with right_col:
            st.markdown("""
            <div class="glass-card">
                <div class="section-title">Experience</div>
                <div class="section-subtitle">
                    Desain dibuat seperti produk modern: clean, dark, visual, dan fokus pada konten.
                </div>
            </div>
            """, unsafe_allow_html=True)

            current_selected = st.session_state.selected_book_last or (book_names[0] if len(book_names) > 0 else "No Book")
            current_poster = title_to_image.get(current_selected)

            render_spotlight(
                selected_title=current_selected,
                poster_url=current_poster
            )

        st.write("")

        # ===== Result Area =====
        if st.session_state.recommended_items:
            render_recommendations(st.session_state.recommended_items)
        else:
            st.info("Pilih sebuah buku lalu tekan **Show Recommendation** untuk menampilkan hasilnya.")

        st.markdown("""
        <div class="footer-note">
            Built with Streamlit • Professional dark UI • Books Recommender System
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        logging.exception("Application error occurred.")
        st.error(f"Terjadi kesalahan pada aplikasi: {e}")


if __name__ == "__main__":
    main()