from database import SessionLocal, engine, Base
from Domain.Models.restaurant import Restaurant
from Domain.Models.dish import Dish

def seed_data():
    # Створюємо підключення до БД
    db = SessionLocal()
    
    # Перевіряємо, чи є вже ресторани, щоб не дублювати
    if db.query(Restaurant).first():
        print("✅ База даних вже містить інформацію. Заповнення не потрібне.")
        db.close()
        return

    print("⏳ Заповнюємо базу тестовими даними...")

    # 1. Створюємо ресторани
    rest1 = Restaurant(
        name="ТеплийСтіл (Головний)",
        description="Найкраща домашня кухня. Затишно, як у мами.",
        address="вул. Центральна, 1",
        rating=4.9
    )
    rest2 = Restaurant(
        name="Кебаб & Дьонер",
        description="Швидка та ситна вулична їжа.",
        address="вул. Студентська, 15",
        rating=4.7
    )
    
    db.add(rest1)
    db.add(rest2)
    db.commit() # Зберігаємо, щоб отримати їхні ID
    db.refresh(rest1)
    db.refresh(rest2)

    # 2. Створюємо страви для першого ресторану
    dishes = [
        Dish(restaurant_id=rest1.id, name="Борщ український", description="Зі сметаною та пампушками", price=150.00),
        Dish(restaurant_id=rest1.id, name="Котлета по-київськи", description="З картопляним пюре", price=180.00),
        Dish(restaurant_id=rest1.id, name="Сирники", description="З домашнього сиру, подаються з джемом", price=120.00),
        
        # Страви для другого ресторану
        Dish(restaurant_id=rest2.id, name="Дьонер з сиром і маслом", description="Великий і дуже соковитий", price=300.00),
        Dish(restaurant_id=rest2.id, name="Картопля фрі", description="Велика порція з сирним соусом", price=90.00)
    ]

    for dish in dishes:
        db.add(dish)
        
    db.commit()
    print("🎉 База даних успішно заповнена! Можна запускати сервер.")
    db.close()

if __name__ == "__main__":
    seed_data()