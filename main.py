import streamlit as st
from config import engine, SessionLocal
from db import create, read_all, delete, update
from models import Base

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db  # oturum boyunca dokunmayacak
    finally:
        db.close()


def app(todo=None):
    with st.container(border=True):
        st.title("ToDo List App with Streamlit")
        with st.form("todo_form", clear_on_submit=True):
            title = st.text_input("Görev Başlığı: ")
            description = st.text_area("Görev Açıklaması: ")
            btn_ekle = st.form_submit_button("Görev Ekle")
            if btn_ekle and title:
                db = next(get_db())
                create(db, title=title, description=description)
                st.success(f"'{title}' görevi eklendi")
                st.rerun()
        st.divider()
        st.header("Görev Listesi")
        db = next(get_db())
        todos = read_all(db)
        if todos:
            for todo in todos:
                c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
                with c1:
                    st.write(f"**{todo.id}**")
                with c2:
                    st.write(todo.title)
                with c3:
                    if todo.completed:
                        st.success("Tamamlandı")
                    else:
                        st.info("Aktif")
                with c4:
                    if st.button("Sil", key=f"del_{todo.id}", use_container_width=True):
                        delete(db, todo_id=todo.id)
                        st.rerun()
                    if st.button("Güncelle", key=f"toggle_{todo.id}", use_container_width=True):
                        update(db, todo.id, completed=not todo.completed)
                        st.rerun()
        else:
            st.write("Görev bulunamadı.")


if __name__ == "__main__":
    app()
