from adapters.rss_adapter import RSSAdapter
from adapters.reddit_adapter import RedditAdapter
from adapters.markdown_adapter import MarkdownPresenter
from use_cases.collect_posts import CollectPostsUseCase

if __name__ == "__main__":

    sources = [
        RSSAdapter("Azure Blog RSS", "Microsoft Azure", "https://azure.microsoft.com/en-us/blog/feed/"),
        RSSAdapter("AWS News RSS", "Amazon AWS", "https://aws.amazon.com/blogs/aws/feed/"),
    ]

    tags = ["mvpbuzz","aws","azure","docker","cloud","kubernetes","javascript","python","devops","golang"]

    for tag in tags:
        sources.append(RSSAdapter(f"Dev.to feed - {tag}", "Cloud & DevOps", f"https://dev.to/feed/tag/{tag}"))
        sources.append(RSSAdapter(f"Medium feed - {tag}", "Cloud & DevOps", f"https://medium.com/feed/tag/{tag}"))


    reddit_subs = {
        "Cloud & DevOps": ["aws","azure","devops","cloudcomputing"],
        "Desenvolvimento": ["programming","webdev","reactjs","javascript","python","golang"],
        "Arquitetura de Software": ["softwarearchitecture","microservices"],
        "Carreira em Tecnologia": ["cscareerquestions","techcareer","developers"],
        "IA & GenAI": ["machinelearning","artificial","OpenAI","genai"],
        "Comunidades & Reconhecimento": ["dotnet","aws","docker","opensource"]
    }
    for cat, subs in reddit_subs.items():
        for sub in subs:
            sources.append(RedditAdapter(sub, cat))

    presenter = MarkdownPresenter()
    use_case = CollectPostsUseCase(sources, presenter)
    use_case.execute()