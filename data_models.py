# this one defines Product class - using __slots__ is a specific competency requirement for our project cuz it tells python
# to allocate fixed memory for these specific attributes instead of using a dynamic dict, wic saves a good amount of RAM when
# processing thousands of products

class Product:
    __slots__ = ('id', 'name', 'price', 'category', 'avg_score', 'review_count')

    def __init__(self, id:int, name:str, price:float, category:str, avg_score:float = 0.0, review_count:int = 0):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.avg_score = avg_score
        self.review_count = review_count

    def to_dict(self) -> dict:
        return{
            "id":self.id,
            "name":self.name,
            "price":self.price,
            "category":self.category,
            "avg_score":self.avg_score,
            "review_count":self.review_count
        }