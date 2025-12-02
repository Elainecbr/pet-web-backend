# backend/seed_db.py
# backend/seed_db.py
"""
Script auxiliar para popular o banco de dados com dados iniciais (raças).

Este script usa a fábrica `create_app()` de `app.py` para instanciar uma
aplicação e obter um contexto onde o SQLAlchemy pode operar. Serve para
preencher o sistema com dados de exemplo úteis durante o desenvolvimento
e demonstração (por exemplo: para o vídeo e testes locais).

Uso:
    python seed_db.py

Observações:
- Garante que a pasta `instance/` exista (onde o arquivo SQLite é criado);
- Evita duplicatas checando se uma raça já existe antes de inseri-la.
"""

import os
from app import create_app # Importa a função create_app do nosso app.py
from model import db, Raca

# --- Configuração ---
# O Flask-SQLAlchemy precisa de um contexto de aplicação para operar o banco de dados.
# Usamos a função create_app para criar uma instância de aplicativo "temporária" e um contexto para as operações de banco.
app = create_app()

# ESTE BLOCO É A CORREÇÃO PRINCIPAL E ESTÁ FALTANDO NO SEU ARQUIVO:
# Garante que a pasta 'instance' exista antes de tentar criar o banco de dados nela.
if not os.path.exists('instance'):
    os.makedirs('instance')
# FIM DO BLOCO DE CORREÇÃO




# Empurra o contexto da aplicação para que possamos usar o SQLAlchemy aqui
app.app_context().push() # Ativa o contexto da aplicação para operações de banco

def seed_database():
    """Popula o banco de dados com dados iniciais de raças."""
    print("Verificando e criando tabelas no banco de dados...")
    # Cria todas as tabelas definidas em database.py se elas ainda não existirem
    db.create_all()

    # Lista de raças de cachorros com seus dados
    # Elaine, adicionei informações fictícias para "cuidados", "comportamento" e "racao"
    # para que os cards do seu Frontend já tenham conteúdo para exibir!
    racas_data = [
        # Cães de Companhia (Porte Pequeno)
        {"nome": "Bulldog Francês", "porte": "Pequeno", "grupo": "Companhia", "imagem": "bulldog-frances.png",
         "cuidados": "Exige atenção com a respiração devido ao focinho curto; evite exercícios extenuantes; limpeza de dobras faciais é essencial para prevenir infecções.",
         "comportamento": "Afetuoso, brincalhão e charmoso; bom com crianças e outros animais; adora a companhia humana e é um excelente cão de colo.",
         "racao": "Ração específica para raças braquicefálicas (focinho curto), com formato de croquete adaptado para facilitar a mastigação e digestão, e ingredientes que promovam a saúde da pele."},
        {"nome": "Chihuahua", "porte": "Pequeno", "grupo": "Companhia", "imagem": "chihuahua.png",
         "cuidados": "Sensível ao frio, necessita de agasalhos em climas mais frios; cuidado com quedas e impactos devido ao seu tamanho frágil; escovação dental regular é crucial para evitar problemas dentários.",
         "comportamento": "Leal e protetor; pode ser teimoso e desenvolver 'complexo de cachorro grande'; precisa de socialização precoce para evitar timidez ou agressividade com estranhos.",
         "racao": "Ração para raças miniatura, com croquetes pequenos e nutrientes que suportem a saúde da pele e a beleza do pelo, além de alta palatabilidade."},
        {"nome": "Lhasa Apso", "porte": "Pequeno", "grupo": "Companhia", "imagem": "lhasa-apso.png",
         "cuidados": "Pelo longo exige escovação diária para evitar nós e emaranhados; banhos regulares com produtos específicos; limpeza dos olhos e ouvidos para prevenir infecções.",
         "comportamento": "Independente e reservado, mas muito leal à família; pode ser desconfiado com estranhos; alerta e um bom cão de guarda, latindo para qualquer novidade.",
         "racao": "Ração para raças pequenas, com ingredientes que auxiliem na saúde da pele, brilho da pelagem e prevenção de bolas de pelo, rica em ômega 3 e 6."},
        {"nome": "Pug", "porte": "Pequeno", "grupo": "Companhia", "imagem": "pug.png",
         "cuidados": "Cuidado com o superaquecimento, especialmente em dias quentes, devido ao focinho curto; limpeza das dobras faciais e dos olhos para evitar irritações; exercícios moderados para evitar obesidade.",
         "comportamento": "Dócil, charmoso e brincalhão; adora estar perto da família e seguir seus tutores pela casa; pode ser um pouco teimoso no treinamento, mas é muito inteligente.",
         "racao": "Ração para raças pequenas com tendência a ganho de peso, focando em fibras para saciedade e proteínas magras, e com croquetes que facilitem a pega."},
        {"nome": "Shih Tzu", "porte": "Pequeno", "grupo": "Companhia", "imagem": "shih-tzu.png",
         "cuidados": "Pelo longo requer escovação diária e tosa regular; limpeza dos olhos e da face para evitar manchas e irritações; cuidado com o calor e exercícios leves, pois não toleram bem temperaturas altas.",
         "comportamento": "Afetuoso, extrovertido e um pouco teimoso; adora colo e atenção, sendo um excelente cão de companhia; geralmente bom com crianças e outros animais se socializado cedo.",
         "racao": "Ração para raças pequenas, com nutrientes para saúde da pele e brilho do pelo, e que ajude a reduzir o odor das fezes."},
        {"nome": "Yorkshire Terrier", "porte": "Pequeno", "grupo": "Companhia", "imagem": "yorkshire-terrier.png",
         "cuidados": "Pelo fino e longo necessita de escovação diária para evitar nós; cuidado com a higiene dental, pois são propensos a tártaro; exercícios leves, mas com bastante brincadeira.",
         "comportamento": "Corajoso, enérgico e com personalidade forte; pode ser um pouco barulhento, latindo para alertar sobre a presença de estranhos; muito leal e apegado à família.",
         "racao": "Ração para raças pequenas/mini, que suporte a alta energia e a saúde do pelo, rica em vitaminas e minerais."},

        # Grupos de Trabalho e Guarda (Porte Grande e Médio) e Outros
        {"nome": "Airedale Terrier", "porte": "Médio", "grupo": "Terrier", "imagem": "airedale-terrier.png",
         "cuidados": "Pelo duro necessita de tosa trimestral ou stripping para manter a textura; exercícios diários intensos para gastar energia e evitar o tédio; adora atividades que o desafiem.",
         "comportamento": "Inteligente, independente e enérgico; pode ser teimoso, exigindo um treinamento consistente; bom companheiro para famílias ativas que ofereçam desafios.",
         "racao": "Ração para raças médias com alta energia, com foco em proteínas de qualidade para manter a massa muscular e nutrientes para a saúde articular."},
        {"nome": "Akita Spitz", "porte": "Grande", "grupo": "Spitz/Primitivos", "imagem": "akita-spitz.png",
         "cuidados": "Pelo denso exige escovação semanal, especialmente durante as trocas de pelo; necessita de socialização desde filhote para aceitar estranhos; exercícios moderados a intensos diariamente.",
         "comportamento": "Digno, corajoso e leal; reservado com estranhos, mas muito apegado à família; pode ser dominante com outros cães do mesmo sexo, exigindo supervisão.",
         "racao": "Ração para raças grandes, com nutrientes para articulações (condroitina e glucosamina) e saúde cardíaca (taurina), além de promover uma pelagem saudável."},
        {"nome": "Basset Hound", "porte": "Médio", "grupo": "Farejadores", "imagem": "basset-hound.png",
         "cuidados": "Orelhas longas precisam de limpeza regular para evitar infecções; exercícios moderados são importantes para evitar obesidade, pois são naturalmente preguiçosos; cuidado com a coluna.",
         "comportamento": "Tranquilo, dócil e amigável; excelente olfato, adora seguir rastros e cheiros; pode ser teimoso e focado em seus próprios interesses, exigindo paciência no treinamento.",
         "racao": "Ração para raças médias, com controle de calorias para evitar sobrepeso e ingredientes que suportem a saúde da pele e ouvidos, propensos a alergias."},
        {"nome": "Beagle", "porte": "Médio", "grupo": "Farejadores", "imagem": "beagle.png",
         "cuidados": "Orelhas precisam de limpeza frequente; requer exercícios diários e atividades que estimulem seu faro para gastar energia e evitar o tédio e comportamentos destrutivos.",
         "comportamento": "Curioso, enérgico e amigável; adora farejar e explorar o ambiente; pode ser difícil de treinar devido à sua independência e foco em cheiros, mas é muito apegado à família.",
         "racao": "Ração para raças médias ativas, com foco em energia sustentada e digestibilidade, e ingredientes para a saúde do trato urinário e pele."},
        {"nome": "Boxer", "porte": "Grande", "grupo": "Trabalho", "imagem": "boxer.png",
         "cuidados": "Pelo curto de fácil manutenção; necessita de exercícios diários intensos e brincadeiras para gastar energia e manter-se saudável; atenção com a temperatura devido ao focinho curto.",
         "comportamento": "Leal, brincalhão e enérgico; excelente cão de guarda e companheiro familiar; pode ser um pouco exuberante e desajeitado na juventude, mas amadurece bem.",
         "racao": "Ração para raças grandes, com foco em massa muscular (proteínas de alta qualidade) e saúde cardíaca (taurina), com croquetes adaptados para mandíbulas fortes."},
        {"nome": "Bull Terrier", "porte": "Médio", "grupo": "Terrier", "imagem": "bull-terrier.png",
         "cuidados": "Pelo curto de fácil cuidado; exercícios diários intensos e mentalmente estimulantes para evitar o tédio e a destruição; requer um tutor com tempo e experiência.",
         "comportamento": "Corajoso, brincalhão e com forte personalidade; leal à família; precisa de socialização e treinamento consistentes desde filhote para ser um cão equilibrado.",
         "racao": "Ração para raças médias/grandes com alta energia e foco em músculos, com ingredientes hipoalergênicos para cães sensíveis à pele."},
        {"nome": "Cane Corso", "porte": "Grande", "grupo": "Guarda", "imagem": "cane-corso.png",
         "cuidados": "Pelo curto de fácil cuidado; necessita de exercícios diários e treinamento firme, consistente e precoce; um cão de família que precisa de socialização intensa.",
         "comportamento": "Protetor, calmo e digno; leal à família, mas desconfiado com estranhos; exige um tutor experiente que saiba lidar com sua força e inteligência, e um bom espaço para viver.",
         "racao": "Ração para raças gigantes, com suporte para articulações (condroitina, glucosamina) e crescimento saudável, controlando o cálcio para evitar problemas ósseos."},
        {"nome": "Cocker Spaniel Americano", "porte": "Médio", "grupo": "Cães de Caça", "imagem": "cocker-spaniel.png",
         "cuidados": "Pelo médio/longo exige escovação regular para evitar nós; limpeza de orelhas frequente; exercícios moderados, mas gosta de brincadeiras e passeios.",
         "comportamento": "Doce, amigável e alegre; ótimo cão de companhia, adora brincar e estar com a família; pode ser sensível e exigir um treinamento positivo.",
         "racao": "Ração para raças médias, com foco na saúde da pele e pelo (ômega 3 e 6), e controle de peso para evitar obesidade."},
        {"nome": "Dachshund (Salsicha)", "porte": "Pequeno", "grupo": "Farejadores", "imagem": "dachshund-salsicha.png",
         "cuidados": "Cuidado com a coluna, evitar pular de lugares altos e subir/descer escadas; exercícios moderados; escovação regular dependendo do tipo de pelo (curto, longo, duro).",
         "comportamento": "Corajoso, curioso e um pouco teimoso; leal e brincalhão; pode ser um bom cão de alerta, latindo para tudo o que vê; adora cavar e explorar.",
         "racao": "Ração para raças pequenas, com controle de peso e suporte para a saúde da coluna (condroprotetores), e croquetes adaptados à sua boca alongada."},
        {"nome": "Dobermann", "porte": "Grande", "grupo": "Trabalho/Guarda", "imagem": "dobermann.png",
         "cuidados": "Pelo curto de baixa manutenção; necessita de exercícios diários intensos e treinamento consistente desde filhote; é um cão sensível ao frio.",
         "comportamento": "Inteligente, leal, protetor e enérgico; excelente cão de guarda, mas também um companheiro familiar afetuoso; exige socialização precoce e um tutor com experiência.",
         "racao": "Ração para raças grandes, com foco em massa muscular (alto teor proteico) e energia, além de nutrientes para a saúde cardíaca e articulações."},
        {"nome": "Golden Retriever", "porte": "Grande", "grupo": "Cães de Caça", "imagem": "golden-retriever.png",
         "cuidados": "Pelo médio exige escovação regular para evitar nós e reduzir a queda; necessita de exercícios diários e atividades que estimulem sua mente, adora nadar e buscar objetos.",
         "comportamento": "Amigável, inteligente e paciente; excelente com crianças e outros animais; fácil de treinar e ansioso para agradar; muito sociável e precisa de companhia.",
         "racao": "Ração para raças grandes, com suporte para articulações (condroitina, glucosamina) e saúde cardíaca, e que ajude a manter um peso saudável."},
        {"nome": "Husky Siberiano", "porte": "Grande", "grupo": "Trabalho", "imagem": "husky-siberiano.png",
         "cuidados": "Pelo denso exige escovação regular, especialmente na troca de pelo (duas vezes ao ano); necessita de muita atividade física diária e um ambiente fresco; não toleram bem o calor.",
         "comportamento": "Independente, amigável e enérgico; pode ser um pouco teimoso e com forte instinto de caça; adora correr e explorar, ideal para pessoas ativas; uiva em vez de latir.",
         "racao": "Ração para raças grandes ativas, com alta energia e nutrientes para a pelagem densa, e ingredientes que promovam a saúde digestiva e articular."},
        {"nome": "Jack Russell Terrier", "porte": "Pequeno", "grupo": "Terrier", "imagem": "jack-russell-terrier.png",
         "cuidados": "Pelo fácil de manter; necessita de *muita* atividade física e mental para gastar energia e evitar o tédio e a destruição; treinamento e socialização desde cedo.",
         "comportamento": "Corajoso, enérgico e com forte instinto de caça; inteligente e brincalhão; exige um tutor ativo e com experiência, e não é recomendado para apartamentos pequenos sem muita saída.",
         "racao": "Ração para raças pequenas com alta demanda energética, rica em proteínas e com ingredientes que auxiliem na manutenção de músculos e ossos fortes."},
        {"nome": "Labrador Retriever", "porte": "Grande", "grupo": "Cães de Caça", "imagem": "labrador.png",
         "cuidados": "Pelo curto de fácil manutenção; necessita de exercícios diários para evitar obesidade (tendem a comer demais); adora água e atividades de busca; propenso a displasia.",
         "comportamento": "Amigável, extrovertido e dócil; excelente com crianças e famílias; fácil de treinar e muito leal; um dos cães mais populares devido ao seu temperamento gentil.",
         "racao": "Ração para raças grandes, com foco em controle de peso e saúde articular, e que ajude a manter um sistema imunológico forte."},
        {"nome": "Pastor Alemão", "porte": "Grande", "grupo": "Pastoreio", "imagem": "pastor-alemao.png",
         "cuidados": "Pelo médio exige escovação regular; necessita de treinamento e socialização desde filhote; exercícios diários e desafios mentais são cruciais para sua saúde e felicidade.",
         "comportamento": "Inteligente, leal, corajoso e protetor; excelente cão de trabalho e guarda; requer um tutor consistente e experiente que lhe dê um propósito e bastante atividade.",
         "racao": "Ração para raças grandes ativas, com foco em massa muscular, suporte articular e digestibilidade sensível, com prebióticos e probióticos."},
        {"nome": "Rottweiler", "porte": "Grande", "grupo": "Trabalho/Guarda", "imagem": "rottweiler.png",
         "cuidados": "Pelo curto de baixa manutenção; necessita de socialização e treinamento desde filhote; exercícios diários são importantes, mas com cuidado em climas quentes; propenso a displasia.",
         "comportamento": "Confidente, calmo e protetor; muito leal à família, mas pode ser distante com estranhos; exige um tutor experiente e responsável que saiba gerenciar sua força e temperamento.",
         "racao": "Ração para raças grandes/gigantes, com foco em força muscular e saúde óssea, além de nutrientes que apoiem a saúde cardíaca e o sistema imunológico."},
        {"nome": "Shiba Inu Spitz", "porte": "Médio", "grupo": "Spitz/Primitivos", "imagem": "shiba-inu-spitz.png",
         "cuidados": "Pelo denso exige escovação regular, especialmente na época de muda; necessita de exercícios diários; pode ser difícil de treinar devido à sua independência e teimosia.",
         "comportamento": "Independente, alerta e fiel; pode ser reservado com estranhos; conhecido por ser um gato em corpo de cachorro, com muita autonomia e uma personalidade única.",
         "racao": "Ração para raças médias, com nutrientes para saúde da pele e pelo, e que ajude a manter o peso ideal para evitar problemas articulares."}
    ]

    print(f"Caminho atual: {os.getcwd()}") # Para depuração, verificar onde o script está sendo executado

    for raca_data in racas_data:
        # Verifica se a raça já existe no banco de dados para evitar duplicatas
        if not Raca.query.filter_by(nome=raca_data['nome']).first():
            raca = Raca(**raca_data) # Cria um novo objeto Raca com os dados
            db.session.add(raca) # Adiciona o objeto à sessão do banco de dados
            print(f"Adicionando raça: {raca_data['nome']}")
        else:
            print(f"Raça {raca_data['nome']} já existe. Pulando.")
    
    db.session.commit() # Salva todas as mudanças pendentes no banco de dados
    print("Banco de dados populado com sucesso (ou já estava populado)!")

if __name__ == '__main__':
    seed_database()
