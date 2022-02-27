from django.db import connection


def total_stats_query():
    with connection.cursor() as cursor:
        # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        # cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])

        cursor.execute("select sum(amnt) as total_items from order_items")
        total_items_sold = cursor.fetchone()

        cursor.execute(
            "select sum(total_price) as total_income, count(distinct customer_id) as unique_customers from orders")
        total_income_and_unique_customers = cursor.fetchone()

        ret_dict = {
            'total_items_sold': total_items_sold[0],
            'total_income': total_income_and_unique_customers[0],
            'unique_customers': total_income_and_unique_customers[1]
        }

    return ret_dict


def best_customers_query(from_date, to_date, count):
    # select o.customer_id, c.name, sum(o.total_price) as aggregated_total from orders o join customers c on o.customer_id = c.id
    # where o.total_price is not null and o.order_date between  date '2020-01-01' and date '2022-02-28'
    # group by o.customer_id, c.name
    # order by aggregated_total desc;
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.customer_id, c.name, sum(o.total_price) as aggregated_total from orders o join customers c on o.customer_id = c.id
            WHERE o.total_price is not null and o.order_date between  date %s and date %s
            GROUP BY o.customer_id, c.name
            ORDER BY aggregated_total desc
            LIMIT %s""",
            [from_date, to_date, count])
        rows = cursor.fetchall()
        res_list = [{"customer_id": row[0], "customer_name": row[1], "total_purchase_sum": row[2]} for row in rows]
        return res_list