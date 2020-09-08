def prefilter_items(data, take_n_popular=5000):
    """Предфильтрация товаров"""
    
    # 1. Удаление товаров, со средней ценой < 1$
    data = data[data.sales_value / data.quantity < 1]
    
    # 2. Удаление товаров со соедней ценой > 30$
    data = data[data.sales_value / data.quantity < 30]
    
    # 3. Придумайте свой фильтр
    data = data[data['retail_disc'] < 0]
    # Уберем товары со скидкой больше 30% (если купили не только из-за цены, то будут встречаться еще без дисконта) 
    data = data[data['retail_disc'] > -30]
    # Удаление 0.5% самых невыгодных с точки зрения объема продаж (количество х средняя цена) товаров
#     data['sold'] = data.groupby('item_id').quantity.transform('sum') 
#     data['revenue'] = data['sold'] * data['price']
#     max_revenue = data['revenue'].max()
#     min_revenue = data['revenue'].min()
#     revenue_treshold = min_revenue + 0.005 * (max_revenue - min_revenue)
#     data = data[data['revenue'] > revenue_treshold]
#     data = data.drop(['price', 'sold', 'revenue'], axis=1)
    # Если товар покупает более половины пользователей, то его рекомендовать не стоит, так как его и так купят.
    popular = data.groupby('item_id')['user_id'].nunique().reset_index()
    users_count = data['user_id'].nunique()
    popular['user_id'] = popular['user_id'].apply(lambda x: x / users_count)
    popular.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    popular.sort_values(by='share_unique_users', ascending=False, inplace=True)
    top_popular = popular[popular['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    
    # 4. Выбор топ-N самых популярных товаров (N = take_n_popular)
    popularity_sales = data.groupby('item_id')['sales_value'].sum().reset_index()
    popularity_sales.sort_values('sales_value', ascending=False, inplace=True)
    n_popular = popularity_sales['item_id'][:take_n_popular].tolist()

    # Заведем фиктивный item_id (если юзер не покупал товары из топ-5000, то он "купил" такой товар)
    data.loc[~data['item_id'].isin(n_popular), 'item_id'] = 9999999
    n_popular.append(9999999)
    
    data = data[data['item_id'].isin(n_popular)]
    
    
    return data