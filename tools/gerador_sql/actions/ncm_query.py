def gerar_sql_ncm(ncms: list) -> str:
    # Remove espaços em branco, itens vazios e duplicatas, mantendo a ordem original
    ncms_processados = [str(ncm).strip() for ncm in ncms if str(ncm).strip()]
    ncms_limpos = list(dict.fromkeys(ncms_processados))

    if not ncms_limpos:
        return "-- Nenhum NCM válido fornecido."

    select_statements = []
    for i, ncm in enumerate(ncms_limpos):
        if i == 0:
            select_statements.append(f"    SELECT '{ncm}' AS ncm_salvo")
        else:
            select_statements.append(f"    UNION ALL\n    SELECT '{ncm}' AS ncm_salvo")
            
    lista_pesquisa_sql = "\n".join(select_statements)

    codigo_sql = f"""WITH lista_pesquisa AS (
{lista_pesquisa_sql}
)
SELECT 
    e.id AS "ID_Encontrado",
    l.ncm_salvo AS "NCM_Pesquisado",
    CASE
        WHEN e.numero_ncm IS NOT NULL
            THEN e.nome_ncm
        ELSE 'NÃO ENCONTRADO'
    END AS "Resultado"
FROM lista_pesquisa l
LEFT JOIN estoque_produtos_ncm e 
    ON l.ncm_salvo = e.numero_ncm;"""

    return codigo_sql