# apps/products/management/commands/seed_shop.py
from __future__ import annotations
from decimal import Decimal
from typing import Optional
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.text import slugify

from apps.products.models import (
    Product,
    ProductSpecification,
    ProductVariant,
    ProductVariantSpecification,
    ProductVariantImage,
)
from apps.categories.models import Category
# na samej górze pliku komendy
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import time
import random
import requests
from django.core.files.base import ContentFile

DOWNLOAD_IMAGES = True
IMAGE_SIZE = (800, 600)
IMAGE_TIMEOUT = 10            # sekund na 1 żądanie
IMAGE_RETRIES = 3             # ile razy próbujemy
IMAGE_BACKOFF = 0.8           # mnożnik sleepa między próbami
USER_AGENT = "YourShopSeeder/1.0 (+https://example.com)"  # cokolwiek sensownego

# alternatywni dostawcy (kolejność = priorytet)
def picsum_url(seed: str, w: int, h: int) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"

def loremflickr_url(seed: str, w: int, h: int) -> str:
    # 'lock' stabilizuje obraz po seedzie
    return f"https://loremflickr.com/{w}/{h}/product,tech,shop?lock={abs(hash(seed)) % 10000}"

IMAGE_PROVIDERS = [picsum_url, loremflickr_url]


def ensure_media_dir():
    media_dir = settings.MEDIA_ROOT / 'products_gallery'
    media_dir.mkdir(parents=True, exist_ok=True)
    return media_dir


def _http_get(url: str) -> bytes | None:
    """Jedna próba pobrania (z UA i timeoutem)."""
    try:
        headers = {"User-Agent": USER_AGENT}
        r = requests.get(url, headers=headers, timeout=IMAGE_TIMEOUT)
        r.raise_for_status()
        return r.content
    except Exception:
        return None


def download_image_bytes(seed: str, size: tuple[int, int]) -> bytes | None:
    """Próbuje pobrać obrazek z listy providerów, z retry i backoffem."""
    w, h = size
    for provider in IMAGE_PROVIDERS:
        url = provider(seed, w, h)
        sleep_s = 0.0
        for attempt in range(1, IMAGE_RETRIES + 1):
            if sleep_s:
                time.sleep(sleep_s)
            content = _http_get(url)
            if content:
                return content
            # mały jitter żeby nie walić identycznie
            sleep_s = (IMAGE_BACKOFF * attempt) + random.uniform(0, 0.25)
    return None


def generate_placeholder_png(seed: str, size: tuple[int, int]) -> bytes:
    """Lokalny placeholder (PNG), żeby seed NIGDY nie padał."""
    w, h = size
    img = Image.new("RGB", size, color=(235, 238, 241))
    draw = ImageDraw.Draw(img)

    # prosty środek
    text = f"{seed}\n{w}x{h}"
    # czcionka systemowa może nie być dostępna; użyj domyślnej
    font = ImageFont.load_default()
    tw, th = draw.multiline_textbbox((0, 0), text, font=font, align="center")[2:]
    draw.multiline_text(
        ((w - tw) / 2, (h - th) / 2),
        text,
        fill=(80, 80, 80),
        font=font,
        align="center",
        spacing=6,
    )

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def add_variant_images(variant: ProductVariant, seeds: list[str]) -> None:
    """Dodaje obrazy do wariantu: najpierw z sieci (z retry), jak padnie – placeholder PNG."""
    if not seeds or not DOWNLOAD_IMAGES:
        return
    ensure_media_dir()

    for i, s in enumerate(seeds, start=1):
        # 1) spróbuj pobrać
        content_bytes = download_image_bytes(s, IMAGE_SIZE)

        # 2) fallback do placeholdera
        if not content_bytes:
            content_bytes = generate_placeholder_png(s, IMAGE_SIZE)

        # 3) zapisz do FileField
        # jeśli udało się z neta -> jpg; placeholder to png
        ext = "jpg" if content_bytes and content_bytes[:3] == b"\xff\xd8\xff" else "png"
        filename = f"{s}.{ext}"
        img = ProductVariantImage(variant=variant, alt_text=f"img-{s}-{i}")
        img.image.save(filename, ContentFile(content_bytes), save=True)


def upsert_category(name: str, parent: Optional[Category] = None, slug: Optional[str] = None) -> Category:
    if not slug:
        slug = slugify(name)
    obj, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "parent": parent})
    # aktualizacja nazwy/parenta jeśli trzeba
    changed = False
    if obj.name != name:
        obj.name, changed = name, True
    if obj.parent_id != (parent.id if parent else None):
        obj.parent, changed = parent, True
    if changed:
        obj.save()
    return obj


def create_product_with_specs(
    *,
    name: str,
    description: str,
    category: Category,
    tax_rate: str | Decimal,
    specs: list[tuple[str, str]],
    slug: Optional[str] = None,
) -> Product:
    slug = slug or slugify(name)
    product, _ = Product.objects.get_or_create(
        slug=slug,
        defaults={
            'name': name,
            'description': description,
            'category': category,
            'tax_rate': Decimal(str(tax_rate)),
            'is_active': True,
        },
    )
    # uaktualnij w razie wielokrotnego uruchomienia
    product.name = name
    product.description = description
    product.category = category
    product.tax_rate = Decimal(str(tax_rate))
    product.is_active = True
    product.save()

    ProductSpecification.objects.filter(product=product).delete()
    ProductSpecification.objects.bulk_create(
        [ProductSpecification(product=product, name=k, value=v) for k, v in specs]
    )
    return product


def create_variant(
    product: Product,
    name: str,
    price: str | Decimal,
    discount_price: str | Decimal | None,
    stock: int,
    sku: Optional[str] = None,
) -> ProductVariant:
    sku = sku or f"{slugify(product.slug)}-{slugify(name)}"
    variant, _ = ProductVariant.objects.get_or_create(
        product=product,
        name=name,
        defaults={
            'sku': sku[:32] if hasattr(ProductVariant, "sku") else None,  # jeśli masz pole sku
            'price': Decimal(str(price)),
            'discount_price': Decimal(str(discount_price)) if discount_price is not None else None,
            'stock': stock,
            'is_active': True,
        },
    )
    variant.price = Decimal(str(price))
    variant.discount_price = Decimal(str(discount_price)) if discount_price is not None else None
    variant.stock = stock
    variant.is_active = True
    if hasattr(variant, "sku") and not variant.sku:
        variant.sku = sku[:32]
    variant.save()
    return variant


def set_variant_specs(variant: ProductVariant, specs: list[tuple[str, str]]) -> None:
    ProductVariantSpecification.objects.filter(variant=variant).delete()
    ProductVariantSpecification.objects.bulk_create(
        [ProductVariantSpecification(variant=variant, name=k, value=v) for k, v in specs]
    )


@transaction.atomic
def seed(flush: bool = False):
    if flush:
        ProductVariantImage.objects.all().delete()
        ProductVariantSpecification.objects.all().delete()
        ProductSpecification.objects.all().delete()
        ProductVariant.objects.all().delete()
        Product.objects.all().delete()
        # nie usuwamy kategorii przy flush, ale możesz dodać jeśli chcesz:
        # Category.objects.all().delete()

    # === Kategorie + Subkategorie ===
    # Główne
    cat_electronics = upsert_category('Elektronika', slug='elektronika')
    cat_agd         = upsert_category('AGD', slug='agd')
    cat_books       = upsert_category('Książki', slug='ksiazki')
    cat_shoes       = upsert_category('Buty', slug='buty')

    # Subkategorie
    subphones   = upsert_category('Telefony', parent=cat_electronics, slug='telefony')
    subtvs      = upsert_category('Telewizory', parent=cat_electronics, slug='telewizory')
    sublaptops  = upsert_category('Laptopy', parent=cat_electronics, slug='laptopy')

    submixers   = upsert_category('Miksery i blendery', parent=cat_agd, slug='miksery-blendery')
    subvacuums  = upsert_category('Odkurzacze', parent=cat_agd, slug='odkurzacze')
    sublamps    = upsert_category('Lampy', parent=cat_agd, slug='lampy')

    subit       = upsert_category('IT / Programowanie', parent=cat_books, slug='ksiazki-it')
    subnovel    = upsert_category('Powieści', parent=cat_books, slug='powiesci')

    subrun      = upsert_category('Bieganie', parent=cat_shoes, slug='bieganie')
    subtrek     = upsert_category('Trekking', parent=cat_shoes, slug='trekking')

    # === PRODUKTY (15+) ===

    # 1–3: Telefony
    phone = create_product_with_specs(
        name='Telefon X10', description='Smartfon 6.1", 128 GB, NFC', category=subphones,
        tax_rate='23.00', specs=[('Ekran', '6.1\" OLED'), ('Pamięć', '128 GB'), ('NFC', 'Tak')],
        slug='telefon-x10'
    )
    p1a = create_variant(phone, 'Czarny / 128 GB', '2199.00', None, 42, sku='TEL-X10-128-BLK')
    p1b = create_variant(phone, 'Niebieski / 128 GB', '2199.00', '1999.00', 15, sku='TEL-X10-128-BLU')
    set_variant_specs(p1a, [('Kolor', 'Czarny'), ('Pamięć', '128 GB')])
    set_variant_specs(p1b, [('Kolor', 'Niebieski'), ('Pamięć', '128 GB')])
    ProductVariantImage.objects.filter(variant__product=phone).delete()
    add_variant_images(p1a, ['phone-x10-black-a', 'phone-x10-black-b'])
    add_variant_images(p1b, ['phone-x10-blue-a', 'phone-x10-blue-b'])

    phone2 = create_product_with_specs(
        name='Telefon X12 Pro', description='Flagowiec 6.7", 256 GB, 5G', category=subphones,
        tax_rate='23.00', specs=[('Ekran', '6.7\" OLED 120 Hz'), ('Pamięć', '256 GB'), ('5G', 'Tak')],
        slug='telefon-x12-pro'
    )
    p2a = create_variant(phone2, 'Czarny / 256 GB', '4299.00', '3899.00', 10, sku='TEL-X12-256-BLK')
    set_variant_specs(p2a, [('Kolor', 'Czarny'), ('Pamięć', '256 GB')])
    add_variant_images(p2a, ['phone-x12-pro-black-a'])

    phone3 = create_product_with_specs(
        name='Telefon Compact C5', description='Kompakt 5.8", 128 GB', category=subphones,
        tax_rate='23.00', specs=[('Ekran', '5.8\" OLED'), ('Pamięć', '128 GB')],
        slug='telefon-compact-c5'
    )
    p3a = create_variant(phone3, 'Srebrny / 128 GB', '1899.00', None, 25, sku='TEL-C5-128-SLV')
    set_variant_specs(p3a, [('Kolor', 'Srebrny'), ('Pamięć', '128 GB')])
    add_variant_images(p3a, ['phone-c5-silver-a'])

    # 4–5: TV
    tv1 = create_product_with_specs(
        name='Telewizor 55" QLED', description='4K QLED, HDR10+', category=subtvs,
        tax_rate='23.00', specs=[('Przekątna', '55\"'), ('HDR', 'HDR10+'), ('Rozdzielczość', '4K')],
        slug='tv-55-qled'
    )
    tv1v = create_variant(tv1, 'Standard', '2799.00', '2499.00', 12, sku='TV-55QLED-STD')
    set_variant_specs(tv1v, [('Tryb', 'Standard')])
    add_variant_images(tv1v, ['tv-55-qled-a'])

    tv2 = create_product_with_specs(
        name='Telewizor 65" OLED', description='65\" OLED 120 Hz', category=subtvs,
        tax_rate='23.00', specs=[('Przekątna', '65\"'), ('Technologia', 'OLED')],
        slug='tv-65-oled'
    )
    tv2v = create_variant(tv2, 'Premium', '6999.00', '6299.00', 6, sku='TV-65OLED-PRE')
    set_variant_specs(tv2v, [('Tryb', 'Premium')])
    add_variant_images(tv2v, ['tv-65-oled-a'])

    # 6–7: Laptopy
    lap1 = create_product_with_specs(
        name='Laptop Ultrabook 14', description='14\" i5/16/512', category=sublaptops,
        tax_rate='23.00', specs=[('CPU', 'i5'), ('RAM', '16 GB'), ('SSD', '512 GB')],
        slug='laptop-ultrabook-14'
    )
    lap1v = create_variant(lap1, 'Srebrny', '4199.00', '3899.00', 11, sku='NB-ULTRA14-SLV')
    set_variant_specs(lap1v, [('Kolor', 'Srebrny')])
    add_variant_images(lap1v, ['ultrabook-14-silver-a'])

    lap2 = create_product_with_specs(
        name='Laptop Gaming 15', description='15.6\" i7/16/1TB/RTX', category=sublaptops,
        tax_rate='23.00', specs=[('GPU', 'RTX'), ('Ekran', '144 Hz')],
        slug='laptop-gaming-15'
    )
    lap2v = create_variant(lap2, 'Czarny', '6299.00', None, 8, sku='NB-GAME15-BLK')
    set_variant_specs(lap2v, [('Kolor', 'Czarny')])
    add_variant_images(lap2v, ['gaming-15-black-a'])

    # 8–10: AGD – blendery/odkurzacze/lampy (część z Twoich)
    blender = create_product_with_specs(
        name='Blender Pro 900', description='Mocny blender kielichowy', category=submixers,
        tax_rate='23.00', specs=[('Moc', '900 W'), ('Pojemność', '1.5 L')],
        slug='blender-pro-900'
    )
    bstd = create_variant(blender, 'Standard (czerwony)', '249.00', None, 20, sku='BL-900-STD-RED')
    bpro = create_variant(blender, 'Premium (inox)', '329.00', '299.00', 12, sku='BL-900-PRE-INX')
    set_variant_specs(bstd, [('Kolor', 'Czerwony')]); set_variant_specs(bpro, [('Kolor', 'Inox')])
    ProductVariantImage.objects.filter(variant__product=blender).delete()
    add_variant_images(bstd, ['blender-red-a']); add_variant_images(bpro, ['blender-inox-a'])

    vacuum = create_product_with_specs(
        name='Odkurzacz Cyclone X', description='Bezworkowy z filtrem HEPA', category=subvacuums,
        tax_rate='23.00', specs=[('Moc', '1200 W'), ('Filtr', 'HEPA H13')],
        slug='odkurzacz-cyclone-x'
    )
    vb = create_variant(vacuum, 'Basic', '399.00', None, 30, sku='VAC-CLX-BSC')
    vt = create_variant(vacuum, 'Turbo', '499.00', '449.00', 18, sku='VAC-CLX-TRB')
    set_variant_specs(vb, [('Końcówki', 'Szczelinowa, podłogowa')])
    set_variant_specs(vt, [('Końcówki', 'Szczelinowa, turbo')])
    ProductVariantImage.objects.filter(variant__product=vacuum).delete()
    add_variant_images(vb, ['vacuum-basic-a']); add_variant_images(vt, ['vacuum-turbo-a'])

    lamp = create_product_with_specs(
        name='Lampka biurkowa LED Flex', description='Regulowana, ciepła/zimna', category=sublamps,
        tax_rate='23.00', specs=[('Moc', '8 W'), ('Zasilanie', 'USB-C')],
        slug='lampka-led-flex'
    )
    lw = create_variant(lamp, 'Biała', '129.00', None, 40, sku='LAMP-FLEX-WHT')
    lb = create_variant(lamp, 'Czarna', '129.00', '109.00', 36, sku='LAMP-FLEX-BLK')
    set_variant_specs(lw, [('Kolor', 'Biały')]); set_variant_specs(lb, [('Kolor', 'Czarny')])
    ProductVariantImage.objects.filter(variant__product=lamp).delete()
    add_variant_images(lw, ['lamp-white-a']); add_variant_images(lb, ['lamp-black-a'])

    # 11–12: Książki IT
    book1 = create_product_with_specs(
        name='Algorytmy w praktyce', description='Wprowadzenie do struktur danych', category=subit,
        tax_rate='5.00', specs=[('Autor', 'J. Kowalski'), ('Stron', '420')],
        slug='algorytmy-w-praktyce'
    )
    b1h = create_variant(book1, 'Twarda oprawa', '119.00', '99.00', 50, sku='BOOK-ALG-HC')
    b1s = create_variant(book1, 'Miękka oprawa', '89.00', None, 80, sku='BOOK-ALG-SC')
    set_variant_specs(b1h, [('Oprawa', 'Twarda')]); set_variant_specs(b1s, [('Oprawa', 'Miękka')])
    ProductVariantImage.objects.filter(variant__product=book1).delete()
    add_variant_images(b1h, ['book-hard-a']); add_variant_images(b1s, ['book-soft-a'])

    book2 = create_product_with_specs(
        name='Python od podstaw', description='Praktyczny kurs Pythona', category=subit,
        tax_rate='5.00', specs=[('Autor', 'A. Nowak'), ('Stron', '360')],
        slug='python-od-podstaw'
    )
    b2 = create_variant(book2, 'Wydanie 2025', '129.00', '109.00', 60, sku='BOOK-PY-2025')
    set_variant_specs(b2, [('Edycja', '2025')]); add_variant_images(b2, ['book-python-a'])

    # 13–15: Buty
    shoe = create_product_with_specs(
        name='Runner Pro', description='Buty do biegania – lekkie', category=subrun,
        tax_rate='23.00', specs=[('Cholewka', 'Siatka'), ('Podeszwa', 'EVA')],
        slug='runner-pro'
    )
    s42 = create_variant(shoe, 'Rozmiar 42, czarne', '349.00', None, 24, sku='SHO-RUN-42B')
    s43 = create_variant(shoe, 'Rozmiar 43, czarne', '349.00', '299.00', 12, sku='SHO-RUN-43B')
    set_variant_specs(s42, [('Rozmiar', '42'), ('Kolor', 'Czarny')])
    set_variant_specs(s43, [('Rozmiar', '43'), ('Kolor', 'Czarny')])
    ProductVariantImage.objects.filter(variant__product=shoe).delete()
    add_variant_images(s42, ['shoe-42-a']); add_variant_images(s43, ['shoe-43-a'])

    trek = create_product_with_specs(
        name='Trek Master', description='Buty trekkingowe, wodoodporne', category=subtrek,
        tax_rate='23.00', specs=[('Membrana', 'WaterProof'), ('Waga', '820 g')],
        slug='trek-master'
    )
    t44 = create_variant(trek, 'Rozmiar 44, brązowe', '449.00', None, 14, sku='SHO-TRK-44BR')
    set_variant_specs(t44, [('Rozmiar', '44'), ('Kolor', 'Brązowy')])
    add_variant_images(t44, ['trek-44-brown-a'])

    # +1, żeby dobić do 15+: Lampka nocna
    night = create_product_with_specs(
        name='Lampka nocna Pixel', description='RGB, dotykowa regulacja', category=sublamps,
        tax_rate='23.00', specs=[('Zasilanie', 'USB-C'), ('Tryby', 'RGB')],
        slug='lampka-nocna-pixel'
    )
    n1 = create_variant(night, 'RGB', '89.00', None, 60, sku='LAMP-NIGHT-RGB')
    set_variant_specs(n1, [('Kolor', 'RGB')]); add_variant_images(n1, ['lamp-night-rgb-a'])
    # 15+ done
    return
        

class Command(BaseCommand):
    help = 'Seeds the database with categories (with subcategories) and 15+ demo products.'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Flush existing products/variants/specs first.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding database...'))
        seed(flush=options.get('flush', False))
        self.stdout.write(self.style.SUCCESS('✅ Seed complete.'))
