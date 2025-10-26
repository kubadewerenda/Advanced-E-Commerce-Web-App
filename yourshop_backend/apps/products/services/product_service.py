from django.db import connection
from django.db.models import Prefetch, IntegerField, Case, When
from apps.products.models import Product, ProductVariant

class ProductService:
    def get_product_list(self, params):
        q = params.get('q', '')
        ordering = params.get('ordering')
        category_slug = params.get('category')
        subcategory_slug = params.get('subcategory')
        price_min = params.get('price_min')
        price_max = params.get('price_max')

        query_sql = '''
            SELECT
                p.id,
                MIN(COALESCE(pv.discount_price, pv.price)) AS min_price
            FROM products p
            LEFT JOIN product_variants pv
                ON pv.product_id = p.id AND pv.is_active = TRUE
            LEFT JOIN categories c
                ON p.category_id = c.id
            LEFT JOIN categories cp
                ON c.parent_id = cp.id
            WHERE 
                (p.name ILIKE %s OR p.description ILIKE %s)
        '''
        params_sql = [f'%{q}%', f'%{q}%']

        if category_slug and not subcategory_slug:
            query_sql += ' AND ((c.slug = %s AND c.parent_id IS NULL) OR (cp.slug = %s)) '
            params_sql += [category_slug, category_slug]

        if subcategory_slug:
            query_sql += ' AND (c.slug = %s AND c.parent_id IS NOT NULL) '
            params_sql += [subcategory_slug]
        
        query_sql += ' GROUP BY p.id '

        having = []
        if price_min:
            having.append('MIN(COALESCE(pv.discount_price, pv.price)) >= %s')
            params_sql.append(float(price_min))
        if price_max:
            having.append('MIN(COALESCE(pv.discount_price, pv.price)) <= %s')
            params_sql.append(float(price_max))
        if having:
            query_sql += ' HAVING ' + ' AND '.join(having)
        
        if ordering == 'price':
            query_sql += ' ORDER BY min_price ASC NULLS LAST '
        elif ordering == '-price':
            query_sql += ' ORDER BY min_price DESC NULLS LAST '
        elif ordering in ('created_at', '-created_at'):
            direction = 'DESC' if ordering.startswith('-') else 'ASC'
            query_sql += f' ORDER BY p.created_at {direction} '
        else:
            query_sql += ' ORDER BY p.id DESC '

        with connection.cursor() as cur:
            cur.execute(query_sql, params_sql)
            rows = cur.fetchall()

        if not rows:
            return Product.objects.none(), {}
        
        ids = [r[0] for r in rows]
        min_price_map = {r[0]: r[1] for r in rows}

        order_case = Case(
            *[When(id=pk, then=pos) for pos, pk in enumerate(ids)],
            output_field=IntegerField()
        )

        qs = (
            Product.objects.filter(id__in=ids)
            .select_related('category')
            .prefetch_related(
                Prefetch(
                    'variants',
                    queryset=ProductVariant.objects.filter(is_active=True)
                        .prefetch_related('images', 'specifications')
                ),
                'specifications'
            )
            .order_by(order_case)
        )
        return qs, min_price_map
    
    def get_product_detail(self, slug: str):
        return Product.objects.select_related('category').prefetch_related(
            'specifications',
            'variants__images',
            'variants__specifications'
        ).get(slug=slug)