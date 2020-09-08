def money_precision_at_k(recommended_list, bought_list, prices_recommended, k=5):
      
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    prices_recommended = np.array(prices_recommended)
    bought_list = bought_list
    recommended_list = recommended_list[:k]
    prices_recommended = prices_recommended[:k]
    flags = np.isin(recommended_list, bought_list)
    precision = (prices_recommended * flags).sum() / prices_recommended.sum()
   
    return precision


def hit_rate_at_k(recommended_list, bought_list, k=5):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list[:k])
    flags = np.isin(bought_list, recommended_list)
    hit_rate = (flags.sum() > 0) * 1
    
    return hit_rate


def recall_at_k(recommended_list, bought_list, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list[:k])
    flags = np.isin(bought_list, recommended_list)
    recall = flags.sum() / len(bought_list)
    
    return recall


def money_recall_at_k(recommended_list, bought_list, prices_recommended, prices_bought, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    prices_bought = np.array(prices_bought)
    bought_list = bought_list  
    recommended_list = recommended_list[:k]
    prices_recommended = prices_recommended[:k]
    flags = np.isin(recommended_list, bought_list)
    recall = sum(flags * prices_recommended) / sum(prices_bought)
    
    return recall



def reciprocal_rank(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    flags = np.isin(recommended_list, bought_list)
    result = np.array([1 / (i + 1) for i, x in enumerate(flags) if x]).mean()
    
    return result


def precision(recommended_list, bought_list):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    flags = np.isin(bought_list, recommended_list)
    
    precision = flags.sum() / len(recommended_list)
    
    return precision


def recall(recommended_list, bought_list):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    flags = np.isin(bought_list, recommended_list)
    
    recall = flags.sum() / len(bought_list)
    
    return recall


def precision_at_k(recommended_list, bought_list, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    bought_list = bought_list  # Тут нет [:k] !!
    recommended_list = recommended_list[:k]
    
    flags = np.isin(bought_list, recommended_list)
    
    precision = flags.sum() / len(recommended_list)
    
    return precision

def get_recommendations(user, model, N=5):
    res = [id_to_itemid[rec[0]] for rec in 
        model.recommend(userid=userid_to_id[user], 
            user_items=sparse_user_item,   # на вход user-item matrix
            N=N, 
            filter_already_liked_items=False, 
            filter_items=None, 
            recalculate_user=True)]
    return res