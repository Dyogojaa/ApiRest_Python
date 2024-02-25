def normalize_path_params(**dados):
    cidade = dados.get('cidade', None)
    return {
        'estrelas_min': dados.get('estrelas_min', 0),
        'estrelas_max': dados.get('estrelas_max', 5),
        'diaria_min': dados.get('diaria_min', 0),
        'diaria_max': dados.get('diaria_max', 10000),
        'cidade': cidade.lower() if cidade else None,
        'limit': dados.get('limit', 50),
        'offset': dados.get('offset', 0)
    }
    
    
