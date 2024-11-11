from sqlalchemy.orm import Session  # Veritabanı işlemleri için SQLAlchemy'nin Session sınıfını içe aktarıyoruz.
from models import Todo  # 'Todo' modelini kullanmak için içe aktarıyoruz.


# Tüm görevleri okuma (read) fonksiyonu
def read_all(db: Session):
    return db.query(Todo).all()
    # Veritabanındaki tüm 'Todo' kayıtlarını sorgulayıp bir liste olarak döndürür.


# Tek bir görevi okuma (read) fonksiyonu
def read_one(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()
    # Veritabanında belirli bir 'id' değeriyle eşleşen ilk 'Todo' kaydını döndürür.
    # Bu, kaydı bulamazsa None döndürür.


# Yeni görev oluşturma (create) fonksiyonu
def create(db: Session, title: str, description: str = None):
    new_todo = Todo(title=title, description=description)
    # 'title' ve isteğe bağlı 'description' parametreleriyle yeni bir 'Todo' nesnesi oluşturulur.

    db.add(new_todo)  # Yeni görevi veritabanı oturumuna ekler.
    db.commit()  # Veritabanında değişiklikleri kalıcı hale getirir.
    db.refresh(new_todo)  # Veritabanından güncel veriyi getirerek 'new_todo' nesnesini günceller.

    return new_todo  # Oluşturulan yeni görevi döndürür.


# Var olan bir görevi güncelleme (update) fonksiyonu
def update(db: Session, todo_id: int, title: str = None, description: str = None, completed: bool = None):
    todo = read_one(db, todo_id)  # Güncellenecek görevi 'id' değerine göre bulur.

    if todo:  # Görev bulunursa, verilen parametrelere göre günceller.
        if title:
            todo.title = title
        if description:
            todo.description = description
        if completed is not None:
            todo.completed = completed

        db.commit()  # Güncellemeleri veritabanına uygular.
        db.refresh(todo)  # Güncellenen veriyi alır ve

    return todo  # Güncellenmiş görevi döndürür veya görev bulunamazsa None döner.


# Var olan bir görevi silme (delete) fonksiyonu
def delete(db: Session, todo_id: int):
    todo = read_one(db, todo_id)  # Silinecek görevi 'id' değerine göre bulur.

    if todo:  # Görev bulunursa silme işlemi yapar.
        db.delete(todo)  # Görevi veritabanı oturumundan kaldırır.
        db.commit()  # Değişiklikleri veritabanına uygular.

    return todo  # Silinen görevi döndürür veya görev bulunamazsa None döner.
