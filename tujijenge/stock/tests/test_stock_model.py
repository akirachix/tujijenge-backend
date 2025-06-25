# tujijenge/stock/tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
from stock.models import Category, Tag, Product, Stock
from users.models import Mamamboga

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fruits")

    def test_category_str(self):
        """Test Category string representation."""
        self.assertEqual(str(self.category), "Fruits")

    def test_category_creation(self):
        """Test creating a Category instance."""
        category = Category.objects.create(name="Vegetables")
        self.assertEqual(category.name, "Vegetables")
        self.assertEqual(Category.objects.count(), 2)

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Organic")

    def test_tag_str(self):
        """Test Tag string representation."""
        self.assertEqual(str(self.tag), "Organic")

    def test_tag_unique_name(self):
        """Test that Tag name is unique."""
        with self.assertRaises(Exception):
            Tag.objects.create(name="Organic")

    def test_tag_creation(self):
        """Test creating a Tag instance."""
        tag = Tag.objects.create(name="Fresh")
        self.assertEqual(tag.name, "Fresh")
        self.assertEqual(Tag.objects.count(), 2)

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fruits")
        self.tag = Tag.objects.create(name="Organic")
        self.product = Product.objects.create(
            product_id="P001",
            product_name="Bananas",
            unit="kg",
            category=self.category,
            product_price=30.00,
            description="Sweet bananas"
        )
        self.product.tags.add(self.tag)

    def test_product_str(self):
        """Test Product string representation."""
        self.assertEqual(str(self.product), "Bananas")

    def test_product_creation(self):
        """Test creating a Product instance."""
        product = Product.objects.create(
            product_id="P002",
            product_name="Apples",
            unit="kg",
            category=self.category,
            product_price=40.00
        )
        self.assertEqual(product.product_name, "Apples")
        self.assertEqual(Product.objects.count(), 2)

    def test_product_price_validation(self):
        """Test that negative product_price raises ValidationError."""
        product = Product(
            product_id="P003",
            product_name="Mangoes",
            unit="kg",
            category=self.category,
            product_price=-10.00
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_tags_relationship(self):
        """Test ManyToMany relationship with Tag."""
        self.assertEqual(self.product.tags.count(), 1)
        self.assertEqual(self.product.tags.first().name, "Organic")

class StockModelTest(TestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            mamamboga_id="M001",
            mamamboga_name="Mama Asha",
            phone_number="0712345678",
            pin="1234"
        )
        self.stock = Stock.objects.create(
            stock_id="S001",
            mamamboga=self.mamamboga,
            price=120.00,
            quantity=15.0,
            expiration_date=timezone_now()
        )

    def test_stock_str(self):
        """Test Stock string representation."""
        self.assertEqual(str(self.stock), f"Stock S001 for Mama Asha")

    def test_stock_creation(self):
        """Test creating a Stock instance."""
        stock = Stock.objects.create(
            stock_id="S002",
            mamamboga=self.mamamboga,
            price=100.00,
            quantity=10.0
        )
        self.assertEqual(stock.price, 100.00)
        self.assertEqual(Stock.objects.count(), 2)

    def test_stock_price_validation(self):
        """Test that negative price raises ValidationError."""
        stock = Stock(
            stock_id="S003",
            mamamboga=self.mamamboga,
            price=-100.00,
            quantity=5.0
        )
        with self.assertRaises(ValidationError):
            stock.full_clean()

    def test_stock_quantity_validation(self):
        """Test that negative quantity raises ValidationError."""
        stock = Stock(
            stock_id="S004",
            mamamboga=self.mamamboga,
            price=80.00,
            quantity=-5.0
        )
        with self.assertRaises(ValidationError):
            stock.full_clean()

    def test_stock_mamamboga_relationship(self):
        """Test ForeignKey relationship with Mamamboga."""
        self.assertEqual(self.stock.mamamboga.mamamboga_name, "Mama Asha")