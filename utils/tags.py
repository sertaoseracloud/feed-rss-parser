def gerar_hashtags_por_categoria(categoria):
    base = {
        "Microsoft Azure": ["#Azure", "#CloudComputing", "#Lançamento", "#MVP"],
        "Amazon AWS": ["#AWS", "#CloudComputing", "#Lançamento", "#AWSCommunityBuilder"],
        "Google Cloud": ["#GoogleCloud", "#CloudComputing", "#Lançamento"],
        "Oracle Cloud": ["#OracleCloud", "#CloudComputing", "#Lançamento"],
        "Cloud & DevOps": ["#DevOps", "#CloudComputing", "#Infraestrutura", "#DockerCaptains"],
        "Desenvolvimento": ["#Desenvolvimento", "#Programação", "#Código"],
        "Arquitetura de Software": ["#Arquitetura", "#Microservices", "#Engenharia"],
        "Carreira em Tecnologia": ["#CarreiraTech", "#DevLife", "#TrabalhoRemoto"],
        "IA & GenAI": ["#InteligenciaArtificial", "#GenAI", "#IA"],
        "Comunidades & Reconhecimento": ["#Comunidade", "#Reconhecimento", "#OpenSource"]
    }
    return base.get(categoria, ["#Tecnologia"])