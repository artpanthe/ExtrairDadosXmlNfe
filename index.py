def extrair_dados_nfe(xml_path):
    # Carregar o XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Espaço de nomes do XML da NFe
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    
    # Inicializar a lista para armazenar os dados
    produtos = []
    
    CODFORNEC = input('Digite o código do fornecedor: ')
    
    # Percorrer os itens da NFe
    for item in root.findall(".//nfe:det", ns):
        produto = {}
        
        # Nome do produto
        nome = item.find(".//nfe:xProd", ns)
        produto['nome'] = nome.text.upper() if nome is not None else "NÃO INFORMADO"
        
        # Código do produto
        codigo = item.find(".//nfe:cProd", ns)
        produto['codigo'] = codigo.text if codigo is not None else "NÃO INFORMADO"
        
        # Código de barras (EAN)
        cod_barras = item.find(".//nfe:cEAN", ns)
        produto['codigo_barras'] = cod_barras.text if cod_barras is not None else "NÃO INFORMADO"
        
        # Código de barras tributável (EANTrib)
        ean_trib = item.find(".//nfe:cEANTrib", ns)
        produto['codigo_barras_tributavel'] = ean_trib.text if ean_trib is not None else "NÃO INFORMADO"
        
        # Unidade de comercialização (uCom)
        u_com = item.find(".//nfe:uCom", ns)
        produto['unidade_comercializacao'] = u_com.text if u_com is not None else "NÃO INFORMADO"
        
        # Unidade de tributação (uTrib)
        u_trib = item.find(".//nfe:uTrib", ns)
        produto['unidade_tributacao'] = u_trib.text if u_trib is not None else "NÃO INFORMADO"
        
        # NCM do produto
        ncm = item.find(".//nfe:NCM", ns)
        produto['ncm'] = ncm.text if ncm is not None else "NÃO INFORMADO"
        
        # Gerar SQL dinâmico para o produto
        sql = (
            f"UPDATE pcprodut SET CODAUXILIAR = '{produto['codigo_barras_tributavel']}', "
            f"DESCRICAO = '{produto['nome'][:40]}', "
            f"NOMEECOMMERCE = '{produto['nome']}', "
            f"UNIDADEMASTER = '{produto['unidade_comercializacao'][:2]}', "
            f"EMBALAGEMMASTER = '{produto['unidade_comercializacao'][:2]}', "
            f"UNIDADE = '{produto['unidade_tributacao'][:2]}', "
            f"EMBALAGEM = '{produto['unidade_tributacao'][:2]}', "
            f"CODNCMEX = '{produto['ncm']}.', "
            f"ENVIAECOMMERCE = 'S' "        
            f"WHERE CODFAB = '{produto['codigo']}' AND CODFORNEC = {CODFORNEC};"
        )
        produto['sql_update'] = sql
        
        # Adicionar o produto à lista
        produtos.append(produto)
    
    return produtos
