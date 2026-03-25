def gerar_sql_materia_prima():
    codigo_sql = """
    SELECT 
        id_materia, 
        nome, 
        quantidade, 
        data_inclusao 
    FROM 
        tb_materias_primas 
    WHERE 
        status = 'ativo';
    """
    return codigo_sql.strip()