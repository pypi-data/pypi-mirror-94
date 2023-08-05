import sys
import os
import re
import getpass
import click
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
from tei2neo import parse, GraphUtils
from .parse import import_categories

NEO4J_HOST = os.environ.get('NEO4J_HOST')
NEO4J_PORT = os.environ.get('NEO4J_PORT')
NEO4J_USER = os.environ.get('NEO4J_USER')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')


def my_sort(coll):
    def my_coll_sort(val):
        match = re.search(r'\d+_Ms_{}_(?P<page>\d+)'.format(coll), val)
        if match:
            return int(match.groupdict()['page'])
        else:
            return 0
    return my_coll_sort


def my_filter(coll):
    def my_coll_filter(val):
        match = re.search(r'^\d+_Ms_{}.*?xml$'.format(coll), val)
        return match
    return my_coll_filter


def get_graph():
    host = NEO4J_HOST or input('hostname (localhost): ') or 'localhost'
    port = NEO4J_PORT or input('port (11002):') or 11002
    user = NEO4J_USER or input('user (neo4j):') or 'neo4j'
    password = NEO4J_PASSWORD or getpass.getpass('password (neo4j):') or 'neo4j'

    graph = Graph(
        host = host, 
        port = port,
        user = user,
        password = password,
    )
    return graph


def import_file(filepath, graph=None):
    if graph is None:
        graph = get_graph()
    ut = GraphUtils(graph)

    filepath = os.path.abspath(filepath)
    filename = os.path.basename(filepath)

    ut.delete_graph_for_file(filename)

    # import
    doc, status, soup = parse(filename=filepath)
    tx = graph.begin()
    doc.save(tx)
    tx.commit()

    # create the relationships within the document
    ut.link_inner_relationships(filename)

    # connect the document to existing categories
    ut.connect_to_categories(filename)

    # get all paragraphs in a file
    paras = ut.paragraphs_for_filename(filename)

    # create the unhyphened tokens
    for para in paras:
        tokens = ut.tokens_in_paragraph(para)
        ut.create_unhyphenated(tokens)


def delete_all_categories(graph=None):
    if graph is None:
        graph = get_graph()

    ut = GraphUtils(graph)
    ut.delete_categories()
    

@click.command()
@click.argument('path')
@click.pass_context
def import_categories_from_path(ctx, path=None, graph=None):
    if path is None:
        try:
            path = sys.argv[1]
        except IndexError:
            while True:
                path = input("please enter location for categories.xml: ")
                path = os.path.expanduser(path)
                if os.path.exists(path) and os.path.isfile(path):
                    break

    if graph is None:
        graph = get_graph()

    tx = graph.begin()
    import_categories(path, tx)
    tx.commit()


def get_files_for_path(path):
    filenames = []
    # get the last directory name as an indicator for the collection
    collection = os.path.basename(os.path.normpath(path))
    for root, dirs, files in os.walk(path):
        for filename in sorted(
                filter(my_filter(coll=collection), files),
                key=my_sort(coll=collection)
        ):
            filepath = os.path.join(root, filename)
            filenames.append({
                "filepath": filepath,
                "filename": filename,
            })

    return filenames


@click.command()
@click.argument('path')
@click.pass_context
def import_tei_from_path(ctx, path, graph=None):
    """Imports all xml files from a given directory.
    These files must fit the pattern and are ordered by their page number
    before they are imorted.
    """
    if os.path.isfile(path):
        import_file(filenpath=path, graph=graph)

    if graph is None:
        graph = get_graph()
    ut = GraphUtils(graph)

    files = get_files_for_path(path)
    first_filename = files[0]
    last_filename = files[:-1]
    for f in files:
        import_file(f["filepath"], graph)

    just_filenames = [f["filename"] for f in files]
    ut.connect_teis(*just_filenames)

#default=os.environ.get('NEO4J_HOSTNAME')
@click.group()
@click.option('-h', '--host',
    default=lambda: os.environ.get('NEO4J_HOSTNAME','localhost'),
    help='Hostname of your Neo4j database or NEO4J_HOSTNAME env')
@click.option('-p', '--port',
    default=lambda: os.environ.get('NEO4J_PORT','7687'),
    help='port of your Neo4j database. NEO4J_PORT env')
@click.option('-u', '--username',
    default=lambda: os.environ.get('NEO4J_USERNAME', 'neo4j'),
    show_default='neo4j',
    help='your Neo4j username. NEO4J_USERNAME env or neo4j')
@click.option('--password', prompt=True, hide_input=True,
    default=lambda: os.environ.get('NEO4J_PASSWORD','neo4j'),
    help='password of your Neo4j database or NEO4J_PASSWORD env')
@click.pass_context
def cli(ctx, host, port, username, password):
    """This is the main entry point for the CLI
    It offers subcommands (defined below) to easily import TEI documents into the
    graph database.
    """
    ctx.ensure_object(dict)
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    ctx.obj['username'] = username
    ctx.obj['password'] = password

cli.add_command(import_tei_from_path)
cli.add_command(import_categories_from_path)


#if __name__ == '__main__':
#    import_tei_from_path(sys.argv[1])

if __name__ == '__main__':
        cli(obj={})
