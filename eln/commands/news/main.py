import click
from eln.commands.news.client import NewsClient
from eln.helpers.logger import log_error


@click.group()
@click.option('--token', envvar='NEWS_API_KEY')
@click.option('--speak', is_flag=True)
@click.option('--full', is_flag=True)
@click.option('--debug/--no-debug', is_flag=True, default=False)
@click.pass_context
def news(ctx, token, speak, debug, full):
    """
    News powered by NewsAPI.org

    https://newsapi.org
    """

    if not token:
        log_error("Missing NEWS_API_KEY in environment.")
        raise click.Abort

    if debug:
        click.secho("Running in debug mode...", fg='yellow')

    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    ctx.obj['speak'] = speak
    ctx.obj['headlines_only'] = not full

    ctx.obj['client'] = NewsClient(
        api_key=token,
        speak=speak,
        debug=debug,
        headlines_only=ctx.obj['headlines_only']
    )


@news.command()
@click.option('-l', '--language', default=None)
@click.option('-co', '--country', default=None)
@click.option('-ca', '--category', default=None)
@click.pass_context
def sources(ctx,  language, country, category):
    """
        List news publishers.
    """
    client = ctx.obj['client']

    _ = client.sources(
        language=language,
        country=country,
        category=category
    )

    client.read()


@news.command()
@click.option('-l', '--language', default='en')
@click.option('-co', '--country', default=None)
@click.option('-ca', '--category', default=None)
@click.option('-s', '--search-keywords', default=None)
@click.option('-so', '--sources', default=None)
@click.option('-p', '--page', default=None, type=int)
@click.option('-ps', '--page-size', default=None, type=int)
@click.pass_context
def headlines(ctx,  language, country, category, search_keywords, sources, page, page_size):
    """
        List live top and breaking headlines.
    """
    client = ctx.obj['client']

    _ = client.headlines(
        language=language,
        country=country,
        category=category,
        q=search_keywords,
        sources=sources,
        page=page,
        pagesize=page_size
    )

    client.read()


@news.command()
@click.option('-l', '--language', default='en')
@click.option('-s', '--search-keywords', default=None)
@click.option('-st', '--search-titles', default=None)
@click.option('-so', '--sources', default='google-news')
@click.option('-d', '--domains', default=None)
@click.option('-ed', '--exclude-domains', default=None)
@click.option('-fd', '--from_date', default=None)
@click.option('-td', '--to_date', default=None)
@click.option('-sb', '--sort-by', default=None)
@click.option('-p', '--page', default=None, type=int)
@click.option('-ps', '--page-size', default=None, type=int)
@click.pass_context
def all(ctx, language, search_keywords, search_titles, sources,
        domains, exclude_domains, from_date, to_date,
        sort_by, page, page_size
        ):

    """
        Search news articles across multiple sources.
    """

    client = ctx.obj['client']

    _ = client.all(
        language=language,
        q=search_keywords,
        qintitle=search_titles,
        sources=sources,
        domains=domains,
        exclude_domains=exclude_domains,
        from_=from_date,
        to=to_date,
        sort_by=sort_by,
        page=page,
        pagesize=page_size
    )

    client.read()
