from app import app, db, Cliente

with app.app_context():
    # Buscar todos os clientes
    clientes = Cliente.query.all()
    print(f"Total de clientes no banco: {len(clientes)}")
    
    # Agrupar por CPF/CNPJ
    cpf_dict = {}
    for cliente in clientes:
        cpf = cliente.cpfcnpj
        if cpf:
            if cpf not in cpf_dict:
                cpf_dict[cpf] = []
            cpf_dict[cpf].append(cliente)
    
    # Remover duplicados
    for cpf, lista in cpf_dict.items():
        if len(lista) > 1:
            print(f"\nCPF/CNPJ {cpf} tem {len(lista)} registros:")
            # Manter o primeiro, deletar os outros
            for i, cliente in enumerate(lista):
                if i == 0:
                    print(f"  ✓ Mantendo: ID {cliente.id} - {cliente.nome}")
                else:
                    print(f"  ✗ Removendo: ID {cliente.id} - {cliente.nome}")
                    db.session.delete(cliente)
    
    db.session.commit()
    print("\n✅ Limpeza concluída!")
    
    # Mostrar resultado final
    clientes_final = Cliente.query.all()
    print(f"\nTotal de clientes após limpeza: {len(clientes_final)}")
