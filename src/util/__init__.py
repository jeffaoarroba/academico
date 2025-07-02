def gerar_endereco_completo(logradouro, bairro, cidade, uf, cep):
    """
    Gera o endereço completo.
    """
    endereco = ", ".join(list(filter(None, [
        logradouro.upper() if logradouro else None,
        bairro.upper() if bairro else None,
        cidade.upper() if cidade else None,
    ]))).strip(", ").strip()
    endereco_completo = endereco + (" - " if endereco and uf else "") + (
        uf.upper() if uf else "") + (" CEP:" + cep if cep else "")
    return endereco_completo


__all__ = []
