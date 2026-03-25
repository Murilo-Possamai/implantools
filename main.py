import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="implantools - Ferramenta de utilidades (CLI e Web)",
        epilog="Exemplo de uso: python main.py --gui"
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true', 
        help="Inicia a interface Web (GUI) no navegador via localhost"
    )
    
    parser.add_argument(
        '--sql-materia-prima', 
        action='store_true', 
        help="Gera o código SQL para a rotina de Matéria Prima"
    )

    parser.add_argument(
        '--sql-ncm', 
        type=str, 
        help="Gera o código SQL para pesquisa de NCMs. Forneça uma lista de NCMs separados por vírgula ou o caminho para um arquivo (ex: ncm.txt)."
    )

    args = parser.parse_args()

    if args.gui:
        from web import iniciar_servidor_web
        iniciar_servidor_web()
        
    elif args.sql_materia_prima:
        from tools.gerador_sql.actions.materia_prima import gerar_sql_materia_prima
        resultado = gerar_sql_materia_prima()
        print("\n--- Resultado Gerador SQL (Matéria Prima) ---")
        print(resultado)
        print("---------------------------------------------\n")
        
    elif args.sql_ncm:
        from tools.gerador_sql.actions.ncm_query import gerar_sql_ncm
        
        ncm_input = args.sql_ncm
        ncms = []
        
        if os.path.isfile(ncm_input):
            with open(ncm_input, 'r', encoding='utf-8') as f:
                content = f.read()
                ncms = content.replace(',', '\n').split('\n')
        else:
            ncms = ncm_input.replace(',', '\n').split('\n')
            
        resultado = gerar_sql_ncm(ncms)
        print("\n--- Resultado Gerador SQL (Pesquisa NCM) ---")
        print(resultado)
        print("---------------------------------------------\n")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()